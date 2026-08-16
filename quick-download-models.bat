@echo off
echo ========================================
echo SHMRY Quick AI Models Downloader
echo ========================================
echo.

echo Starting download of essential models...
echo.

REM Download the most reliable models first
echo [1/5] Downloading Llama2 models...
ollama pull llama2:7b-chat
ollama pull llama2:13b-chat

echo [2/5] Downloading Mistral models...
ollama pull mistral:7b-instruct
ollama pull mistral:7b

echo [3/5] Downloading DeepSeek models...
ollama pull deepseek:7b
ollama pull deepseek-coder:6.7b

echo [4/5] Downloading CodeLlama models...
ollama pull codellama:7b-instruct
ollama pull codellama:13b-instruct

echo [5/5] Downloading Phi models...
ollama pull phi:3.5
ollama pull phi:3.8b-instruct

echo.
echo ========================================
echo Quick Download Complete!
echo ========================================
echo.
echo Available models:
ollama list
echo.
echo Testing a model...
ollama run llama2:7b-chat "What is SHMRY platform?"
echo.
pause
