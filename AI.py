"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json


load_dotenv()
google = os.getenv("GOOGLE")
genai.configure(api_key=google)

def runAI():
  # Set up the model
  generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
  }

  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE"
    },
  ]

  model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  convo = model.start_chat(history=[
  ])

  convo.send_message("You are an event generator in a game called RogueAI, a game where the player's goal is to help an AI to take over. Your goal is to describe an event that happens that will cause the user to get a point to spend on his AI. Make it fun about a world event happening or something. Make sure to reply in a json with only the title and description. Make the description one pargraph. Make sure the event is AI related. However, be creative.")
  print(convo.last.text)

  #extract json
  try:
    json_data = json.loads(convo.last.text)
  except:
    new = convo.last.text.removeprefix("```json").removesuffix("```")
    try:
      json_data = json.loads(new)
    except:
      new = new.replace('"', '\\\"')
      json_data = json.loads(new)

  # extract title and description
  try:
    title = json_data["title"]
    description = json_data["description"]
  except:
    title = json_data["Title"]
    description = json_data["Description"]
  return title, description