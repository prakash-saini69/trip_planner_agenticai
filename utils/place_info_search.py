import requests
# Reverting to community import to fix the crash
from langchain_community.tools import TavilySearchResults

class FoursquarePlaceSearchTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.foursquare.com/v3/places/search"
        self.headers = {
            "Accept": "application/json",
            "Authorization": self.api_key
        }

    def _search_foursquare(self, place: str, query: str, limit: int = 10) -> list:
        """
        Helper method to query Foursquare API.
        """
        params = {
            "near": place,
            "query": query,
            "limit": limit
        }
        try:
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Format the results into a readable list
            results = []
            for item in data.get("results", []):
                name = item.get("name")
                location = item.get("location", {}).get("formatted_address", "Address not available")
                results.append(f"{name} ({location})")
            return results
        except Exception as e:
            return [f"Error searching Foursquare: {str(e)}"]

    def foursquare_search_attractions(self, place: str) -> list:
        return self._search_foursquare(place, "attractions")

    def foursquare_search_restaurants(self, place: str) -> list:
        return self._search_foursquare(place, "restaurants")

    def foursquare_search_activity(self, place: str) -> list:
        return self._search_foursquare(place, "arts & entertainment")

    def foursquare_search_transportation(self, place: str) -> list:
        return self._search_foursquare(place, "travel & transport")


class TavilyPlaceSearchTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def _run_tavily(self, query: str):
        """
        Helper to initialize and run Tavily tool safely
        """
        try:
            # Using the stable community tool
            tool = TavilySearchResults(
                tavily_api_key=self.api_key, 
                max_results=5,
                include_answer=True
            )
            return tool.invoke(query)
        except Exception as e:
            return f"Error running Tavily: {str(e)}"

    def tavily_search_attractions(self, place: str) -> dict:
        return self._run_tavily(f"top attractive places in and around {place}")
    
    def tavily_search_restaurants(self, place: str) -> dict:
        return self._run_tavily(f"what are the top 10 restaurants and eateries in and around {place}?")
    
    def tavily_search_activity(self, place: str) -> dict:
        return self._run_tavily(f"popular activities and things to do in and around {place}")

    def tavily_search_transportation(self, place: str) -> dict:
        return self._run_tavily(f"What are the different modes of transportation available in {place}")