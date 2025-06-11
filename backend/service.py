from .repository import Repository
from .models import Session, Item, RecItem
from typing import Optional, Dict, Any

class Service:
    def __init__(self, repository: Repository):
        self._repository = repository

    def create_session(self) -> Session:
        """Create a new user session"""
        return self._repository.create_session()
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID"""
        return self._repository.get_session(session_id)
    
    def update_session(self, session_id: str, update_data: Dict[str, Any]) -> Optional[Session]:
        """Update a session with new data"""
        session = self._repository.get_session(session_id)
        if session is None:
            return None
        
        # Update session fields
        for field, value in update_data.items():
            if hasattr(session, field) and value is not None:
                setattr(session, field, value)
        
        # Save updated session
        self._repository.update_session(session)
        return session
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        return self._repository.delete_session(session_id)

    def get_item_metadata(self, article_id: int) -> Optional[Item]:
        """Get item metadata (no session required)"""
        return self._repository.get_metadata(article_id)
    
    def set_query_item(self, session_id: str, article_id: int) -> bool:
        """Set the query item for a session"""
        return self._repository.put_query_item(session_id, article_id)
    
    def get_query_item(self, session_id: str) -> Optional[Item]:
        """Get the query item for a session"""
        return self._repository.get_query_item(session_id)
    
    def get_recommendations(self, session_id: str) -> list[RecItem]:
        """Get recommendations for a session"""
        return self._repository.get_recommendations(session_id)
