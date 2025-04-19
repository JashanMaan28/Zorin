import pyaudio
import numpy as np
import time

def measure_mic_levels(duration=3):
    pa = pyaudio.PyAudio()
    best_device = None
    highest_volume = 0

    print("🎧 Testing available input devices...\n")

    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"🔍 Testing device {i}: {info['name']}")

            try:
                stream = pa.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    input_device_index=i,
                    frames_per_buffer=1024
                )

                frames = []
                start_time = time.time()

                while time.time() - start_time < duration:
                    data = stream.read(1024, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    volume = np.abs(audio_data).mean()
                    frames.append(volume)

                stream.stop_stream()
                stream.close()

                avg_volume = np.mean(frames)
                print(f"   ➡️ Avg Volume: {avg_volume:.2f}\n")

                if avg_volume > highest_volume:
                    highest_volume = avg_volume
                    best_device = {
                        "index": i,
                        "name": info["name"],
                        "volume": avg_volume
                    }

            except Exception as e:
                print(f"   ❌ Could not record from device {i}: {e}\n")

    pa.terminate()

    if best_device:
        print("🎤 Best Microphone Found:")
        print(f"   ✅ Device Index {best_device['index']}: {best_device['name']}")
        print(f"   🔊 Average Volume: {best_device['volume']:.2f}")
    else:
        print("❗No working input devices were found.")

if __name__ == "__main__":
    measure_mic_levels()
