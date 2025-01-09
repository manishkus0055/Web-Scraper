# THIS FILE IS FOR FUNCTIONALY OF SCRAPING THE DESIRED DATA

from bs4 import BeautifulSoup
import scrapy

def parse(source_html):
    """Parses HTML source and returns a formatted string."""
    parsed_html = BeautifulSoup(source_html, 'html.parser')
    pretty_html = parsed_html.prettify()
    return pretty_html

def get_titles(source_html):
    """Extracts the title from the HTML source."""
    parsed_html = BeautifulSoup(source_html, 'html.parser')
    title = parsed_html.title.string if parsed_html.title else "No title found"
    return title

def get_headings(source_html):
    """Extracts heading (h1, h2, h3, etc.) from the HTML source."""
    parsed_html = BeautifulSoup(source_html, 'html.parser')
    
    heading = []
    for i in range(1, 50):
        heading.extend(h.text.strip() for h in parsed_html.findAll(f"h{i}"))
    return heading

def get_links(source_html):
    """Extracts all hyperlinks from HTML source."""
    parsed_html = BeautifulSoup(source_html, 'html.parser')
    links = [a['href'] for a in parsed_html.find_all('a', href=True)]
    return links

def get_text(source_html):
    """Extracts all the text from HTML source."""
    parsed_html = BeautifulSoup(source_html, 'html.parser')
    body = parsed_html.find("body", class_="td-home")
    text = [body.get_text(strip=True)]
    return text