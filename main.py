import json
import time

import urllib3

import sql_functions as sqlf

urllib3.disable_warnings()
http = urllib3.PoolManager()

API_KEY = "u77x867vyhu2uzbeufvht52fzyey2b8g"

regions = ("us", "eu")
servers = {
    # todo: Connected EU Realms
    "eu": {
        "Aegwynn": [], "Aman'Thul": [], "Antonidas": [], "Archimonde": [], "Ashenvale": [], "Azuregos": [],
        "Blackhand": [], "Blackmoore": [], "Blackrock": [], "Blackscar": [], "Borean Tundra": [], "C'Thun": [],
        "Chamber of Aspects": [], "Deathguard": [], "Die Aldor": [], "Draenor": [], "Dun Modr": [], "Eredar": [],
        "Eversong": [], "Fordragon": [], "Frostmane": [], "Frostwolf": [], "Galakrond": [], "Goldrinn": [],
        "Gordunni": [], "Howling Fjord": [], "Hyjal": [], "Kazzak": [], "Khaz Modan": [], "Kirin Tor": [],
        "Magtheridon": [], "Nemesis": [], "Outland": [], "Pozzo dell'Eternità": [], "Ragnaros": [],
        "Ravencrest": [], "Silvermoon": [], "Soulflayer": [], "Stormscale": [], "Sylvanas": [], "Thrall": [],
        "Twisting Nether": [], "Ysondre": []
    },
    "us": {
        "Aegwynn": ["Aegwynn", "Bonechewer", "Daggerspine", "Gurubashi", "Hakkar"], "Aerie Peak": [],
        "Agamaggan": ["Agamaggan", "Archimonde", "Jaedenar", "The Underbog"], "Aggramar": ["Aggramar", "Fizzcrank"],
        "Akama": ["Akama", "Dragonmaw", "Mug'thol"], "Alexstrasza": ["Alexstrasza", "Terokkar"],
        "Alleria": ["Alleria", "Khadgar"],
        "Altar of Storms": ["Altar of Storms", "Anetheron", "Magtheridon", "Ysondre"],
        "Alterac Mountains": ["Alterac Mountains", "Balnazzar", "Gorgonnash", "The Forgotten Coast", "Warsong"],
        "Aman'Thul": [], "Andorhal": ["Andorhal", "Scilla", "Ursin", "Zuluhed"],
        "Anetheron": ["Altar of Storms", "Anetheron", "Magtheridon", "Ysondre"], "Antonidas": ["Antonidas", "Uldum"],
        "Anub'arak": ["Anub'arak", "Chromaggus", "Chrushridge", "Garithos", "Nathrezim", "Smolderthorn"],
        "Anvilmar": ["Anvilmar", "Undermine"], "Arathor": ["Drenden", "Arathor"],
        "Archimonde": ["Agamaggan", "Archimonde", "Jaedenar", "The Underbog"], "Area 52": [],
        "Argent Dawn": ["The Scryers", "Argent Dawn"], "Arthas": [], "Arygos": ["Arygos", "Llane"],
        "Auchindoun": ["Auchindoun", "Cho'gall", "Laughing Skull"],
        "Azgalor": ["Azgalor", "Azshara", "Destromath", "Thunderlord"], "Azjol-Nerub": ["Azjol-Nerub", "Khaz Modan"],
        "Azralon": [], "Azshara": ["Azgalor", "Azshara", "Destromath", "Thunderlord"],
        "Azuremyst": ["Azuremyst", "Staghelm"],
        "Baelgun": ["Doomhammer", "Baelgun"],
        "Balnazzar": ["Alterac Mountains", "Balnazzar", "Gorgonnash", "The Forgotten Coast", "Warsong"],
        "Barthilas": [],
        "Black Dragonflight": ["Black Dragonflight", "Gul'dan", "Skullcrusher"],
        "Blackhand": ["Blackhand", "Galakrond"],
        "Blackrock": [], "Blackwater Raiders": ["Blackwater Raiders", "Shadow Council"],
        "Blackwing Lair": ["Blackwing Lair", "Dethecus", "Detheroc", "Lethon", "Haomarush"],
        "Blade's Edge": ["Blade's Edge", "Thunderhorn"], "Bladefist": ["Bladefist", "Kul Tiras"], "Bleeding Hollow": [],
        "Blood Furnace": ["Blood Furnace", "Mannoroth", "Nazjatar"], "Bloodhoof": ["Duskwood", "Bloodhoof"],
        "Bloodscalp": ["Bloodscalp", "Boulderfist", "Dunemaul", "Maiev", "Stonemaul"],
        "Bonechewer": ["Aegwynn", "Bonechewer", "Daggerspine", "Gurubashi", "Hakkar"],
        "Borean Tundra": ["Borean Tundra", "Shadowsong"],
        "Boulderfist": ["Bloodscalp", "Boulderfist", "Dunemaul", "Maiev", "Stonemaul"],
        "Bronzebeard": ["Bronzebeard", "Shandris"], "Burning Blade": ["Burning Blade", "Lightning's Blade", "Onyxia"],
        "Caelestrasz": ["Nagrand", "Caelestrasz"], "Cairne": ["Cairne", "Perenolde"], "Cenarius": [],
        "Cho'gall": ["Auchindoun", "Cho'gall", "Laughing Skull"],
        "Chromaggus": ["Anub'arak", "Chromaggus", "Chrushridge", "Garithos", "Nathrezim", "Smolderthorn"],
        "Chrushridge": ["Anub'arak", "Chromaggus", "Chrushridge", "Garithos", "Nathrezim", "Smolderthorn"],
        "Coilfang": ["Coilfang", "Dark Iron", "Dalvengyr", "Demon Soul"],
        "Daggerspine": ["Aegwynn", "Bonechewer", "Daggerspine", "Gurubashi", "Hakkar"], "Dalaran": [],
        "Dalvengyr": ["Coilfang", "Dark Iron", "Dalvengyr", "Demon Soul"],
        "Dark Iron": ["Coilfang", "Dark Iron", "Dalvengyr", "Demon Soul"], "Darkspear": [],
        "Darrowmere": ["Darrowmere", "Windrunner"], "Dath'Remar": ["Dath'Remar", "Khaz'goroth"],
        "Dawnbringer": ["Dawnbringer", "Madoran"],
        "Deathwing": ["Deathwing", "Executus", "Kalecgos", "Shattered Halls"],
        "Demon Soul": ["Coilfang", "Dark Iron", "Dalvengyr", "Demon Soul"], "Dentarg": ["Dentarg", "Whisperwind"],
        "Destromath": ["Azgalor", "Azshara", "Destromath", "Thunderlord"],
        "Dethecus": ["Blackwing Lair", "Dethecus", "Detheroc", "Lethon", "Haomarush"],
        "Detheroc": ["Shadowmoon", "Detheroc"],
        "Doomhammer": ["Doomhammer", "Baelgun"], "Draenor": ["Draenor", "Echo Isles"],
        "Dragonblight": ["Fenris", "Dragonblight"], "Dragonmaw": ["Akama", "Dragonmaw", "Mug'thol"],
        "Drak'Tharon": ["Drak'Tharon", "Firetree", "Malorne", "Rivendare", "Spirestone", "Stormscale"],
        "Drak'thul": ["Drak'thul", "Skywall"], "Draka": ["Draka", "Suramar"], "Drakkari": [],
        "Dreadmaul": ["Dreadmaul", "Thaurissan"], "Drenden": ["Drenden", "Arathor"],
        "Dunemaul": ["Bloodscalp", "Boulderfist", "Dunemaul", "Maiev", "Stonemaul"], "Durotan": ["Ysera", "Durotan"],
        "Duskwood": ["Duskwood", "Bloodhoof"], "Earthen Ring": [], "Echo Isles": ["Draenor", "Echo Isles"],
        "Eitrigg": ["Eitrigg", "Shu'halo"], "Eldre'Thalas": ["Eldre'Thalas", "Korialstrasz"],
        "Elune": ["Gilneas", "Elune"],
        "Emerald Dream": [], "Eonar": ["Eonar", "Velen"],
        "Eredar": ["Eredar", "Gorefiend", "Spinebreaker", "Wildhammer"],
        "Executus": ["Deathwing", "Executus", "Kalecgos", "Shattered Halls"], "Exodar": ["Exodar", "Medivh"],
        "Farstriders": ["Farstriders", "Silver Hand", "Thorium Brotherhood"],
        "Feathermoon": ["Scarlet Crusade", "Feathermoon"], "Fenris": ["Fenris", "Dragonblight"],
        "Firetree": ["Drak'Tharon", "Firetree", "Malorne", "Rivendare", "Spirestone", "Stormscale"],
        "Fizzcrank": ["Aggramar", "Fizzcrank"], "Frostmane": ["Frostmane", "Ner'zhul", "Tortheldrin"],
        "Frostmourne": [],
        "Frostwolf": ["Frostwolf", "Vashj"], "Galakrond": ["Blackhand", "Galakrond"], "Gallywix": [],
        "Garithos": ["Anub'arak", "Chromaggus", "Chrushridge", "Garithos", "Nathrezim", "Smolderthorn"], "Garona": [],
        "Garrosh": [], "Ghostlands": ["Ghostlands", "Kael'thas"], "Gilneas": ["Gilneas", "Elune"],
        "Gnomeregan": ["Gnomeregan", "Moonrunner"], "Goldrinn": [],
        "Gorefiend": ["Eredar", "Gorefiend", "Spinebreaker", "Wildhammer"],
        "Gorgonnash": ["Alterac Mountains", "Balnazzar", "Gorgonnash", "The Forgotten Coast", "Warsong"],
        "Greymane": ["Tanaris", "Greymane"], "Grizzly Hills": ["Grizzly Hills", "Lothar"],
        "Gul'dan": ["Black Dragonflight", "Gul'dan", "Skullcrusher"], "Gundrak": ["Gundrak", "Jubei'Thos"],
        "Gurubashi": ["Aegwynn", "Bonechewer", "Daggerspine", "Gurubashi", "Hakkar"],
        "Hakkar": ["Aegwynn", "Bonechewer", "Daggerspine", "Gurubashi", "Hakkar"],
        "Haomarush": ["Blackwing Lair", "Dethecus", "Detheroc", "Lethon", "Haomarush"],
        "Hellscream": ["Hellscream", "Zangarmarsh"], "Hydraxis": ["Hydraxis", "Terenas"], "Hyjal": [],
        "Icecrown": ["Icecrown", "Malygos"], "Illidan": [],
        "Jaedenar": ["Agamaggan", "Archimonde", "Jaedenar", "The Underbog"], "Jubei'Thos": ["Gundrak", "Jubei'Thos"],
        "Kael'thas": ["Ghostlands", "Kael'thas"], "Kalecgos": ["Deathwing", "Executus", "Kalecgos", "Shattered Halls"],
        "Kargath": ["Kargath", "Norgannon"], "Kel'Thuzad": [], "Khadgar": ["Alleria", "Khadgar"],
        "Khaz Modan": ["Azjol-Nerub", "Khaz Modan"], "Khaz'goroth": ["Dath'Remar", "Khaz'goroth"], "Kil'jaeden": [],
        "Kilrogg": ["Kilrogg", "Winterhoof"], "Kirin Tor": ["Kirin Tor", "Sentinels", "Steamwheedle Cartel"],
        "Korgath": [],
        "Korialstrasz": ["Eldre'Thalas", "Korialstrasz"], "Kul Tiras": ["Bladefist", "Kul Tiras"],
        "Laughing Skull": ["Auchindoun", "Cho'gall", "Laughing Skull"],
        "Lethon": ["Blackwing Lair", "Dethecus", "Detheroc", "Lethon", "Haomarush"], "Lightbringer": [],
        "Lightning's Blade": ["Burning Blade", "Lightning's Blade", "Onyxia"], "Llane": ["Arygos", "Llane"],
        "Lothar": ["Grizzly Hills", "Lothar"], "Madoran": ["Dawnbringer", "Madoran"],
        "Maelstrom": ["The Venture Co", "Maelstrom"],
        "Magtheridon": ["Altar of Storms", "Anetheron", "Magtheridon", "Ysondre"],
        "Maiev": ["Bloodscalp", "Boulderfist", "Dunemaul", "Maiev", "Stonemaul"], "Mal'Ganis": [],
        "Malfurion": ["Malfurion", "Trollbane"],
        "Malorne": ["Drak'Tharon", "Firetree", "Malorne", "Rivendare", "Spirestone", "Stormscale"],
        "Malygos": ["Icecrown", "Malygos"], "Mannoroth": ["Blood Furnace", "Mannoroth", "Nazjatar"],
        "Medivh": ["Exodar", "Medivh"], "Misha": ["Misha", "Rexxar"], "Mok'Nathal": ["Mok'Nathal", "Silvermoon"],
        "Moon Guard": [], "Moonrunner": ["Gnomeregan", "Moonrunner"], "Mug'thol": ["Akama", "Dragonmaw", "Mug'thol"],
        "Muradin": ["Nordrassil", "Muradin"], "Nagrand": ["Nagrand", "Caelestrasz"],
        "Nathrezim": ["Anub'arak", "Chromaggus", "Chrushridge", "Garithos", "Nathrezim", "Smolderthorn"],
        "Nazgrel": ["Nazgrel", "Nesingwary/Vek'nilash"], "Nazjatar": ["Blood Furnace", "Mannoroth", "Nazjatar"],
        "Nemesis": [],
        "Ner'zhul": ["Frostmane", "Ner'zhul", "Tortheldrin"],
        "Nesingwary/Vek'nilash": ["Nazgrel", "Nesingwary/Vek'nilash"],
        "Nordrassil": ["Nordrassil", "Muradin"], "Norgannon": ["Kargath", "Norgannon"],
        "Onyxia": ["Burning Blade", "Lightning's Blade", "Onyxia"], "Perenolde": ["Cairne", "Perenolde"],
        "Proudmoore": [],
        "Quel'Thalas": [], "Quel'dorei": ["Quel'dorei", "Sen'jin"], "Ragnaros": [],
        "Ravencrest": ["Uldaman", "Ravencrest"],
        "Ravenholdt": ["Ravenholdt", "Twisting Nether"], "Rexxar": ["Misha", "Rexxar"],
        "Rivendare": ["Drak'Tharon", "Firetree", "Malorne", "Rivendare", "Spirestone", "Stormscale"],
        "Runetotem": ["Runetotem", "Uther"], "Sargeras": [], "Saurfang": [],
        "Scarlet Crusade": ["Scarlet Crusade", "Feathermoon"], "Scilla": ["Andorhal", "Scilla", "Ursin", "Zuluhed"],
        "Sen'jin": ["Quel'dorei", "Sen'jin"], "Sentinels": ["Kirin Tor", "Sentinels", "Steamwheedle Cartel"],
        "Shadow Council": ["Blackwater Raiders", "Shadow Council"], "Shadowmoon": ["Shadowmoon", "Detheroc"],
        "Shadowsong": ["Borean Tundra", "Shadowsong"], "Shandris": ["Bronzebeard", "Shandris"],
        "Shattered Halls": ["Deathwing", "Executus", "Kalecgos", "Shattered Halls"],
        "Shu'halo": ["Eitrigg", "Shu'halo"],
        "Silver Hand": ["Farstriders", "Silver Hand", "Thorium Brotherhood"],
        "Silvermoon": ["Mok'Nathal", "Silvermoon"],
        "Skullcrusher": ["Black Dragonflight", "Gul'dan", "Skullcrusher"], "Skywall": ["Drak'thul", "Skywall"],
        "Smolderthorn": ["Anub'arak", "Chromaggus", "Chrushridge", "Garithos", "Nathrezim", "Smolderthorn"],
        "Spinebreaker": ["Eredar", "Gorefiend", "Spinebreaker", "Wildhammer"],
        "Spirestone": ["Drak'Tharon", "Firetree", "Malorne", "Rivendare", "Spirestone", "Stormscale"],
        "Staghelm": ["Azuremyst", "Staghelm"], "Steamwheedle Cartel": ["Kirin Tor", "Sentinels", "Steamwheedle Cartel"],
        "Stonemaul": ["Bloodscalp", "Boulderfist", "Dunemaul", "Maiev", "Stonemaul"], "Stormrage": [],
        "Stormreaver": [],
        "Stormscale": ["Drak'Tharon", "Firetree", "Malorne", "Rivendare", "Spirestone", "Stormscale"],
        "Suramar": ["Draka", "Suramar"], "Tanaris": ["Tanaris", "Greymane"], "Terenas": ["Hydraxis", "Terenas"],
        "Terokkar": ["Alexstrasza", "Terokkar"], "Thaurissan": ["Dreadmaul", "Thaurissan"],
        "The Forgotten Coast": ["Alterac Mountains", "Balnazzar", "Gorgonnash", "The Forgotten Coast", "Warsong"],
        "The Scryers": ["The Scryers", "Argent Dawn"],
        "The Underbog": ["Agamaggan", "Archimonde", "Jaedenar", "The Underbog"],
        "The Venture Co": ["The Venture Co", "Maelstrom"],
        "Thorium Brotherhood": ["Farstriders", "Silver Hand", "Thorium Brotherhood"], "Thrall": [],
        "Thunderhorn": ["Blade's Edge", "Thunderhorn"],
        "Thunderlord": ["Azgalor", "Azshara", "Destromath", "Thunderlord"],
        "Tichondrius": [], "Tol Barad": [], "Tortheldrin": ["Frostmane", "Ner'zhul", "Tortheldrin"],
        "Trollbane": ["Malfurion", "Trollbane"], "Turalyon": [], "Twisting Nether": ["Ravenholdt", "Twisting Nether"],
        "Uldaman": ["Uldaman", "Ravencrest"], "Uldum": ["Antonidas", "Uldum"], "Undermine": ["Anvilmar", "Undermine"],
        "Ursin": ["Andorhal", "Scilla", "Ursin", "Zuluhed"], "Uther": ["Runetotem", "Uther"],
        "Vashj": ["Frostwolf", "Vashj"],
        "Velen": ["Eonar", "Velen"],
        "Warsong": ["Alterac Mountains", "Balnazzar", "Gorgonnash", "The Forgotten Coast", "Warsong"],
        "Whisperwind": ["Dentarg", "Whisperwind"], "Wildhammer": ["Eredar", "Gorefiend", "Spinebreaker", "Wildhammer"],
        "Windrunner": ["Darrowmere", "Windrunner"], "Winterhoof": ["Kilrogg", "Winterhoof"], "Wyrmrest Accord": [],
        "Ysera": ["Ysera", "Durotan"], "Ysondre": ["Altar of Storms", "Anetheron", "Magtheridon", "Ysondre"],
        "Zangarmarsh": ["Hellscream", "Zangarmarsh"], "Zul'jin": [],
        "Zuluhed": ["Andorhal", "Scilla", "Ursin", "Zuluhed"]
    }
}

