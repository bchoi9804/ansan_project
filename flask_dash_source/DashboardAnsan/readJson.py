import json
from unicodedata import name

with open("result.json", "r") as result_json:

    json_data = json.load(result_json)
index = len(json_data)
print(json_data[index-1])



