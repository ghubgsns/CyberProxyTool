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
    for row in proxy_table.find_all("tr")[1:10]:  # Still limiting to 10
        cols = row.find_all("td")
        if len(cols) > 1:
            ip = cols[0].text
            port = cols[1].text
            proxies.append(f"{ip}:{port}")
    return proxies

def test_proxy(proxy):
    try:
        ip, port = proxy.split(":")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5-second timeout
        start_time = time.time()
        sock.connect((ip, int(port)))
        latency = (time.time() - start_time) * 1000  # milliseconds
        sock.close()
        return f"{proxy} - Alive (Latency: {latency:.2f}ms)"
    except:
        return f"{proxy} - Dead"

if __name__ == "__main__":
    print("Scraping free proxies...")
    proxy_list = scrape_proxies()
    print(f"Found {len(proxy_list)} proxies. Testing them now...\n")
    for proxy in proxy_list:
        result = test_proxy(proxy)
        print(result)
    print("\nNote: Free proxies are still trash. Check README for premium options.")
