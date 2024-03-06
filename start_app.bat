@echo off
docker-compose up -d
timeout /t 3
start http://localhost:8000
