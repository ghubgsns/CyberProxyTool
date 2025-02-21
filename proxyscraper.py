import requests
from bs4 import BeautifulSoup
import socket
import time

def scrape_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxy_table = soup.find("table")
    proxies = []
    for row in proxy_table.find_all("tr")[1:10]:
        cols = row.find_all("td")
        if len(cols) > 1:
            ip = cols[0].text
            port = cols[1].text
            proxies.append(f"{ip}:{port}")
    return proxies

def guess_proxy_type(proxy):
    ip, port = proxy.split(":")
    port = int(port)
    if port in [80, 8080, 3128]:
        return "HTTP"
    elif port in [443, 8443]:
        return "HTTPS"
    elif port in [1080, 9050]:
        return "SOCKS"
    return "Unknown"

def test_proxy(proxy):
    proxy_type = guess_proxy_type(proxy)
    try:
        ip, port = proxy.split(":")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        start_time = time.time()
        sock.connect((ip, int(port)))
        latency = (time.time() - start_time) * 1000
        sock.close()
        return f"{proxy} - {proxy_type} - Alive (Latency: {latency:.2f}ms)"
    except:
        return f"{proxy} - {proxy_type} - Dead"

if __name__ == "__main__":
    print("Scraping free proxies...")
    proxy_list = scrape_proxies()
    print(f"Found {len(proxy_list)} proxies. Testing them now...\n")
    
    alive_proxies = []
    with open("proxies.txt", "w") as f:
        for proxy in proxy_list:
            result = test_proxy(proxy)
            print(result)
            f.write(f"{result}\n")
            if "Alive" in result:
                latency = float(result.split("Latency: ")[1].split("ms")[0])
                alive_proxies.append((proxy, latency))
    
    if alive_proxies:
        top_proxies = sorted(alive_proxies, key=lambda x: x[1])[:3]
        print("\nTop 3 Fastest Proxies:")
        for i, (proxy, latency) in enumerate(top_proxies, 1):
            print(f"{i}. {proxy} - {latency:.2f}ms")
    
    print("\nSaved to proxies.txt. Free proxies still suck—see README for more reliable proxies.")
