import requests
from bs4 import BeautifulSoup
import time
import random
from requests.exceptions import RequestException

# List of user agents
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
]

def get_random_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def google_search(query, num_results=10, max_retries=5):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    
    for attempt in range(max_retries):
        try:
            headers = get_random_header()
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for item in soup.select('div.g'):
                title_element = item.select_one('h3')
                link_element = item.select_one('.yuRUbf a')
                description_element = item.select_one('.VwiC3b')
                
                if title_element and link_element:
                    title = title_element.text
                    link = link_element['href']
                    description = description_element.text if description_element else ''
                    
                    results.append({
                        'title': title,
                        'url': link,
                        'description': description
                    })
                
                if len(results) >= num_results:
                    break
            
            return results
        
        except RequestException as e:
            if attempt < max_retries - 1:
                sleep_time = (2 ** attempt) + random.random()
                print(f"Attempt {attempt + 1} failed. Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Max retries reached. Error: {e}")
                return []
