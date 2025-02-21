import requests
from bs4 import BeautifulSoup

def scrape_proxies():
    url = "https://free-proxy-list.net/"  # Public proxy site
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    proxy_table = soup.find("table")
    proxies = []
    for row in proxy_table.find_all("tr")[1:10]:  # Limit to 10 for simplicity
        cols = row.find_all("td")
        if len(cols) > 1:
            ip = cols[0].text
            port = cols[1].text
            proxies.append(f"{ip}:{port}")
    return proxies

if __name__ == "__main__":
    print("Scraping free proxies...")
    proxy_list = scrape_proxies()
    for proxy in proxy_list:
        print(proxy)
    print("\nNote: Free proxies sometimes work but they kinda suck. Use low cost premium ones for real shit—see README.")
