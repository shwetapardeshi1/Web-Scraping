# import libraries
from bs4 import BeautifulSoup
import urllib.request
import csv
import requests
import re
import time 
from datetime import datetime
from random import randint

# specify the url
urlpage =  r"https://www.simplyrecipes.com/?s"

def find_url(url_page):
    
    time.sleep(randint(8,15))
    page = requests.get(url_page)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    page_urls = soup.find_all('a', class_= 'page-numbers')
    recipe_urls = soup.find_all('a', href=True)
   
    return page_urls, recipe_urls

Recipe_urls=[]

for i in range(2,192):

    page_urls , recipe_urls = find_url(urlpage)
  
    for f in page_urls:
        if str(i) == f.text:
            urlpage = f.get('href')

    for recipe in recipe_urls:
        link = recipe.find('div', class_="site-search")
        try:
            Recipe_urls.append(link.get('href'))
            print(link.get('href'))
        except:
            continue   

with open("simple_recipes.csv", mode='w') as csvfile:
    fieldnames = ['recp_name','url','ingredients']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

total_recipes = 0

for url in Recipe_urls:
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', id ='sr-recipe-callout')
        recipe_name = recp_soup.find('h2', class_="recipe-callout-buttons").text
        job_elems = results.find_all('div', class_='entry-details recipe-ingredients')
        for job_elem in job_elems:
            ingredients = job_elem.find_all('ul')
    
        for elem in ingredients:
            s= elem.get_text()
            s = s.replace('\n', '', 1)
            s = re.sub(r'\n', ';', s)
        total_recipes+=1
        writer.writerow({'recp_name':recipe_name, 'url':url, 'ingredients':s})
    except:
        continue

    print("Recipes added till now: "+str(total_recipes))

    





