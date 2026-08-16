# Shmry AI Setup Guide

## Prerequisites
- Ollama installed on your computer
- Internet connection for model downloads

## Step 1: Install Ollama (if not already installed)

### Windows
```bash
winget install Ollama.Ollama
```

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Step 2: Start Shmry AI Service

```bash
# Start Ollama (it will run on http://localhost:11434)
ollama serve
```

## Step 3: Download Base Model

```bash
# Download a base model (llama3.2 is recommended)
ollama pull llama3.2
```

## Step 4: Create Custom Shmry Model

```bash
# Create a Modelfile for the Shmry model
echo FROM llama3.2 > Modelfile
echo SYSTEM "You are Shmry, an advanced AI assistant specialized in edge computing, cloud services, and technical solutions. You provide helpful, accurate, and practical assistance to users." >> Modelfile
echo TEMPLATE "{{ .System }}" >> Modelfile
echo PARAMETER temperature 0.7 >> Modelfile
echo PARAMETER top_p 0.9 >> Modelfile

# Create the model
ollama create -f Modelfile badrpk/shmry

# Push to Ollama Hub (optional)
ollama push badrpk/shmry
```

## Alternative: Copy Existing Model

```bash
# If you prefer to copy an existing model
ollama cp llama3.2 badrpk/shmry
ollama push badrpk/shmry
```

## Step 5: Verify Installation

```bash
# List all models
ollama list

# Test the Shmry model
ollama run badrpk/shmry "Hello, I'm testing the Shmry AI model"
```

## Integration with Shmry Platform

The Shmry platform will automatically connect to your local Ollama instance at `http://localhost:11434`.

### Features Available:
1. AI-powered search and assistance
2. Code generation and review
3. Documentation generation
4. Performance optimization
5. Debugging help

## Troubleshooting

### Common Issues:
1. **Connection Failed**: Ensure Ollama is running: `ollama serve`
2. **Model Not Found**: Check available models: `ollama list`
3. **Model Errors**: Remove and recreate model if needed: `ollama rm badrpk/shmry`
4. **Service Issues**: Check Ollama logs for errors

### Performance Tips:
- Use SSD storage for faster model loading
- Ensure sufficient RAM (8GB+ recommended)
- Close unnecessary applications during model operations

## Security & Privacy

- Ollama runs locally on your machine for privacy
- No data is sent to external servers
- Models are stored locally
- API key authentication for Shmry integration

## Support

1. Check Ollama documentation: https://ollama.ai/docs
2. Verify Shmry platform connection
3. Test with simple queries first
4. Monitor system resources during operation
