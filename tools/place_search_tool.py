import os
from utils.place_info_search import FoursquarePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv() # This loads variables from your .env file
        
        # Load API keys from .env
        self.foursquare_api_key = os.environ.get("FOURSQUARE_API_KEY")
        self.tavily_api_key = os.environ.get("TAVILY_API_KEY")
        
        # Initialize the tools with the keys
        # We pass the keys here so the utility classes don't have to guess where they are
        self.foursquare_search = FoursquarePlaceSearchTool(self.foursquare_api_key)
        self.tavily_search = TavilyPlaceSearchTool(self.tavily_api_key)
        
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                # Primary: Try Foursquare
                attraction_result = self.foursquare_search.foursquare_search_attractions(place)
                if attraction_result:
                    return f"Following are the attractions of {place} as suggested by Foursquare: {attraction_result}"
                else:
                    raise Exception("No results from Foursquare")
            except Exception as e:
                # Fallback: Use Tavily
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                return f"Foursquare could not find details due to error: {e}. \nFollowing are the attractions of {place} found via web search: {tavily_result}"

        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                restaurants_result = self.foursquare_search.foursquare_search_restaurants(place)
                if restaurants_result:
                    return f"Following are the restaurants of {place} as suggested by Foursquare: {restaurants_result}"
                else:
                    raise Exception("No results from Foursquare")
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Foursquare could not find details due to error: {e}. \nFollowing are the restaurants of {place} found via web search: {tavily_result}"

        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                activity_result = self.foursquare_search.foursquare_search_activity(place)
                if activity_result:
                    return f"Following are the activities in and around {place} as suggested by Foursquare: {activity_result}"
                else:
                    raise Exception("No results from Foursquare")
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Foursquare could not find details due to error: {e}. \nFollowing are the activities of {place} found via web search: {tavily_result}"

        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                transport_result = self.foursquare_search.foursquare_search_transportation(place)
                if transport_result:
                    return f"Following are the modes of transportation available in {place} as suggested by Foursquare: {transport_result}"
                else:
                    raise Exception("No results from Foursquare")
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Foursquare could not find details due to error: {e}. \nFollowing are the modes of transportation available in {place} found via web search: {tavily_result}"

        return [search_attractions, search_restaurants, search_activities, search_transportation]