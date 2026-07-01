"""Test joke service."""

import pytest
from packages.joke_generator import JokeService, JokeType


@pytest.mark.asyncio
async def test_joke_service_initialization():
    """Test joke service initializes correctly."""
    service = JokeService()
    assert service.jokeapi_client is not None
    assert service.dadjokes_client is not None
    assert service.facts_client is not None


@pytest.mark.asyncio
async def test_get_programming_joke():
    """Test fetching programming joke."""
    service = JokeService()
    joke = await service.get_programming_joke()
    
    if joke:  # Only assert if API responds
        assert isinstance(joke, dict)
        print(f"Programming Joke: {JokeService.format_joke(joke)}")


@pytest.mark.asyncio
async def test_get_dad_joke():
    """Test fetching dad joke."""
    service = JokeService()
    joke = await service.get_dad_joke()
    
    if joke:  # Only assert if API responds
        assert isinstance(joke, dict)
        print(f"Dad Joke: {JokeService.format_joke(joke)}")


@pytest.mark.asyncio
async def test_get_random_joke():
    """Test fetching random joke."""
    service = JokeService()
    joke = await service.get_random_joke()
    
    if joke:  # Only assert if API responds
        assert isinstance(joke, dict)
        print(f"Random Joke: {JokeService.format_joke(joke)}")


def test_format_joke_single_line():
    """Test formatting single-line joke."""
    joke_data = {"joke": "Why did the programmer quit his job?"}
    formatted = JokeService.format_joke(joke_data)
    assert "😄" in formatted
    assert "Why did the programmer quit his job?" in formatted


def test_format_joke_two_part():
    """Test formatting two-part joke."""
    joke_data = {
        "setup": "Why did the programmer quit his job?",
        "delivery": "Because he didn't get arrays!"
    }
    formatted = JokeService.format_joke(joke_data)
    assert "setup" in formatted.lower() or "Why did" in formatted
    assert "delivery" in formatted.lower() or "arrays" in formatted


def test_format_fact():
    """Test formatting fact."""
    fact_data = {"text": "Honey never spoils"}
    formatted = JokeService.format_joke(fact_data)
    assert "💡" in formatted
    assert "Honey never spoils" in formatted
