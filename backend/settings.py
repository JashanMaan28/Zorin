import eel
import os
from dotenv import load_dotenv, set_key
import json

# Load environment variables
load_dotenv()

@eel.expose
def get_env_settings():
    """Get current environment settings"""
    return {
        "COHERE_API_KEY": os.getenv("COHERE_API_KEY", ""),
        "GroqAPIKey": os.getenv("GroqAPIKey", ""),
        "HuggingFaceAPIKey": os.getenv("HuggingFaceAPIKey", ""),
        "pvporcupine_ACCESS_KEY": os.getenv("pvporcupine_ACCESS_KEY", ""),
        "Model": os.getenv("Model", "llama3-70b-8192"),
        "Username": os.getenv("Username", "")
    }

@eel.expose
def save_env_settings(settings):
    """Save settings to .env file"""
    try:
        env_path = ".env"
        
        # Create the file if it doesn't exist
        if not os.path.exists(env_path):
            open(env_path, 'w').close()
            
        # Update each key in the .env file
        for key, value in settings.items():
            set_key(env_path, key, value)
            
        return {"success": True, "message": "Settings saved successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}