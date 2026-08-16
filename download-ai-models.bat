@echo off
echo ========================================
echo SHMRY AI Models Downloader
echo ========================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Ollama...
    powershell -Command "Invoke-WebRequest -Uri 'https://ollama.ai/download/ollama-windows-amd64.exe' -OutFile 'ollama-installer.exe'"
    echo Please run ollama-installer.exe as administrator
    pause
    exit /b 1
)

echo Ollama is installed. Starting model downloads...
echo.

REM Create models directory
if not exist "models" mkdir models
cd models

echo ========================================
echo Downloading Latest AI Models
echo ========================================
echo.

REM GPT Models
echo [1/20] Downloading GPT models...
ollama pull gpt4all:latest
ollama pull gpt4all:jina
ollama pull gpt4all:mistral

REM Grok Models
echo [2/20] Downloading Grok models...
ollama pull grok:latest
ollama pull grok:open

REM Llama Models
echo [3/20] Downloading Llama models...
ollama pull llama2:latest
ollama pull llama2:7b
ollama pull llama2:13b
ollama pull llama2:70b
ollama pull llama2:7b-chat
ollama pull llama2:13b-chat
ollama pull llama2:70b-chat

REM DeepSeek Models
echo [4/20] Downloading DeepSeek models...
ollama pull deepseek:latest
ollama pull deepseek:7b
ollama pull deepseek:67b
ollama pull deepseek-coder:latest
ollama pull deepseek-coder:6.7b
ollama pull deepseek-coder:33b

REM Mistral Models
echo [5/20] Downloading Mistral models...
ollama pull mistral:latest
ollama pull mistral:7b
ollama pull mistral:7b-instruct
ollama pull mistral:7b-v0.1
ollama pull mistral:7b-instruct-v0.1

REM Qwen Models
echo [6/20] Downloading Qwen models...
ollama pull qwen:latest
ollama pull qwen:7b
ollama pull qwen:14b
ollama pull qwen:72b
ollama pull qwen:7b-chat
ollama pull qwen:14b-chat
ollama pull qwen:72b-chat

REM Claude Models
echo [7/20] Downloading Claude models...
ollama pull claude:latest
ollama pull claude:3-sonnet
ollama pull claude:3-haiku
ollama pull claude:3-opus

REM GitHub Copilot Models
echo [8/20] Downloading GitHub Copilot models...
ollama pull codellama:latest
ollama pull codellama:7b
ollama pull codellama:13b
ollama pull codellama:34b
ollama pull codellama:7b-instruct
ollama pull codellama:13b-instruct
ollama pull codellama:34b-instruct

REM Gemini Models
echo [9/20] Downloading Gemini models...
ollama pull gemma:latest
ollama pull gemma:2b
ollama pull gemma:7b
ollama pull gemma:2b-it
ollama pull gemma:7b-it

REM Hunyuan Models
echo [10/20] Downloading Hunyuan models...
ollama pull hunyuan:latest
ollama pull hunyuan:7b
ollama pull hunyuan:13b

REM Ernie Models
echo [11/20] Downloading Ernie models...
ollama pull ernie:latest
ollama pull ernie:3.5
ollama pull ernie:4.0

REM Sensenova Models
echo [12/20] Downloading Sensenova models...
ollama pull sensenova:latest
ollama pull sensenova:7b
ollama pull sensenova:13b

REM Spark Models
echo [13/20] Downloading Spark models...
ollama pull spark:latest
ollama pull spark:7b
ollama pull spark:13b

REM BLOOM Models
echo [14/20] Downloading BLOOM models...
ollama pull bloom:latest
ollama pull bloom:7b1
ollama pull bloom:176b

REM Stable Diffusion Models
echo [15/20] Downloading Stable Diffusion models...
ollama pull stable-diffusion:latest
ollama pull stable-diffusion:2.1
ollama pull stable-diffusion:xl

REM Falcon Models
echo [16/20] Downloading Falcon models...
ollama pull falcon:latest
ollama pull falcon:7b
ollama pull falcon:40b
ollama pull falcon:7b-instruct
ollama pull falcon:40b-instruct

REM GPT-NeoX Models
echo [17/20] Downloading GPT-NeoX models...
ollama pull gpt-neox:latest
ollama pull gpt-neox:20b

REM Kimi Models
echo [18/20] Downloading Kimi models...
ollama pull kimi:latest
ollama pull kimi:7b
ollama pull kimi:13b

REM Whisper Models
echo [19/20] Downloading Whisper models...
ollama pull whisper:latest
ollama pull whisper:base
ollama pull whisper:small
ollama pull whisper:medium
ollama pull whisper:large

REM Additional Top Models
echo [20/20] Downloading additional top models...
ollama pull phi:latest
ollama pull phi:2.7b
ollama pull phi:3.5
ollama pull phi:3.8b
ollama pull phi:3.8b-instruct

ollama pull neural-chat:latest
ollama pull neural-chat:7b
ollama pull neural-chat:13b

ollama pull openchat:latest
ollama pull openchat:3.5
ollama pull openchat:3.5-0106

ollama pull solar:latest
ollama pull solar:10.7b
ollama pull solar:10.7b-instruct

echo.
echo ========================================
echo Model Download Complete!
echo ========================================
echo.
echo Available models:
ollama list
echo.
echo To use a specific model for SHMRY search:
echo ollama run [model-name] "Your search query"
echo.
echo Example: ollama run llama2:7b-chat "What is SHMRY platform?"
echo.
pause
