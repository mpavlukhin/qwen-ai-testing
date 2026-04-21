"""
Database module for storing calculation history.
Uses SQLite for file-based storage.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


DB_PATH = Path(__file__).parent.parent.parent / "calculators.db"


def get_connection() -> sqlite3.Connection:
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            calculator_type TEXT NOT NULL,
            operation TEXT NOT NULL,
            input_data TEXT NOT NULL,
            result_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_calculator_type 
        ON calculation_history(calculator_type)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_created_at 
        ON calculation_history(created_at)
    """)
    
    conn.commit()
    conn.close()


def save_calculation(
    calculator_type: str,
    operation: str,
    input_data: Dict[str, Any],
    result_data: Dict[str, Any]
) -> int:
    """
    Save a calculation to history.
    
    Returns:
        The ID of the inserted record
    """
    import json
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO calculation_history 
        (calculator_type, operation, input_data, result_data)
        VALUES (?, ?, ?, ?)
    """, (
        calculator_type,
        operation,
        json.dumps(input_data),
        json.dumps(result_data)
    ))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return record_id


def get_history(
    calculator_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get calculation history.
    
    Args:
        calculator_type: Filter by calculator type (optional)
        limit: Maximum number of records to return
        offset: Number of records to skip
    
    Returns:
        List of calculation records
    """
    import json
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if calculator_type:
        cursor.execute("""
            SELECT id, calculator_type, operation, input_data, result_data, created_at
            FROM calculation_history
            WHERE calculator_type = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (calculator_type, limit, offset))
    else:
        cursor.execute("""
            SELECT id, calculator_type, operation, input_data, result_data, created_at
            FROM calculation_history
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row["id"],
            "calculator_type": row["calculator_type"],
            "operation": row["operation"],
            "input_data": json.loads(row["input_data"]),
            "result_data": json.loads(row["result_data"]),
            "created_at": row["created_at"]
        }
        for row in rows
    ]


def clear_history(calculator_type: Optional[str] = None) -> int:
    """
    Clear calculation history.
    
    Args:
        calculator_type: If provided, only clear history for this type
    
    Returns:
        Number of deleted records
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if calculator_type:
        cursor.execute("""
            DELETE FROM calculation_history
            WHERE calculator_type = ?
        """, (calculator_type,))
    else:
        cursor.execute("DELETE FROM calculation_history")
    
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    return deleted_count


def get_history_stats() -> Dict[str, Any]:
    """Get statistics about calculation history."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total count
    cursor.execute("SELECT COUNT(*) as total FROM calculation_history")
    total = cursor.fetchone()["total"]
    
    # Count by calculator type
    cursor.execute("""
        SELECT calculator_type, COUNT(*) as count
        FROM calculation_history
        GROUP BY calculator_type
        ORDER BY count DESC
    """)
    by_type = {row["calculator_type"]: row["count"] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        "total_calculations": total,
        "by_calculator_type": by_type
    }
