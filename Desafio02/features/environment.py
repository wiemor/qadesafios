import uiautomator2 as u2
import time

def before_all(context):
    try:
        print("Initializing uiautomator2...")
        context.d = u2.connect("emulator-5554")
        print("uiautomator2 initialization complete")

        # Iniciar la aplicación
        context.d.app_start("com.booking", "com.booking.startup.HomeActivity")
        print("Application started")

        # Esperar a que la aplicación se cargue
        time.sleep(5)

        # Configurar implicitly wait
        context.d.implicitly_wait(30)

    except Exception as e:
        print(f"Failed to set up uiautomator2: {e}")
        raise e

def after_all(context):
    if hasattr(context, 'd'):
        context.d.app_stop("com.booking")
        print("uiautomator2 session stopped")
    else:
        print("No uiautomator2 session to stop")

# Puedes agregar más funciones de ayuda aquí si lo necesitas
def wait_and_click(context, selector, timeout=10):
    context.d(selector).wait(timeout=timeout)
    context.d(selector).click()

def wait_and_send_keys(context, selector, text, timeout=10):
    context.d(selector).wait(timeout=timeout)
    context.d(selector).clear_text()
    context.d(selector).send_keys(text)