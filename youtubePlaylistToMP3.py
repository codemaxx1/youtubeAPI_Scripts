
# This code sample creates a private playlist in the authorizing user's
# YouTube channel.
# Usage:
#   python playlist_updates.py --title=<TITLE> --description=<DESCRIPTION>

import argparse
import os
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
from pytube import YouTube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import youtube_dl


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets

CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


# Authorize the request and store authorization credentials.
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def listItemsInPlaylist(youtube, playlistID):
    next_page_token = ''
    videos = []
    while True:
        videoReturn = (
            youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                pageToken=next_page_token,
                playlistId=playlistID
            ).execute()
        )

        videos.append(videoReturn)

        try:
            if(videoReturn['nextPageToken']):
                next_page_token = videoReturn['nextPageToken']
            else:
                break
        except:
            break
        print("next page:")
        print(videoReturn['nextPageToken'])


    return videos


def downloadYoutubeVideoAudio(vidUrl):
    video_info = youtube_dl.YoutubeDL().extract_info(url = vidUrl,download=False)
    filename = f"{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))


if __name__ == '__main__':



    youtube = get_authenticated_service()
    try:
        fileName = "youtubeURLs.txt"
        file = open(fileName, "r")
        responses = file.readlines()

        ''' either create a new playlist or define which playlist to enter the videos into '''
        #playlist = add_playlist(youtube, args)
        playlist = "PLaJf0XdxMRdHOoXnnKw6qchqfTPuae-9R"

        #
        videos = listItemsInPlaylist(youtube, playlist)

        urlList = []

        print("\n\n")
        iteration = 0
        for j in videos:
            for i in j['items']:
                iteration+=1
                print(i)
                print("\niteration:" + str(iteration))
                urlList.append(str("https://www.youtube.com/watch?v=") + str(i['snippet']['resourceId']['videoId']))

        for i in urlList:
            print("downloading " + str(i))
            downloadYoutubeVideoAudio(i)


        print("\n\n")

        file.close()

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content) )
