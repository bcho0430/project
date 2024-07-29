import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
from datetime import datetime

# Function to fetch and parse the webpage
def fetch_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    
    # Example structure - adjust based on actual HTML structure
    for article in soup.find_all('article'):
        title = article.find('h2').get_text() if article.find('h2') else 'N/A'
        author = article.find('span', class_='author').get_text() if article.find('span', class_='author') else 'N/A'
        category = article.find('a', class_='category').get_text() if article.find('a', class_='category') else 'N/A'
        link = article.find('a')['href'] if article.find('a') else 'N/A'
        
        articles.append({
            'title': title,
            'author': author,
            'category': category,
            'link': link,
            'timestamp': datetime.now()
        })
    
    return articles

# Function to save articles to a CSV file
def save_articles(articles, filename='articles.csv'):
    df = pd.DataFrame(articles)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

# Main function to run the scraper
def run_scraper():
    url_nytimes = 'https://www.nytimes.com/'
    url_latimes = 'https://www.latimes.com/'
    
    articles_nytimes = fetch_articles(url_nytimes)
    articles_latimes = fetch_articles(url_latimes)
    
    save_articles(articles_nytimes, 'nytimes_articles.csv')
    save_articles(articles_latimes, 'latimes_articles.csv')

# Schedule the scraper to run every 15 minutes
schedule.every(15).minutes.do(run_scraper)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
