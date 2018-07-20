import json
import time

import urllib3

import sql_functions as sqlf

urllib3.disable_warnings()
http = urllib3.PoolManager()

API_KEY = "u77x867vyhu2uzbeufvht52fzyey2b8g"
servers = (
    "Illidan",
    "Dalaran",
)

auction_req_url = "https://us.api.battle.net/wow/auction/data/{{server}}?locale=en_US&apikey={key}".format(key=API_KEY)
item_req_url = "https://us.api.battle.net/wow/item/{{id}}?locale=en_US&apikey={key}".format(key=API_KEY)
auction_file_name = "auctions_{server}.json"

item_info = {}


def download_auctions(server):
    # Downloads auction list to returned filename.
    req_data = check_auction(server)
    url = req_data["files"][0]["url"]

    filename = auction_file_name.format(server=server)
    download(url, filename)

    return filename


def get_item_info(id):
    # Returns info for given item id. Retrieves info from API if it isn't saved.
    if id in item_info:
        return item_info[id]

    print("Fetching info...", id)

    url = item_req_url.format(id=id)

    def get_info():
        return json.loads(http.request("GET", url).data)

    for _ in range(5):  # Give up after 5 tries
        info = get_info()

        if "code" in info:
            # Failed request
            print("Failed to retrieve info: ", info)
            continue

        if "status" in info:
            print("Failed to retrieve info: ", info)
            if info["status"] == "nok":
                return None
            else:
                continue

        # Successful if it gets to here
        item_info[id] = info
        return info

    else:
        return None


def write_item_db(items=item_info):
    # Writes item info to the database
    sqlf.update_item_info(items)


def read_item_db():
    # Reads item info from database

    items = sqlf.sql_query("item_info")
    items = {x["id"]: x for x in items}
    item_info.update(items)


def download(url, filename):
    # Downloads a file to given filename
    r = http.request("GET", url, preload_content=False)
    with open(filename, "wb") as f:
        print("Downloading...")
        size = 0
        while True:
            # 1MB at a time
            data = r.read(1024 ** 2)

            size += 1
            print("... {}MB".format(size))

            if not data:
                break

            f.write(data)

    r.release_conn()


def read_json(filename):
    with open(filename, "rb") as f:
        return json.loads(f.read())


def update_item_info(auctions):
    # Retrieves item info for unknown items
    ids = set(a["item"] for a in auctions["auctions"])
    unknown_ids = ids - item_info.keys()

    new_items = {}
    i = 0
    for id in unknown_ids:
        info = get_item_info(id)
        if not info:
            continue

        new_items[id] = info

        i += 1
        if i >= 100:
            print("Saving item database...")
            write_item_db(new_items)
            new_items = {}
            i = 0

    print("Saving item database...")
    write_item_db(new_items)


def check_auction(server):
    # Checks for a new auction list file
    req = http.request("GET", auction_req_url.format(server=server))
    req_data = json.loads(req.data)

    if not req_data:
        print("Error getting data...", req_data)
        return check_auction(server)

    return req_data


if __name__ == '__main__':
    sqlf.open_db()

    read_item_db()

    i = 0
    while True:
        server = servers[i]

        time_query = sqlf.sql_query(sqlf.Tables.LATEST_UPDATE, server=server)
        latest_mod_time = time_query[0]["updated"] if time_query else 0

        req_data = check_auction(server)

        last_mod = req_data["files"][0]["lastModified"]

        if last_mod > latest_mod_time:
            print("New file!", server, last_mod)
            auction_url = req_data["files"][0]["url"]

            download_auctions(server)
            auctions = read_json(auction_file_name.format(server=server))
            update_item_info(auctions)
            sqlf.update_auctions(auctions["auctions"], last_mod)

            print("Done")
            del auctions

            latest_mod_time = last_mod

        i = (i + 1) % len(servers)

        # Wait 3 sec
        time.sleep(3)
        print("...")
