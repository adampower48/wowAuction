from main import read_json

auctions = read_json("auction.json")

print(len(set(a["item"] for a in auctions["auctions"])))
