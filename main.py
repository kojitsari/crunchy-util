import json
import os
import getpass
import signal
import sqlite3
from modules.database import *
from modules.crunchy_scraper import *
from modules.streaming import *
from subprocess import Popen
from sys import platform

if __name__ == "__main__":
    database_name = r"crunchy-util.db"
    anime_name = input('Enter anime name: ')
    anime_name = anime_name.replace(' ', '-').lower()
    watching = input('Do you plan to watch a show? [Enter "yes" or "no"]: ').lower()
    watching = watching.lower()
    conn = create_connection(database_name)

    if conn is not None:
        extract_all_links(conn, anime_name)
        data = query_data(conn, anime_name)
        if not data:
            extract_all_links_nsfw(conn, anime_name)
        else:
            pass
    else:
        print("Error! cannot create the database connection.")

    while True:
            try:
                watching in ['yes', 'no']
                break
            except ValueError:
                print("Expected either 'yes' or 'no,' please re-run and enter a valid option.")
                exit()
    
    if watching == 'yes':
        episode = input('Enter the episode number you wish to watch: ')
        quality = input('''Enter the quality you would like to watch: worst/240p/480p/720p/1080p/best \nCan be skipped by pressing 'Enter' and defaults to 'best'
                        ''')
        cr_user = input('''Enter your crunchy roll username: \nNot required, but some shows will not play and those that will are limited to 480p.
                        ''')
        cr_pass = getpass.getpass('''Enter your crunchy roll password: \nNot required (unless you input a username), but some shows will not play and those that will are limited to 480p.
                                  ''')
        playlist = input('Would you like to continuously play episodes? [Enter "yes" or "no"]: ').lower()

        while True:
            try:
                val = int(episode)
                break
            except ValueError:
                print("Episode is required, please re-run and enter a valid number (greater than 0).")
                exit()
            try:
                playlist in ['yes', 'no']
                break
            except ValueError:
                print("Expected either 'yes' or 'no,' please re-run and enter a valid option.")
                exit()

        launch_streamlink(conn, anime_name, episode, quality, cr_user, cr_pass, playlist)
    else:
        exit()
