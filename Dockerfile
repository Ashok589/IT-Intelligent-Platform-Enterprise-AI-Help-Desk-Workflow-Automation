# =========================================================
# ENTERPRISE IT INTELLIGENCE PLATFORM
# DOCKERFILE — PRODUCTION BUILD
# =========================================================
#
# Multi-stage build:
#   Stage 1: builder   — Install Python dependencies
#   Stage 2: runtime   — Lean production image
#
# Build:
#   docker build -t enterprise-it-platform .
#
# Run:
#   docker run -p 8501:8501 --env-file .env enterprise-it-platform
#
# =========================================================

# ---------------------------------------------------------
# Stage 1: Builder
# ---------------------------------------------------------

FROM python:3.11-slim AS builder

WORKDIR /build

# Install build tools for native extensions (ChromaDB, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        libffi-dev \
        libssl-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install all Python dependencies into a prefix directory
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------------------------------------------------------
# Stage 2: Runtime
# ---------------------------------------------------------

FROM python:3.11-slim AS runtime

LABEL maintainer="Enterprise IT Team"
LABEL version="1.0.0"
LABEL description="Enterprise IT Intelligence Platform — Hybrid RAG + Agentic AI"

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

WORKDIR /app

# Runtime-only system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY --chown=appuser:appuser . .

# Create data directories (will be volume-mounted in production)
RUN mkdir -p \
        DATA/incidents \
        DATA/audit \
        DATA/memory \
        DATA/escalations \
        DATA/it_sop \
        DATA/it_policies \
        DATA/technical_docs \
        DATA/incident_reports \
        vectorstore \
        logs \
    && chown -R appuser:appuser /app

# Streamlit config directory
RUN mkdir -p /home/appuser/.streamlit && chown -R appuser:appuser /home/appuser

# Create Streamlit config for production (theme + server settings)
RUN cat > /home/appuser/.streamlit/config.toml << 'EOF'
[server]
headless = true
address = "0.0.0.0"
port = 8501
runOnSave = false
fileWatcherType = "none"
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
base = "dark"
primaryColor = "#6366f1"
backgroundColor = "#0a0e1a"
secondaryBackgroundColor = "#111827"
textColor = "#f1f5f9"
font = "sans serif"

[logger]
level = "warning"
EOF

# Switch to non-root user
USER appuser

# Port exposed
EXPOSE 8501

# Health check — verifies Streamlit is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Entrypoint
CMD ["python", "startup.py", "--host", "0.0.0.0", "--port", "8501"]
