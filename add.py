import requests
import json
import os


def do_request(url):
    json = requests.get(url).json()
    return json


def search_value(json, val):
    found = []
    if isinstance(json, dict):
        for key in json.keys():
            if val in key or val in str(json[key]):
                obj = {"key": key, "val": str(json[key]), "label": None}
                found.append(obj)

    if isinstance(json, list):
        for d in json:
            if not isinstance(d, dict):
                raise ValueError("Falsches Format")
            label = d["label"]
            for key in d.keys():
                if val in key or val in str(d[key]):
                    if isinstance(d[key], dict) or isinstance(d[key], list):
                        continue
                    obj = {"key": key, "val": str(d[key]), "label": label}
                    found.append(obj)
    return found


normal_params = ["module", "format", "idSite", "period", "date",
                 "filter_limit", "format_metrics", "fetch_archive_state",
                 "token_auth", "force_api_session"]


def is_normal_param(param):
    for normal_param in normal_params:
        if param.startswith(normal_param + "="):
            return True
    return False


def build_url_dict(url):
    d = {}
    params = url.split("?")[1].split("&")
    for param in params:
        if is_normal_param(param):
            continue
        key, val = param.split("=")
        d[key] = val
    return d


def printResults(sites_to_fetch, table_data):
    print("\n\nsites_to_fetch: \n")
    print(json.dumps(sites_to_fetch, indent=4))
    print("\n\ntable_data: \n")
    print(json.dumps(table_data, indent=4))

    print("\n\033[31;1mDaran denken 'idx' zu ändern\033[0m")


def is_dict_equal_except_columns(dict1, dict2):
    for key in set(dict1.keys()).union(dict2.keys()):
        if key == "showColumns":
            continue
        if dict1.get(key) != dict2.get(key):
            return False
    return True


def put_results_in_data_file(sites_to_fetch, table_data):
    print("Schreibe in die data.json...")
    with open(os.getcwd() + "/data.json", 'r+', encoding='utf-8') as data_file:
        try:
            fetch_data = json.load(data_file)
        except ValueError as e:
            raise ValueError(f"JSON-Fehler: {e}")
        saved_stf = fetch_data["sites_to_fetch"]
        exists = 0
        idx = 0
        for site in saved_stf:
            if site == sites_to_fetch:
                exists = 1
                break
            if is_dict_equal_except_columns(site, sites_to_fetch):
                exists = 2
                break
            idx += 1

        if exists == 0:
            saved_stf.append(sites_to_fetch)
            fetch_data["sites_to_fetch"] = saved_stf

        if exists == 2:
            if table_data["field"] not in saved_stf[idx]["showColumns"].split(","):
                saved_stf[idx]["showColumns"] += f",{table_data['field']}"
                fetch_data["sites_to_fetch"] = saved_stf

        saved_td = fetch_data["table_data"]
        for td in saved_td:
            if td["name"] == table_data["name"]:
                print("\033[31;1mDieser Name existiert bereits!\033[0m")
                return
        table_data["idx"] = idx
        saved_td.append(table_data)
        fetch_data["table_data"] = saved_td

        data_file.seek(0)
        data_file.write(json.dumps(fetch_data, indent=4))
        data_file.truncate()
        print("Erfolg!")


def main():
    url = input("Bitte URL eingeben > ")
    data = do_request(url)
    value = input("Bitte jetzigen Wert eingeben > ")

    keys = search_value(data, value)
    if len(keys) == 0:
        print("\033[31;1mKeine Datenpunkte für diesen Wert gefunden!\033[0m")
        return

    searched_value = None
    i = 0
    for key in keys:
        i += 1
        label = ""
        if key["label"] is not None:
            label = " / Label = " + key["label"]
        print(f"\033[31;1m{i}\033[0m: {key['key']} = {key['val']}{label}")

    idx = input("Bitte Zahl mit dem richtigen Wert angeben > ")
    if not idx.isdigit():
        print("\033[31;1mFEHLER: Bitte eine Zahl eingeben!\033[0m")
        return
    if int(idx) > len(keys):
        print("\033[31;1mFEHLER: Die Zahl ist zu groß\033[0m")
        return
    searched_value = keys[int(idx) - 1]

    name = input("Wie soll der Wert in der Tabelle heißen? > ")

    table_data = {
        "idx": -1,
        "field": searched_value["key"],
        "name": name
    }

    if searched_value["label"] is not None:
        table_data["label"] = searched_value["label"]

    sites_to_fetch = build_url_dict(url)

    if os.path.isfile(os.getcwd() + "/data.json"):
        put_results_in_data_file(sites_to_fetch, table_data)
    else:
        printResults(sites_to_fetch, table_data)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"\033[31;1mFEHLER: {e}\033[0m")
    input("\n\nBitte [ENTER] zum Beenden drücken")
