from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

def scraper():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    title, text = mars_news(browser)

    data = {
        'title': title,
        'paragraph': text,
        'image': featured_image(browser),
        'facts': mars_facts(),
        'hemispheres': hemispheres(browser)
    }
    browser.quit()
    return data

# ### NASA Mars News
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

    news_soup = bs(browser.html, 'html.parser')
    title = news_soup.select_one('div.content_title a').text
    paragraph = news_soup.select_one('div.article_teaser_body').text

    return title, paragraph

    # ### JPL Mars Space Images - Featured Image
    # * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)
    browser.find_by_id('full_image').click()
    time.sleep(1)
    browser.find_link_by_partial_text('more info').click()
    featured_image = browser.find_by_css('figure.lede a')['href']
    return featured_image

# ### Mars Facts
# * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.
def mars_facts():
    mars_facts = pd.read_html('https://space-facts.com/mars/')[0].to_html(classes='table table-stripped')
    return mars_facts

# ### Mars Hemispheres
# 
# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# Open browser to USGS Astrogeology site
def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(2)

    hemispheres = []

    # Search for the names of all four hemispheres
    links = browser.find_by_css('a.itemLink h3')

    # Get text and store in list
    for i in range(len(links)):
        browser.find_by_css('a.itemLink h3')[i].click()

        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere['image_url'] = browser.find_link_by_partial_text('Sample')['href']
        hemispheres.append(hemisphere)

        browser.back()
    return hemispheres

