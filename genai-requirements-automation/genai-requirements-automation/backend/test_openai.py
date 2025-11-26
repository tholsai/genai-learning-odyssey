#!/usr/bin/env python3
"""Test OpenAI connection."""
import os
from openai import OpenAI
from core.config import settings

print(f"API Key loaded: {bool(settings.openai_api_key)}")
print(f"API Key starts with: {settings.openai_api_key[:10] if settings.openai_api_key else 'None'}...")
print(f"Model: {settings.openai_model}")
print(f"Base URL: {settings.openai_api_base}")

try:
    client = OpenAI(
        api_key=settings.openai_api_key,
        base_url=settings.openai_api_base
    )
    
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": "Hello, test message"}],
        max_tokens=10
    )
    
    print("✅ OpenAI connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI connection failed: {e}")