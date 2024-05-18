# AI counter app from my talk at PyCon US 2024

This little macOS app listens through the microphone and increments a visible counter any time anyone says "AI" or "Artificial Intelligence".

You need to download and extract the model file from here: https://alphacephei.com/vosk/models

Get the `vosk-model-en-us-0.22-lgraph` 128MB zip file and uncompress it. You need to have that `vosk-model-en-us-0.22-lgraph` folder in the same folder as `counter.py`

Then:
```bash
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python counter.py
```

