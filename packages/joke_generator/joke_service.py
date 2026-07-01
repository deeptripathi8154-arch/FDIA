"""Joke service with multiple API integrations."""

import random
from typing import Optional, Dict, Any

from packages.logging import get_logger
from .clients import JokeAPIDevClient, UselessFactsAPIClient, DadJokesAPIClient
from .models import JokeType

logger = get_logger(__name__)


class JokeService:
    """Service for fetching jokes from multiple external APIs."""

    def __init__(self):
        """Initialize joke service with multiple clients."""
        self.jokeapi_client = JokeAPIDevClient()
        self.dadjokes_client = DadJokesAPIClient()
        self.facts_client = UselessFactsAPIClient()
        logger.info("Joke service initialized with 3 API clients")

    async def get_random_joke(self) -> Optional[Dict[str, Any]]:
        """Get a random joke from a random source.
        
        Returns:
            Joke data or None if all sources fail
        """
        sources = [
            ("jokeapi", self._get_jokeapi_joke),
            ("dadjokes", self._get_dadjoke),
            ("facts", self._get_useless_fact),
        ]
        
        # Shuffle sources for randomness
        random.shuffle(sources)
        
        for source_name, fetch_func in sources:
            try:
                joke = await fetch_func()
                if joke:
                    return joke
            except Exception as e:
                logger.warning(f"Failed to get joke from {source_name}: {e}")
                continue
        
        logger.error("All joke sources failed")
        return None

    async def get_programming_joke(self) -> Optional[Dict[str, Any]]:
        """Get a programming-specific joke.
        
        Returns:
            Programming joke or None
        """
        logger.info("Fetching programming joke")
        return await self.jokeapi_client.get_joke("Programming")

    async def get_knock_knock_joke(self) -> Optional[Dict[str, Any]]:
        """Get a knock-knock joke.
        
        Returns:
            Knock-knock joke or None
        """
        logger.info("Fetching knock-knock joke")
        return await self.jokeapi_client.get_joke("Knock-Knock")

    async def get_general_joke(self) -> Optional[Dict[str, Any]]:
        """Get a general joke.
        
        Returns:
            General joke or None
        """
        logger.info("Fetching general joke")
        return await self.jokeapi_client.get_joke("General")

    async def get_dad_joke(self) -> Optional[Dict[str, Any]]:
        """Get a dad joke.
        
        Returns:
            Dad joke or None
        """
        logger.info("Fetching dad joke")
        return await self.dadjokes_client.get_joke()

    async def get_useless_fact(self) -> Optional[Dict[str, Any]]:
        """Get a useless fact (fun alternative to jokes).
        
        Returns:
            Useless fact or None
        """
        logger.info("Fetching useless fact")
        return await self.facts_client.get_joke()

    async def _get_jokeapi_joke(self) -> Optional[Dict[str, Any]]:
        """Get a joke from JokeAPI.dev."""
        return await self.jokeapi_client.get_joke("Any")

    async def _get_dadjoke(self) -> Optional[Dict[str, Any]]:
        """Get a dad joke."""
        return await self.dadjokes_client.get_joke()

    async def _get_useless_fact(self) -> Optional[Dict[str, Any]]:
        """Get a useless fact."""
        return await self.facts_client.get_joke()

    @staticmethod
    def format_joke(joke_data: Dict[str, Any], source: str = "unknown") -> str:
        """Format joke data into a readable string.
        
        Args:
            joke_data: Joke data from API
            source: Source of the joke
            
        Returns:
            Formatted joke string
        """
        if not joke_data:
            return "No joke available"
        
        # Handle JokeAPI.dev format
        if "joke" in joke_data:
            return f"😄 {joke_data['joke']}"
        
        # Handle two-part jokes
        if "setup" in joke_data and "delivery" in joke_data:
            return f"😄 {joke_data['setup']}\n\n😂 {joke_data['delivery']}"
        
        # Handle Dad Jokes format
        if "joke" in joke_data:
            return f"😄 {joke_data['joke']}"
        
        # Handle Useless Facts format
        if "text" in joke_data:
            return f"💡 {joke_data['text']}"
        
        # Fallback
        return str(joke_data)
