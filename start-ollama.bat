@echo off
echo Starting Shmry AI Platform...
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo Shmry AI is not installed. Installing Ollama now...
    winget install Ollama.Ollama
    if %errorlevel% neq 0 (
        echo Failed to install Ollama. Please install manually from https://ollama.ai
        pause
        exit /b 1
    )
    echo Ollama installed successfully!
)

REM Start Ollama service
echo Starting Shmry AI service...
start /B ollama serve

REM Wait a moment for Ollama to start
echo Waiting for Shmry AI to start...
timeout /t 5 /nobreak >nul

REM Check if Ollama is running
echo Checking Shmry AI connection...
curl -s http://localhost:11434/api/tags >nul 2>nul
if %errorlevel% neq 0 (
    echo Shmry AI is not responding. Please check if it's running.
    pause
    exit /b 1
)

echo Shmry AI is running successfully!

REM Check if the Shmry model exists
ollama list | findstr "badrpk/shmry" >nul
if %errorlevel% neq 0 (
    echo Shmry model not found. Creating it now...
    
    REM Pull base model if not available
    ollama list | findstr "llama3.2" >nul
    if %errorlevel% neq 0 (
        echo Pulling base model...
        ollama pull llama3.2
    )
    
    REM Create Modelfile
    echo FROM llama3.2 > Modelfile
    echo SYSTEM "You are Shmry, an advanced AI assistant specialized in edge computing, cloud services, and technical solutions. You provide helpful, accurate, and practical assistance to users." >> Modelfile
    echo TEMPLATE "{{ .System }}" >> Modelfile
    echo PARAMETER temperature 0.7 >> Modelfile
    echo PARAMETER top_p 0.9 >> Modelfile
    
    REM Create the model
    ollama create -f Modelfile badrpk/shmry
    
    echo Shmry model created successfully!
) else (
    echo Shmry model already exists!
)

echo.
echo Shmry AI is ready for use!
echo You can now use the Shmry platform with your local AI models.
pause
