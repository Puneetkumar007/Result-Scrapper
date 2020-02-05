#!/usr/bin/env python3
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import os
# Uncomment the following to run text to speech on android (Qpython)
# import androidhelper


def is_connected():
    url = "http://bcetgsp.ac.in"
    timeout = 2
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("\nConnection Error")
    except requests.exceptions.Timeout:
        print("\nTimeout occurred")
    return False


running = True

# Path for android
# file = '/storage/emulated/0/Download/CSE2016_6th_sem_result.pdf'

# Path (Change this path accordingly)
file = '/home/Puneet/Downloads/CSE2016_6th_sem_result.pdf'


def get_result():
    global running
    if is_connected():
        try:
            r = requests.get("http://bcetgsp.ac.in/displayres.php?exam=PTU%20April-May%202019", timeout=2)
        except requests.exceptions.Timeout:
            print("\nTimeout occurred")
        except requests.ConnectionError:
            print("\nConnection error")

        print("Status Code: ", r.status_code)
        print(r.url)

        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.findAll('a')

        for link in links:
            link_text = link.text

            if link_text == 'Download':
                link_href = link.attrs['href']

                if link_href[:72] == 'resultupload/results/CSE/B-Tech_Regular_PTU April-May 2019_6th_CSE2016-':
                    # print(link_href)
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    try:
                        r = requests.get("http://bcetgsp.ac.in/" + link_href, timeout=2)
                    except requests.exceptions.Timeout:
                        print("\nTimeout occurred")
                    except requests.ConnectionError:
                        print("\nConnection error")
            
                    if os.path.isfile(file) and os.stat(file).st_size != 0:
                        print("File already present")
                    else:
                        with open(file, 'wb') as f:
                            f.write(r.content)
                            # Uncomment the following two lines for android text to speech
                            # droid = androidhelper.Android()
                            # droid.ttsSpeak("Hey Puneet, your result is declared. Hurry go to Download folder")
                            print("Hey your result is out and is stored in the Download directory")
                            print("Result uploaded on: ", dt_string)
                            running = False

        if not os.path.isfile(file):
            print("\nResult is not declared yet\n")

    else:
        print("\nHost unreachable.\nEither the host is down\nor\nYou are offline")


while True:
    get_result()
