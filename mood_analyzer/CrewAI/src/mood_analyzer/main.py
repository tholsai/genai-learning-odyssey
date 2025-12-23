#!/usr/bin/env python
import warnings
import csv
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from mood_analyzer.crew import MoodAnalyzer

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# File path for mood analysis CSV
CSV_FILE_PATH = "output/mood_analysis.txt"

# Suppress specific warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_mood_analysis(mood_type: str, mood_description: str):
    """
    Read the CSV file and return the analysis for the given mood.
    """
    try:
        with open(CSV_FILE_PATH, 'r', encoding="utf-8") as file:
            reader = file.read()
            return reader
    except FileNotFoundError:
        return None
    return None

@app.get("/wellnessadvice", response_class=PlainTextResponse)
def run(mood_type: str, mood_description: str):
    """
    Main endpoint to run the mood analyzer and return results.
    """
    inputs = {
        "mood_type": mood_type,
        "mood_description": mood_description
    }

    try:
        # Run the MoodAnalyzer crew
        MoodAnalyzer().crew().kickoff(inputs=inputs)
    except Exception as e:
        return f"Error: An error occurred while running the crew: {e}"

    # Read and return CSV content
    content = get_mood_analysis(mood_type, mood_description)
    if content:
        return content
    else:
        return f"Error: Output file {CSV_FILE_PATH} not found or no matching entry."
