# Multi-Engine Search Package

This package provides a unified interface to perform web searches across multiple popular search engines.

## Features

- Supports Google, Bing, DuckDuckGo, Yahoo, and Baidu search engines
- Simple, consistent API for all supported search engines
- Configurable number of results
- API key support for engines that require it (e.g., Bing)

## Installation

To install the package, use pip:

```
pip install multi_search_engine
```


## Usage

Here's a basic example of how to use the package:

```python
from multi_engine_search import search

# Perform a Google search
results = search("Python programming", num_results=5)

# Perform a Bing search (requires API key)
bing_results = search("Machine learning", num_results=10, search_engine="bing", api_key="your_bing_api_key")

# Perform a DuckDuckGo search
ddg_results = search("Privacy", search_engine="duckduckgo")

# Perform a Google search
results = search("Python programming", num_results=5)

# Perform a Bing search (requires API key)
bing_results = search("Machine learning", num_results=10, search_engine="bing", api_key="your_bing_api_key")

# Perform a DuckDuckGo search
ddg_results = search("Privacy", search_engine="duckduckgo")
```

## API Reference

```
search(query, num_results=10, search_engine="google")
```
#
Performs a web search using the specified search engine.

### Parameters:
- `query` (str): The search query.
- `num_results` (int, optional): The number of results to return. Defaults to 10.
- `search_engine` (str, optional): The search engine to use. Options are "google", "bing", "duckduckgo", "yahoo", and "baidu". Defaults to "google".

### Returns:
A list of search results. The exact format may vary depending on the search engine used.

### Raises:
`ValueError`: If an unsupported search engine is specified.

## Supported Search Engines
- Google
- Bing (requires API key)
- DuckDuckGo
- Yahoo
- Baidu

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
