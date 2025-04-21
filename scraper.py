# THIS FILE IS FOR FUNCTIONALY OF TEST SCRAPING THE DESIRED DATA

from bs4 import BeautifulSoup
# import scrapy

class NormalSites:
    def parse(self, source_html):
        """Parses HTML source and returns a formatted string."""
        parsed_html = BeautifulSoup(source_html, 'html.parser')
        pretty_html = parsed_html.prettify()
        return pretty_html

    def get_titles(self, source_html):
        """Extracts the title from the HTML source."""
        parsed_html = BeautifulSoup(source_html, 'html.parser')
        title = parsed_html.title.string if parsed_html.title else "No title found"
        return title

    def get_headings(self, source_html):
        """Extracts heading (h1, h2, h3, etc.) from the HTML source."""
        parsed_html = BeautifulSoup(source_html, 'html.parser')

        heading = []
        for i in range(1, 50):
            heading.extend(h.text.strip() for h in parsed_html.findAll(f"h{i}"))
        return heading

    def get_links(self, source_html):
        """Extracts all hyperlinks from HTML source."""
        parsed_html = BeautifulSoup(source_html, 'html.parser')
        links = [a['href'] for a in parsed_html.find_all('a', href=True)]
        return links

    def get_text(self, source_html):
        """Extracts all the text from HTML source."""
        parsed_html = BeautifulSoup(source_html, 'html.parser')
        body = parsed_html.find("body", class_="td-home")
        text = [body.get_text(strip=True)]
        return text
    

# Modified Instagram data extraction functions
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import time
import random
import os
import instaloader

class InstagramData:
    def __init__(self, driver=None, htmlcode=None):
        self.driver = driver
        self.soup = BeautifulSoup(htmlcode or driver.page_source, 'html.parser')
    
    def id_info(self):
        html_paths = {
            'id_class': 'x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft',
            'profile_name_class': 'x1lliihq x1plvlek xryxfnj x1n2onr6 x1ji0vk5 x18bv5gf x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj',
            'profile_pic_class': 'xpdipgo x972fbf xcfux6l x1qhh985 xm0m39n xk390pu x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r xl1xv1r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3',
            'bio_class': '_ap3a _aaco _aacu _aacx _aad7 _aade',
            'stats_class': 'xl565be x1m39q7l x1uw6ca5 x2pgyrj',
            'profile_category_class': '_ap3a _aaco _aacu _aacy _aad6 _aade'
        }

        profile_pic = self.soup.find('img', class_=html_paths['profile_pic_class'])
        profile_pic = profile_pic.get('src') if profile_pic else 'N/A'

        id = self.soup.find('span', class_=html_paths['id_class'])
        id = id.text.strip() if id else 'N/A'

        profile_name = self.soup.find('span', class_=html_paths['profile_name_class'])
        profile_name = profile_name.get_text(strip=True) if profile_name else 'N/A'

        bio = self.soup.find_all('span', class_=html_paths['bio_class'])
        bio = ' '.join([span.get_text(strip=True) for span in bio]) if bio else "N/A"

        profile_category = self.soup.find('div', class_=html_paths['profile_category_class'])
        profile_category = profile_category.text.strip() if profile_category else 'N/A'

        external_link = self.soup.find('a', href=re.compile(r'linktr\.ee'))
        external_link = external_link.get('href') if external_link else 'N/A'

        stats = self.soup.find_all('li', class_=html_paths['stats_class'])
        posts = stats[0].find('span', class_='html-span').text.strip() if len(stats) > 0 else "N/A"
        followers = stats[1].find('span', class_='html-span').text.strip() if len(stats) > 1 else "N/A"
        following = stats[2].find('span', class_='html-span').text.strip() if len(stats) > 2 else "N/A"

        info = {
            'Profile Pic': profile_pic,
            'User Name': id,
            'Profile Name': profile_name,
            'Bio': bio,
            'Profile Category': profile_category,
            'External Link': external_link,
            'Stats': {
                'Posts': posts,
                'Followers': followers,
                'Following': following
            }
        }

        return info

    def get_post_reel_data(self, num_scrolls=1):
        pd.set_option('display.max_colwidth', None)

        post_class = 'x1lliihq x1n2onr6 xh8yej3 x4gyw5p x11i5rnm x1ntc13c x9i3mqj x2pgyrj'
        seen_urls = set()
        posts_data = []

        for _ in range(num_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(4, 6))

            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            post_elements = self.soup.find_all('div', class_= post_class)

            for post in post_elements:
                link_tag = post.find('a', href=True)
                img_tag = post.find('img', src=True)

                media_url = None
                caption = 'No Caption'
                media_type = 'unknown'
                post_link = None

                if img_tag:
                    media_url = img_tag.get('src')
                    caption = img_tag.get('alt', 'No Caption')
                    media_type = 'image'

                if link_tag:
                    href = link_tag['href']
                    if '/reel/' in href:
                        post_link = f"https://www.instagram.com{href}"
                        media_type = 'reel'
                
                if link_tag:
                    href = link_tag['href']
                    if '/p/' in href:
                        post_link = f"https://www.instagram.com{href}"
                        media_type = 'slide_image'

                if media_url and media_url not in seen_urls:
                    seen_urls.add(media_url)
                    
                    posts_data.append({
                        'Index': len(posts_data) + 1,
                        'Media Type': media_type,
                        'Media URL': media_url,
                        'Caption': caption,
                        'Post Link': post_link or 'N/A'
                    })

        return pd.DataFrame(posts_data)
                
    def download_media(self, link):
        try:
            # Extract shortcode from link
            shortcode_match = re.search(r'/([A-Za-z0-9_-]{10,})/', link)
            if not shortcode_match:
                print(f"Invalid Instagram link format: {link}")
                return

            shortcode = shortcode_match.group(1)

            # Ensure the downloads folder exists
            os.makedirs("downloads", exist_ok=True)

            # Create and configure instaloader instance
            loader = instaloader.Instaloader(
                download_comments=False,
                download_video_thumbnails=False,
                save_metadata=False,
                post_metadata_txt_pattern="",
                dirname_pattern="downloads"
            )

            # Load the post and download it
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            loader.download_post(post, target="")

            print(f"Downloaded: {link}")
        except Exception as e:
            print(f"Failed to download from {link}: {e}") 