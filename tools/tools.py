from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_tavily_url(name: str):
    search = TavilySearchResults()
    results = search.run(f"{name}")
    return results