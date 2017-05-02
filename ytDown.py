#!/usr/bin/env python3
import os
import youtube_dl

## Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class YtDown:
    def __init__(self):
        self.urlDic = {}
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.youtube.com")
        self.driver.maximize_window()
        assert "YouTube" in self.driver.title

    def tryToFind(self, css, type):
        try:
            if(type == "id"):
                return self.driver.find_element_by_id(css)
            if(type == "class"):
                return self.driver.find_element_by_class_name(css)
        except Exception:
            return self.driver

    def wCss(self, css, m=None, t=5):
        try:
            element = WebDriverWait(self.driver, t).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css))
            )
        except Exception:
            pass

    def next(self):
        self.wCss("div.html5-video-container")
        self.wCss("span#eow-title")
        description = self.tryToFind("eow-title", "id")
        self.urlDic[description.text] = self.driver.current_url
        self.wCss("div.autoplay-bar")
        items = self.driver.find_element_by_class_name("video-list")
        items = items.find_elements_by_tag_name("li")
        for item in items:
            try:
                item.click()
                break;
            except Exception:
                pass;
            break;

    def BurnBabyBurn(self, searchText):
        elem = self.driver.find_element_by_name("search_query")
        elem.clear()
        elem.send_keys(searchText)
        elem.send_keys(Keys.RETURN)
        self.wCss("p.num-results")
        numResults = self.driver.find_element_by_class_name("num-results")
        print(numResults.text)
        items = self.driver.find_element_by_id("results")
        items = items.find_element_by_class_name("item-section")
        items = items.find_elements_by_tag_name("li")
        for item in items:
            try:
                print("Printando antes de empezar a pasar por cada DIV")
                print(item.text)
                item.click()
                time.sleep(4)
                self.next()
                break;
            except Exception:
                pass;
            break;


    def download_song(self, song_url, song_title, dl_directory='./'):
        """
        Download a song using youtube url and song title
        """
        global location

        dl_directory = os.path.abspath(os.path.expanduser(dl_directory))
        print(dl_directory)
        location = dl_directory + "\\output\\"

        if not os.path.exists(location):
            os.makedirs(location)
        outtmpl = song_title + '.%(ext)s'
        print("Descargando: " + str(location) + "---" + str(outtmpl))
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(location, outtmpl),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
                {'key': 'FFmpegMetadata'},
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(song_url, download=True)
                title = info_dict.get("title","idk.extension")
                notAllowed = ["~",'"',"#","%","&","*",":","<",">","?","/","\\",'{','|','}','.']
                for caracter in notAllowed:
                    title = title.replace(caracter,"")
            except Exception:
                pass

    def getMeThat(self, searchText, quantity=10):
        self.BurnBabyBurn(searchText)
        for i in range(quantity):
            time.sleep(2)
            self.wCss("div#watch8-action-buttons")
            self.next()

        time.sleep(2)
        self.wCss("div.html5-video-container")
        self.wCss("span#eow-title")
        description = self.driver.find_element_by_id("eow-title")
        print(description.text)
        self.urlDic[description.text] = self.driver.current_url

        print(self.urlDic)
        print("\n--------------------------")
        print (" Youtube Video Downloader")
        print ("--------------------------\n")

        for k, v in self.urlDic.items():
            self.download_song(v, k)

        print("\n Done.")

