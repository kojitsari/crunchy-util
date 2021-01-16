import psutil
import time
from subprocess import Popen
from sys import platform
from . import database

def check_processRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def launch_streamlink(conn, anime_name, episode, quality, cr_user, cr_pass, playlist):
    data = database.query_data(conn, anime_name)
    print(data)
    ep = int(episode) - 1
    print(data[ep][2])
    print(data[ep][3])
    if quality not in ['best', '480p', '720p', '1080p', '240p', '360p']:
        quality = 'best'
    else:
        pass
    temp = int(episode)
    while playlist == 'yes':
        while True:
            if check_processRunning('mpv') or check_processRunning('vlc'):
                print(check_processRunning('vlc') + 'vlc running')
                print(check_processRunning('mpv') + 'vlc running')
                pass
            else:
                length = len(data)
                if int(episode) > length:
                    print(f'Reached end of episodes according to data found in crunchy-util.db, exiting.')
                    exit()
                else:
                    play_url = data[ep][2]
                    print(play_url)
                    usr = '--crunchyroll-username=' + cr_user
                    pwd = '--crunchyroll-password=' + cr_pass
                    cmd = ['streamlink', play_url, quality, usr, pwd]
                    Popen(cmd)
                    temp += 1
                    episode = temp
                    time.sleep(15)
    else:
        for elem in data:
            if episode == elem[0]:
                play_url = elem[2]
            else:
                continue
        usr = '--crunchyroll-username=' + cr_user
        pwd = '--crunchyroll-password=' + cr_pass
        cmd = ['streamlink', play_url, quality, usr, pwd]
        Popen(cmd)