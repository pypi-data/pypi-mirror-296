import asyncio
import datetime
import aiohttp
import bs4
import re
from tqdm.asyncio import tqdm

COOKIE_KEY = "PHPSESSID"
LINK_CLASS = "item"
LINK_FILTER = "afficher/periode"
ACTIVITY_LIST_CLASS = "ui tab scrollable-tab"
REPORT_FILTER = "ACTIVIT"
DESCRIPTION_CLASS = "description"
BOOK_CLASS = "ui no-disabled-opacity form"
END_OF_ACTIVITY = "Pièces jointes du questionnaire"
ACTIVITIES_DIV_CLASS = "field"
ACTIVITY_DIV_CLASS = "accordion"
CONTENT_ACTIVE_CLASS = "content active"
FIELD_REPLACE = "[Moyenne des réponses : ]"
class LoginError(Exception):
    pass

class ParsingError(Exception):
    pass

class Scraper:
    def __init__(self, 
                 url: str,
                 email: str = None, 
                 password: str = None, 
                 cookie: str = None, 
                 verbose: bool = False):
        if not url.startswith('http://') or not url.startswith('https://'):
            url = f"https://{url}"
        self.url = url
        self.email = email
        self.password = password
        self.cookie = cookie
        self.verbose = verbose
        self.session = None
    async def __aenter__(self):
        """Async context manager."""
        # Create a new session when entering the context manager.
        self.session = aiohttp.ClientSession()
        try:
            await self.login()
        except Exception as e:
            await self.session.close()
            raise e
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        """Async context manager."""
        # Close the session when exiting the context manager.
        await self.session.close()
    
    async def login(self):

        if self.cookie:
            """Cookie authentication."""
            cookie_dict = {COOKIE_KEY: self.cookie}
            self.session.cookie_jar.update_cookies(cookie_dict, self.url)
            if self.verbose:
                print("Testing the cookie...")
            async with self.fetch(f"{self.url}/_connexion") as response:
                if "Connexion" in response:
                    raise LoginError("The cookie provided is invalid")
                
        elif self.email:
            """Email authentication."""
            if self.verbose:
                print("Logging in with email and password...")
            data={
                "_username": self.email,
                "_password": self.password,
                "_remember_me": 1,
            }
            login_response = await self.session.post(
                f"{self.url}/_connexion",
                data=data
            )
            if login_response.status != 200:
                if self.verbose:
                    print(f"Login request failed with status code {login_response.status}")
                raise LoginError(f"The login request failed with status code {login_response.status}")
            elif "Identifiants invalides" in await login_response.text():
                raise LoginError("Invalid email or password.")
            else:
                if self.verbose:
                    print("Login successful.")
            
        else:
            raise ValueError("Please provide either a cookie or an email and password.")

    async def fetch(self, full_url: str = None):
        if self.verbose:
            print(f"Fetching {full_url}...")
        async with self.session.get(full_url) as response:
            return await response.text(encoding="utf-8")
    
    
    async def list_activities(self):
        """List the activities."""
        if self.verbose:
            print("Listing the activities...")
        response = await self.fetch(f"{self.url}/book/liste#/alll")
        soup = bs4.BeautifulSoup(response, "html.parser")
        all_pages_list = soup.find_all("div", class_=ACTIVITY_LIST_CLASS)[-1]

        all_pages_links = all_pages_list.find_all("a", class_=LINK_CLASS)

        filtered_links = {}
        for link in all_pages_links:
            if REPORT_FILTER in link.text and LINK_FILTER in link["href"]:
                description = link.find('div', class_=DESCRIPTION_CLASS)
                description = description.text.strip()
                date = description[-10:]
                try:
                    date_obj = datetime.datetime.strptime(date, "%d/%m/%Y")
                except ValueError as e:
                    raise ParsingError(f"Error while parsing the date: {e}")
                filtered_links[date_obj] = link["href"]
                if self.verbose:
                    print(f"Found activity due to {date} ({self.url}{link['href']})")
        return filtered_links
    
    def _clean_text(self, text: str) -> str:
        text = text.replace("\n ", "\n")
        text = text.strip()
        
       
        # remove tabs
        text = re.sub(r"\t+", "", text)
        # remove multiple spaces
        text = re.sub(r" +", " ", text)

        # remove multiple newlines
        text = re.sub(r"\n+", "\n", text)
        
        # interprete all unicode escape sequences
        #  \u00e0 transform to à
        # replace all \
        # use a lambda function to replace all unicode escape sequences
        
        
        
        return text
    
    def _clean_field(self, field: bs4.element.Tag) -> str:
        # decode
        text = field.text.strip()
        text = text.replace(FIELD_REPLACE, "")
        text = self._clean_text(text)
        return text
    
    def _parse_activity(self, activity_div: bs4.element.Tag) -> dict:
        activity = {}
        activity_fields = []
        new_activity = False
        try:
            activity_fields = activity_div.find('div', class_=CONTENT_ACTIVE_CLASS).find_all('div', class_=CONTENT_ACTIVE_CLASS)
        except AttributeError as e:
            activity_fields = activity_div.find_all('div', class_="ui segment")
            new_activity = True
        cleaned_fields = []
        i = 0
        for field in activity_fields:
            if not new_activity:
                if i >= 2:
                    field = field.find_all('div', class_="field")[1].find('div', class_="ui segment")
            i+=1
            cleaned_fields.append(self._clean_field(field))
        if new_activity:
            activity["title"] = cleaned_fields[0]
            activity["goal"] = cleaned_fields[1]
            activity["results"] = cleaned_fields[2]
            activity["skills"] = cleaned_fields[3]
            activity["issue_encountered"] = cleaned_fields[4]
            activity["facts"] = cleaned_fields[5]
        else:
            activity["title"] = f"{cleaned_fields[0]} ({cleaned_fields[1]})"
            activity["goal"] = cleaned_fields[2]
            activity["results"] = cleaned_fields[3]
            activity["skills"] = cleaned_fields[4]
            activity["issue_encountered"] = cleaned_fields[5]
            activity["facts"] = cleaned_fields[6]
        return activity

    def _parse_report(self, report_div: bs4.element.Tag) -> dict:
        activities_divs = report_div.find("div", class_=ACTIVITIES_DIV_CLASS).find("div")
        individual_activities = activities_divs.find_all("div", recursive=False)
        if len(individual_activities) == 0:
            activities_divs = report_div.find_all("div", class_=ACTIVITIES_DIV_CLASS)[1].find("div").find("div").find("div")
            individual_activities = activities_divs.find_all("div", class_="ui segment field")
        activities = []
        for activity_div in activities_divs.find_all("div", recursive=False):
            activities.append(self._parse_activity(activity_div))
        return activities

    async def get_all_activity(self):
        """Get all the activities."""
        activities = await self.list_activities()
        futures = [self.fetch(f"{self.url}{link}") for link in activities.values()]
        responses = []
        if self.verbose:
            responses = await tqdm.gather(*futures)
        else:
            responses = await asyncio.gather(*futures)
        act_text = {}
        for i in range(len(responses)):
            title = list(activities.keys())[i]
            if self.verbose:
                print(f"Parsing activity: {title}")
            response = responses[i]
            soup = bs4.BeautifulSoup(response, "html.parser")
            book = soup.find("form", class_=BOOK_CLASS)
            act_text[title] = self._parse_report(book)
           
        
        # sort the activities by date
        act_text = dict(sorted(act_text.items()))
        return act_text
