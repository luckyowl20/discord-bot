"""
serpstack info

Account #1
==================================================
name: Jones Davison
email: iznofwrjquzgtyfjit@ttirv.net
pass: iznofwrjquzgtyfjit
street: 576  Smith Road
city: Marietta
state: Georgia
zip: 30067
api key: ff7864adaab76a54c5a8d6cda3fdc6cc

Account #2
==================================================
name: Davis jonsey
email: dsnzxgaoaxbogsbgmx@ttirv.com
pass: dsnzxgaoaxbogsbgmx
street: 3130  Dog Hill Lane
city: home
state: Kansas
zip: 66438
api key: 7e47661d9410ba09b21acf3509cd4bec
"""

from operator import itemgetter
import requests
import json
import os

api_keys_path = "api_keys.json"
max_requests = 475

prev_searches = os.listdir("past_searches")
for i in range(len(prev_searches)):
    prev_searches[i] = prev_searches[i]
print(f"database entries: {prev_searches}\n")


def get_key_info(path):
    keys = []
    total_accs = 0
    with open(path, "r") as file:
        key_info = json.load(file)

    for key in key_info:
        total_accs += key_info[key]["num_accesses"]
        temp_key = [key, key_info[key]["key"], key_info[key]["num_accesses"]]
        keys.append(temp_key)
    return keys, total_accs, key_info


def use_key(keys):
    print(f"using key {sorted(keys, key=itemgetter(2))[0]}, out of {sorted(keys, key=itemgetter(2))}")
    return sorted(keys, key=itemgetter(2))[0]


def update_key(key_used, raw_keys):
    print(f"{key_used[0]} ({key_used[1]} was used, now has {key_used[2] + 1} uses)")

    key_used[2] += 1
    raw_keys[key_used[0]]["num_accesses"] = key_used[2]

    with open(api_keys_path, "w") as file:
        json.dump(raw_keys, file)


def assign_data(data_in, start, num_results):
    urls = []
    for j in range(num_results):
        urls.append(data_in["image_results"][start + j]["image_url"])
    return urls


def get_image(query: str, start=0, num_results=1, modifier=""):
    global prev_searches
    keys, total_accesses, raw_keys = get_key_info(api_keys_path)
    error = False

    print(os.getcwd())
    print(f"Query: {query}, Start: {start}, Number of Results: {num_results}")

    if f"{query}_{modifier}.json" not in prev_searches and total_accesses < max_requests:
        print("USED API")
        prev_searches.append(f"{query}_{modifier}.json")

        if modifier != "":
            query_modded = query + f" {modifier}"
        else:
            query_modded = query

        url = "http://api.serpstack.com/search?access_key={k}&query={q}&type=images"
        key = use_key(keys)

        print(f"url request = {url.format(q=query_modded, k=key[1])}")
        result = requests.get(url.format(q=query_modded, k=key[1]))
        data = json.loads(result.text)
        update_key(key, raw_keys)
        print(f"query result: {data}")

        with open(f"past_searches/{query}_{modifier}.json", "w") as f:
            json.dump(data, f)

        image_urls = assign_data(data, start, num_results)

    elif total_accesses < max_requests:
        with open(f"past_searches/{query}_{modifier}.json", "r") as f:
            print("LOADED FROM DATABASE")
            data = json.load(f)

        image_urls = assign_data(data, start, num_results)

    else:
        image_urls = ""
        error = True

    print(f"   image urls: {image_urls}")
    return image_urls, start, error


# printing keys when initialized
print(get_key_info(api_keys_path)[0])
print()
