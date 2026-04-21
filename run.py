#!/usr/bin/env python3
"""
Calculator Hub - Simple Launch Script
Run this file to start the application.

Usage:
    python run.py
"""

import sys
from pathlib import Path

# Add the workspace directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import main

if __name__ == "__main__":
    main()
