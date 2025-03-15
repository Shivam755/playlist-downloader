# playlist-downloader

This project is intended to automate the process of downloading playlists.

It searches for the song name on youtube and downloads the results using yt-dlp. You can specify the number of results you want to download for each song as the first result isn't always what we want.

***Note:***
Currently it only supports json files with a specific structure. Refer [`sample.json`](sample.json)

# Disclaimer

This project is intended for **educational purposes only**. It is not meant to be used for downloading copyrighted content without proper authorization. The developers are **not responsible** for any misuse of this tool.  

By using this software, you agree to comply with all applicable laws and regulations.  

# How to execute

1. Clone the Repository
2. Prepare your playlist json file (Refer [`sample.json`](sample.json))
3. Enter proper values in  [`config.json`](config.json)
```
{
    "maxYTResult": 3, // The number of results you want to download
    "PlayListPath":"./sample.json", // the path to your playlist json file
    "PlaylistFilter": [ "Classics", ... ] // if you have multple playlist mentioned in the file but only want to download a selected few, then mention the playlist names here. Leaving it empty will result in all playlists being downloaded.
}
```
4. Create and activate a virtual environment (optional)
5. Install the pip requirements
    `pip install -r requirements.txt`
6. Execute the script `python downloader.py` . The songs will be downloaded and stored in a tree like structure:
   ```
    playlist-downloader/
    |   Playlist1/
    |   |--Song1/
    |   |   |--Result1
    |   |   |--Result2
    |   |--Song2/
    |   |   |--Result1
    |   |   |--Result2
    |   Playlist2/
    |   |--Song1/
    |   |   |--Result1
    |   |   |--Result2
    ...
   ```


*Note:* Make sure you have installed ffmpeg for file conversion