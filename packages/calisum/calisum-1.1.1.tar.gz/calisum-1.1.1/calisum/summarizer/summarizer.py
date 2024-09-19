import asyncio
import aiohttp
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm
from calisum.summarizer.models import Models
from calisum.util import activity_to_plain_text

DEFAULT_LANG = 'fr'
DEFAULT_JANAI_API_ENDPOINT = 'http://localhost:1337/v1'
SUMMY_SENTENCE_OUTPUT = 2 # Number of sentences to return per activity
DUMMY_TOKEN = "NOTATOKEN"
INDIVIDIUAL_PROMPT = "Résume cette activité ci-dessous en quelques phrases essentielles : En quoi consiste grossièrement la tache et qu'est ce qu'elle m'a apportée ?"
SEPARATOR = '\n___\n'
GLOBAL_PROMPT= f"Fait un résumé cohérent de l'ensemble de ces activités (celles si son séparées par '{SEPARATOR}' et classé par ordre chronologique). Déduit une évolution et prend du recul par rapport à celles-ci"


class SummarizerException(Exception):
    pass

class SummarizerNotConfiguredException(SummarizerException):
    pass

class Summarizer:
    def __init__(
            self,
            verbose: bool = False, 
            model: int = Models.SUMY, 
            model_url : str = "",
            model_token: str = DUMMY_TOKEN,
        ):
        """Init the summarizer with the chosen model and settings

        Args:
            verbose (bool, optional): If set to True will log what summarizer is doing. Defaults to False.
            model (int, optional): Choose a model from Models enum. Defaults to Models.SUMY.
            model_url (str, optional): Url of the model api to request. Defaults to "".
            model_token (str, optional): Token of the model api to request. Defaults to "".
        """
        self.verbose = verbose
        if model == Models.JANAI and model_url == "":
            model_url = DEFAULT_JANAI_API_ENDPOINT
        self.url = model_url
        self.token = model_token if model_token is not None else DUMMY_TOKEN
        self.__llm_id = None

        self.model = model
        if model != Models.SUMY:
            self.llm = AsyncOpenAI(
                api_key=self.token,
                base_url=self.url
            )
        self._func_dict = {
            Models.SUMY : self.__sum_sumy,
            Models.CHATGPT: self.__sum_llm,
            Models.JANAI: self.__sum_llm,
            Models.CUSTOM: self.__sum_llm
        }
    @property
    def llm_id(self):
        return self.__llm_id

    async def set_llm_id(self, value):
        # Checks that id is one of the value possible
        list_of_id = []
        for model in await self.list_llm_models():
            list_of_id.append(model['id'])
        
        if value not in list_of_id:
            raise ValueError(f"{value} not in available model id")
        self.__llm_id = value


    async def __aenter__(self):
        """context manager."""
        # Create a new session when entering the context manager.
        if self.model == Models.SUMY:
            # Install tokenizer
            nltk.download('punkt_tab')
            self.tokenizer = Tokenizer(DEFAULT_LANG)
            self.summarizer = LsaSummarizer()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """context manager."""
        pass

    async def summarize_activities(self, activities : list[dict]) -> list[str]:
        """Summarize activities individualy 

        Args:
            activities (list[dict]): List of activities to summarize

        Returns:
            list[str]: Return a list of summarized activity
        """ 
        futures = []
        output = []
        for activity in activities:
            text = activity_to_plain_text(activity)
            futures.append(self._func_dict[self.model](text))
        if self.verbose:
            output = await tqdm.gather(*futures)
        else:
            output = await asyncio.gather(*futures)
        return output
    
    async def list_llm_models(self) -> list[dict]:
        """List available llm models on the remote server.
        Models should be one of JAN, CUSTOM, or CHATGPT

        Returns:
            list[dict]: List of available llm models on the dictionary
        """
        if self.model not in [Models.CHATGPT, Models.CUSTOM, Models.JANAI]:
            raise SummarizerException(f"Model {self.model} does not support listing model")
        models_obj = list(await self.llm.models.list())[0][1]
        output = [dict(model_obj) for model_obj in models_obj]
        return output
    
    async def summarize(self, text : str) -> str :
        """Summarize the text

        Args:
            text (str, optional): Text to summarize.

        Returns:
            str: Summary of the text
        """
        return self._func_dict[self.model](text)

    async def __sum_sumy(self, text : str, nb_of_sentence: int = SUMMY_SENTENCE_OUTPUT) -> str:
        """Summarize with summy

        Args:
            text (str): Text to summarize

        Returns:
            str: Summary
        """
        parser = PlaintextParser.from_string(text, self.tokenizer)
        summarizer = self.summarizer(parser.document, nb_of_sentence)
        return''.join([str(sentence) for sentence in summarizer])

    async def __sum_llm(self, text : str, prompt: str = INDIVIDIUAL_PROMPT) -> str:
        """Summarize using llm requires a model id
        will fail if llm_id is not defined

        Args:
            text (str): Text to summarize

        Returns:
            str: Summarized text
        """
        if self.llm_id is None :
            raise SummarizerNotConfiguredException('llm_id is not defined')

        payload = {
            'role' : 'user',
            'content' : prompt + ' ' + text
        }
        response = await self.llm.chat.completions.create(messages=[payload], model=self.llm_id)
        return response.to_dict()['choices'][0]['message']['content']

    async def summarize_global(self, text : list[str]) -> str:
        """Summarize a list of texts globally

        Args:
            text (list[str]): List of texts to summarize

        Returns:
            str: Summarized text
        """
        merged_text = SEPARATOR.join(text)
        if self.model == Models.SUMY:
            return await self.__sum_sumy(merged_text, len(text)//5 + 1)
        else :
            return await self.__sum_llm(merged_text, GLOBAL_PROMPT)