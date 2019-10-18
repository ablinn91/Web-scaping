from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\chrome_driver\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # this pulls the titles. 
    browser = init_browser()
    listings = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    listings["news_title"] = soup.find(class_="content_title").get_text()
    listings["article_body"] = soup.find(class_= "article_teaser_body").get_text()
    
    browser.quit()

    #this is where we get our pircure
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("FULL IMAGE")

    browser.is_element_present_by_text('more info', wait_time=1)
    browser.click_link_by_partial_text("more info")


    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    listings["picture"] = "https://www.jpl.nasa.gov" + soup.find("img",class_="main_image").get('src')

    browser.quit()
    
    #now we are going to extract our table

    import urllib.request
    import requests
    url = urllib.request.urlopen("https://space-facts.com/mars/").read()
    soup = BeautifulSoup(url,'lxml')
    table = soup.find('table')
    table_rows = table.find_all('tr')

    table = soup.find("table", id = "tablepress-p-mars")
    rows = table.findAll('tr')

    column1 = []
    column2 = []

    for tr in rows:
        td = tr.find_all('td')
        n =0
        row = []
        for i in td:
            a = i.text
            if n==0:
                column1.append((a))
                n = n+1
            elif n ==1: 
                column2.append((a))
                n = n+1 

    mars_data_df = pd.DataFrame(column2,column1)
    
    htmldata = mars_data_df.to_html(justify  = "left")
    htmldata2 = htmldata.replace('\n', '')
    listings['table'] = htmldata2


    #get info from twitter 
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    #now we are going to pull the pictures. 


    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    listings["twiiter"] = soup.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    browser.quit()
    #now we are going to pull the pictures. 
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("Cerberus Hemisphere Enhanced")
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    listings["picture2"] = "https://astrogeology.usgs.gov" + soup.find("img",class_="wide-image").get('src')
    browser.quit()
#get the next picture
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("Schiaparelli Hemisphere Enhanced")
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    listings["picture3"] = "https://astrogeology.usgs.gov" + soup.find("img",class_="wide-image").get('src')
    browser.quit()
#get the next picture
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("Syrtis Major Hemisphere Enhanced")
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    listings["picture4"] = "https://astrogeology.usgs.gov" + soup.find("img",class_="wide-image").get('src')
    browser.quit()
#get the next picture
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text("Valles Marineris Hemisphere Enhanced")
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    listings["picture5"] = "https://astrogeology.usgs.gov" + soup.find("img",class_="wide-image").get('src')
    browser.quit()
    

    


    # trying for a loop
    # for i in range(4):
 
    #     browser = init_browser()
    #     url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #     browser.visit(url)
    #     if i == 0:
    #         browser.click_link_by_partial_text("Cerberus Hemisphere Enhanced")
    #     elif i==1:
    #         browser.click_link_by_partial_text("Schiaparelli Hemisphere Enhanced")
    #     elif i==2:
    #         browser.click_link_by_partial_text("Syrtis Major Hemisphere Enhanced")
    #     elif i==3: 
    #         browser.click_link_by_partial_text("Valles Marineris Hemisphere Enhanced")           

    #     html = browser.html

    #     soup = BeautifulSoup(html, "html.parser")

    #     listings["picture"+i] = "https://astrogeology.usgs.gov"+soup.find("img",class_="wide-image").get('src')
    #     browser.quit()


    
    return listings
