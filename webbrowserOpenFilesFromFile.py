# created by Nicholas Garrett

import re
import webbrowser
import time

def google(command):
    webbrowser.open("https://" + str(command))





if __name__ == '__main__':
    fileName = "youtubeURLs.txt"
    file = open(fileName, "r")
    responses = file.readlines()
    iter = 350

    for iteration in range(iter, len(responses)):
        item = responses[iteration]
        iteration += 1
        print("item:" + str(item))
        google(item)


    file.close()

