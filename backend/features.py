from playsound import playsound

# Assistant Sound Playing function
def playAssistantSound():
    music_dir = "./frontend/assets/audio/start_sound.mp3"
    try:
        playsound(music_dir)
    except Exception as e:
        print(f"Error playing sound: {e}")