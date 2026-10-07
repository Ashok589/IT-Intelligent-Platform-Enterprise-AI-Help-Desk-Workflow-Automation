# =========================================================
# ENTERPRISE IT INTELLIGENCE PLATFORM
# DEVELOPER MAKEFILE
# =========================================================
#
# Usage:
#   make run          - Start the platform locally
#   make dev          - Start in dev mode (auto-reload)
#   make test         - Run all tests
#   make test-cov     - Run tests with HTML coverage report
#   make ingest       - Ingest documents into vector store
#   make docker-build - Build Docker image
#   make docker-run   - Run Docker container
#   make docker-stop  - Stop Docker container
#   make clean        - Remove cache files
#   make lint         - Run flake8 linter
#   make format       - Run black formatter
#
# =========================================================

.PHONY: run dev test test-cov ingest docker-build docker-run docker-stop clean lint format help

# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

APP_NAME    := enterprise-it-platform
APP_PORT    := 8501
DOCKER_TAG  := $(APP_NAME):latest
PYTHON      := python

# ---------------------------------------------------------
# LOCAL RUN
# ---------------------------------------------------------

run:
	@echo "🚀 Starting Enterprise IT Intelligence Platform..."
	$(PYTHON) startup.py

dev:
	@echo "🔧 Starting in development mode..."
	$(PYTHON) startup.py --dev

# ---------------------------------------------------------
# TESTS
# ---------------------------------------------------------

test:
	@echo "🧪 Running test suite..."
	$(PYTHON) -m pytest tests/ -v --tb=short

test-cov:
	@echo "📊 Running tests with coverage report..."
	$(PYTHON) -m pytest tests/ -v --cov=SRC --cov-report=html --cov-report=term-missing
	@echo "Coverage report: htmlcov/index.html"

test-quick:
	@echo "⚡ Running smoke tests only..."
	$(PYTHON) -m pytest tests/test_graph_smoke.py -v

# ---------------------------------------------------------
# DATA INGESTION
# ---------------------------------------------------------

ingest:
	@echo "📥 Ingesting documents into vector store..."
	$(PYTHON) scripts/ingest_documents.py

ingest-force:
	@echo "📥 Force re-ingesting all documents..."
	$(PYTHON) scripts/ingest_documents.py --force

# ---------------------------------------------------------
# DOCKER
# ---------------------------------------------------------

docker-build:
	@echo "🐳 Building Docker image: $(DOCKER_TAG)..."
	docker build -t $(DOCKER_TAG) .
	@echo "✅ Image built: $(DOCKER_TAG)"

docker-run:
	@echo "🐳 Running Docker container on port $(APP_PORT)..."
	docker run -d \
		--name $(APP_NAME) \
		-p $(APP_PORT):8501 \
		--env-file .env \
		-v $(PWD)/DATA:/app/DATA \
		-v $(PWD)/vectorstore:/app/vectorstore \
		-v $(PWD)/enterprise_it_checkpoints.db:/app/enterprise_it_checkpoints.db \
		$(DOCKER_TAG)
	@echo "✅ Container started. Visit: http://localhost:$(APP_PORT)"

docker-compose-up:
	@echo "🐳 Starting with Docker Compose..."
	docker-compose up -d
	@echo "✅ Services started. Visit: http://localhost:$(APP_PORT)"

docker-compose-down:
	@echo "🐳 Stopping Docker Compose services..."
	docker-compose down

docker-stop:
	@echo "🐳 Stopping container: $(APP_NAME)..."
	docker stop $(APP_NAME) || true
	docker rm $(APP_NAME) || true

docker-logs:
	docker logs -f $(APP_NAME)

# ---------------------------------------------------------
# CODE QUALITY
# ---------------------------------------------------------

lint:
	@echo "🔍 Running flake8 linter..."
	$(PYTHON) -m flake8 SRC/ --max-line-length=120 --ignore=E501,W503

format:
	@echo "✨ Formatting with black..."
	$(PYTHON) -m black SRC/ scripts/ tests/ --line-length=100

format-check:
	@echo "✨ Checking formatting..."
	$(PYTHON) -m black SRC/ scripts/ tests/ --check --line-length=100

# ---------------------------------------------------------
# CLEAN
# ---------------------------------------------------------

clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "✅ Clean complete"

# ---------------------------------------------------------
# HELP
# ---------------------------------------------------------

help:
	@echo ""
	@echo "Enterprise IT Intelligence Platform — Make Commands"
	@echo "===================================================="
	@echo ""
	@echo "  make run           - Start platform (production)"
	@echo "  make dev           - Start platform (development, auto-reload)"
	@echo "  make test          - Run all unit tests"
	@echo "  make test-cov      - Run tests with HTML coverage"
	@echo "  make ingest        - Ingest documents into vector store"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run containerized application"
	@echo "  make docker-compose-up  - Start full stack (compose)"
	@echo "  make lint          - Run flake8 linter"
	@echo "  make format        - Auto-format with black"
	@echo "  make clean         - Remove cache/build files"
	@echo ""
