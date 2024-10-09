import uiautomator2 as u2
import time
from collections import defaultdict
import sys
import io
import codecs


# Configurar la salida estándar para usar UTF-8
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

def connect_device(device_id="emulator-5554"):
    d = u2.connect(device_id)
    print(f"Device connected: {device_id}")
    return d

def get_element_details(element):
    try:
        info = element.info
        return {
            "text": info.get('text', ''),
            "resource_id": info.get('resourceId', ''),
            "class_name": info.get('className', ''),
            "description": info.get('contentDescription', ''),
            "enabled": info.get('enabled', False),
            "clickable": info.get('clickable', False),
            "focusable": info.get('focusable', False),
            "focused": info.get('focused', False),
            "scrollable": info.get('scrollable', False),
            "selected": info.get('selected', False),
            "package": info.get('package', ''),
            "hint": info.get('hint', ''),
        }
    except Exception as e:
        print(f"Error processing element: {e}")
        return None

def analyze_screen(d):
    time.sleep(2)
    elements = d.xpath('//*').all()
    elements_by_id = defaultdict(list)

    for element in elements:
        details = get_element_details(element)
        if details:
            resource_id = details['resource_id']
            elements_by_id[resource_id].append(details)

    for resource_id, elements in elements_by_id.items():
        print(f"\nResource ID: {resource_id}")
        print(f"Number of elements with this ID: {len(elements)}")
        for i, element in enumerate(elements, 1):
            print(f"  Element {i}:")
            unique_id = f"{resource_id}_{i}"
            print(f"    Unique Identifier: {unique_id}")
            for key, value in element.items():
                if key != 'resource_id':
                    safe_value = str(value).encode('ascii', 'replace').decode('ascii')
                    print(f"    {key}: {safe_value}")
            print("    ---")

def input_text_to_element(d, unique_id, text):
    parts = unique_id.split('_')
    if len(parts) < 2:
        print(f"Error: Invalid unique identifier format. Expected at least 2 parts, got {len(parts)}")
        print(f"Unique identifier: {unique_id}")
        return

    resource_id = '_'.join(parts[:-1])  # Join all parts except the last one (which is the index)
    try:
        index = int(parts[-1]) - 1  # Convert to 0-based index
    except ValueError as e:
        print(f"Error: Invalid index value in unique identifier: {e}")
        print(f"Unique identifier: {unique_id}")
        return

    print(f"Attempting to find element with resourceId='{resource_id}' at index {index}")
    
    # Usar xpath para encontrar todos los elementos con el resource_id
    elements = d.xpath(f'//*[@resource-id="{resource_id}"]').all()
    
    if 0 <= index < len(elements):
        target_element = elements[index]
        # Crear un selector UIAutomator2 para el elemento encontrado
        selector = d(resourceId=resource_id, instance=index)
        
        # Limpiar el texto existente
        selector.clear_text()
        # Ingresar el nuevo texto
        selector.send_keys(text)
        print(f"Text '{text}' input to element with Unique Identifier: {unique_id}")
    else:
        print(f"Element with Unique Identifier {unique_id} not found")
        print(f"Found {len(elements)} elements with resourceId='{resource_id}'")

