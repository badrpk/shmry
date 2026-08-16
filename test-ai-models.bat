@echo off
echo ========================================
echo SHMRY AI Models Test
echo ========================================
echo.

echo Testing available AI models...
echo.

REM Test Llama2
echo Testing Llama2 7B Chat...
ollama run llama2:7b-chat "What is SHMRY platform? Give a brief explanation."
echo.

REM Test Mistral
echo Testing Mistral 7B Instruct...
ollama run mistral:7b-instruct "Explain SHMRY platform in one sentence."
echo.

REM Test DeepSeek
echo Testing DeepSeek 7B...
ollama run deepseek:7b "What are the main features of SHMRY platform?"
echo.

REM Test CodeLlama
echo Testing CodeLlama 7B Instruct...
ollama run codellama:7b-instruct "Write a simple Python function to search SHMRY platform."
echo.

echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If all tests passed, SHMRY search should work!
echo.
pause
