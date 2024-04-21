import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient

def retrieve_html(url):
    try:
        with urllib.request.urlopen(url) as response:
            print ("Retrieved HTML from", url)
            html = response.read()
            return html
    except Exception as e:
        print("Error retrieving HTML:", e)
        return None

def parse(html, base_url):
    parsed_urls = set()
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url.startswith(base_url):
                parsed_urls.add(full_url)
    return parsed_urls


def store_page(url, html, collection):
    try:
        html_decoded = html.decode('utf-8')
    except UnicodeDecodeError:
        html_decoded = html.decode('utf-8', 'ignore')
        print("Warning: Some characters could not be decoded.")
    page_data = {
        "url": url,
        "html": html_decoded
    }
    collection.insert_one(page_data)

def target_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all('h1')
    for heading in headings:
        if heading.text.strip() == "Permanent Faculty":
            return True
    return False

def crawler_thread(frontier, collection, base_url):
    while not frontier.done():
        url = frontier.next_url()
        html = retrieve_html(url)
        if html:
            store_page(url, html, collection)
            if target_page(html):
                print("Target page found:", url)
                frontier.clear()
            else:
                for parsed_url in parse(html, base_url):
                    frontier.add_url(parsed_url)

class Frontier:
    def __init__(self):
        self.urls = []
        self.visited_urls = set()

    def add_url(self, url):
        if url not in self.visited_urls:
            self.urls.append(url)

    def next_url(self):
        url = self.urls.pop(0)
        self.visited_urls.add(url)
        return url

    def done(self):
        return len(self.urls) == 0

    def clear(self):
        self.urls.clear()
        self.visited_urls.clear()

def main():
    start_url = "https://www.cpp.edu/sci/computer-science/"
    frontier = Frontier()
    frontier.add_url(start_url)

    client = MongoClient()
    db = client['crawler_db']
    collection = db['pages']

    crawler_thread(frontier, collection, start_url)

if __name__ == "__main__":
    main()
