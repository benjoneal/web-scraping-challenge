#Libraries/Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
import time

def init_browser():    
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

#Find the Article Title and Text
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    article = soup.find('div', class_='content_title')
    headline = article.text

    article_text = soup.find('div', class_='article_teaser_body')
    article_teaser = article_text.text


#Get the most recent image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)

    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = bs(html, 'html.parser')

    featured_image_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = print(f'https://www.jpl.nasa.gov{featured_image_url}')
    featured_image_url

#Get the most recent tweet and take the weather from it.
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    time.sleep(3)

    html = browser.html
    tweet_soup = bs(html, 'html.parser')


    tweet_container = tweet_soup.find_all('div', class_="js-tweet-text-container")


    for tweet in tweet_container: 
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            break
        else: 
            pass


#Set up website to scrape.
    mars_facts = 'https://space-facts.com/mars/'
    browser.visit(mars_facts)

    html = browser.html

#Find the Table
    table = pd.read_html(mars_facts)
    mars_facts_table = table[0]

    mars_facts_table

#Get the title and image from the Mars Hemisphere site.
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)

    html = browser.html
    hemisphere_soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    results = hemisphere_soup.find('div', class_ = 'result-list')
    hemispheres = results.find_all('div', class_='item')

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
    


#Store the Data

    mars_data = {
        'headline': headline,
        'article_teaser': article_teaser,
        'featured_image_url': featured_image_url,
        'mars_weater': mars_weather,
        'mars_facts_table': mars_facts_table,
        'hemisphere_image_urls': hemisphere_image_urls

    }

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()