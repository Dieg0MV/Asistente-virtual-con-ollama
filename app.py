import json
from flask import Flask, render_template, request
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("recorder.html")

@app.route("/audio", methods=["POST"])
def audio():
    #Obtener audio grabado y transcribirlo
    audio = request.files.get("audio")
    text = Transcriber().transcrib(audio)
    
    #Utilizar el LLM para ver si llamar una funcion
    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:
        #Si se desea llamar una funcion de las que tenemos
        if function_name == "get_weather":
            #Llamar a la funcion del clima
            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")
            
            final_response = llm.process_response(text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "send_email":
            #Llamar a la funcion para enviar un correo
            final_response = "Tu que estas leyendo el codigo, implementame y envia correos muahaha"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + args["website"]
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
        
        elif function_name == "dominate_human_race":
            final_response = "No te creas. Suscríbete al canal!"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}
    else:
        final_response = "No tengo idea de lo que estás hablando, Ringa Tech"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}