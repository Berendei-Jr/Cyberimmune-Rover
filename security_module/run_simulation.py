import json
import re

str = "1: VFR_HUD {airspeed : 0.0, groundspeed : 0.027554601430892944, heading : 353, throttle : 0, alt : 583.9299926757812, climb : -0.004994789604097605}"
data_str = str.split('{', 1)[1].rsplit('}', 1)[0]

# Преобразуем строку в словарь
data_dict = {}
for item in data_str.split(','):
    key, value = item.split(':', 1)
    data_dict[key.strip()] = float(value.strip()) if '.' in value else int(value.strip())

json = json.dumps(data_dict)
print(json)
