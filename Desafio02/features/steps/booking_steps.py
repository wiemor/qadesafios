# Import statements
from behave import given, when, then
import uiautomator2 as u2
import time
from typing import Optional

# Constants
TIMEOUT = 10
SCROLL_SCALE = 0.5
MAX_ATTEMPTS = 20

# Utility functions
def wait_and_click(device: u2.Device, description: str, timeout: int = TIMEOUT) -> bool:
    """Wait for an element with the given description and click it."""
    element = device(description=description)
    return element.wait(timeout=timeout) and element.click()

def find_and_click_by_resource_id(device: u2.Device, resource_id: str, instance: int = 0, timeout: int = TIMEOUT) -> bool:
    """Find an element by resource ID and instance, then click it."""
    element = device(resourceId=resource_id, instance=instance)
    if element.wait(timeout=timeout) and element.exists:
        element.click()
        print(f"Element with resourceId '{resource_id}' (instance {instance}) clicked successfully")
        return True
    print(f"Could not find or click element with resourceId '{resource_id}' (instance {instance})")
    return False

def scroll_numberpicker_to_value(device: u2.Device, target_value: str, max_attempts: int = MAX_ATTEMPTS) -> bool:
    """Scroll a NumberPicker to the target value."""
    numberpicker = device(resourceId="android:id/numberpicker_input")
    if not numberpicker.exists:
        print("NumberPicker not found")
        return False

    for _ in range(max_attempts):
        if numberpicker.get_text() == target_value:
            print(f"Value set to '{target_value}' successfully")
            ok_button = device(text="OK")
            if ok_button.exists:
                ok_button.click()
                print("Selection confirmed with OK button")
            return True
        device.swipe_ext("up", scale=SCROLL_SCALE)
        time.sleep(0.5)

    print(f"Could not set value to '{target_value}' after {max_attempts} attempts")
    return False

def input_text_to_element(device: u2.Device, unique_id: str, text: str) -> None:
    """Input text to an element identified by a unique ID."""
    parts = unique_id.split('_')
    if len(parts) < 2:
        print(f"Error: Invalid unique identifier format: {unique_id}")
        return

    resource_id = '_'.join(parts[:-1])
    try:
        index = int(parts[-1]) - 1
    except ValueError:
        print(f"Error: Invalid index in unique identifier: {unique_id}")
        return

    elements = device.xpath(f'//*[@resource-id="{resource_id}"]').all()
    if 0 <= index < len(elements):
        selector = device(resourceId=resource_id, instance=index)
        selector.clear_text()
        selector.send_keys(text)
        print(f"Text '{text}' input to element with Unique Identifier: {unique_id}")
    else:
        print(f"Element with Unique Identifier {unique_id} not found")

def select_leisure_option(device: u2.Device, max_attempts: int = 3) -> bool:
    """Select the 'Leisure' option."""
    for attempt in range(max_attempts):
        element = device(text="Leisure")
        if element.exists():
            element.click()
            if device(selected=True, text="Leisure").exists:
                print("Leisure option selected successfully")
                return True
        print(f"Attempt {attempt + 1} failed to select Leisure option")
        time.sleep(2)
    print("Failed to select Leisure option after all attempts")
    return False

def get_element_text(device: u2.Device, resource_id: str, timeout: int = TIMEOUT) -> Optional[str]:
    """Get the text of an element identified by resource ID."""
    try:
        element = device(resourceId=resource_id)
        if element.wait(timeout=timeout):
            return element.get_text()
        print(f"Element with resource ID {resource_id} not found within {timeout} seconds")
    except Exception as e:
        print(f"Error getting text from element with resource ID {resource_id}: {e}")
    return None

# Step implementations
@given('estoy en el home')
def step_impl(context):
    assert context.d is not None, "uiautomator2 is not initialized"
    back_button = context.d(description="Navigate up")
    if back_button.exists:
        back_button.click()
    time.sleep(1)
    stays_element = context.d(resourceId="com.booking:id/facet_entry_point_item_label", text="Stays")
    assert stays_element.exists, "The 'Stays' element is not present"

@when('busco hoteles en {city}')
def step_impl(context, city):
    # Search for hotels
    time.sleep(1)
    search_field = context.d(resourceId="com.booking:id/facet_search_box_basic_field_label")
    if search_field.exists:
        search_field.click()
        time.sleep(1)
        context.d.send_keys(city)
        print(f"Destination '{city}' entered successfully")
        time.sleep(2)

    # Select the first result
    results = context.d(className="android.widget.TextView")
    place_results = [r for r in results if r.info.get('text') and ',' in r.info.get('text')]
    if place_results:
        place_results[0].click()

    # Select dates
    wait_and_click(context.d, "14 October 2024")
    wait_and_click(context.d, "18 October 2024")
    find_and_click_by_resource_id(context.d, "com.booking:id/facet_date_picker_confirm")

    # Add a child
    find_and_click_by_resource_id(context.d, "com.booking:id/facet_search_box_basic_field_label", instance=2)
    find_and_click_by_resource_id(context.d, "com.booking:id/bui_input_stepper_add_button", instance=2)
    scroll_numberpicker_to_value(context.d, "5 years old")

    time.sleep(1)
    find_and_click_by_resource_id(context.d, "com.booking:id/group_config_apply_button")
    time.sleep(1)

@when('selecciono el segundo hotel disponible')
def step_impl(context):
    find_and_click_by_resource_id(context.d, "com.booking:id/facet_search_box_cta")
    time.sleep(2)
    find_and_click_by_resource_id(context.d, "com.booking:id/bui_banner_close_button")
    time.sleep(2)
    context.d.click(800, 1870)  # Select second result
    time.sleep(2)
    find_and_click_by_resource_id(context.d, "com.booking:id/select_room_cta")
    time.sleep(3)
    find_and_click_by_resource_id(context.d, "com.booking:id/rooms_item_select_text_view")
    time.sleep(1)
    context.d(resourceId="com.booking:id/main_action", text="Reserve").click()

@when('ingreso informacion personal')
def step_impl(context):
    time.sleep(2)
    personal_info = [
        ("com.booking:id/bui_input_container_content_1", "John"),
        ("com.booking:id/bui_input_container_content_2", "Doe"),
        ("com.booking:id/bui_input_container_content_3", "john.doe@example.com"),
        ("com.booking:id/bui_input_container_content_4", "Colombia"),
        ("com.booking:id/bui_input_container_content_5", "999999999")
    ]
    for unique_id, text in personal_info:
        input_text_to_element(context.d, unique_id, text)

    context.d.swipe_ext("up", scale=SCROLL_SCALE)
    time.sleep(1)
    select_leisure_option(context.d)
    time.sleep(1)
    find_and_click_by_resource_id(context.d, "com.booking:id/action_button")
    time.sleep(1)
    find_and_click_by_resource_id(context.d, "com.booking:id/action_button")
    time.sleep(8)
    find_and_click_by_resource_id(context.d, "com.booking:id/bui_bottom_sheet_close")

@when('ingreso credit card information')
def step_impl(context):
    if context.d(resourceId="com.booking:id/new_credit_card_number_edit").exists:
        input_text_to_element(context.d, "com.booking:id/new_credit_card_number_edit_1", "9999999")
        time.sleep(2)
        context.d(text="Select your card type").click()
        time.sleep(1)
        context.d(text="Visa").click()
        input_text_to_element(context.d, "com.booking:id/new_credit_card_expiry_date_edit_1", "02/25")



@then('deberia ver el booking')
def step_impl(context):
    final_price = get_element_text(context.d, "com.booking:id/title")
    if final_price:
        print(f"The final price is: {final_price}")