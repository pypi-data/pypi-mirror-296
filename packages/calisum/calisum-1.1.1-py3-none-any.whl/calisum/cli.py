""" Command line interface for the calisum package. """

import argparse
import json
import bullet
from getpass import getpass

import tabulate
from calisum import PARSING_ERROR, SCRAPING_ERROR, __app_name__, __version__
from calisum.scraper import LoginError, ParsingError, Scraper, COOKIE_KEY
from calisum.summarizer import Summarizer, Models
from calisum.util import activities_dict_to_plain_text, activities_dict_to_items

KEYS_SHOWS_LLM_PICK_MENU = [
    "id",
    "name",
    "version"
]

def show_version():
    """Print the version of the package."""
    print(f"{__app_name__} {__version__}")

def setup_parser():
    """Create the command line interface parser."""
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description="Summarize Caliap activity data."
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Display the version of the package."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase the verbosity of the output."
    )
    parser.add_argument(
        "-O",
        "--output",
        help="Output file to save the summary to. default to stdout "
    )
    parser.add_argument(
        "-o",
        "--original-output",
        action="store_true",
        help="Output the original data instead of the summary.")
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help='Output the result as json'
    )

    scraper = parser.add_argument_group("Scraper options")

    scraper.add_argument(
        "url_to_scrape",
        help="URL to scrape the data from.",
        nargs="?"
    )
    auth_group = scraper.add_mutually_exclusive_group()

    auth_group.add_argument(
        "-e",
        "--email",
        help="Email address to use for authentication. Must be used together with --password."
    )
    scraper.add_argument(
        "-p",
        "--password",
        help="Password to use for authentication. Must be used together with --email."
    )
    auth_group.add_argument(
        "-c",
        "--cookie",
        help=f"Cookie to use for authentication ({COOKIE_KEY}). Mutually exclusive with --email and --password."
    )
    llm = parser.add_argument_group("LLM options")
    llm.add_argument(
        "-l",
        "--llm-url",
        help="URL to the LLM page open api endpoint (compatible with openai api standard)."
    )
    llm.add_argument(
        "-t",
        "--llm-token",
        help="LLM token (usefull with openai)"
    )
    llm.add_argument(
        "-n",
        "--jan-ai",
        action="store_true",
        help="Use localhost default jan-ai config."
    )
    llm.add_argument(
        "-m",
        "--model-id",
        help="OpenAI form model id (eg: mistral-ins-7b-q4)"
    )
    llm.add_argument(
        "-g",
        "--global-summary",
        help="Do a global summary of individual activity (works only if original output is not selected)",
        action="store_true"
    )
    return parser
    
def dict_to_menu(input_dicts : list[dict[str, str]]) -> dict[str,str]:
    """Shows a menu in stdout to pick one value of the dict

    Args:
        input_dict (list): list of dict 

    Returns:
        dict: Selected dictionnary
    """
    table = tabulate.tabulate(input_dicts, headers='keys')
    table_lines = table.split('\n')
    prompt = str.join("\n", table_lines[:2])
    picker = bullet.Bullet(choices=table_lines[2:], bullet="•", prompt=str.join("\n", table_lines[:2]), return_index=True)
    print(prompt)
    choice = picker.launch()[1] # Grab index from returned tuple
    return input_dicts[choice]
    
    
def strip_values(input_dicts : dict) -> dict:
    new_dict = {}
    for key in input_dicts:
        if key in KEYS_SHOWS_LLM_PICK_MENU:
            new_dict[key] = input_dicts[key]
    return new_dict


async def main():
    """Run the command line interface."""
    parser = setup_parser()
    args = parser.parse_args()
    if args.version:
        show_version()
        return
    elif args.url_to_scrape is None:
        print("Please provide a URL to scrape.")
        print("Use --help for more information.")
        return 
    elif args.jan_ai and args.llm_url:
        print("You cannot use both --jan-ai and --llm_url")
        exit(PARSING_ERROR)
    if args.email:
        """Email authentication."""
        password = args.password
        if password is None:
            password = getpass("Enter your password for {}: ".format(args.email))
    else:
        """Cookie authentication."""
        if args.cookie is None:
            print("Please provide a cookie for authentication or use email and password.")
            exit(PARSING_ERROR)
    if args.original_output and args.global_summary:
        print("--original-output and --global-summary are mutually exclusive.")
        exit(PARSING_ERROR)
    try:
        async with Scraper(
            url=args.url_to_scrape,
            email=args.email,
            password=password,
            cookie=args.cookie,
            verbose=args.verbose
        ) as scraper:
            if args.verbose:
                print("Scraping the data...")
            activities_dict = await scraper.get_all_activity()
            if args.original_output:
                # No summary
                text = activities_dict_to_plain_text(activities_dict)
                if args.json:
                    text = json.dumps(
                        activities_dict_to_items(activities_dict),
                        indent=3
                    )
                if args.output:
                    with open(args.output, "w") as file:
                        file.write(text)
                else:
                    print(text)
                
            else:
                # Part where we summarize the data
                model = Models.SUMY
                model_url = ""
                model_token = ""
                text = ""
                if args.llm_url is not None and args.jan_ai is False:
                    model = Models.CUSTOM
                    model_url = args.llm_url
                    model_token = args.llm_token
                elif args.jan_ai is True and args.llm_url is None:
                    model = Models.JANAI
                elif args.llm_url is not None:
                    model= Models.CUSTOM
                async with Summarizer(
                    verbose=args.verbose,
                    model=model,
                    model_url=model_url,
                    model_token=model_token,
                ) as summarizer:
                    if model in [Models.JANAI, Models.CUSTOM, Models.CHATGPT]:
                        # Ask using curse
                        if args.model_id is None:
                            llm_list = [strip_values(model) for model in await summarizer.list_llm_models()]
                            llm_selected = dict_to_menu(llm_list)
                            await summarizer.set_llm_id(llm_selected['id'])
                        else:
                            await summarizer.set_llm_id(args.model_id)
                    texts = await summarizer.summarize_activities(activities_dict_to_items(activities_dict))
                    if args.global_summary:
                        if args.verbose:
                            print("Summarizing globally")
                        await summarizer.summarize_global(texts)
                    if args.json:
                        text = json.dumps(texts, indent=3)
                    else:
                        text = "\n".join(texts)
                if args.output:
                    with open(args.output, "w") as file:
                        file.write(text)
                else:
                    print(text)
    except LoginError as e:
        if args.verbose:
            print(f"Error while logging in: {e}")
        exit(SCRAPING_ERROR)
    except ParsingError as e:
        if args.verbose:
            print(f"Error while parsing the data: {e}")
        exit(PARSING_ERROR)