
# This code sample creates a private playlist in the authorizing user's
# YouTube channel.
# Usage:
#   python playlist_updates.py --title=<TITLE> --description=<DESCRIPTION>

import argparse
import os
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

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


def add_playlist(youtube, args):
    body = dict(
        snippet=dict(
            title=args.title,
            description=args.description
        ),
        status=dict(
            privacyStatus='private'
        )
    )

    playlists_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body=body
    ).execute()

    id = playlists_insert_response['id']

    print( 'New playlist ID: %s' % id)
    return id


def add_video_to_playlist(youtube, videoID, playlistID):
    add_video_request = youtube.playlistItems().insert(
        part="snippet",
        body={
            'snippet': {
                'playlistId': playlistID,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': videoID
                }
                # 'position': 0
            }
        }
    ).execute()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--title',
                        default='Test Playlist',
                        help='The title of the new playlist.')
    parser.add_argument('--description',
                        default='A private playlist created with the YouTube Data API.',
                        help='The description of the new playlist.')

    args = parser.parse_args()

    youtube = get_authenticated_service()
    try:
        fileName = "youtubeURLs.txt"
        file = open(fileName, "r")
        responses = file.readlines()

        ''' either create a new playlist or define which playlist to enter the videos into '''
        #playlist = add_playlist(youtube, args)
        playlist = "PLaJf0XdxMRdHOoXnnKw6qchqfTPuae-9R"

        ''' start point to read from in the file '''
        start = 419

        ''' '''
        for iteration in range(start, len(responses)):
            item = responses[iteration]
            iteration += 1
            print("adding video:" + str(item))
            videoID = item.split("watch?v=")
            videoID = videoID[-1]
            videoID = videoID.strip('\n')

            time.sleep(0.5)

            try:
                print("adding vid ID:|" + str(videoID) + "|")
                add_video_to_playlist(youtube, str(videoID), playlist)

            except HttpError as e:
                #print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content) )
                try:
                    videoID = videoID.split('&')
                    videoID=videoID[0]
                    #print("splitting on & to get new vid ID:|" + str(videoID) + "|")
                    add_video_to_playlist(youtube, str(videoID), playlist)
                except:
                    print('An error %d occurred:\n%s' % (e.resp.status, e.content))
                    print("video:" + str(item))

            print("iteration: " + str(iteration))

            #if iteration > start + 5:
            #    break

            print("\n\n")

        file.close()

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content) )
