import json
import time

import urllib3

urllib3.disable_warnings()
http = urllib3.PoolManager()

API_KEY = "u77x867vyhu2uzbeufvht52fzyey2b8g"
server = "illidan"

auction_req_url = "https://us.api.battle.net/wow/auction/data/{server}?locale=en_US&apikey={key}".format(server=server,
                                                                                                         key=API_KEY)
item_req_url = "https://us.api.battle.net/wow/item/{id}?locale=en_US&apikey={key}"

ITEM_DB_FILENAME = "item_info.json"
item_info = {}


def download_auctions(server):
    url = auction_req_url.format(server=server, key=API_KEY)
    filename = "auctions_{}.json".format(server)
    download(url, filename)

    return filename


def get_item_info(id):
    id = str(id)
    if id in item_info:
        return item_info[id]

    print("Fetching info...", id)

    url = item_req_url.format(id=id, key=API_KEY)
    req = http.request("GET", url)
    info = json.loads(req.data)

    item_info[id] = info
    return info


def write_item_db():
    with open(ITEM_DB_FILENAME, "w") as f:
        json.dump(item_info, f, indent=0)


def read_item_db():
    item_info.update(read_json(ITEM_DB_FILENAME))


def download(url, filename):
    # Downloads a file over http
    r = http.request("GET", url, preload_content=False)
    with open(filename, "wb") as f:
        while True:
            data = r.read(1024 ** 2)
            if not data:
                break

            f.write(data)

    r.release_conn()


def read_json(filename):
    with open(filename, "rb") as f:
        j = json.loads(f.read())
        print(len(j))
        return j


def update_item_info(auctions):
    ids = set(str(a["item"]) for a in auctions["auctions"])
    unknown_ids = ids - item_info.keys()

    i = 0
    for id in unknown_ids:
        get_item_info(id)

        i += 1
        if i >= 100:
            print("Saving item database...")
            write_item_db()
            i = 0

    print("Saving item database...")
    write_item_db()


if __name__ == '__main__':
    read_item_db()

    latest_mod_time = 0
    while True:

        req = http.request("GET", auction_req_url)
        req_data = json.loads(req.data)
        print(req_data)
        if not req_data:
            print("Error getting data...", req_data)
            time.sleep(5)
            continue

        last_mod = req_data["files"][0]["lastModified"]

        if last_mod > latest_mod_time:
            print("New file!", last_mod)
            auction_url = req_data["files"][0]["url"]

            # download(auction_url, "auction.json")
            auctions = read_json("auction.json")
            update_item_info(auctions)

            latest_mod_time = last_mod

        # Wait 3 sec
        time.sleep(3)
        print("...")
