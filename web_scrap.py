import utils

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import pandas


session = HTMLSession()

def google_search(query: str) -> list:
    query += " filmography"
    query = query.replace(" ", "+")
    url = f"https://google.co.in/search?q={query}&cr=countryIN&hl=en"
    response = session.get(url)

    if response.status_code == 200:
        links = list(response.html.absolute_links)

        google_domains = ('https://www.google.', 
                            'https://google.', 
                            'https://webcache.googleusercontent.', 
                            'http://webcache.googleusercontent.', 
                            'https://policies.google.',
                            'https://support.google.',
                            'https://maps.google.')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        return links
    else:
        print("unble to process the request")
        print(f"status code: {response.status_code}, status message: {response.reason}")
        return None


def wikipedia_scrap(url: str) -> dict:
    wiki_collection = {}
    invalid_tags = ["See also", "Notes", "References", "Bibliography", "External links"]

    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # raw_tags = soup.find_all(attrs={"class": "mw-headline"})
        # raw_tags = [ele.text.strip() for ele in raw_tags if ele.text.strip() not in invalid_tags]
        raw_tables = soup.find_all(attrs={"class": "wikitable"})

        for raw_table in raw_tables:
            raw_tag = raw_table.find_previous(attrs={"class": "mw-headline"})
            for span_tag in raw_table.findAll('span'):
                if "Green tick" in str(span_tag): span_tag.replace_with("yes")
            table = pandas.read_html(str(raw_table))
            wiki_df = table[0]
            if type(wiki_df.columns) == pandas.core.indexes.multi.MultiIndex: wiki_df.columns = wiki_df.columns.droplevel(0)
            if "yes" in wiki_df.columns: wiki_df.drop("yes", axis=1, inplace=True)
            wiki_df.replace("yesyes", "yes", inplace=True)
            wiki_collection[raw_tag.text.strip()] = wiki_df

        # wiki_table = pandas.read_html(url, attrs={"class": ["wikitable", "wikitable sortable", "wikitable sortable jquery-tablesorter", 
        #                                                     "wikitable sortable plainrowheaders jquery-tablesorter"]})
        # wiki_table = pandas.read_html(url)
        return wiki_collection
    else:
        print("unble to process the request")
        print(f"status code: {response.status_code}, status message: {response.reason}")
        return None   

def scrap_data(name: str) -> dict:
    results = google_search(name)
    index = [idx for idx, s in enumerate(results) if "wikipedia" in s][0]
    wiki_url = results[index]
    # wiki_url = "https://en.wikipedia.org/wiki/Kamal_Haasan_filmography"
    wiki_info = wikipedia_scrap(wiki_url)
    wiki_info["name"] = utils.get_name(wiki_url)
    return wiki_info






