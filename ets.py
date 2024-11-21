import os

file_path = "C:/Users/diego/OneDrive/Escritorio/carpetas/ModelsAI/audio.mp3"
if os.path.exists(file_path):
    print("Archivo encontrado")
else:
    print("Archivo no encontrado")