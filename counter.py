import time
import tkinter as tk
from tkinter import font
import pyaudio
import re
import json
from vosk import Model, KaldiRecognizer

ai_pattern = re.compile(r'\b(ai|hey hi|a high|a i|artificial intelligence)\b', re.IGNORECASE)

def count_ai_or_variants(input_string):
    matches = ai_pattern.findall(input_string)
    return len(matches)


class CounterApp:
    def __init__(self, root):
        self.root = root
        self.counter = 0

        # Configure window
        self.root.overrideredirect(True)

        window_width = 200
        window_height = 100
        screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()

        # Calculate position x, y
        x = screen_width - window_width
        y = 0

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.attributes("-topmost", True)
\
        # Font configuration
        self.custom_font = font.Font(size=48, weight='bold')

        # Label to display counter
        self.label = tk.Label(self.root, text=str(self.counter), font=self.custom_font)
        self.label.pack(expand=True)

    def update_counter(self, increment=1):
        self.counter += increment
        self.label.config(text=str(self.counter))


def listen_with_retry(app):
    while True:
        try:
            done = listen_for_ai(app)
            if done is stopped:
                 return
        except:
            time.sleep(0.2)


stopped = object()


def listen_for_ai(app):
    model_path = "vosk-model-en-us-0.22-lgraph"
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()

    try:
        while True:
            data = stream.read(4096)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print(result)
                counts = count_ai_or_variants(result.get('text', ''))
                if counts:
                    app.update_counter(counts)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
    return stopped

if __name__ == "__main__":
    root = tk.Tk()
    app = CounterApp(root)

    import threading
    listener_thread = threading.Thread(target=listen_with_retry, args=(app,))
    listener_thread.daemon = True
    listener_thread.start()

    root.mainloop()