def select_leisure_option(d, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            # Intento 1: Usar el texto "Leisure"
            element = d(text="Leisure")
            if element.exists():
                element.click()
                if verify_selection(d, "Leisure"):
                    print("Leisure option selected successfully using text")
                    return True
                
            print("intento:",attempts,"-paso1")
            time.sleep(10)  # Esperar antes de intentar de nuevo

            # Si llegamos aquí, ningún intento funcionó
            print(f"Attempt {attempts + 1} failed to select Leisure option")
            attempts += 1
            time.sleep(2)  # Esperar antes de intentar de nuevo
        except Exception as e:
            print(f"Error during attempt {attempts + 1}: {e}")
            attempts += 1
            time.sleep(2)

    print("Failed to select Leisure option after all attempts")
    return False

def verify_selection(d, option_text):
    # Verificar si la opción está seleccionada
    selected_element = d(selected=True, text=option_text)
    return selected_element.exists

def find_element(d, **kwargs):
    """
    Find an element using multiple strategies.
    """
    strategies = [
        lambda: d(**kwargs),
        lambda: d.xpath(f'//*[@text="{kwargs.get("text", "")}"]'),
        lambda: d.xpath(f'//*[@resource-id="{kwargs.get("resourceId", "")}"]'),
        lambda: d.xpath(f'//*[@content-desc="{kwargs.get("description", "")}"]'),
    ]

    for strategy in strategies:
        try:
            element = strategy()
            if element.exists:
                return element
        except Exception:
            continue
    
    return None

def input_text(d, identifier, text):
    element = find_element(d, text=identifier) or find_element(d, resourceId=identifier) or find_element(d, description=identifier)
    
    if element:
        element.clear_text()
        element.send_keys(text)
        print(f"Text '{text}' input to element with identifier: {identifier}")
    else:
        print(f"Element with identifier {identifier} not found")

def select_option(d, option_text, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            element = find_element(d, text=option_text)
            if element:
                element.click()
                if verify_selection(d, option_text):
                    print(f"{option_text} option selected successfully")
                    return True
            
            print(f"Attempt {attempts + 1} failed to select {option_text} option")
            attempts += 1
            time.sleep(2)
        except Exception as e:
            print(f"Error during attempt {attempts + 1}: {e}")
            attempts += 1
            time.sleep(2)

    print(f"Failed to select {option_text} option after all attempts")
    return False

def wait_and_click(d, description, timeout=10, interval=1):
    """
    Espera a que un elemento sea clickeable y luego hace clic en él.
    """
    end_time = time.time() + timeout
    while time.time() < end_time:
        element = d(description=description)
        if element.exists and element.info.get('clickable', False):
            element.click()
            print(f"Clicked on element with description: {description}")
            return True
        time.sleep(interval)
    print(f"Element with description '{description}' not clickable after {timeout} seconds")
    return False

def wait_and_click(d, desc, timeout=10):
    element = d(description=desc)
    return element.wait(timeout=timeout) and element.click()

def click_search_field(d, timeout=10):
    # Extraer el resourceId base y el índice del Unique Identifier
    base_id = "com.booking:id/facet_search_box_basic_field_label"
    index = 2  # El índice 2 corresponde al tercer elemento (ya que la indexación comienza en 0)

    # Buscar el elemento y hacer clic
    element = d(resourceId=base_id, instance=index)
    if element.wait(timeout=timeout) and element.exists:
        element.click()
        print(f"Campo de búsqueda (índice {index}) clickeado exitosamente")
        return True
    else:
        print(f"No se pudo encontrar o clickear el campo de búsqueda (índice {index})")
        return False

def click_addchild_button(d, timeout=10):
    # ResourceId exacto del botón
    button_id = "com.booking:id/bui_input_stepper_add_button"
    # Índice del botón (2 porque la indexación empieza en 0)
    button_index = 2

    # Buscar el botón específico y hacer clic
    button = d(resourceId=button_id, instance=button_index)
    if button.wait(timeout=timeout) and button.exists:
        button.click()
        print(f"Botón (índice {button_index}) clickeado exitosamente")
        return True
    else:
        print(f"No se pudo encontrar o clickear el botón (índice {button_index})")
        return False
       
def scroll_numberpicker_to_value_5yo(d, target_value, max_attempts=20):
    numberpicker = d(resourceId="android:id/numberpicker_input")
    if not numberpicker.exists:
        print("No se pudo encontrar el NumberPicker")
        return False

    for _ in range(max_attempts):
        current_value = numberpicker.get_text()
        if current_value == target_value:
            print(f"Valor establecido a '{target_value}' exitosamente")

            ok_button = d(text="OK")
            if ok_button.exists:
                ok_button.click()
                print("Selección confirmada con botón OK")
            return True

        # Determinar dirección de desplazamiento
        d.swipe_ext("up", scale=0.5)  # Desplazar hacia abajo

        time.sleep(0.5)  # Breve pausa entre desplazamientos

    print(f"No se pudo establecer el valor a '{target_value}' después de {max_attempts} intentos")
    return False

def interact_with_booking_app(d):

    # City
    time.sleep(1)
    search_field = d(resourceId="com.booking:id/facet_search_box_basic_field_label")
    if search_field.exists:
        search_field.click()
        time.sleep(1)  
        
        # Ingresar el destino
        d.send_keys("Cusco")
        print("Destino 'Cusco' ingresado exitosamente")
        time.sleep(2)


    # Click list result cusco
    results = d(className="android.widget.TextView")
    place_results = [r for r in results if r.info.get('text') and ',' in r.info.get('text')]
    
    if place_results:
        first_result = place_results[0]
        first_result.click()

    # Dates
    if wait_and_click(d, "14 October 2024"):
        print("Fecha de inicio seleccionada")

    if wait_and_click(d, "18 October 2024"):
        print("Fecha de inicio seleccionada")
    
    # click button select date
    button_select_date = d(resourceId="com.booking:id/facet_date_picker_confirm")
    if button_select_date.wait(timeout=2) and button_select_date.exists:
        button_select_date.click()

    # Child
    if click_search_field(d):
        print("Campo de búsqueda seleccionado correctamente")

    if click_addchild_button(d):
        print("Botón específico seleccionado correctamente")

    if scroll_numberpicker_to_value_5yo(d, "5 years old"):
        print("Edad del niño establecida correctamente")


    time.sleep(1)  

    # click button apply
    button_apply = d(resourceId="com.booking:id/group_config_apply_button")
    if button_apply.wait(timeout=2) and button_apply.exists:
        button_apply.click()

    time.sleep(1)  

    # click button search home
    button_search_home = d(resourceId="com.booking:id/facet_search_box_cta")
    if button_search_home.wait(timeout=2) and button_search_home.exists:
        button_search_home.click()

    time.sleep(2)

    # cerrar el close button
    button_close_button = d(resourceId="com.booking:id/bui_banner_close_button")
    if button_close_button.wait(timeout=2) and button_close_button.exists:
        button_close_button.click()

    time.sleep(2)

    # second result
    d.click(800, 1870)

    time.sleep(2)

    # click Select room/see your options LIST
    button_select_room = d(resourceId="com.booking:id/select_room_cta")
    if button_select_room.wait(timeout=2) and button_select_room.exists:
        button_select_room.click()

    time.sleep(2)

    # SELECT ROOM
    button_select_text_room = d(resourceId="com.booking:id/rooms_item_select_text_view")
    if button_select_text_room.wait(timeout=2) and button_select_text_room.exists:
        button_select_text_room.click()

    time.sleep(1)

    d(resourceId="com.booking:id/main_action", text="Reserve").click()

    ######### Filll your data

    time.sleep(1)
    input_text_to_element(d, "com.booking:id/bui_input_container_content_1", "John")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_2", "Doe")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_3", "john.doe@example.com")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_4", "Colombia")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_5", "999999999")

    time.sleep(1)
    d.swipe_ext("up", scale=0.5)  # Desplazar hacia abajo
    time.sleep(1)

    # Seleccionar la opción "Leisure"
    if select_leisure_option(d):
        print("Leisure option selected successfully")

    time.sleep(1)
    # boton Add missing details    
    button_add_missing = d(resourceId="com.booking:id/action_button")
    if button_add_missing.wait(timeout=2) and button_add_missing.exists:
        button_add_missing.click()


    time.sleep(1)
    # siguiente pantalla
    button_book_now = d(resourceId="com.booking:id/action_button")
    if button_book_now.wait(timeout=2) and button_book_now.exists:
        button_book_now.click()
    
    time.sleep(8)

    ### Button Close
    button_btn_close = d(resourceId="com.booking:id/bui_bottom_sheet_close")
    if button_btn_close.wait(timeout=2) and button_btn_close.exists:
        button_btn_close.click()
    


def main():
    d = connect_device()
    # Analyze the screen
    analyze_screen(d)
    interact_with_booking_app(d)

if __name__ == "__main__":
    main()