import os
from dotenv import load_dotenv

from web_scrap import scrap_data
import process_data
from utils import content_check




os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    load_dotenv()
    name = input("Enter the name to begin search: ")
    print(f"******** searching <{name}> ********")

    wiki_info = scrap_data(name)
    wiki_info, check = content_check(wiki_info)
    if check: start_process(wiki_info, name)
    else:
        print("No results found")
        url = input("Enter the wikipedia filmography url: ")
        start_process(scrap_data(name, url), name)


def start_process(wiki_info: dict, name):
    name = wiki_info.get("name")
    print(f"Personality identified is: {name}")
    formatted = process_data.format_data(wiki_info)
    if process_data.merge_to_database(formatted): print(f"{name}'s data added to the archive")
    else: print(f"error occured while processing {name}'s data")


if __name__ == "__main__":
    main()