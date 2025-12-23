#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from mood_analyzer.crew import MoodAnalyzer

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Query, HTTPException
import csv

app = FastAPI()

CSV_FILE_PATH = "output/mood_analysis.csv"

def get_mood_analysis(mood_type: str, mood_description: str):
    """
    Get the mood analysis from the CSV file.
    """
    with open(CSV_FILE_PATH, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == mood_type and row[1] == mood_description:
                return row[2]

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'mood_type': 'Depression',
        'mood_description': 'I feel like I am not good enough and I am not able to do anything right',
    }
    
    try:
        MoodAnalyzer().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


