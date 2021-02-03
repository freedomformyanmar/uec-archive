import json
from bs4 import BeautifulSoup
from pywebcopy import save_webpage
import os
import urllib
from datetime import datetime

with open('data.json') as f:
    full_data = json.load(f)
    for data in full_data['data']:
        try:
            url = data['attributes']['url']
            print("title : {}".format(data['attributes']['title']))

            response = urllib.request.urlopen(url)
            webContent = response.read()

            filename = "archives/{}/content.html".format(data['id'])
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname) 
            with open(filename, 'wb') as output_f:
                output_f.write(webContent)

            soup = BeautifulSoup(webContent, "html.parser")
            images = soup.findAll('img')
            for image in images:
                src = image['src']
                if (src.startswith("https://")):
                    print("saving image {}".format(src))
                    name = os.path.basename(src)
                    response = urllib.request.urlopen(src)
                    webContent = response.read()

                    filename = "archives/{}/{}".format(data['id'], name)

                    with open(filename, 'wb') as output_f:
                        output_f.write(webContent)
        except Exception:
            pass

    with open("log.txt", 'a') as logfile:
        sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
        logfile.write(sttime)