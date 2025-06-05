from functools import lru_cache
from fastapi import Depends
from .repository import Repository
from .service import Service

@lru_cache()
def get_repository() -> Repository:
    """
    Create a singleton repository instance.
    Uses lru_cache to ensure only one instance is created per application lifecycle.
    """
    return Repository()

def get_service(repository: Repository = Depends(get_repository)) -> Service:
    """
    Create a service instance with dependency injection.
    """
    return Service(repository) 