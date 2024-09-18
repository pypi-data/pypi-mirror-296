import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import random
from fake_useragent import UserAgent

class TooManyRequestsException(Exception):
    pass

def duckduckgo_search(query, num_results=10, max_retries=3):
    encoded_query = quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={encoded_query}"
    
    ua = UserAgent()
    
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': ua.random,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': 'https://duckduckgo.com/'
            }
            
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 429:
                raise TooManyRequestsException("Too many requests, try again later.")
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('div', {'class': 'result__body'}, limit=num_results):
                link = result.find('a', {'class': 'result__a'})
                if link:
                    title = link.text.strip()
                    href = link['href']
                    snippet = result.find('a', {'class': 'result__snippet'})
                    description = snippet.text.strip() if snippet else ''
                    results.append({
                        'title': title,
                        'url': href,
                        'description': description
                    })
            
            return results
        
        except TooManyRequestsException as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(5, 15)
                print(f"Waiting for {wait_time:.2f} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Unable to complete the search.")
                return []
        
        except requests.RequestException as e:
            print(f"An error occurred: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(2, 5)
                print(f"Waiting for {wait_time:.2f} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Unable to complete the search.")
                return []
        
        time.sleep(random.uniform(1, 3))  # Random delay between attempts