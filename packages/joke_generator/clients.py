"""Joke API clients for different joke sources."""

import aiohttp
from typing import Optional, Dict, Any
from packages.logging import get_logger

logger = get_logger(__name__)


class JokeAPIClient:
    """Base client for joke APIs."""

    async def get_joke(self) -> Optional[Dict[str, Any]]:
        """Get a joke from the API."""
        raise NotImplementedError


class JokeAPIDevClient(JokeAPIClient):
    """Client for JokeAPI.dev (https://jokeapi.dev)."""

    BASE_URL = "https://v2.jokeapi.dev/joke"

    async def get_joke(self, joke_type: str = "Any") -> Optional[Dict[str, Any]]:
        """Get a joke from JokeAPI.dev.
        
        Args:
            joke_type: Type of joke (Any, General, Programming, Knock-Knock)
            
        Returns:
            Joke data or None if request failed
        """
        try:
            url = f"{self.BASE_URL}/{joke_type}"
            logger.info(f"Fetching joke from JokeAPI.dev: {joke_type}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully fetched joke: {data.get('category')}")
                        return data
                    else:
                        logger.error(f"API returned status {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Failed to fetch joke from JokeAPI.dev: {e}")
            return None


class UselessFactsAPIClient(JokeAPIClient):
    """Client for Useless Facts API (similar to jokes)."""

    BASE_URL = "https://uselessfacts.jscinc.com/random.json"

    async def get_joke(self) -> Optional[Dict[str, Any]]:
        """Get a useless fact (joke alternative).
        
        Returns:
            Fact data or None if request failed
        """
        try:
            logger.info("Fetching useless fact from API")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully fetched fact")
                        return data
                    else:
                        logger.error(f"API returned status {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Failed to fetch fact: {e}")
            return None


class DadJokesAPIClient(JokeAPIClient):
    """Client for icanhazdadjoke API (https://icanhazdadjoke.com)."""

    BASE_URL = "https://icanhazdadjoke.com/random"

    async def get_joke(self) -> Optional[Dict[str, Any]]:
        """Get a dad joke.
        
        Returns:
            Joke data or None if request failed
        """
        try:
            logger.info("Fetching dad joke from icanhazdadjoke.com")
            
            async with aiohttp.ClientSession() as session:
                headers = {"Accept": "application/json"}
                async with session.get(self.BASE_URL, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully fetched dad joke")
                        return data
                    else:
                        logger.error(f"API returned status {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Failed to fetch dad joke: {e}")
            return None
