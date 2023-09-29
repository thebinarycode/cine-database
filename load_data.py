import os

import utils

from dotenv import load_dotenv
import pandas


os.chdir(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

def load_data() -> pandas.DataFrame:
    if os.path.exists(os.getenv("MOVIE_DATABASE_ID")):
        df = pandas.read_csv(os.getenv("MOVIE_DATABASE_ID"))
    else: print("database file not present")

def save_data(data: dict):
    pandas.DataFrame.to_csv(os.getenv("DATABASE_ID"))
    print("database file saved successfully")

def process_data(wiki_data: dict) -> pandas.DataFrame:
    processed = {}
    movie_df = pandas.DataFrame(columns=["Year", "Film", "Language", "Director", "Writer", "Cast", "Producer"])

    for key in wiki_data.keys():
        if "actor" in str(key).lower():
            actor_df = wiki_data[key]
            if movie_df.empty:
                if "Language" in actor_df.columns: movie_df["Language"] = actor_df["Language"]
                movie_df[["Year", "Film"]] = actor_df[["Year", "Film"]].copy(deep=True)
                movie_df["Cast"] = wiki_data["name"]
            else:
                movie_df = utils.append_data(movie_df, actor_df, wiki_data["name"], False)

        if "director" in str(key).lower():
            director_df = wiki_data[key]
            if movie_df.empty:
                movie_df[["Year", "Film", "Director"]] = director_df[["Year", "Film", "Director"]].copy(deep=True)
                movie_df["Language"] = director_df["Language"] if "Language" in director_df.columns else ""
                movie_df["Producer"] = director_df["Producer"] if "Producer" in director_df.columns else ""
                movie_df["Writer"] = director_df["Writer"] if "Writer" in director_df.columns else ""
            else:
                if "Language" not in director_df.columns: director_df["Language"] = ""
                if "Producer" not in director_df.columns: director_df["Producer"] = ""
                if "Writer" not in director_df.columns: director_df["Writer"] = ""
                movie_df = utils.append_data(movie_df, director_df, wiki_data["name"], True)

            movie_df.loc[(movie_df["Director"] == "yes") | (movie_df["Producer"] == "Yes"), "Director"] = wiki_data["name"]
            movie_df.loc[(movie_df["Producer"] == "yes") | (movie_df["Producer"] == "Yes"), "Producer"] = wiki_data["name"]
            movie_df.loc[(movie_df["Writer"] == "yes") | (movie_df["Writer"] == "Yes"), "Writer"] = wiki_data["name"]
    return movie_df


# dir = pandas.read_csv("dir.csv")
# act = pandas.read_csv("act.csv")

# dic = {"As Actor": act, "As Director": dir, "name": "Kamal Haasan"}
# res = process_data(dic)
# res.to_csv("out.csv")





