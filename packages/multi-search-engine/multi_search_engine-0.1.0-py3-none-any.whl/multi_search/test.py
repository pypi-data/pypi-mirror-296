from google_search import google_search
from yahoo_search import yahoo_search
from baidu_search import baidu_search
from bing_search import bing_search
from duckduckgo_search import duckduckgo_search
# Example query
query = "Python programming tutorials"

print("google search")
# Google Search
google_results = google_search(query, num_results=5)
for result in google_results:
    print(result)

print("yahoo search")
# Yahoo Search
yahoo_results = yahoo_search(query, num_results=5)
for result in yahoo_results:
    print(result)


print("Baidu search")
# Baidu Search
baidu_results = baidu_search(query, num_results=5)
for result in baidu_results:
    print(result)

print("bing search")
# bing Search
yandex_results = bing_search(query, num_results=5)
for result in yandex_results:
    print(result)

print("duck search")
# duck Search
baidu_results = duckduckgo_search(query, num_results=5)
for result in baidu_results:
    print(result)
