# pocketgroq/__init__.py

from .groq_provider import GroqProvider
from .exceptions import GroqAPIKeyMissingError, GroqAPIError
from .config import get_api_key

__all__ = ['GroqProvider', 'GroqAPIKeyMissingError', 'GroqAPIError', 'get_api_key']

# Import ChainOfThoughtManager and LLMInterface only if they're used directly from pocketgroq
# Otherwise, they can be imported from pocketgroq.chain_of_thought
from .chain_of_thought import ChainOfThoughtManager, LLMInterface
__all__ += ['ChainOfThoughtManager', 'LLMInterface']    