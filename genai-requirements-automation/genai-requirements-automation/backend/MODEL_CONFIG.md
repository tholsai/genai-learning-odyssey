# Ollama/Mistral Model Configuration

## Current Model
The default model is now set to **`mistral`** running locally via Ollama.

## Setup

### 1. Install Ollama
Download and install Ollama from https://ollama.ai

### 2. Pull the Mistral Model
```bash
ollama pull mistral
```

### 3. Start Ollama (if not running as a service)
```bash
ollama serve
```

Ollama will run on `http://localhost:11434` by default.

## Configuration

### Option 1: Environment Variable (Recommended)
Add to your `backend/.env` file:
```env
OLLAMA_API_BASE=http://localhost:11434/v1
OLLAMA_MODEL=mistral
```

### Option 2: Edit Config File
Edit `backend/core/config.py`:
```python
ollama_api_base: str = "http://localhost:11434/v1"
ollama_model: str = "mistral"  # Change this value
```

## Available Models

You can use any model available in Ollama. Some popular alternatives:

1. **`mistral`** (Default)
   - Good balance of quality and speed
   - ~7B parameters
   - Fast inference

2. **`mistral:7b-instruct`**
   - Instruction-tuned version
   - Better for structured outputs

3. **`llama2`**
   - Alternative open-source model
   - Pull with: `ollama pull llama2`

4. **`codellama`**
   - Code-focused model
   - Good for technical documentation

5. **`mixtral`**
   - Mixture of experts model
   - Higher quality but slower

To use a different model:
```bash
# Pull the model
ollama pull <model-name>

# Update your .env file
OLLAMA_MODEL=<model-name>
```

## After Changing the Model

**Restart the server** for changes to take effect:
1. Stop the current server (Ctrl+C)
2. Start it again:
   ```bash
   cd backend
   uv run uvicorn app:app --reload
   ```

## Troubleshooting

### Model Not Found
1. Verify the model is downloaded: `ollama list`
2. If not found, pull it: `ollama pull <model-name>`
3. Check the model name matches exactly (case-sensitive)

### Connection Issues
1. Ensure Ollama is running: `ollama serve`
2. Test the connection: `curl http://localhost:11434/api/tags`
3. Check firewall settings if using a different host

### Performance
- Models run locally, so performance depends on your hardware
- GPU acceleration is recommended for faster inference
- Adjust `max_tokens` in config if responses are too long/short

## Advantages of Local Models

- **Privacy**: All data stays on your machine
- **No API costs**: Free to use
- **Offline**: Works without internet (after initial model download)
- **Customizable**: Can fine-tune models for your use case

## Cost Considerations

- **Free**: No API costs, runs on your hardware
- **Hardware**: Requires sufficient RAM/VRAM for the model
- **Mistral 7B**: Requires ~8GB RAM minimum, ~4GB VRAM recommended
