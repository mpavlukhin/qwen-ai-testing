"""
API routes for history management.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from app.api.database import (
    save_calculation,
    get_history,
    clear_history,
    get_history_stats
)


router = APIRouter(prefix="/api/history", tags=["history"])


class HistoryResponse(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    total: int


@router.get("")
def get_calculation_history(
    calculator_type: Optional[str] = Query(None, description="Filter by calculator type"),
    limit: int = Query(50, ge=1, le=200, description="Number of records"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
) -> Dict[str, Any]:
    """Get calculation history with optional filtering and pagination."""
    try:
        history = get_history(calculator_type, limit, offset)
        stats = get_history_stats()
        
        return {
            "success": True,
            "data": history,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": stats["total_calculations"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_statistics() -> Dict[str, Any]:
    """Get calculation history statistics."""
    try:
        stats = get_history_stats()
        return {"success": True, **stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("")
def delete_history(
    calculator_type: Optional[str] = Query(None, description="Clear specific type or all if not provided")
) -> Dict[str, Any]:
    """Clear calculation history."""
    try:
        deleted_count = clear_history(calculator_type)
        return {
            "success": True,
            "message": f"Deleted {deleted_count} records",
            "deleted_count": deleted_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Helper function to save calculations from other routes
def log_calculation(
    calculator_type: str,
    operation: str,
    input_data: Dict[str, Any],
    result_data: Dict[str, Any]
) -> Optional[int]:
    """Log a calculation to history. Returns record ID or None on failure."""
    try:
        return save_calculation(calculator_type, operation, input_data, result_data)
    except Exception:
        # Don't fail the main operation if logging fails
        return None
