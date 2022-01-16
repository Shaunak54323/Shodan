import requests

# Enter your API key in vuldbAPI.txt
with open("vuldbAPI.txt", "r") as f:
    apiKey = f.read()

def VuldbLookup(product, version=None):
    url = "https://vuldb.com/?api"
    if version:
        q = "product:%s, version:%s" % (product, version)
    else:
        q = "product:%s" % product
    query = {
        "apiKey": apiKey,
        "advancedSearch": q
    }
    results = requests.post(url, query)
    j = results.json()
    if "results" in j:
        sources = [results["source"] for results in j["results"] if "source" in results]
        return sources
    else:
        return []