#!/usr/bin/env python3
# =========================================================
# ENTERPRISE IT INTELLIGENCE PLATFORM
# ROOT ENTRY POINT — for Streamlit Cloud / local startup
# =========================================================
#
# This file is the main entry point for:
#   1. Streamlit Community Cloud  (set Main file path = streamlit_app.py)
#   2. Local run: python startup.py (which calls SRC/app.py)
#
# When deployed on Streamlit Cloud, this re-routes to SRC/app.py
# =========================================================

import sys
import runpy
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Run the main Streamlit application
runpy.run_path(str(PROJECT_ROOT / "SRC" / "app.py"), run_name="__main__")
