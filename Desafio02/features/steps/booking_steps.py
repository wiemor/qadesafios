from behave import given, when, then
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import os


@given('estoy en el home')
def step_impl(context):
    assert context.driver is not None, "El driver no está inicializado"

    wait = WebDriverWait(context.driver, 20)

    back_button = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.ImageButton[@content-desc='Navigate up']"
    )))
    back_button.click()

    stays_element = wait.until(EC.presence_of_element_located((
        AppiumBy.XPATH, "//android.widget.TextView[@resource-id='com.booking:id/facet_entry_point_item_label' and @text='Stays']"
    )))
    assert stays_element.is_displayed()


@when('busco hoteles en {city}')
def step_impl(context, city):
    wait = WebDriverWait(context.driver, 7)
     
    # Destination
    search_box = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.TextView[@resource-id='com.booking:id/facet_search_box_basic_field_label' and @text='Enter your destination']"
    )))
    search_box.click()
    
    # Esperar a que aparezca el campo de entrada real y escribir la ciudad
    input_field = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.EditText[@resource-id='com.booking:id/facet_with_bui_free_search_booking_header_toolbar_content']"
    )))
    input_field.send_keys(city)

    # Seleccionar ciudad
    wait.until(EC.presence_of_element_located((
        AppiumBy.ID, "com.booking:id/facet_disambiguation_content"
    )))
    
    # Seleccionar el primer resultado
    first_result = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.booking:id/facet_disambiguation_content']/android.view.ViewGroup[1]"
    )))
    first_result.click()
    
    # Dates
    try:
        # Intentar hacer clic en el campo de fecha usando el ID del recurso
        date_field = wait.until(EC.element_to_be_clickable((
            AppiumBy.ID, "com.booking:id/facet_search_box_basic_field_label_2"
        )))
        date_field.click()
    except TimeoutException:        
        context.driver.tap([(755, 780)])

    # Seleccionar fecha de inicio (14 de octubre 2024)
    start_date = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.view.View[@content-desc='14 October 2024']"
    )))
    start_date.click()
    
    # Seleccionar fecha de fin (18 de octubre 2024)
    end_date = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.view.View[@content-desc='18 October 2024']"
    )))
    end_date.click()
    
    # Hacer clic en el botón "Select dates"
    select_dates_button = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, 
        "com.booking:id/facet_date_picker_confirm"
    )))
    select_dates_button.click()

    # Hacer clic en el selector de habitaciones y huéspedes
    context.driver.tap([(800, 940)])
    
    # Agregar 
    context.driver.tap([(978, 1882)])
    
    # Hacer clic en "Apply"
    context.driver.tap([(677, 2049)])
    context.driver.tap([(677, 2049)])

    # Hacer clic en "Search"
    context.driver.tap([(730, 1131)])


@when('selecciono el segundo hotel disponible')
def step_impl(context):
    wait = WebDriverWait(context.driver, 5)
    # Intentar cerrar el banner de actualización si está presente
    """try:
        dismiss_button = wait.until(EC.element_to_be_clickable((
            AppiumBy.ID, "com.booking:id/bui_banner_close_button"
        )))
        dismiss_button.click()
    except TimeoutException:
        print("Banner de actualización no encontrado o ya cerrado")"""

    # Seleccionar el segundo hotel de la lista
    try:
        hotel = wait.until(EC.element_to_be_clickable((
            AppiumBy.XPATH, 
            "//android.view.ViewGroup[@class='android.view.ViewGroup' and @instance='32']"
        )))
        hotel.click()
    except TimeoutException:
        context.driver.tap([(876, 1801)])

    # Esperar a que se cargue la página de detalles del hotel
    wait.until(EC.presence_of_element_located((
        AppiumBy.ID, "com.booking:id/facet_price_view"
    )))
    
    # Seleccionar la opción recomendada 
    recommended_option = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, "com.booking:id/facet_price_view"
    )))
    recommended_option.click()

    # Esperar a que se cargue la página de detalles del hotel y seleccionar la opción de habitación
    room_option = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, "com.booking:id/rooms_item_select_text_view"
    )))
    room_option.click()

    reserve_button = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, "com.booking:id/main_action"
    )))
    reserve_button.click()


