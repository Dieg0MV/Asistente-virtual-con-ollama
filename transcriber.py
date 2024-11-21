import whisper

class Transcriber:
    def __init__(self):
        pass
        
    #Siempre guarda y lee del archivo audio.mp3
    #Utiliza whisper en de manera local
    def transcrib(self, audio):
        
        modelo = whisper.load_model("base")
        audio.save("audio.wav")
        audio_file= "./audio.wav"
        
        transcript = modelo.transcribe(audio_file, fp16=False)
        return transcript["text"]

