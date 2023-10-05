import os
import difflib

import pandas
import numpy



def get_name(url: str) -> str:
    url = url.replace("_filmography", "")
    return url.split("/")[-1].replace("_", " ")


def get_best_match(results: list, query: str) -> str:
    try:
        indices = [idx for idx, s in enumerate(results) if "wikipedia" not in s]
        results = numpy.delete(results, indices).tolist()
        if len(results) == 1: return results[0]
        elif len(results) > 1:
            sub_idx = [idx for idx, s in enumerate(results) if "filmography" in s]
            if len(sub_idx) == 1: return results[sub_idx[0]]
            else:
                url_dict = {}
                for e in results: url_dict[get_name(e).lower()] = e
                return url_dict[difflib.get_close_matches(query.lower(), url_dict.keys(), 1, cutoff=0.5)[0]]
        else:
            print("wikipedia site may be down, try again later") 
            return None
    except Exception as err:
        print(f"Exception occured: {err}")
        return None


def append_data(df1: pandas.DataFrame, df2: pandas.DataFrame, name: str, isactor: bool) -> pandas.DataFrame:
    keys = ["Director", "Producer", "Writer"] if "Director" in df2.columns else ["Cast"]
    # df2.rename(columns = {'Title':'Film'}, inplace=True)
    for _, row in df2.iterrows():
        # if df1[["Year", "Film"]].isin(row[["Year", "Film"]][index]).any().any():
        # match_index = df1.index[df1[["Year", "Film"]] == row[["Year", "Film"]]].tolist()
        match_index = df1[(df1["Year"] == row["Year"]) & (df1["Film"] == row["Film"])].index.tolist()
        if match_index: 
            if all(pandas.isnull(df1.loc[match_index, keys])): df1.loc[match_index, keys] = name if isactor else row[["Director", "Producer", "Writer"]].values
            else:
                for key in keys: 
                    if pandas.isnull(df1.loc[match_index, key]): df1.loc[match_index, key] = row[key].values
        else:
            castname = name if isactor else ""
            language = row["Language"] if "Language" in df2.columns else ""
            director = row["Director"] if "Director" in df2.columns else ""
            writer = row["Writer"] if "Writer" in df2.columns else ""
            producer = row["Producer"] if "Producer" in df2.columns else ""
    
            row = pandas.Series([row["Year"], row["Film"], language, director, writer, castname, producer], index=df1.columns)

            # row = pandas.Series([row["Year"], row["Film"], row["Language"], row["Director"], row["Writer"], castname, row["Producer"]], index=df1.columns)
            df1 = pandas.concat([df1, pandas.DataFrame([row])], ignore_index=True)
    return df1


def get_data(file_name: str) -> pandas.DataFrame:
    if os.path.exists(file_name):
        df = pandas.read_csv(file_name)
        return df
    else:
        print("database file not present")
        return pandas.DataFrame()


# def save_data(data: dict, file_name: str) -> bool:
#     try:
#         pandas.DataFrame.to_csv(file_name)
#         return True
#     except Exception as err:
#         print(f"Exception occured: {err}")
#         return False


def save_data(data: pandas.DataFrame, file_name: str) -> bool:
    try:
        data.reset_index(drop=True)
        data.to_csv(file_name, index=False)
        return True
    except Exception as err:
        print(f"Exception occured: {err}")
        return False
    

def content_check(data_dict: dict) -> (dict, bool):
    pop_key = []
    for key, val in data_dict.items():
        if key == "name": continue
        if not isinstance(val, pandas.DataFrame): pop_key.append(key)
        else:
            df = data_dict[key]
            if df.empty: pop_key.append(key)
            elif not any([e in df.columns for e in ["Director", "Producer", "Writer", "Role", "Roles", "Role(s)"]]): pop_key.append(key)
    for e in pop_key: data_dict.pop(e)
    if len(data_dict) > 1: return data_dict, True
    else: return data_dict, False



            

    