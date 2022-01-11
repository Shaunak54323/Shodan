import dns
import dns.resolver
import socket

dictionary = {}
d = "subdomains.txt"
with open(d, "r") as f:
    dictionary = f.read().splitlines()

hosts = {}

def reverseDNS(ip):
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]] + result[1]
    except:
        return []

def DNSrequest(sub, domain):
    global hosts
    hostname = sub + domain
    try:
        result = dns.resolver.resolve(hostname)
        if result:
            for answer in result:
                ip = answer.to_text()
                hostnames = reverseDNS(ip)
                subs = [sub]
                for hostname in hostnames:
                    if hostname.endswith(domain):
                        s = hostname.rstrip(domain)
                        subs.append(s)
                if ip in hosts:
                    s = hosts[ip]["subs"]
                    hosts[ip] = list(dict.fromkeys(s + subs))
                else:
                    hosts[ip] = list(dict.fromkeys(subs))
    except:
        return

def subDomainSearch(domain, nums):
    success = []
    for word in dictionary:
        DNSrequest(word, domain)
        if nums:
            for i in range(10):
                DNSrequest(word + str(i), domain)

def DNSsearch(domain, nums):
    subDomainSearch(domain, nums)
    return hosts

domain = ".google.com"
hosts = DNSsearch(domain, True)
for ip in hosts:
    print(ip, hosts[ip])
    