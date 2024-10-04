from behave import given, when, then
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@given('estoy en el home')
def step_impl(context):
    assert context.driver is not None, "El driver no está inicializado"

    """wait0 = WebDriverWait(context.driver, 20)

    back_button = wait0.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.ImageButton[@content-desc='Navigate up']"
    )))
    back_button.click()"""

    wait = WebDriverWait(context.driver, 10)

    stays_element = wait.until(EC.presence_of_element_located((
        AppiumBy.XPATH, "//android.widget.TextView[@resource-id='com.booking:id/facet_entry_point_item_label' and @text='Stays']"
    )))
    assert stays_element.is_displayed()


@when('busco hoteles en {city}')
def step_impl(context, city):
     
    # Destination
    wait2 = WebDriverWait(context.driver, 20)
    search_box = wait2.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.TextView[@resource-id='com.booking:id/facet_search_box_basic_field_label' and @text='Enter your destination']"
    )))
    search_box.click()
    
    # Esperar a que aparezca el campo de entrada real y escribir la ciudad
    input_field = wait2.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.widget.EditText[@resource-id='com.booking:id/facet_with_bui_free_search_booking_header_toolbar_content']"
    )))
    input_field.send_keys(city)

    # Seleccionar ciudad
    wait2.until(EC.presence_of_element_located((
        AppiumBy.ID, "com.booking:id/facet_disambiguation_content"
    )))
    
    # Seleccionar el primer resultado
    first_result = wait2.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//androidx.recyclerview.widget.RecyclerView[@resource-id='com.booking:id/facet_disambiguation_content']/android.view.ViewGroup[1]"
    )))
    first_result.click()
    
    # Dates
    try:
        # Intentar hacer clic en el campo de fecha usando el ID del recurso
        date_field = wait2.until(EC.element_to_be_clickable((
            AppiumBy.ID, "com.booking:id/facet_search_box_basic_field_label"
        )))
        date_field.click()
    except TimeoutException:
        # Si falla, intentar con un enfoque alternativo usando coordenadas
        print("No se pudo encontrar el campo de fecha. Intentando con tap en coordenadas.")
        
        # Realizar tap en las coordenadas calculadas
        context.driver.tap([(755, 780)])


    # Seleccionar fecha de inicio (14 de octubre 2024)
    start_date = wait2.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.view.View[@content-desc='14 October 2024']"
    )))
    start_date.click()
    
    # Seleccionar fecha de fin (18 de octubre 2024)
    end_date = wait2.until(EC.element_to_be_clickable((
        AppiumBy.XPATH, 
        "//android.view.View[@content-desc='18 October 2024']"
    )))
    end_date.click()
    
    # Hacer clic en el botón "Select dates"
    select_dates_button = wait2.until(EC.element_to_be_clickable((
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

    # Hacer clic en "Search"
    context.driver.tap([(730, 1131)])


@when('selecciono el segundo hotel disponible')
def step_impl(context):
    wait = WebDriverWait(context.driver, 30)
    # Intentar cerrar el banner de actualización si está presente
    try:
        dismiss_button = wait.until(EC.element_to_be_clickable((
            AppiumBy.ID, "com.booking:id/bui_banner_close_button"
        )))
        dismiss_button.click()
    except TimeoutException:
        print("Banner de actualización no encontrado o ya cerrado")

    # Seleccionar el segundo hotel de la lista
    try:
        hotel = wait.until(EC.element_to_be_clickable((
            AppiumBy.XPATH, 
            "//android.view.ViewGroup[@class='android.view.ViewGroup' and @instance='32']"
        )))
        hotel.click()
    except TimeoutException:
        print("Click en segundo")
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

@then('deberia ver el estado del booking')
def step_impl(context):
    print("No se continua por limitaciones de hardware del equipo.")