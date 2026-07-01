"""Joke type enums."""

from enum import Enum


class JokeType(str, Enum):
    """Available joke types."""

    GENERAL = "general"
    PROGRAMMING = "programming"
    KNOCK_KNOCK = "knock-knock"
    RANDOM = "random"
