import requests
from bs4 import BeautifulSoup

def bing_search(query, num_results=10):
    query = query.replace(' ', '+')  # Format the query for the search URL
    url = f"https://www.bing.com/search?q={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse the search results
    results = []
    for item in soup.find_all('li', {'class': 'b_algo'}, limit=num_results):
        title_element = item.find('h2')
        if title_element and title_element.find('a'):
            title = title_element.find('a').text
            link = title_element.find('a')['href']
            description = item.find('p').text if item.find('p') else ''
            
            results.append({
                'title': title,
                'url': link,
                'snippet': description
            })

    return results
