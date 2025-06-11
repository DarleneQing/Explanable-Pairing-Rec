from fastapi import APIRouter, HTTPException, Depends
from .service import Service
from .models import Item, Session, RecItem
from .dependencies import get_service
from typing import List, Dict, Any

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/health")
async def health_check():
    """Simple health check that doesn't depend on repository"""
    return {"status": "ok", "message": "Server is responsive"}

@router.get("/api/test")
async def test_endpoint():
    return {"status": "success", "message": "Backend is connected!"}

@router.post("/session", response_model=Session)
async def create_session(service: Service = Depends(get_service)):
    """Create a new user session"""
    try:
        session = service.create_session()
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

@router.get("/session/{session_id}", response_model=Session)
async def get_session(session_id: str, service: Service = Depends(get_service)):
    """Get a session by ID"""
    session = service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/session/{session_id}")
async def delete_session(session_id: str, service: Service = Depends(get_service)):
    """Delete a session"""
    success = service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}

@router.get("/item/{article_id}", response_model=Item)
async def get_item_metadata(article_id: str, service: Service = Depends(get_service)):
    """Get item metadata by article ID"""
    try:
        item = service.get_item_metadata(int(article_id))
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/session/{session_id}/query-item/{article_id}")
async def set_query_item(session_id: str, article_id: str, service: Service = Depends(get_service)):
    """Set the query item for a session"""
    try:
        success = service.set_query_item(session_id, int(article_id))
        if not success:
            raise HTTPException(status_code=404, detail="Session not found or item not found")
        return {"message": "Query item set successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid article ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/session/{session_id}/query-item", response_model=Item)
async def get_query_item(session_id: str, service: Service = Depends(get_service)):
    """Get the query item for a session"""
    query_item = service.get_query_item(session_id)
    if query_item is None:
        raise HTTPException(status_code=404, detail="Query item not found for this session")
    return query_item

@router.get("/session/{session_id}/recommendations", response_model=List[RecItem])
async def get_recommendations(session_id: str, service: Service = Depends(get_service)):
    """Get recommendations for a session"""
    try:
        recommendations = service.get_recommendations(session_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/session/{session_id}", response_model=Session)
async def update_session(session_id: str, update_data: Dict[str, Any], service: Service = Depends(get_service)):
    """Update a session with new data"""
    try:
        session = service.update_session(session_id, update_data)
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update session: {str(e)}")