import cloudscraper
import json
import re
import os
import getpass
import psutil
import time
import signal
from bs4 import BeautifulSoup
from subprocess import Popen
from sys import platform

def check_processRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def save_function(episode_data):
    file_name = anime_name + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(episode_data, outfile)

def extract_all_links(site):
    print(f'Updating {anime_name}.json with current data.')
    episode_data = []
    regex = r"(?:[^episode-]*-\s*){2}(.*)-[^-]*$"
    regex2 = r"episode-(\d+(?:-\d+)*)"

    scraper = cloudscraper.create_scraper()
    html = scraper.get("https://www.crunchyroll.com/" + site).text
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    episode_urls = [links for links in links if (anime_name + '/episode') in links]
    for e in episode_urls:
            url = ('https://www.crunchyroll.com' + e)
            title = re.findall(regex, e)[0]
            title = title.replace('-', ' ')
            episode_num =  re.findall(regex2, e)[0]
            episode_num = episode_num.replace('-', '')
            episode = {
                'episode_num': episode_num,
                'title': title,
                'url': url
            }
            episode_data.append(episode)
    return save_function(episode_data)

def extract_all_links_nsfw(site):
    print(f'Crunchyroll deemed {anime_name} NSFW, bypassing and updating {anime_name}.json with current data.')
    episode_data = []
    regex = r"(?:[^episode-]*-\s*){2}(.*)-[^-]*$"
    regex2 = r"episode-(\d+(?:-\d+)*)"
    

    scraper = cloudscraper.create_scraper()
    html = scraper.get("https://www.crunchyroll.com/" + site + '?skip_wall=1').text
    soup = BeautifulSoup(html, 'html.parser').find_all('a')
    links = [link.get('href') for link in soup]
    episode_urls = [links for links in links if (anime_name + '/episode') in links]
    for e in episode_urls:
            url = ('https://www.crunchyroll.com' + e)
            title = re.findall(regex, e)[0]
            title = title.replace('-', ' ')
            episode_num =  re.findall(regex2, e)[0]
            episode_num = episode_num.replace('-', '')
            episode = {
                'episode_num': episode_num,
                'title': title,
                'url': url
            }
            episode_data.append(episode)
    return save_function(episode_data)

def launch_streamlink(episode, quality, cr_user, cr_pass, playlist):
    anime_file = anime_name + '.json'
    with open(anime_file, 'r') as temp_file:
        data=temp_file.read()
    obj = json.loads(data)
    if quality not in ['best', '480p', '720p', '1080p', '240p', '360p']:
        quality = 'best'
    else:
        pass
    temp = int(episode)
    while playlist == 'yes':
        while True:
            if check_processRunning('mpv') or check_processRunning('vlc'):
                pass
            else:
                length = len(obj)
                if int(episode) > length:
                    print(f'Reached end of episodes according to {anime_name}.json, exiting.')
                    exit()
                else:
                    for elem in obj:
                        if str(episode) in elem['episode_num']:
                            play_url = elem['url']
                        else:
                            continue
                    usr = '--crunchyroll-username=' + cr_user
                    pwd = '--crunchyroll-password=' + cr_pass
                    cmd = ['streamlink', play_url, quality, usr, pwd]
                    Popen(cmd)
                    temp += 1
                    episode = temp
                    time.sleep(15)
    else:
        for elem in obj:
            if episode in elem['episode_num']:
                play_url = elem['url']
            else:
                continue
        usr = '--crunchyroll-username=' + cr_user
        pwd = '--crunchyroll-password=' + cr_pass
        cmd = ['streamlink', play_url, quality, usr, pwd]
        Popen(cmd)

if __name__ == "__main__":
    anime_name = input('Enter anime name: ')
    anime_name = anime_name.replace(' ', '-')
    play_url = ''
    if os.path.exists(f'{anime_name}.json'):
        refresh_data = input(f'Do you need to refresh data in {anime_name}.json? [Enter "yes" or "no"]: ')
        refresh_data = refresh_data.lower()
        if refresh_data is not ['yes', 'no']:
            refresh_data = 'no'
        else:
            pass
    else:
        refresh_data = 'yes'

    watching = input('Do you plan to watch a show? [Enter "yes" or "no"]: ')
    watching = watching.lower()

    if refresh_data == 'yes':
        extract_all_links(anime_name)
        if os.path.getsize(f'{anime_name}.json') <= 2:
            extract_all_links_nsfw(anime_name)
        else:
            pass
    else:
        pass

    if watching == 'yes':
        episode = input('Enter the episode number you wish to watch: ')
        quality = input('Enter the quality you would like to watch [480p/720p/1080p/best]: ')
        cr_user = input('Enter your crunchy roll username: ')
        cr_pass = getpass.getpass("Enter your password: ")
        playlist = input('Would you like to continuously play episodes? [Enter "yes" or "no"]: ')
        launch_streamlink(episode, quality, cr_user, cr_pass, playlist)
    else:
        exit()