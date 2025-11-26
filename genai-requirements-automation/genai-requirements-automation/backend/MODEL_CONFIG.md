# OpenAI GPT-5 nano Model Configuration

## Current Model
The application now uses **GPT-5 nano** via OpenAI's API.

## Setup

### 1. Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)

### 2. Configure Environment
Add to your `backend/.env` file:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5-nano
OPENAI_API_BASE=https://api.openai.com/v1
```

## Configuration Options

### Environment Variables
```env
# Required
OPENAI_API_KEY=sk-...

# Optional (defaults provided)
OPENAI_MODEL=gpt-5-nano
OPENAI_API_BASE=https://api.openai.com/v1
TEMPERATURE=0.7
MAX_TOKENS=4000
```

### Alternative Models
If GPT-5 nano is not available, you can use:
- `gpt-4-turbo`
- `gpt-4`
- `gpt-3.5-turbo`

Update the `OPENAI_MODEL` in your `.env` file.

## After Configuration

Restart the server for changes to take effect:
```bash
cd backend
uv run uvicorn app:app --reload
```

## Troubleshooting

### Invalid API Key
- Verify your API key is correct
- Check you have sufficient credits
- Ensure the key has proper permissions

### Model Not Found
- Verify the model name is correct
- Check if you have access to GPT-5 nano
- Try an alternative model like `gpt-4-turbo`

### Rate Limits
- OpenAI has rate limits based on your plan
- Consider upgrading your OpenAI plan if needed
- Implement retry logic for production use

## Advantages of GPT-5 nano

- **High Quality**: Latest OpenAI model with improved capabilities
- **Fast**: Optimized for speed and efficiency
- **Reliable**: Cloud-based with high availability
- **Scalable**: No local hardware requirements