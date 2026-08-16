# SHMRY AI Models Downloader - PowerShell Version
# Downloads latest open-source AI models for reliable SHMRY search

Write-Host "========================================" -ForegroundColor Green
Write-Host "SHMRY AI Models Downloader" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if Ollama is installed
try {
    $ollamaVersion = ollama --version
    Write-Host "✅ Ollama is installed: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama is not installed. Installing..." -ForegroundColor Red
    Write-Host "Downloading Ollama installer..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://ollama.ai/download/ollama-windows-amd64.exe" -OutFile "ollama-installer.exe"
    Write-Host "Please run ollama-installer.exe as administrator" -ForegroundColor Yellow
    Read-Host "Press Enter to continue after installation"
}

Write-Host ""
Write-Host "Starting model downloads..." -ForegroundColor Cyan
Write-Host ""

# Create models directory
if (!(Test-Path "models")) {
    New-Item -ItemType Directory -Name "models"
}
Set-Location "models"

Write-Host "========================================" -ForegroundColor Green
Write-Host "Downloading Latest AI Models" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Function to download models with error handling
function Download-Model {
    param($ModelName, $Description)
    Write-Host "[$Description] Downloading $ModelName..." -ForegroundColor Yellow
    try {
        ollama pull $ModelName
        Write-Host "✅ $ModelName downloaded successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to download $ModelName: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# GPT Models
Write-Host "1 of 20 - GPT Models" -ForegroundColor Cyan
Download-Model "gpt4all:latest" "GPT4All Latest"
Download-Model "gpt4all:jina" "GPT4All Jina"
Download-Model "gpt4all:mistral" "GPT4All Mistral"

# Grok Models
Write-Host "2/20 - Grok Models" -ForegroundColor Cyan
Download-Model "grok:latest" "Grok Latest"
Download-Model "grok:open" "Grok Open"

# Llama Models
Write-Host "3/20 - Llama Models" -ForegroundColor Cyan
Download-Model "llama2:latest" "Llama2 Latest"
Download-Model "llama2:7b" "Llama2 7B"
Download-Model "llama2:13b" "Llama2 13B"
Download-Model "llama2:70b" "Llama2 70B"
Download-Model "llama2:7b-chat" "Llama2 7B Chat"
Download-Model "llama2:13b-chat" "Llama2 13B Chat"
Download-Model "llama2:70b-chat" "Llama2 70B Chat"

# DeepSeek Models
Write-Host "4/20 - DeepSeek Models" -ForegroundColor Cyan
Download-Model "deepseek:latest" "DeepSeek Latest"
Download-Model "deepseek:7b" "DeepSeek 7B"
Download-Model "deepseek:67b" "DeepSeek 67B"
Download-Model "deepseek-coder:latest" "DeepSeek Coder Latest"
Download-Model "deepseek-coder:6.7b" "DeepSeek Coder 6.7B"
Download-Model "deepseek-coder:33b" "DeepSeek Coder 33B"

# Mistral Models
Write-Host "5/20 - Mistral Models" -ForegroundColor Cyan
Download-Model "mistral:latest" "Mistral Latest"
Download-Model "mistral:7b" "Mistral 7B"
Download-Model "mistral:7b-instruct" "Mistral 7B Instruct"
Download-Model "mistral:7b-v0.1" "Mistral 7B v0.1"
Download-Model "mistral:7b-instruct-v0.1" "Mistral 7B Instruct v0.1"

# Qwen Models
Write-Host "6/20 - Qwen Models" -ForegroundColor Cyan
Download-Model "qwen:latest" "Qwen Latest"
Download-Model "qwen:7b" "Qwen 7B"
Download-Model "qwen:14b" "Qwen 14B"
Download-Model "qwen:72b" "Qwen 72B"
Download-Model "qwen:7b-chat" "Qwen 7B Chat"
Download-Model "qwen:14b-chat" "Qwen 14B Chat"
Download-Model "qwen:72b-chat" "Qwen 72B Chat"

# Claude Models
Write-Host "7/20 - Claude Models" -ForegroundColor Cyan
Download-Model "claude:latest" "Claude Latest"
Download-Model "claude:3-sonnet" "Claude 3 Sonnet"
Download-Model "claude:3-haiku" "Claude 3 Haiku"
Download-Model "claude:3-opus" "Claude 3 Opus"

# GitHub Copilot Models
Write-Host "8/20 - GitHub Copilot Models" -ForegroundColor Cyan
Download-Model "codellama:latest" "CodeLlama Latest"
Download-Model "codellama:7b" "CodeLlama 7B"
Download-Model "codellama:13b" "CodeLlama 13B"
Download-Model "codellama:34b" "CodeLlama 34B"
Download-Model "codellama:7b-instruct" "CodeLlama 7B Instruct"
Download-Model "codellama:13b-instruct" "CodeLlama 13B Instruct"
Download-Model "codellama:34b-instruct" "CodeLlama 34B Instruct"

# Gemini Models
Write-Host "9/20 - Gemini Models" -ForegroundColor Cyan
Download-Model "gemma:latest" "Gemma Latest"
Download-Model "gemma:2b" "Gemma 2B"
Download-Model "gemma:7b" "Gemma 7B"
Download-Model "gemma:2b-it" "Gemma 2B Instruct"
Download-Model "gemma:7b-it" "Gemma 7B Instruct"

# Hunyuan Models
Write-Host "10/20 - Hunyuan Models" -ForegroundColor Cyan
Download-Model "hunyuan:latest" "Hunyuan Latest"
Download-Model "hunyuan:7b" "Hunyuan 7B"
Download-Model "hunyuan:13b" "Hunyuan 13B"

# Ernie Models
Write-Host "11/20 - Ernie Models" -ForegroundColor Cyan
Download-Model "ernie:latest" "Ernie Latest"
Download-Model "ernie:3.5" "Ernie 3.5"
Download-Model "ernie:4.0" "Ernie 4.0"

# Sensenova Models
Write-Host "12/20 - Sensenova Models" -ForegroundColor Cyan
Download-Model "sensenova:latest" "Sensenova Latest"
Download-Model "sensenova:7b" "Sensenova 7B"
Download-Model "sensenova:13b" "Sensenova 13B"

# Spark Models
Write-Host "13/20 - Spark Models" -ForegroundColor Cyan
Download-Model "spark:latest" "Spark Latest"
Download-Model "spark:7b" "Spark 7B"
Download-Model "spark:13b" "Spark 13B"

# BLOOM Models
Write-Host "14/20 - BLOOM Models" -ForegroundColor Cyan
Download-Model "bloom:latest" "BLOOM Latest"
Download-Model "bloom:7b1" "BLOOM 7B1"
Download-Model "bloom:176b" "BLOOM 176B"

# Stable Diffusion Models
Write-Host "15/20 - Stable Diffusion Models" -ForegroundColor Cyan
Download-Model "stable-diffusion:latest" "Stable Diffusion Latest"
Download-Model "stable-diffusion:2.1" "Stable Diffusion 2.1"
Download-Model "stable-diffusion:xl" "Stable Diffusion XL"

# Falcon Models
Write-Host "16/20 - Falcon Models" -ForegroundColor Cyan
Download-Model "falcon:latest" "Falcon Latest"
Download-Model "falcon:7b" "Falcon 7B"
Download-Model "falcon:40b" "Falcon 40B"
Download-Model "falcon:7b-instruct" "Falcon 7B Instruct"
Download-Model "falcon:40b-instruct" "Falcon 40B Instruct"

# GPT-NeoX Models
Write-Host "17/20 - GPT-NeoX Models" -ForegroundColor Cyan
Download-Model "gpt-neox:latest" "GPT-NeoX Latest"
Download-Model "gpt-neox:20b" "GPT-NeoX 20B"

# Kimi Models
Write-Host "18/20 - Kimi Models" -ForegroundColor Cyan
Download-Model "kimi:latest" "Kimi Latest"
Download-Model "kimi:7b" "Kimi 7B"
Download-Model "kimi:13b" "Kimi 13B"

# Whisper Models
Write-Host "19/20 - Whisper Models" -ForegroundColor Cyan
Download-Model "whisper:latest" "Whisper Latest"
Download-Model "whisper:base" "Whisper Base"
Download-Model "whisper:small" "Whisper Small"
Download-Model "whisper:medium" "Whisper Medium"
Download-Model "whisper:large" "Whisper Large"

# Additional Top Models
Write-Host "20/20 - Additional Top Models" -ForegroundColor Cyan
Download-Model "phi:latest" "Phi Latest"
Download-Model "phi:2.7b" "Phi 2.7B"
Download-Model "phi:3.5" "Phi 3.5"
Download-Model "phi:3.8b" "Phi 3.8B"
Download-Model "phi:3.8b-instruct" "Phi 3.8B Instruct"

Download-Model "neural-chat:latest" "Neural Chat Latest"
Download-Model "neural-chat:7b" "Neural Chat 7B"
Download-Model "neural-chat:13b" "Neural Chat 13B"

Download-Model "openchat:latest" "OpenChat Latest"
Download-Model "openchat:3.5" "OpenChat 3.5"
Download-Model "openchat:3.5-0106" "OpenChat 3.5-0106"

Download-Model "solar:latest" "Solar Latest"
Download-Model "solar:10.7b" "Solar 10.7B"
Download-Model "solar:10.7b-instruct" "Solar 10.7B Instruct"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Model Download Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Available models:" -ForegroundColor Cyan
ollama list

Write-Host ""
Write-Host "To use a specific model for SHMRY search:" -ForegroundColor Yellow
Write-Host "ollama run [model-name] 'Your search query'" -ForegroundColor White
Write-Host ""
Write-Host "Example: ollama run llama2:7b-chat 'What is SHMRY platform?'" -ForegroundColor White
Write-Host ""

# Test a model
Write-Host "Testing a model..." -ForegroundColor Cyan
try {
    $testResult = ollama run llama2:7b-chat "What is SHMRY platform?" 2>&1
    Write-Host "Test result: $testResult" -ForegroundColor Green
} catch {
    Write-Host "Test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "Press Enter to continue"