auction_req_url = "https://{{region}}.api.battle.net/wow/auction/data/{{server}}?locale=en_US&apikey={key}".format(
    key=API_KEY)
item_req_url = "https://us.api.battle.net/wow/item/{{id}}?locale=en_US&apikey={key}".format(key=API_KEY)
auction_file_name = "auctions_temp/auctions_{region}_{server}.json"

item_info = {}


def urlify(s):
    return s.replace(" ", "%20")


def download_auctions(region, server):
    # Downloads auction list to returned filename.
    req_data = check_auction(region, server)
    url = req_data["files"][0]["url"]

    filename = auction_file_name.format(region=region, server=urlify(server))
    download(url, filename)

    return filename


def get_item_info(id):
    # Returns info for given item id. Retrieves info from API if it isn't saved.
    if id in item_info:
        return item_info[id]

    print("Fetching info...", id)

    url = item_req_url.format(id=id)

    for _ in range(1):  # Give up after n tries
        info = json.loads(http.request("GET", url).data)

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


def check_auction(region, server):
    # Checks for a new auction list file

    req = http.request("GET", auction_req_url.format(region=region, server=urlify(server)))
    req_data = json.loads(req.data)

    if not req_data:
        print("Error getting data...", req_data)
        return check_auction(region, server)

    return req_data


def main():
    sqlf.open_db()

    read_item_db()

    region = regions[1]
    servers_loc = list(servers[region].keys())

    i = 0
    while True:
        server = servers_loc[i]

        # Fetch latest updated time
        time_query = sqlf.sql_query(sqlf.Tables.LATEST_UPDATE, region=region, server=server)
        latest_mod_time = time_query[0]["updated"] if time_query else 0

        req_data = check_auction(region, server)

        try:
            last_mod = req_data["files"][0]["lastModified"]
        except KeyError:
            print(req_data)
            continue

        if last_mod > latest_mod_time:
            print("New file!", region, server, last_mod)

            download_auctions(region, server)
            auctions = read_json(auction_file_name.format(region=region, server=server))
            update_item_info(auctions)
            sqlf.update_auctions(auctions["auctions"], region, server, last_mod)

            print("Done")
            del auctions

        i = (i + 1) % len(servers_loc)

        # Wait 3 sec
        time.sleep(3)
        print("...")


if __name__ == '__main__':
    main()
