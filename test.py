# server_list = {
#     "Aegwynn": [], "Aman'Thul": [], "Antonidas": [], "Archimonde": [], "Ashenvale": [], "Azuregos": [],
#     "Blackhand": [], "Blackmoore": [], "Blackrock": [], "Blackscar": [], "Borean Tundra": [], "C'Thun": [],
#     "Chamber of Aspects": [], "Deathguard": [], "Die Aldor": [], "Draenor": [], "Dun Modr": [], "Eredar": [],
#     "Eversong": [], "Fordragon": [], "Frostmane": [], "Frostwolf": [], "Galakrond": [], "Goldrinn": [],
#     "Gordunni": [], "Howling Fjord": [], "Hyjal": [], "Kazzak": [], "Khaz Modan": [], "Kirin Tor": [],
#     "Magtheridon": [], "Nemesis": [], "Outland": [], "Pozzo dell'Eternità": [], "Ragnaros": [],
#     "Ravencrest": [], "Silvermoon": [], "Soulflayer": [], "Stormscale": [], "Sylvanas": [], "Thrall": [],
#     "Twisting Nether": [], "Ysondre": []
# }
#
# for line in sys.stdin:
#     servers = line.strip().split("\t")[0]
#     if "[CR]" in servers:
#         continue
#
#     print(servers)
#     if servers in server_list:
#         print(servers, "FUCK")
#     server_list[servers] = []
#
# with open("eu_connected.json", "w") as f:
#     json.dump(server_list, f, sort_keys=True)
