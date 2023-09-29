import pandas

def get_name(url: str) -> str:
    url = url.replace("_filmography", "")
    return url.split("/")[-1].replace("_", " ")

def append_data(df1: pandas.DataFrame, df2: pandas.DataFrame, name: str, isactor: bool) -> pandas.DataFrame:
    keys = ["Director", "Producer", "Writer"] if "Director" in df2.columns else ["Cast"]
    for index, row in df2.iterrows():
        # if df1[["Year", "Film"]].isin(row[["Year", "Film"]][index]).any().any():
        # match_index = df1.index[df1[["Year", "Film"]] == row[["Year", "Film"]]].tolist()
        match_index = df1[(df1["Year"] == row["Year"]) & (df1["Film"] == row["Film"])].index.tolist()
        if match_index:
            df1.loc[match_index, keys] = name if isactor else row[["Director", "Producer", "Writer"]].values
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
            

    