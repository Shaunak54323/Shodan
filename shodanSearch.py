import shodan

# place your Shodan API key in apiKey.txt
with open('apiKey.txt', 'r') as f:
    apiKey = f.read()
api = shodan.Shodan(apiKey)

def queryShodan(query):
    hosts = {}
    try:
        results = api.search(query)
        for service in results['matches']:
            ip = service['ip_str']
            port = service['port']
            print('IP: {} Port: {}'.format(ip, port))
            if ip in hosts:
                hosts[ip]["ports"] += [port]
            else:
                hosts[ip] = {"ports": [port]}
        return hosts
    except Exception as e:
        print('Error: %s' % e)

def shodanLookup(ip):
    try:
        results = api.host(ip)
        record = []
        # print(results)
        for item in results['data']:
            r = {
                "port": item['port'],
                "banner": item['data']
            }
            if "product" in item:
                r["product"] = item["product"]
            if "version" in item:
                r["version"] = item["version"]
            if "cpe" in item:
                r["cpe"] = item["cpe"]
            record += [r]
        return record
    except Exception as e:
        print('Error: %s' % e)
        return []

results = queryShodan("org:Google LLC")
print(results)