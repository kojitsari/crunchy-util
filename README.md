# crunchy-util
*Crunchy-util* is a script that automates fetching of episode urls per anime, stores them into a json file, and plays them via Streamlink. 

## Legal Warning

This application is not endorsed or affliated with *CrunchyRoll*. The usage of this application enables streaming of episodes via a thrid party service, which may be forbidden by law in your country and/or a violation of CrunchyRoll terms of service. A tool is not responsible for your actions; please make an informed decision prior to using this application. 

## Prerequisites

* Python 3.6+ (Tested with Python 3.8)
* [Streamlink](https://streamlink.github.io/)
* [MPV](https://mpv.io/) or [VLC](https://www.videolan.org/)

Python libaries - pip install

* cloudscraper
* psutil
* beautifulsoup4

### Command-line Interface

The script prompts for the information:

* Anime name - Enter the name, casing does not matter and if the show has multiple words separate them with a space 
* Data refresh - only prompts if you already have a corresponding "anime-name.json" (you will need to do this if there have been new episodes released). If you do **not** want to refresh you can bypass by pressing Enter
* Watch a show - do you want to actually stream an episode via streamlink, versus just updating a file for later usage. If you do **not** want to watch an episode you can bypass by pressing Enter
* Episode number - You have to provide the episode number you wish to watch as an integer (ie 1)
* Quality - Any quality option Streamlink will take works here (ie 480p/720p/1080p). If you bypass by pressing Enter and it will default to the "best" quality option
* Crunchyroll username - Required for some shows and higher quality streaming
* Crunchyroll password - Required for some shows and higher quality streaming
* Continuous playback - The script will loop through all episodes from your selected episode onwawrd until there are no more episodes in the json file. Bypassing with Enter defaults to 'no.'

# This was for developed for educational purposes only
