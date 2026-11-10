@echo off
title Traffic Management System - Backend
echo Starting FastAPI Backend & SUMO Controller...
set PYTHONPATH=packages/shared;packages/adaptive-policy;packages/sumo-engine;packages/cv-pipeline;backend
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
