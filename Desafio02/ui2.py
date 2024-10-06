from uiautomator2 import connect
import time

d = connect("emulator-5554")
print("Device connected")

# Espera a que la interfaz de usuario esté lista
time.sleep(2)

# Obtener todos los elementos de la pantalla
elements = d.xpath('//*').all()

for element in elements:
    try:
        info = element.info
        print(f"Text: {info.get('text')}")
        print(f"Resource ID: {info.get('resourceId')}")
        print(f"Class Name: {info.get('className')}")
        print(f"Description: {info.get('contentDescription')}")
        print(f"Bounds: {info.get('bounds')}")
        print("---")
    except Exception as e:
        print(f"Error processing element: {e}")