""" Command line interface for the calisum package. """

import argparse
from openai import OpenAI
from getpass import getpass
from calisum import PARSING_ERROR, SCRAPING_ERROR, __app_name__, __version__
from calisum.scrapper import LoginError, ParsingError, Scrapper, COOKIE_KEY


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
    scraper.add_argument(
        "-o",
        "--original-output",
        action="store_true",
        help="Output the original data instead of the summary.")

    llm = parser.add_argument_group("LLM options")
    llm.add_argument(
        "--custom-llm",
        help="URL to the LLM page open api endpoint."
    )
    llm.add_argument(
        "--jan-ai",
        action="store_true",
        help="Use localhost jan-ai."
    )
    
    return parser
    


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
    try:
        async with Scrapper(
            url=args.url_to_scrape,
            email=args.email,
            password=password,
            cookie=args.cookie,
            verbose=args.verbose
        ) as scrapper:
            print("Scraping the data...")
            activities_dict = await scrapper.get_all_activity()
            single_activity_list = []
            for activity_list in activities_dict.values():
                single_activity_list.extend(activity_list)
            single_text = ""
            for activity in single_activity_list:
                activity_text = f"{activity['title']}\n\tGoal: {activity['goal']}\n\tResults: {activity['results']}\n\tIssue_encountered: {activity['issue_encountered']}\n\tSkills mastered: {activity['skills']}\n\tFacts: {activity['facts']}\n"
                single_text += activity_text
            if args.original_output:
                if args.output:
                    with open(args.output, "w") as file:
                        file.write(single_text)
                else:
                    print(single_text)
            else:
                print("TODO: Summarize the data.")
                raise NotImplementedError
    except LoginError as e:
        if args.verbose:
            print(f"Error while logging in: {e}")
        exit(SCRAPING_ERROR)
    except ParsingError as e:
        if args.verbose:
            print(f"Error while parsing the data: {e}")
        exit(PARSING_ERROR)