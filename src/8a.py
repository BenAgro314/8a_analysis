#!/usr/bin/env python3
from prettytable import PrettyTable
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from multiprocessing import Manager
import json
import requests
import re
from datetime import date

def color_text(text, rgb = [255,255,255]):
    reset =  "\033[0m"
    leading = "\033[38;2;" + str(rgb[0]) + ";" + str(rgb[1]) + ";" + str(rgb[2]) + "m";
    return leading + text + reset

front ='https://www.8a.nu' 

def process_crag(info): 
    URL = info[0]
    crag_name = info[1] 
    crag_data = {}

    count = 1
    while (URL is not None):
        print(color_text('Crag: ' + crag_name + ', page #' + str(count), [255,0,255]))
        try:
            root_page = requests.get(URL,timeout =20)
        except:
            return crag_data
        if root_page.status_code == 404:
            return crag_data
        soup = bs(root_page.content, 'html.parser')
        if (soup.body):
            table_body = soup.body.tbody
            if (table_body is None):
                return crag_data
        else:
            return crag_data
        for area in table_body.find_all('tr'):
            name_col =area.find(class_ = re.compile("name"))
            if (name_col is None or name_col.p is None or name_col.p.a is None):
                continue
            name = name_col.p.a.text.strip()
            ascents = area.find(class_ = re.compile("ascents"))
            if (ascents is None or ascents.text is None):
                continue
            ascents = ascents.text.strip()
            ratio = area.find(class_ = re.compile("ratio"))
            if (ratio is None or ratio.text is None):
                continue
            ratio = ratio.text.strip()
            recommend = area.find(class_ = re.compile("recommend"))
            if (recommend is None or recommend.text is None):
                continue
            recommend = recommend.text.strip()
            grade_col =area.find(class_ = re.compile("grade"))
            if (grade_col.div is None or grade_col.div.text is None):
                continue
            grade = grade_col.div.text.strip()
            print(color_text(grade + " " + name, [255,255,255]))
            crag_data[name] = {'ascents':ascents, 'fl/os ratio':ratio, 'recommended %':recommend, 'grade':grade}

        URL = None
        count +=1
        for a in soup.find_all(href = re.compile('page')):
            if (a.text == "NEXT"):
               URL = front + a['href'].strip() 

    return crag_data

def process_area(URL, area_data, name):
    count = 1
    while (URL is not None):
        print(color_text('Area: ' + name + ', page #' + str(count), [255,100,100]))
        try:
            root_page = requests.get(URL,timeout =20)
        except:
            return
        if root_page.status_code == 404:
            return
        soup = bs(root_page.content, 'html.parser')
        if (soup.body):
            table_body = soup.body.tbody
            if (table_body is None):
                return 
        else:
            return
        links = []
        datas = []
        for area in table_body.find_all('tr'):
            name_col =area.find(class_ = re.compile("name"))
            if (name_col is None or name_col.p is None or name_col.p.a is None or name_col.p.a.text is None):
                continue
            crag_name = name_col.p.a.text.strip()
            if ('href' not in name_col.p.a.attrs):
                continue
            link = front + name_col.p.a['href'].strip() 
            ascents = area.find(class_ = re.compile("ascents"))
            if (ascents is None or ascents.text is None):
                continue
            ascents = ascents.text.strip()
            ratio = area.find(class_ = re.compile("ratio"))
            if (ratio is None or ratio.text is None):
                continue
            ratio = ratio.text.strip()
            recommend = area.find(class_ = re.compile("recommend"))
            if (recommend is None or recommend.text is None):
                continue
            recommend = recommend.text.strip()
            #print(crag_name, ascents, ratio, recommend)
            area_data[crag_name] = {'ascents': ascents, 'fl/os ratio': ratio, 'recommended %': recommend}
            links.append((link, crag_name))
            
        try:
            p = Pool()
            res = p.map(process_crag,links)
            for i in range(len(res)):
                d = res[i]
                n = links[i][1]
                area_data[n]['climbs'] = d
            p.terminate()
            p.join()
        except:
            print("error processing a crag")

            
        URL = None
        count +=1
        for a in soup.find_all(href = re.compile('page')):
            if (a.text == "NEXT"):
               URL = front + a['href'].strip() 
               
        


def read_table(URL, filename):

    count = 1
    data = {}
    while (URL is not None):
        print(color_text('Page #' + str(count), [100,255,150]))
        try:
            root_page = requests.get(URL,timeout =20)
        except:
            return
        if root_page.status_code == 404:
            return
        soup = bs(root_page.content, 'html.parser')
        if (soup.body):
            table_body = soup.body.tbody
            if (table_body is None):
                return 
        else:
            return
        for area in table_body.find_all('tr'):
            name_col = area.find(class_ = re.compile("name"))
            if (name_col.p is None or name_col.p.a is None):
                continue
            name_col = name_col.p.a
            if (name_col.text is None):
                continue
            name = name_col.text.strip()
            if ('href' not in name_col.attrs):
                continue
            link = front + name_col['href'].strip()
            country = area.find(class_ = re.compile("country"))
            if (country.a is None or country.a.text is None):
                continue
            
            country = country.a.text.strip()
            data[name] = {'country': country, 'crags': {}}
            count = 1
            try:
                process_area(link, data[name]['crags'], name)
            except:
                print("Error processing area: " + name)
            with open(filename, 'w') as outfile:
                json.dump(data,outfile, indent = 4)

        count+=1
        URL = None
        for a in soup.find_all(href = re.compile('page')):
            if (a.text == "NEXT"):
               URL = front + a['href'].strip() 


def main():
    link = front + '/areas'
    filename = "../data/" + str(date.today()) + "_8a_data.json"
    read_table(link, filename)

if __name__ == "__main__":
    main()
