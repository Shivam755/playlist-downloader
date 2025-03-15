from youtubesearchpython import VideosSearch
from os import system,path,makedirs,listdir,rename
from json import loads
from pathlib import Path
import sys
import string
import re


def MoveFile(sourcePath, destPath, pattern=".*"):
    # create a folder if not exists
    if not path.exists(destPath):
        makedirs(destPath)
        print(f"Path created!! path: {destPath}")

    for file in listdir(sourcePath):
        try:
            if re.search(pattern, file):
                rename(f"{sourcePath}\\{file}",f"{destPath}\\{file}")
        except FileExistsError:
            print(f"{sourcePath}\\{file}",f"{destPath}\\{file} already exists!!")

def formate_foldername(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def search_youtube(track_name:str) -> list:
    configFile = open("./config.json")
    configJson = None
    if configFile:
        configJson = loads(configFile.read())
    else:
        sys.exit("config file doesn't exist aborting!!")
    maxResults = int(configJson["maxYTResult"])
    search = VideosSearch(track_name, maxResults)
    results = search.result()
    if results['result']:
        return results['result']

def download_song(youtube_uri:str, downloadPath:str = None)->None:
    extra = ''
    if downloadPath:
        extra = f"-o {downloadPath}"
    try:
        system(f'yt-dlp -x --audio-format mp3 --audio-quality 320k {extra} "{youtube_uri}"')
    except FileExistsError:
        print(f"File already exists for song: {youtube_uri}")

def read_playlists(filepath:str)->list:
    f = open(filepath,encoding='utf-8')
    file_content = f.read()
    playlist_dict = loads(file_content)
    return playlist_dict['playlists']

def iterate_tracks_from_playlist(playlists:list, playlist_name:str)->None:
    selected_playlist:list = list(filter(lambda plist : plist['name'] == playlist_name, playlists))
    tracks = selected_playlist[0]['items']
    for track in tracks:
        search_string = track['track']['trackName'] + ' ' + track['track']['artistName']
        yt_uris = search_youtube(search_string)
        for uri in yt_uris:
            download_song(uri['link'])
            print(f"Download complete for song: {search_string}\turl: {uri['link']}")

def download_tracks(trackList:list, savePath:str):
    downloadPath = Path().resolve().absolute().__str__()
    
    print(f"Download Path: {downloadPath}")
    for track in trackList:
        search_string = track['track']['trackName'] + ' ' + track['track']['artistName']
        yt_uris = search_youtube(search_string)
        tempsavePath = f"{savePath}\\{formate_foldername(track['track']['trackName'])}"
        for uri in yt_uris:
            download_song(uri['link'])
            print(f"Download complete for song: {search_string}\turl: {uri['link']}")
        MoveFile(downloadPath, tempsavePath, r".*\.mp3$")


def download_all_playlist(playlist_filepath:str,destination_folder:str,filterNames:list =None):
    f = open(playlist_filepath,encoding='utf-8')
    file_content = f.read()
    playlists = loads(file_content)['playlists']
    filtered_playlists = playlists
    if filterNames and filterNames.count() > 0:
        filtered_playlists:list = list(filter(lambda plist : plist['name'] in filterNames, playlists))

    for playlist in filtered_playlists:
        save_folder = destination_folder + f"\\{formate_foldername(playlist['name'])}"
        download_tracks(playlist['items'], save_folder)
        
        

if __name__ == '__main__':
    configFile = open("./config.json")
    configJson = None
    if configFile:
        configJson = loads(configFile.read())
    else:
        sys.exit("config file doesn't exist aborting!!")
    filePath:str = configJson['PlayListPath']
    filterList = configJson['PlaylistFilter']# list of playlist names you want to download. Leave empty for all
    downloadPath:str = Path().resolve().absolute().__str__()
    download_all_playlist(filePath, downloadPath, filterList)
    
