import csv
import json

import requests


searchfor = ["parrot", "dji"]


def addRecord(key: str, row: list[str], store: dict[str, dict[str, str]]):
    macbase = row[1]
    company_full = row[2]
    if store.get(key) is None:
        store[key] = {}
    if store[key].get(macbase) is None:
        store[key][macbase] = company_full


with requests.Session() as session:

    out = {}
    # Currently, parrot and dji are only in the MA-L registry
    for url in [
        "http://standards-oui.ieee.org/oui/oui.csv",
        "http://standards-oui.ieee.org/oui28/mam.csv",
        "http://standards-oui.ieee.org/oui36/oui36.csv",
    ]:
        print("Grabbing {}".format(url))
        download = session.get(url)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        for row in cr:
            for key in searchfor:
                if key in row[2].lower():
                    addRecord(key, row, out)
    for key in out.keys():
        print("Found {} records for {}".format(len(out[key]), key))
    with open("./flight_bot/agents/macs.json", "w") as f:
        json.dump(out, f)
