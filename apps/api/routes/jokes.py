"""API endpoints for joke generation."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from packages.joke_generator import JokeService, JokeType
from packages.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/jokes", tags=["Jokes"])

# Initialize service
joke_service = JokeService()


class JokeResponse(BaseModel):
    """Joke response model."""

    joke: str
    source: str
    type: str = "unknown"
    status: str = "success"


class JokeErrorResponse(BaseModel):
    """Error response model."""

    status: str = "error"
    message: str


@router.get("/random", response_model=JokeResponse)
async def get_random_joke():
    """Get a random joke from any source.
    
    Returns:
        Random joke from one of the integrated APIs
    """
    try:
        joke_data = await joke_service.get_random_joke()
        
        if not joke_data:
            raise HTTPException(
                status_code=503,
                detail="All joke sources are currently unavailable"
            )
        
        formatted_joke = JokeService.format_joke(joke_data)
        
        return JokeResponse(
            joke=formatted_joke,
            source="random",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error fetching random joke: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/programming", response_model=JokeResponse)
async def get_programming_joke():
    """Get a programming-specific joke.
    
    Returns:
        Programming joke from JokeAPI.dev
    """
    try:
        joke_data = await joke_service.get_programming_joke()
        
        if not joke_data:
            raise HTTPException(
                status_code=503,
                detail="Failed to fetch programming joke"
            )
        
        formatted_joke = JokeService.format_joke(joke_data, "programming")
        
        return JokeResponse(
            joke=formatted_joke,
            source="jokeapi.dev",
            type="programming",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error fetching programming joke: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knock-knock", response_model=JokeResponse)
async def get_knock_knock_joke():
    """Get a knock-knock joke.
    
    Returns:
        Knock-knock joke from JokeAPI.dev
    """
    try:
        joke_data = await joke_service.get_knock_knock_joke()
        
        if not joke_data:
            raise HTTPException(
                status_code=503,
                detail="Failed to fetch knock-knock joke"
            )
        
        formatted_joke = JokeService.format_joke(joke_data, "knock-knock")
        
        return JokeResponse(
            joke=formatted_joke,
            source="jokeapi.dev",
            type="knock-knock",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error fetching knock-knock joke: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/general", response_model=JokeResponse)
async def get_general_joke():
    """Get a general joke.
    
    Returns:
        General joke from JokeAPI.dev
    """
    try:
        joke_data = await joke_service.get_general_joke()
        
        if not joke_data:
            raise HTTPException(
                status_code=503,
                detail="Failed to fetch general joke"
            )
        
        formatted_joke = JokeService.format_joke(joke_data, "general")
        
        return JokeResponse(
            joke=formatted_joke,
            source="jokeapi.dev",
            type="general",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error fetching general joke: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dad-joke", response_model=JokeResponse)
async def get_dad_joke():
    """Get a dad joke.
    
    Returns:
        Dad joke from icanhazdadjoke.com
    """
    try:
        joke_data = await joke_service.get_dad_joke()
        
        if not joke_data:
            raise HTTPException(
                status_code=503,
                detail="Failed to fetch dad joke"
            )
        
        formatted_joke = JokeService.format_joke(joke_data, "dad-joke")
        
        return JokeResponse(
            joke=formatted_joke,
            source="icanhazdadjoke.com",
            type="dad-joke",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error fetching dad joke: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/facts", response_model=JokeResponse)
async def get_useless_fact():
    """Get a useless fact (fun alternative to jokes).
    
    Returns:
        Useless fact from Useless Facts API
    """
    try:
        fact_data = await joke_service.get_useless_fact()
        
        if not fact_data:
            raise HTTPException(
                status_code=503,
                detail="Failed to fetch useless fact"
            )
        
        formatted_fact = JokeService.format_joke(fact_data, "fact")
        
        return JokeResponse(
            joke=formatted_fact,
            source="uselessfacts.jscinc.com",
            type="fact",
            status="success"
        )
    except Exception as e:
        logger.error(f"Error fetching useless fact: {e}")
        raise HTTPException(status_code=500, detail=str(e))
