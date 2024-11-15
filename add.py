import requests
import json


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

    d = {
        "idx": -1,
        "field": searched_value["key"],
        "name": name
    }

    if searched_value["label"] is not None:
        d["label"] = searched_value["label"]

    print("\n\nsites_to_fetch: \n")
    print(json.dumps(build_url_dict(url), indent=4))
    print("\n\ntable_data: \n")
    print(json.dumps(d, indent=4))

    print("\n\033[31;1mDaran denken 'idx' zu ändern\033[0m")


if __name__ == "__main__":
    main()
    input("\n\nBitte [ENTER] zum Beenden drücken")
