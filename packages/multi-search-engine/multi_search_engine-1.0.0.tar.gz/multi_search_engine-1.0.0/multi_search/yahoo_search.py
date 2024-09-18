import requests
from bs4 import BeautifulSoup

def yahoo_search(query, num_results=10):
    query = query.replace(' ', '+')  # Format the query for the search URL
    url = f"https://search.yahoo.com/search?p={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse the search results
    results = []
    for item in soup.find_all('div', {'class': 'Sr'}, limit=num_results):
        title_element = item.find('h3')
        if title_element:
            title = title_element.text
            link = item.find('a')['href']
            description = item.find('p').text if item.find('p') else ''
            
            results.append({
                'title': title,
                'url': link,
                'snippet': description
            })
    
    return results
