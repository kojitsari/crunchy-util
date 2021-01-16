import cloudscraper
import re
from bs4 import BeautifulSoup
from . import database

def extract_all_links(conn, anime_name):
    print(f'Updating crunchy-util.db with {anime_name}\'s current data.')
    episode_urls = []
    regex = r"(?:[^episode-]*-\s*){2}(.*)-[^-]*$"
    regex2 = r"episode-(\d+(?:\d+)*)"
    regex3 = r"(\d+)[^-]*$"

    scraper = cloudscraper.create_scraper()
    html = scraper.get("https://www.crunchyroll.com/" + anime_name).text
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    episode_urls = [links for links in links if (anime_name + '/episode') in links]
    database.create_table(conn, anime_name)
    for e in episode_urls:
            url = ('https://www.crunchyroll.com' + e)
            title = re.findall(regex, e)[0]
            title = title.replace('-', ' ')
            episode_num =  re.findall(regex2, e)[0]
            episode_num = episode_num.replace('-', '')
            unique_id = re.findall(regex3, e)[0]
            database.insert_data(conn, anime_name, episode_num, title, url, unique_id)
 
def extract_all_links_nsfw(conn, anime_name):
    print(f'Crunchyroll deemed {anime_name} NSFW, bypassing and updating crunchy-util.db with {anime_name}\'s current data.')
    episode_urls = []
    regex = r"(?:[^episode-]*-\s*){2}(.*)-[^-]*$"
    regex2 = r"episode-(\d+(?:\d+)*)"
    regex3 = r"(\d+)[^-]*$"
    
    scraper = cloudscraper.create_scraper()
    html = scraper.get("https://www.crunchyroll.com/" + anime_name + '?skip_wall=1').text
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    episode_urls = [links for links in links if (anime_name + '/episode') in links]
    database.create_table(conn, anime_name)
    for e in episode_urls:
            url = ('https://www.crunchyroll.com' + e)
            title = re.findall(regex, e)[0]
            title = title.replace('-', ' ')
            episode_num =  re.findall(regex2, e)[0]
            episode_num = episode_num.replace('-', '')
            unique_id = re.findall(regex3, e)[0]
            database.insert_data(conn, anime_name, episode_num, title, url, unique_id)