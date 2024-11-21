import os
import json
import ollama


class LLM():
    def __init__(self):
        pass
    def process_functions(self, text):
       
        response = ollama.chat(

            model="llama3.2:latest",
            messages=[
                    #Parametros del modelo
                    {"role": "system", "content": "Eres un asistente experto en marketing digital"},
                    {"role": "user", "content": text},
            ], 
        )
        
        message = response["choices"][0]["message"]
        
        #Aqui si la IA quiere ejecutar alguna funcion 
        if message.get("function_call"):
            #Sip
            function_name = message["function_call"]["name"] #Que funcion?
            args = message.to_dict()['function_call']['arguments'] #Con que datos?
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message
    
    #Una vez que llamamos a la funcion (e.g. obtener clima, encender luz, etc)
    #Podemos llamar a esta funcion con el msj original, la funcion llamada y su
    #respuesta, para obtener una respuesta en lenguaje natural (en caso que la
    #respuesta haya sido JSON por ejemplo
    def process_response(self, text, message, function_name, function_response):
        
        response = ollama.chat(
            model="llama3.2:latest",
            messages=[
                #Aqui tambien puedes cambiar como se comporta
                {"role": "system", "content": "Eres un asistente malhablado"},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response["choices"][0]["message"]["content"]