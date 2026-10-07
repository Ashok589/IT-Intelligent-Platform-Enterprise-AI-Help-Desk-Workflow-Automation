# =========================================================
# ENTERPRISE IT INTELLIGENCE PLATFORM
# CENTRALIZED CONFIGURATION
# =========================================================
#
# All runtime settings are controlled here.
# Override via environment variables or .env file.
#
# Usage:
#   from config import settings
#   print(settings.APP_PORT)
#
# =========================================================

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# =========================================================
# CONFIGURATION CLASS
# =========================================================

class Settings:
    """
    Centralized platform settings.

    All values can be overridden via environment variables.
    """

    # -------------------------------------------------
    # APPLICATION
    # -------------------------------------------------

    APP_NAME: str            = "Enterprise IT Intelligence Platform"
    APP_VERSION: str         = "1.0.0"
    APP_PORT: int            = int(os.getenv("APP_PORT", "8501"))
    APP_HOST: str            = os.getenv("APP_HOST", "0.0.0.0")
    APP_ENV: str             = os.getenv("APP_ENV", "production")   # development | production
    DEBUG: bool              = os.getenv("DEBUG", "false").lower() == "true"

    # -------------------------------------------------
    # GOOGLE GEMINI LLM
    # -------------------------------------------------

    GOOGLE_API_KEY: str      = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str        = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.1"))

    # -------------------------------------------------
    # PATHS
    # -------------------------------------------------

    DATA_DIR: Path           = PROJECT_ROOT / "DATA"
    VECTORSTORE_DIR: Path    = PROJECT_ROOT / "vectorstore"
    CHECKPOINTS_DB: Path     = PROJECT_ROOT / "enterprise_it_checkpoints.db"
    LOGS_DIR: Path           = PROJECT_ROOT / "logs"

    # Sub-directories
    INCIDENTS_DIR: Path      = DATA_DIR / "incidents"
    AUDIT_DIR: Path          = DATA_DIR / "audit"
    MEMORY_DIR: Path         = DATA_DIR / "memory"
    ESCALATIONS_DIR: Path    = DATA_DIR / "escalations"
    IT_SOP_DIR: Path         = DATA_DIR / "it_sop"
    IT_POLICIES_DIR: Path    = DATA_DIR / "it_policies"
    TECHNICAL_DOCS_DIR: Path = DATA_DIR / "technical_docs"
    INCIDENT_REPORTS_DIR: Path = DATA_DIR / "incident_reports"

    # -------------------------------------------------
    # VECTOR STORE (CHROMA)
    # -------------------------------------------------

    CHROMA_COLLECTION_IT: str     = os.getenv("CHROMA_COLLECTION_IT", "it_knowledge")
    CHROMA_COLLECTION_POLICY: str = os.getenv("CHROMA_COLLECTION_POLICY", "policies")
    CHROMA_COLLECTION_INCIDENT: str = os.getenv("CHROMA_COLLECTION_INCIDENT", "incidents")

    EMBEDDING_MODEL: str     = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # -------------------------------------------------
    # HYBRID RAG
    # -------------------------------------------------

    TOP_K_DENSE: int         = int(os.getenv("TOP_K_DENSE", "5"))
    TOP_K_SPARSE: int        = int(os.getenv("TOP_K_SPARSE", "5"))
    TOP_K_RERANK: int        = int(os.getenv("TOP_K_RERANK", "3"))

    RERANKER_MODEL: str      = os.getenv(
        "RERANKER_MODEL",
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    # -------------------------------------------------
    # AGENT
    # -------------------------------------------------

    MAX_AGENT_ITERATIONS: int = int(os.getenv("MAX_AGENT_ITERATIONS", "5"))

    # -------------------------------------------------
    # INCIDENT MANAGEMENT
    # -------------------------------------------------

    # Severity SLA in hours
    SLA_P1_HOURS: int        = int(os.getenv("SLA_P1_HOURS", "1"))
    SLA_P2_HOURS: int        = int(os.getenv("SLA_P2_HOURS", "4"))
    SLA_P3_HOURS: int        = int(os.getenv("SLA_P3_HOURS", "24"))
    SLA_P4_HOURS: int        = int(os.getenv("SLA_P4_HOURS", "72"))

    # -------------------------------------------------
    # SECURITY (future use)
    # -------------------------------------------------

    AUTH_ENABLED: bool       = os.getenv("AUTH_ENABLED", "false").lower() == "true"
    AUTH_SECRET_KEY: str     = os.getenv("AUTH_SECRET_KEY", "change-me-in-production")

    # -------------------------------------------------
    # LOGGING
    # -------------------------------------------------

    LOG_LEVEL: str           = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str          = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    def validate(self) -> list[str]:
        """
        Validate required settings.
        Returns a list of validation error messages.
        Empty list means all settings are valid.
        """
        errors = []

        if not self.GOOGLE_API_KEY:
            errors.append(
                "GOOGLE_API_KEY is not set. "
                "Add it to your .env file or environment."
            )

        if not self.VECTORSTORE_DIR.exists():
            errors.append(
                f"Vector store directory not found: {self.VECTORSTORE_DIR}. "
                "Run: python scripts/ingest_documents.py"
            )

        return errors

    def ensure_dirs(self):
        """Create all required data directories."""
        dirs = [
            self.DATA_DIR,
            self.INCIDENTS_DIR,
            self.AUDIT_DIR,
            self.MEMORY_DIR,
            self.ESCALATIONS_DIR,
            self.LOGS_DIR,
            self.VECTORSTORE_DIR,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def __repr__(self) -> str:
        return (
            f"Settings(env={self.APP_ENV}, "
            f"port={self.APP_PORT}, "
            f"model={self.GEMINI_MODEL}, "
            f"auth={self.AUTH_ENABLED})"
        )


# =========================================================
# SINGLETON
# =========================================================

settings = Settings()
