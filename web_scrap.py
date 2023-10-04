import utils

from bs4 import BeautifulSoup
from requests_html import HTMLSession

import pandas


session = None

def web_search(query: str) -> list:
    search_engines = ["https://google.com/", "https://search.yahoo.com/", "https://www.bing.com/"]

    filter_domains = ("https://www.google.", 
                                "https://google.", 
                                "https://posts.google.com",
                                "https://webcache.googleusercontent.", 
                                "http://webcache.googleusercontent.", 
                                "https://policies.google.",
                                "https://support.google.",
                                "https://maps.google.",
                                "http://go.microsoft.com",
                                "https://r.search.yahoo.com/",
                                "https://search.yahoo.com/",
                                "https://images.search.yahoo.com/",
                                "https://news.search.yahoo.com/",
                                "https://www.youtube.com",
                                "https://music.youtube.com",
                                "https://www.bing.com",
                                "https://microsoft.com",
                                "https://mail.yahoo.com"
                                "https://www.facebook.com",
                                "https://www.instagram.com",
                                "https://in.bookmyshow.com")
    
    query += " filmography"
    query = query.replace(" ", "+")
    
    links = []
    for run in search_engines: 
        search_url = run + f"search?q={query}&cr=countryIN&hl=en"
        response = session.get(search_url)

        if response.status_code == 200: links = links + list(response.html.absolute_links)
        else:
            print("unble to process the request")
            print(f"status code: {response.status_code}, status message: {response.reason}")

    for url in links[:]:
        if url.startswith(filter_domains): links.remove(url)

    return list(set(links))


def wikipedia_scrap(url: str) -> dict:
    wiki_collection = {}
    invalid_tags = ["See also", "Notes", "References", "Bibliography", "External links"]

    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # raw_tags = soup.find_all(attrs={"class": "mw-headline"})
        # raw_tags = [ele.text.strip() for ele in raw_tags if ele.text.strip() not in invalid_tags]
        raw_tables = soup.find_all(attrs={"class": "wikitable"})

        for raw_table in raw_tables:
            raw_tag = raw_table.find_previous(attrs={"class": "mw-headline"})
            for span_tag in raw_table.findAll("span"):
                if "Green tick" in str(span_tag): span_tag.replace_with("yes")
            table = pandas.read_html(str(raw_table))
            wiki_df = table[0]
            if type(wiki_df.columns) == pandas.core.indexes.multi.MultiIndex: wiki_df.columns = wiki_df.columns.droplevel(0)
            if "yes" in wiki_df.columns: wiki_df.drop("yes", axis=1, inplace=True)
            wiki_df.replace("yesyes", "yes", inplace=True)
            wiki_df.dropna(thresh=4, inplace=True)
            wiki_collection[raw_tag.text.strip()] = wiki_df

        # wiki_table = pandas.read_html(url, attrs={"class": ["wikitable", "wikitable sortable", "wikitable sortable jquery-tablesorter", 
        #                                                     "wikitable sortable plainrowheaders jquery-tablesorter"]})
        # wiki_table = pandas.read_html(url)
        return wiki_collection
    else:
        print("unble to process the request")
        print(f"status code: {response.status_code}, status message: {response.reason}")
        return None   


def scrap_data(name: str, wiki_url:str = None) -> dict:
    if wiki_url:
        wiki_info = wikipedia_scrap(wiki_url)
        wiki_info["name"] = utils.get_name(wiki_url)
        return wiki_info
    else:
        global session
        session = HTMLSession()
        results = web_search(name)
        wiki_url = utils.get_best_match(results, name)
        print(f"best match url from the search: {wiki_url}")
        try:
            if wiki_url:
                # wiki_url = results[index]
                # wiki_url = "https://en.wikipedia.org/wiki/Kamal_Haasan_filmography"
                wiki_info = wikipedia_scrap(wiki_url)
                wiki_info["name"] = utils.get_name(wiki_url)
                return wiki_info
            else:
                print("google results doesn't contain relevant result") 
                return {}
        except Exception as err:
            print(f"Exception occured: {err}")
            return {}  






