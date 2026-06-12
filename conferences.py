import pandas as pd
import json

confs = pd.read_json("_data/Conference.json")
confs.dropna(inplace=True)
result = confs.sort_values("date", ascending=False).to_json(
    orient="records", date_format="iso"
)
parsed = json.loads(result)
parsed
json.dump(parsed, open("_data/sorted_confs.json", "w"), indent=4)
