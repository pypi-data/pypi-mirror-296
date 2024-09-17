from dataclasses import dataclass, field
from logging import Logger, getLogger
from typing import Dict, List, Union

from pyflowery.version import VERSION


@dataclass
class Voice:
    """Voice object returned from the Flowery API

    Attributes:
        id (str): UUID of the voice
        name (str): Name of the voice
        gender (str): Gender of the voice
        source (str): Source of the voice
        language (Language): Language object
    """
    id: str
    name: str
    gender: str
    source: str
    language: 'Language'

@dataclass
class Language:
    """Language object returned from the Flowery API

    Attributes:
        name (str): Name of the language
        code (str): Code of the language
    """
    name: str
    code: str

@dataclass
class Result:
    """Result returned from low-level RestAdapter

    Attributes:
        success (bool): Boolean of whether the request was successful
        status_code (int): Standard HTTP Status code
        message (str = ''): Human readable result
        data (Union[List[Dict], Dict]): Python List of Dictionaries (or maybe just a single Dictionary on error)
    """
    success: bool
    status_code: int
    message: str = ''
    data: Union[List[Dict], Dict] = field(default_factory=dict)


@dataclass
class FloweryAPIConfig:
    """Configuration for the Flowery API

    Attributes:
        user_agent (str): User-Agent string to use for the HTTP requests
        logger (Logger): Logger to use for logging messages
    """
    user_agent: str = f"PyFlowery/{VERSION}"
    logger: Logger = getLogger('pyflowery')
    allow_truncation: bool = False
