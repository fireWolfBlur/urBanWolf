import json
data = {
    "event_id": 0,
    "title": None,
    "description": None,
    "media": None,
    "data_start": None,
    "data_end": None
}
with open('data.json','w') as f:
    data_format = json.dumps(data)
    f.write(data_format)