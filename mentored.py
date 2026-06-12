import pandas as pd
import json

mentored = pd.read_json("_data/mentored.json")
mentored.drop_duplicates(keep=False, inplace=True)
mentored.dropna(inplace=True)
mentored.sort_values("date", ascending=False, inplace=True)
parsed = json.loads(mentored.to_json(orient="records", date_format="iso"))

json.dump(parsed, open("_data/sorted_mentored.json", "w"), indent=4)
