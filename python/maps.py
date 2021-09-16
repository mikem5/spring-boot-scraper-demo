import sys
import praw
import tld
import requests
import bs4
import uuid
import datetime
import os
import shutil
import datetime
import time
import logging
from PIL import Image
from imgur_downloader import ImgurDownloader
import json
import time






# Reddit id and secret for praw
CLIENTID = ''
SECRET = ''
# Useragents
user_agent = ''
USERAGENT = ''
USER_AGENT_DEVIANT = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/6.0'

# Default filepath to download images to - this is disabled for testing, work and just remove the return
DEFAULT_FILE_PATH = '/somewhere'



def url_parser(url, meta):
    
    # main parser which will seperate and manage urls
    # takes a url (string) in ->
    # determines where to send it for subprocess


    try:
        res = tld.get_tld(url, as_object=True, fix_protocol=True)
    except:
        return

    if res.domain == "imgur":
        try:
            imgur_parser(url,meta)
        except:
            logging.exception('imgur')


    if res.domain == "deviantart":
        try:
            deviant_parser(url,meta)
        except:
            logging.exception('deviant')


    if res.domain == "artstation":
        try:
            artstation_parser(url,meta)
        except:
            logging.exception('artstation')


    else:
        try:
            def_parser(url, meta)
        except:
            logging.exception('else')





def imgur_parser(url,meta):
    # parses imgur links

    guid = gen_uuid(url)
    ts = datetime.datetime.now()


    if meta != '':
        filename = meta[:50] + str(time.time())[:12] 
    else:
        filename = url.split('/')[-1]



    file_path =  DEFAULT_FILE_PATH+filename


    if check_ids(guid, 'maps') == True:
        try:
            downloader = ImgurDownloader(url,DEFAULT_FILE_PATH, filename)
            total_dl = downloader.save_images()
            if downloader.num_images() > 1:
                row = [guid, ts, url, file_path+'/'+filename, meta]
            else:
                row = [guid, ts, url, file_path, meta]


            add_row(row, 'maps')


        except:
            pass


        #time.sleep(.2)

    return


def deviant_parser(url, meta):

  
    if check_image(url) == True:
        def_parser(url,meta)
    
    else:
        guid = gen_uuid(url)

        if check_ids(guid, 'maps') == True:


            ts = datetime.datetime.now()

            

            r = requests.get(url)
            c = r.content
            soup = bs4.BeautifulSoup(c, 'html.parser')
            
            # this should work?
            link = soup.find_all('img', class_='_1izoQ')

            try:
                imgurl = link[0].get('src')
                durl = imgurl
                token = ''
            except:
                logging.exception('failed to find link in deviantart: '+url)
                return 

            if check_image(imgurl) == False:

                try:
                    temp_l = imgurl.split('?')
                    durl = temp_l[0]
                    token = temp_l[1].split('=')[-1]

                    end = imgurl.split('/')[-1].split('?')[0].split('.')[-1]
                    
                except:
                    logging.exception('cant get end type: ' + imgurl)
                    return

            else:
                end = imgurl.split('.')[-1]


            if meta != '':
                filename = meta[:50] + str(time.time())[:12] +'.' + end

            else:
                filename = imgurl.split('/')[-1].split('?')[0]


            file_path = DEFAULT_FILE_PATH + filename


            try:
 
                response = requests.get(durl + '?token=' + token, headers={'user-agent': USER_AGENT_DEVIANT} )

                filenm = os.path.join(DEFAULT_FILE_PATH, file_path)

                with open(filenm, 'wb') as out_file:
                    out_file.write(response.content)

                del response


                row = [guid, ts, url, file_path, meta]

                add_row(row, 'maps')
            except:
                pass


            #time.sleep(.2)
    
    return



def artstation_parser(url, meta):

    guid = gen_uuid(url)
    ts = datetime.datetime.now()
 
    filen1 = url.split('/')[-1].split('?')[0]      
    end = filen1.split('.')[-1]

    if meta != '':
        filename = meta[:50] + str(time.time())[:12] + '.' + end
#    else:
    filename = filen1


    file_path = DEFAULT_FILE_PATH +filename

    if check_ids(guid, 'maps') == True:


        try:
            download_file(url,file_path)
            row = [guid, ts, url, file_path, meta]

            add_row(row, 'maps')
        except:
            logging.exception('in artstation parser download/add row')
            pass


        #time.sleep(.2)

    return






def def_parser(url,meta):
 
    if check_image(url) == True:

        guid = gen_uuid(url)
        ts = datetime.datetime.now()
    

        filename = meta[:50] + str(time.time())[:12] + '.' + url.split('.')[-1]
  
        file_path = DEFAULT_FILE_PATH +filename

        if check_ids(guid, 'maps') == True:


            try:
                download_file(url,file_path)
                row = [guid, ts, url, file_path, meta]

                add_row(row, 'maps')
            except:
                pass


            #time.sleep(.2)

    return













def gen_uuid(ids):
    return str(uuid.uuid3(uuid.UUID('00000000-0000-0000-0000-000000000000'), ids))



def check_image(url):
    # test if a url links to an image
    end = url.split('.')[-1]
    if end == 'jpg' or end == 'png' or end == 'gif':
        return True
    else:
        return False



def download_file(url, dest_dir):
    return True # for testing
    print("downloading " + url)
    response = requests.get(url, headers={'user-agent': USER_AGENT_DEVIANT} )
    filenm = os.path.join(DEFAULT_FILE_PATH, dest_dir)

    with open(filenm, 'wb') as out_file:
        out_file.write(response.content)

    del response




def check_ids(guid, table):

    
    if requests.get("http://localhost:8080/maps/id/"+ str(guid)).status_code != 200:
        return True
    else:
        print("found matching id: %s" % guid)
        return False



def add_row(row, table):
    print("adding row") 
    print(row)
    print(table)
    if table == 'maps':
        data = {"id": str(row[0]), "date": str(row[1]), "url": str(row[2]), "file_path": str(row[3]), "meta": str(row[4]) }
        requests.post("http://localhost:8080/maps/new", json=data)
    



reddit = praw.Reddit(client_id = CLIENTID, client_secret = SECRET, user_agent=USERAGENT)


for x in ['dungeondraft','IsometricDND', 'battlemaps', 'dndmaps']:
    a = x
    print(a)
    total = 0
    for submission in reddit.subreddit(a).new(limit=25):
        total+=1
        meta = submission.title
        url = submission.url
        url_parser(url,meta)




