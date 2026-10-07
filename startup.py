#!/usr/bin/env python3
# =========================================================
# ENTERPRISE IT INTELLIGENCE PLATFORM
# PRODUCTION STARTUP SCRIPT
# =========================================================
#
# This script:
#   1. Validates environment variables
#   2. Ensures required directories exist
#   3. Checks vectorstore is initialized
#   4. Launches the Streamlit application
#
# Usage:
#   python startup.py
#   python startup.py --port 8501 --host 0.0.0.0
#
# =========================================================

import sys
import os
import argparse
import subprocess
import logging
from pathlib import Path

# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# =========================================================
# LOGGING SETUP
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("startup")

# =========================================================
# BANNER
# =========================================================

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║          ENTERPRISE IT INTELLIGENCE PLATFORM                 ║
║          Hybrid RAG  ·  Agentic AI  ·  LangGraph             ║
║          Version 1.0.0  —  Production Startup                ║
╚══════════════════════════════════════════════════════════════╝
"""

# =========================================================
# VALIDATION
# =========================================================

def validate_environment() -> bool:
    """Validate required environment variables and file system."""

    log.info("Validating environment...")
    errors = []
    warnings = []

    # Required: Google API key
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        errors.append(
            "❌  GOOGLE_API_KEY is not set. "
            "Add it to .env or export it in your shell."
        )
    else:
        log.info(f"✅  GOOGLE_API_KEY found (length: {len(api_key)})")

    # Vectorstore
    vectorstore_dir = PROJECT_ROOT / "vectorstore"
    if not vectorstore_dir.exists() or not any(vectorstore_dir.iterdir()):
        warnings.append(
            "⚠️   vectorstore/ is empty. "
            "Run: python scripts/ingest_documents.py"
        )
    else:
        log.info("✅  Vector store directory found")

    # Checkpoints DB (auto-created by LangGraph, warn if missing)
    db_path = PROJECT_ROOT / "enterprise_it_checkpoints.db"
    if not db_path.exists():
        log.info("ℹ️   Checkpoints DB will be created on first run")
    else:
        log.info(f"✅  Checkpoints DB found ({db_path.stat().st_size / 1024:.1f} KB)")

    # DATA directories
    for sub in ["incidents", "audit", "memory", "escalations", "it_sop", "it_policies"]:
        d = PROJECT_ROOT / "DATA" / sub
        d.mkdir(parents=True, exist_ok=True)
    log.info("✅  DATA directories ensured")

    # SRC package
    src_init = PROJECT_ROOT / "SRC" / "__init__.py"
    if not src_init.exists():
        errors.append("❌  SRC/__init__.py is missing")
    else:
        log.info("✅  SRC package found")

    # Print warnings (non-fatal)
    for w in warnings:
        log.warning(w)

    # Print errors (fatal)
    if errors:
        log.error("\n\nStartup validation failed:")
        for e in errors:
            log.error(f"  {e}")
        return False

    return True


# =========================================================
# STREAMLIT LAUNCHER
# =========================================================

def launch_streamlit(host: str, port: int, dev_mode: bool = False):
    """Launch the Streamlit application."""

    app_path = PROJECT_ROOT / "SRC" / "app.py"

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        "--server.address", host,
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
        "--theme.base", "dark",
        "--theme.primaryColor", "#6366f1",
        "--theme.backgroundColor", "#0a0e1a",
        "--theme.secondaryBackgroundColor", "#111827",
        "--theme.textColor", "#f1f5f9",
    ]

    if not dev_mode:
        cmd += [
            "--server.runOnSave", "false",
            "--logger.level", "warning",
        ]
    else:
        cmd += [
            "--server.runOnSave", "true",
            "--logger.level", "info",
        ]

    log.info(f"\n🚀  Launching Enterprise IT Intelligence Platform")
    log.info(f"   URL:  http://{host}:{port}")
    log.info(f"   App:  {app_path}")
    log.info(f"   Mode: {'development' if dev_mode else 'production'}\n")

    subprocess.run(cmd)


# =========================================================
# MAIN
# =========================================================

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="Enterprise IT Intelligence Platform — Production Startup"
    )
    parser.add_argument(
        "--host", default=os.getenv("APP_HOST", "0.0.0.0"),
        help="Host to bind Streamlit (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=int(os.getenv("APP_PORT", "8501")),
        help="Port to bind Streamlit (default: 8501)"
    )
    parser.add_argument(
        "--dev", action="store_true",
        help="Run in development mode (auto-reload on save)"
    )
    parser.add_argument(
        "--skip-validation", action="store_true",
        help="Skip startup validation checks"
    )
    args = parser.parse_args()

    # Load .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        log.info("✅  .env file loaded")
    except ImportError:
        log.warning("python-dotenv not installed — using system environment only")

    # Validate
    if not args.skip_validation:
        if not validate_environment():
            log.error("\n💥  Startup aborted due to validation errors.")
            sys.exit(1)

    log.info("\n✅  All checks passed. Starting application...\n")

    # Launch
    launch_streamlit(
        host=args.host,
        port=args.port,
        dev_mode=args.dev,
    )


if __name__ == "__main__":
    main()
