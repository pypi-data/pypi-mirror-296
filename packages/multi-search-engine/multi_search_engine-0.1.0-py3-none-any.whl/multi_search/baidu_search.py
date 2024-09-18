import requests
from bs4 import BeautifulSoup

def baidu_search(query, num_results=10):
    query = query.replace(' ', '+')  # Format the query for the search URL
    url = f"https://www.baidu.com/s?wd={query}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Parse the search results
    results = []
    for item in soup.find_all('div', {'class': 'result'}, limit=num_results):
        title_element = item.find('a')
        if title_element:
            title = title_element.text
            link = title_element['href']
            description = item.find('div', {'class': 'c-abstract'}).text if item.find('div', {'class': 'c-abstract'}) else ''
            
            results.append({
                'title': title,
                'url': link,
                'snippet': description
            })

    return results
