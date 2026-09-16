import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
import time
import sys
import subprocess

load_dotenv()

def ejecutar_pytest(ruta_test):
    comando = ["python", "-m", "pytest", ruta_test]
    try:
        env_actual = os.environ.copy()
        env_actual["PYTHONPATH"] = os.getcwd()
        resultado = subprocess.run(
            comando,
            capture_output=True, 
            text=True,
            env=env_actual           
        )
        tests_pasaron = (resultado.returncode == 0)
        return tests_pasaron, resultado.stdout, resultado.stderr
    except Exception as e:
        return False, "", f"Error crítico al ejecutar pytest: {e}"

def extraer_codigo_python(texto):
    lineas = texto.split('\n')
    codigo_limpio = []
    dentro_del_bloque = False

    for linea in lineas:
        if linea.strip().startswith("```python"):
            dentro_del_bloque = True
            continue
        elif linea.strip().startswith("```") and dentro_del_bloque:
            dentro_del_bloque = False
            continue
        if dentro_del_bloque:
            codigo_limpio.append(linea)

    if not codigo_limpio:
        return texto.strip()
    return '\n'.join(codigo_limpio)

def main(ruta_archivo, output_folder):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: No se encontró la variable GEMINI_API_KEY en el entorno.")
        sys.exit(1)
    os.makedirs(output_folder, exist_ok=True)
    print(f"Iniciando Agente de Testing Automático...")
    print(f"Ruta del archivo: {ruta_archivo}")
    print(f"Directorio de salida: {output_folder}")

    client = genai.Client()
    start_time = time.time()
    time_budget = 120  

    test_valido = False
    intentos = 0
    nombre_archivo_base = os.path.basename(ruta_archivo)
    nombre_clase = os.path.splitext(nombre_archivo_base)[0]
    ruta_archivo_temporal = os.path.join(output_folder, f"test_{nombre_clase}.py")

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo_fuente = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de código en {ruta_archivo}")
        sys.exit(1)
    

    while not test_valido:
        tiempo_restante = time_budget - (time.time() - start_time)
        if tiempo_restante < 10:
            break
            
        intentos += 1
        print(f"\n--- Iteración {intentos} --- (Tiempo restante: {tiempo_restante:.1f}s)")

        try:
            if intentos == 1:
                prompt = f"""
                        Eres un experto en testing en Python. Tu tarea es generar pruebas unitarias con pytest 
                        para el siguiente código fuente ubicado en: {ruta_archivo}.
                        
                        CÓDIGO FUENTE:
                        ```python
                        {codigo_fuente}
                        ```
                        
                        Responde SOLO con el código Python de las pruebas. No incluyas explicaciones.
                        """
            else:
                prompt = "Los tests anteriores fallaron con X error. Corrige el código y genera una nueva versión que pase todas las aserciones."
            chat = client.chats.create(model="gemini-3.1-flash-lite") 
            response = chat.send_message(prompt)
            codigo_generado_crudo = response.text
            print(f"Generado intento {intentos}...")
            print(f"Respuesta de prueba del modelo:\n--> {codigo_generado_crudo }\n")
            
            time.sleep(2) 
            if intentos >= 3:
                break

        except Exception as e:
            print(f"Error al comunicarse con la API de Gemini: {e}")
            sys.exit(1)
        
        codigo_limpio = extraer_codigo_python(codigo_generado_crudo)

        with open(ruta_archivo_temporal, "w", encoding="utf-8") as archivo:
            archivo.write(codigo_limpio)
        print(f"Ejecutando pruebas en {ruta_archivo_temporal}...")
        exito, stdout, stderr = ejecutar_pytest(ruta_archivo_temporal)

        if exito:
            print("¡Los tests pasaron la ejecución inicial!")
            test_valido = True 
        else:
            print("Los tests fallaron. Preparando el siguiente prompt...")
            prompt = f"""
                El código generado falló al ejecutarse con pytest. 
                Aquí está el error capturado:
                
                STDOUT:
                {stdout}
                
                STDERR:
                {stderr}
                
                Por favor, analiza el error, corrige el código y genera una nueva versión.
                """
            if intentos >= 3:
                print("Límite de intentos de prueba alcanzado.")
                break

   
    print(f"\nGeneración finalizada en {time.time() - start_time:.1f} segundos.")
    print(f"Exportando resultados finales en {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agente basado en LLM para generación iterativa de tests.")

    parser.add_argument("ruta_archivo", type=str)
    parser.add_argument("output_folder", type=str)
    
    args = parser.parse_args()
    
    main(args.ruta_archivo, args.output_folder)