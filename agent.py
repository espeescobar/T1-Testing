import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
import time
import sys
import subprocess
import json

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


def ejecutar_coverage(ruta_test, ruta_codigo_fuente):
    env_actual = os.environ.copy()
    env_actual["PYTHONPATH"] = os.getcwd()
    ruta_abs_fuente = os.path.abspath(ruta_codigo_fuente)
    cmd_run = ["coverage", "run", "--branch", "-m", "pytest", ruta_test]
    subprocess.run(cmd_run, capture_output=True, env=env_actual)
    cmd_json = ["coverage", "json", "--include", ruta_abs_fuente, "-o", "coverage.json"]
    subprocess.run(cmd_json, capture_output=True, env=env_actual)
    
    try:
        with open("coverage.json", "r") as f:
            data = json.load(f)
            
        resumen = data["totals"]
        line_cov = resumen.get("percent_covered", 0) / 100
        branch_cov = resumen.get("percent_branches_covered", 0) / 100
        
        return line_cov, branch_cov
        
    except (FileNotFoundError, KeyError):
        return 0.0, 0.0


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
    ruta_importacion = ruta_archivo.replace("/", ".").replace("\\", ".").replace(".py", "")
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            codigo_fuente = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de código en {ruta_archivo}")
        sys.exit(1)
    

    prompt = f"""
            Eres un ingeniero de QA Senior experto en Python y pytest. 
            Tu tarea es generar pruebas unitarias exhaustivas con pytest para el siguiente código fuente ubicado en: {ruta_archivo}.
            
            CÓDIGO FUENTE:
            ```python
            {codigo_fuente}
            ```
            
            REGLA DE IMPORTACIÓN CRÍTICA:
            Para testear las clases o funciones, DEBES importarlas utilizando exactamente esta ruta base:
            from {ruta_importacion} import [NombreDeClaseOFuncion]
            REGLA DE MOCKING:
            Si necesitas simular objetos, dependencias o clases externas (como cartas, dealers, etc.), NO crees clases Mock personalizadas desde cero (ej. 'class MockCard:'). 
            Utiliza EXCLUSIVAMENTE 'MagicMock' de la librería 'unittest.mock' y configura sus valores de retorno para evitar problemas de referencias de memoria o ValueError al usar funciones como '.index()'.
                    
            No utilices importaciones relativas.
            
            Responde SOLO con el código Python de las pruebas. No incluyas explicaciones.
            """
    chat = client.chats.create(model="gemini-3.1-flash-lite") 
    
    tiempo_restante = time_budget - (time.time() - start_time)
    while not test_valido and  10 < tiempo_restante:
        tiempo_restante = time_budget - (time.time() - start_time)
        if tiempo_restante < 10:
            break
            
        intentos += 1
        print(f"\n--- Iteración {intentos} --- (Tiempo restante: {tiempo_restante:.1f}s)")

        try:
            if intentos != 1:
                prompt = "Los tests anteriores fallaron con X error. Corrige el código y genera una nueva versión que pase todas las aserciones."
         
            response = chat.send_message(prompt)
            codigo_generado_crudo = response.text
            print(f"Generado intento {intentos}...")
            print(f"Respuesta de prueba del modelo:\n--> {codigo_generado_crudo }\n")
            
            time.sleep(3)

        except Exception as e:
            mensaje_error = str(e)
            print(f"Error de API: {mensaje_error}")
        
            if "503" in mensaje_error or "429" in mensaje_error or "UNAVAILABLE" in mensaje_error:
                print("El servidor de Gemini está saturado...")
                time.sleep(5)
                intentos -= 1  
                continue       
            else:
                sys.exit(1)
        
        codigo_limpio = extraer_codigo_python(codigo_generado_crudo)

        with open(ruta_archivo_temporal, "w", encoding="utf-8") as archivo:
            archivo.write(codigo_limpio)
        print(f"Ejecutando pruebas en {ruta_archivo_temporal}...")
        exito, stdout, stderr = ejecutar_pytest(ruta_archivo_temporal)

        if exito:
            line_cov, branch_cov = ejecutar_coverage(ruta_archivo_temporal, ruta_archivo)
            print(f"Métricas actuales -> Line Coverage: {line_cov:.2f}, Branch Coverage: {branch_cov:.2f}")
            if line_cov >= 0.80 and branch_cov >= 0.50:
                print("¡Cobertura suficiente alcanzada!")
                test_valido = True
            else:
                print("La cobertura es baja. Solicitando más tests al LLM...")
                prompt = f"""
                Tus pruebas pasaron, pero la cobertura de código es insuficiente.
                - Line Coverage actual: {line_cov*100}% (Mínimo requerido: 80%).
                - Branch Coverage actual: {branch_cov*100}% (Mínimo requerido: 50%).
                
                CÓDIGO FUENTE ORIGINAL:
                ```python
                {codigo_fuente}
                ```
                
                PRUEBAS ACTUALES:
                ```python
                {codigo_limpio}
                ```
                
                Por favor, analiza el código fuente original y agrega más casos de prueba 
                (especialmente para cubrir ramas if/else, excepciones o casos de borde) 
                para mejorar la cobertura. Responde SOLO con el código Python completo de los tests.
                """
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
         
   
    print(f"\nGeneración finalizada en {time.time() - start_time:.1f} segundos.")
    print(f"Exportando resultados finales en {output_folder}")
    print(f"\nGeneración finalizada en {time.time() - start_time:.1f} segundos.")
    
    line_cov_final, branch_cov_final = ejecutar_coverage(ruta_archivo_temporal, ruta_archivo)
    metricas = {
        "line_coverage": round(line_cov_final, 2),
        "branch_coverage": round(branch_cov_final, 2),
        "mutation_score": 0.0  
    }
    
    ruta_metricas = os.path.join(output_folder, "metrics.json")
    with open(ruta_metricas, "w") as f:
        json.dump(metricas, f, indent=4)
        
    print(f"Resultados finales guardados en {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agente basado en LLM para generación iterativa de tests.")

    parser.add_argument("ruta_archivo", type=str)
    parser.add_argument("output_folder", type=str)
    
    args = parser.parse_args()
    
    main(args.ruta_archivo, args.output_folder)