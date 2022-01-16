from scapy.modules.six import *
from shodanSearch import shodanLookup
from portScan import *
import re
import requests
import socket

defaults = {
    "smpt": [25],
    "dns": [53],
    "ns": [53],
    "web": [80, 443],
    "www": [80, 443],
    "api": [80, 443],
    "ftp": [20, 21]
}


def serviceID(ip, subs):
    records = []
    for sub in subs:
        s = sub.strip("0123456789")
        if s in defaults:
            records = [bannerRecord(ip, p) for p in defaults[s]]

        if len(records) == 0:
            records = shodanLookup(ip)
            for r in records:
                if not "product" in r:
                    [r["product"], r["version"]] = parseBanner(
                        r["banner"], r["port"])

        if len(records) == 0:
            records = [bannerGrab(ip, p) for p in synScan[s]]

        return records


def bannerRecord(ip, p):
    product = ""
    version = ""
    if p in [80, 443, 8080, 8443]:
        response = HTTPHeaderGrab(ip.p)
        server = response.headers["Server"]
        [product, version] = parseBanner(server, p)
    else:
        banner = bannerGrab(ip, p)
        if banner:
            [product, version] = parseBanner(banner, p)
    r = {
        "port": p,
        "product": product,
        "version": version
    }
    return r


def parseBanner(banner, port):
    product = ""
    version = ""
    if port in [80, 443, 8080, 8443]:
        if banner.startswith("HTTP"):
            match = re.search("Server: ([^\r\n]*}", banner)
            if match:
                server = match.groups()[0]
            else:
                server = ""
        else:
            server = banner
        vals = server.split(" ")[0].split("/")
        product = vals[0]
        version = vals[1] if len(vals) > 1 else ""
    else:
        x = re.search("([A-Za-z0-9]+)[/ _](([0-9]+([.][0-9]+)+))", banner)
        if x:
            product = x.groups()[0]
            version = x.groups()[1]
        else:
            x = re.findall("([a-z0-9]*((smpt)|(ftp))[a-z0-9]*)", banner.lower())
            if x:
                for y in x:
                    if y[0] == "esmtp":
                        product = y[0]
                        break
    return [product, version]


records = serviceID("3.20.135.129", "")
for r in records:
    print(r)
