# THIS FILE IS FOR A WEBSITE AND GUI USING STREAMLIT
# streamlit requests beautifulsoup4 Scrapy selenium cloudscraper 2captcha-python mechanize fake-useragent torpy

import streamlit as st
from web_automation import web_automation_normal
from scraper import parse, get_titles, get_links, get_headings, get_text


st.set_page_config("Web Scraper")
st.title("Web Scaper")

url = st.text_input("Enter the URL to scrape:")

if st.button("Scrape"):
    if url:
        result = web_automation_normal(url)

        # This code is from utils and it handel all the functions for desired scraping data.

        parsed = parse(result)
        title = get_titles(parsed)
        headings = get_headings(parsed)
        links = get_links(parsed)
        texts = get_text(parsed)

        #st.code(parsed, language="html", line_numbers=True, wrap_lines=True)
        st.title(title)

        st.subheader("Headings Found:")
        st.text(headings)

        st.subheader("Link Found:")
        st.markdown(f"{links}")

        st.subheader("Text Found:")
        st.text(texts)
        
    else:
        st.error("Please enter a valid URL.")