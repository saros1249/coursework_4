from .genres import api as genres_ns
from .director import api as directors_ns
from .movie import api as movies_ns

__all__ = [
    'genres_ns', 'directors_ns', 'movies_ns',
]
