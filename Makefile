.PHONY: help setup start stop restart logs logs-fe logs-all clean

# Default target
help:
	@echo ""
	@echo "  Article Reputation Analyzer"
	@echo ""
	@echo "  make setup       Copy .env.example to .env and build Docker images"
	@echo "  make start       Start all services (Ctrl+C to stop)"
	@echo "  make stop        Stop all services"
	@echo "  make restart     Restart all services"
	@echo "  make logs        Follow backend logs"
	@echo "  make logs-fe     Follow frontend logs"
	@echo "  make logs-all    Follow all logs"
	@echo "  make clean       Remove containers, volumes, and caches"
	@echo ""
	@echo "  Windows users: run the docker compose commands directly."
	@echo "  See README.md for the equivalent commands."
	@echo ""

setup:
	@test -f .env || (cp .env.example .env && echo "Created .env from .env.example — open it and add your OPENAI_API_KEY")
	@docker compose build

start:
	@echo ""
	@echo "  Starting services..."
	@echo "  Backend:  http://localhost:8000"
	@echo "  Frontend: http://localhost:3000"
	@echo "  API Docs: http://localhost:8000/docs"
	@echo ""
	@docker compose up

stop:
	@docker compose down

restart:
	@docker compose restart

logs:
	@docker compose logs -f backend

logs-fe:
	@docker compose logs -f frontend

logs-all:
	@docker compose logs -f

clean:
	@docker compose down -v --remove-orphans
	@docker system prune -f
