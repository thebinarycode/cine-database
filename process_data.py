import os

import pandas

import utils


def format_data(wiki_data: dict) -> pandas.DataFrame:
    processed = {}
    movie_df = pandas.DataFrame(columns=["Year", "Film", "Language", "Director", "Writer", "Cast", "Producer"])

    for key in wiki_data.keys():
        if key == "name": continue
        if "actor" in str(key).lower(): movie_df = actor_format(wiki_data, movie_df, key)  
        elif "director" in str(key).lower(): movie_df = dir_format(wiki_data, movie_df, key)
        else:
            df = wiki_data[key]
            if any([e in df.columns for e in ["Role", "Roles", "Role(s)"]]): movie_df = actor_format(wiki_data, movie_df, key)
            # elif set(["Director", "Producer", "Writer"]).issubset(df.columns): movie_df = dir_format(wiki_data, movie_df, key)
            elif any([e in df.columns for e in ["Director", "Producer", "Writer"]]): dir_format(wiki_data, movie_df, key)
            else: continue                          
    return movie_df


def actor_format(wiki_data: pandas.DataFrame, movie_df: pandas.DataFrame, key: str):
    actor_df = wiki_data[key]
    if actor_df.empty: return movie_df
    else:
        actor_df.rename(columns={'Title':'Film', 'Movie':'Film', 'Language(s)':'Language', 'Languages':'Language'}, inplace=True)
        if movie_df.empty:
            # if "Language" in actor_df.columns: movie_df["Language"] = actor_df["Language"]
            selection_col = ["Year", "Film"]
            if "Director" in actor_df.columns: selection_col.append("Director")
            if "Language" in actor_df.columns: selection_col.append("Language")
            movie_df[selection_col] = actor_df[selection_col].copy(deep=True)
            movie_df["Cast"] = wiki_data["name"]
        else: movie_df = utils.append_data(movie_df, actor_df, wiki_data["name"], True)
        return movie_df


def dir_format(wiki_data: pandas.DataFrame, movie_df: pandas.DataFrame, key: str) -> pandas.DataFrame:
    director_df = wiki_data[key]
    if director_df.empty: return None
    else:
        director_df.rename(columns={'Language(s)':'Language', 'Languages':'Language', 'Title': 'Film', 'Movie':'Film'}, inplace=True)

        if "Language" not in director_df.columns: director_df["Language"] = ""
        if "Director" not in director_df.columns: director_df["Director"] = ""
        if "Producer" not in director_df.columns: director_df["Producer"] = ""
        if "Writer" not in director_df.columns: director_df["Writer"] = ""

        if movie_df.empty:
            selection_col = ["Year", "Film", "Language", "Director", "Producer", "Writer"]
            movie_df[selection_col] = director_df[selection_col].copy(deep=True)
        else: movie_df = utils.append_data(movie_df, director_df, wiki_data["name"], False)

        movie_df.loc[(movie_df["Director"] == "yes") | (movie_df["Director"] == "Yes"), "Director"] = wiki_data["name"]
        movie_df.loc[(movie_df["Producer"] == "yes") | (movie_df["Producer"] == "Yes"), "Producer"] = wiki_data["name"]
        movie_df.loc[(movie_df["Writer"] == "yes") | (movie_df["Writer"] == "Yes"), "Writer"] = wiki_data["name"]
        return movie_df


def merge_to_database(movie_df: pandas.DataFrame) -> bool:
    archive_df = utils.get_data(os.getenv("MOVIE_DATABASE_ID"))
    if not archive_df.empty:
        default_cols = list(archive_df.columns)
        update_cols = ["Language", "Director", "Writer", "Cast", "Producer"]
        movie_df["Year"] = movie_df["Year"].astype("Int64")
        archive_df = pandas.merge(archive_df, movie_df, on=["Year", "Film"], how="outer")
        for col in default_cols: 
            if col not in list(archive_df.columns): archive_df[col] = "" 
        for i, row in archive_df.iterrows():
            for col in update_cols: 
                if row[col+"_x"] == row[col+"_y"]: archive_df.at[i, col] = row[col+"_x"]
                elif type(row[col+"_x"]) is list: 
                    row[col+"_x"].append(row[col+"_y"])
                    archive_df.at[i, col] = row[col+"_x"]
                elif (pandas.isnull(row[col+"_x"]) or pandas.isnull(row[col+"_y"])):
                    archive_df.at[i, col] = row[col+"_x"] if pandas.isnull(row[col+"_y"]) else row[col+"_y"] if pandas.isnull(row[col+"_x"]) else ""
                else: archive_df.at[i, col] = [row[col+"_x"], row[col+"_y"]]
        remove_cols = [col for col in list(archive_df.columns) if col not in default_cols]
        archive_df.drop(remove_cols, axis=1, inplace=True)
        resp = utils.save_data(archive_df, os.getenv("MOVIE_DATABASE_ID"))
    else:
        resp = utils.save_data(movie_df, os.getenv("MOVIE_DATABASE_ID"))
    return resp




# dir = pandas.read_csv("dir.csv")
# act = pandas.read_csv("act.csv")

# dic = {"As Actor": act, "As Director": dir, "name": "Kamal Haasan"}
# res = process_data(dic)
# res.to_csv("out.csv")





