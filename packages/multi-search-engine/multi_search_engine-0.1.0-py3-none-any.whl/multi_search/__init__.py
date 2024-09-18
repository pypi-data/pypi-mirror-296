from .google_search import google_search
from .bing_search import bing_search
from .duckduckgo_search import duckduckgo_search
from .yahoo_search import yahoo_search
from .baidu_search import baidu_search

SEARCH_ENGINES = {
    "google": google_search,
    "bing": bing_search,
    "duckduckgo": duckduckgo_search,
    "yahoo": yahoo_search,
    "baidu": baidu_search,
}

def search(query, num_results=10, search_engine="google", api_key=None):
    if search_engine not in SEARCH_ENGINES:
        raise ValueError(f"Search engine '{search_engine}' is not supported.")
    
    search_func = SEARCH_ENGINES[search_engine]
    
    if search_engine in ["bing"]:  # Some search engines may require an API key
        return search_func(query, num_results, api_key)
    
    return search_func(query, num_results)

__all__ = ['search', 'google_search', 'bing_search', 'duckduckgo_search', 'yahoo_search', 'baidu_search']