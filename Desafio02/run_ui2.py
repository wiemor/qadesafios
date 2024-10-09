import subprocess
import codecs

def run_ui2():
    try:
        # Ejecutar ui2.py y capturar su salida
        result = subprocess.run(['python', 'ui2.py'], capture_output=True, text=True, encoding='utf-8')
        
        # Escribir la salida a un archivo
        with codecs.open('a.txt', 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        
        # Si hay errores, escribirlos en un archivo separado
        if result.stderr:
            with codecs.open('error.log', 'w', encoding='utf-8') as f:
                f.write(result.stderr)
        
        print("Ejecución completada. Revisa 'a.txt' para ver los resultados.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        with codecs.open('error.log', 'w', encoding='utf-8') as f:
            f.write(str(e))

if __name__ == "__main__":
    run_ui2()