@when('ingreso informacion personal')
def step_impl(context):

    wait = WebDriverWait(context.driver, 5)

    # First Name
    input_field_first_name = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.EditText[@resource-id='com.booking:id/bui_input_container_content']"
    )))
    input_field_first_name.send_keys("Jose")

    input_field_last_name = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.EditText[@resource-id='com.booking:id/bui_input_container_content_2']"
    )))
    input_field_last_name.send_keys("Hurtado")

    """
    wait = WebDriverWait(context.driver, 5)

    # Contenedor
    container = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.booking:id/bui_input_container_content")))
    input_fields = container.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")

    # First Name
    input_fields[0].send_keys("Jose") 

    # Last Name
    input_fields[1].send_keys("Hurtado") 

    # Email
    input_fields[2].send_keys("jose.hurtado@email.com") 
    """
    """ input_field_first_name = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.EditText[@resource-id='com.booking:id/bui_input_container_content_1']"
    )))
    input_field_first_name.send_keys("Jose")

    # Last Name
    input_field_last_name = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.EditText[@resource-id='com.booking:id/bui_input_container_content_2']"
    )))
    input_field_last_name.send_keys("Hurtado")
    """
    # Ensure the app is in the foreground
    """context.device.app_start("com.booking")
    context.device.wait_activity(".flights.FlightSearchActivity", timeout=10)

    # Fill the form
    input_text_to_element(context.device, "com.booking:id/bui_input_container_content_1", "John")
    input_text_to_element(context.device, "com.booking:id/bui_input_container_content_2", "Doe")
    input_text_to_element(context.device, "com.booking:id/bui_input_container_content_3", "john.doe@example.com")
    input_text_to_element(context.device, "com.booking:id/bui_input_container_content_4", "Colombia")
    input_text_to_element(context.device, "com.booking:id/bui_input_container_content_5", "999999999")

    # Select the "Leisure" option
    context.device(resourceId="com.booking:id/business_purpose_leisure_1").click()"""

def input_text_to_element(device, resource_id, text):
    element = device(resourceId=resource_id)
    element.clear_text()
    element.set_text(text)

    """wait = WebDriverWait(context.driver, 10)

    # First Name
    input_field_first_name = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, 
        "com.booking:id/bui_input_container_content_1"
    )))
    input_field_first_name.send_keys("Jose")

    # Last Name
    input_field_last_name = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, 
        "com.booking:id/bui_input_container_content_2"
    )))
    input_field_last_name.send_keys("Hurtado")

    # Email
    input_field_email = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, 
        "com.booking:id/bui_input_container_content_3"
    )))
    input_field_email.send_keys("jose@email.com")

    # City 
    input_field_city = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, 
        "com.booking:id/bui_input_container_content_4"
    )))
    input_field_city.send_keys("Lima")

    # Mobile 
    input_field_mobile = wait.until(EC.element_to_be_clickable((
        AppiumBy.ID, 
        "com.booking:id/bui_input_container_content_5"
    )))
    input_field_mobile.send_keys("999999999")


    # Leisure
    element = wait.until(EC.element_to_be_clickable((
        AppiumBy.XPATH,
        "//android.widget.RadioButton[@resource-id='com.booking:id/business_purpose_leisure_1' or @text='Leisure']"
    )))
    element.click()
    """

    """
    # Input First Name
    context.driver.press_keycode(61)
    context.driver.press_keycode(61)
    context.driver.press_keycode(61)
    time.sleep(0.5) 

    # First Name
    context.driver.press_keycode(38) # j
    context.driver.press_keycode(43)  # o
    context.driver.press_keycode(47) # s
    context.driver.press_keycode(33) # e
    context.driver.press_keycode(61) # tab
    
       

    context.driver.press_keycode(61)
    print("fin last name")"""

    # Email address
    """for char in "josehurtado@gmail.com":
        context.driver.press_keycode(ord(char))
    time.sleep(0.5)
    context.driver.press_keycode(61)
    context.driver.press_keycode(61)

    # Mobile Phone
    for char in "930731660":
        context.driver.press_keycode(ord(char))
    time.sleep(0.5)
    context.driver.press_keycode(61)
    context.driver.press_keycode(61)

    # Presionar SPACE
    context.driver.press_keycode(62)

    # Presionar ESCAPE
    context.driver.press_keycode(111)

    # Next Step
    context.driver.tap([(500, 2100)])

    # Final Step
    context.driver.tap([(500, 2100)])"""

@when('ingreso credit card information')
def step_impl(context):

    # Card Number
    """context.driver.tap([(500, 700)])
    for char in "4555 7887 6544 3333":
        context.driver.press_keycode(ord(char))
    time.sleep(0.5)
    context.driver.press_keycode(61)

    # Holder's Name
    for char in "0225":
        context.driver.press_keycode(ord(char))
    time.sleep(0.5)"""
 
@then('deberia ver el booking')
def step_impl(context):
    print("Recuperar precio.")