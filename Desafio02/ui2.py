import uiautomator2 as u2
import time
from collections import defaultdict
import sys
import io

# Configurar la salida estándar para usar UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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
            # Intento 1: Usar el ID de recurso específico
            element = d(resourceId="com.booking:id/business_purpose_leisure_1")
            if element.exists():
                element.click()
                if verify_selection(d, "Leisure"):
                    print("Leisure option selected successfully using resource ID")
                    return True

            # Intento 2: Usar el texto "Leisure"
            element = d(text="Leisure")
            if element.exists():
                element.click()
                if verify_selection(d, "Leisure"):
                    print("Leisure option selected successfully using text")
                    return True

            # Intento 3: Usar XPath
            element = d.xpath('//*[@text="Leisure"]')
            if element.exists:
                element.click()
                if verify_selection(d, "Leisure"):
                    print("Leisure option selected successfully using XPath")
                    return True

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

def main():
    d = connect_device()
    analyze_screen(d)
    
    # Ejemplo de cómo ingresar texto en elementos específicos
    input_text_to_element(d, "com.booking:id/bui_input_container_content_1", "John")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_2", "Doe")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_3", "john.doe@example.com")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_4", "Colombia")
    input_text_to_element(d, "com.booking:id/bui_input_container_content_5", "999999999")

    # Seleccionar la opción "Leisure"
    if select_leisure_option(d):
        print("Leisure option selected successfully")
    else:
        print("Failed to select Leisure option")

if __name__ == "__main__":
    main()