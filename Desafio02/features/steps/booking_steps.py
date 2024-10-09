from behave import given, when, then
import uiautomator2 as u2
import time

@given('estoy en el home')
def step_impl(context):
    assert context.d is not None, "uiautomator2 no está inicializado"

    back_button = context.d(description="Navigate up")
    if back_button.exists:
        back_button.click()

    stays_element = context.d(resourceId="com.booking:id/facet_entry_point_item_label", text="Stays")
    assert stays_element.exists, "El elemento 'Stays' no está presente"

@when('busco hoteles en {city}')
def step_impl(context, city):
    # Destination
    search_box = context.d(resourceId="com.booking:id/facet_search_box_basic_field_label", text="Enter your destination")
    search_box.click()
    
    input_field = context.d(resourceId="com.booking:id/facet_with_bui_free_search_booking_header_toolbar_content")
    input_field.set_text(city)

    # Seleccionar el primer resultado
    context.d(resourceId="com.booking:id/facet_disambiguation_content").child(className="android.view.ViewGroup", instance=0).click()
    
    # Dates
    date_field = context.d(resourceId="com.booking:id/facet_search_box_basic_field_label_2")
    if date_field.exists:
        date_field.click()
    else:
        context.d.click(755, 780)

    # Seleccionar fecha de inicio (14 de octubre 2024)
    context.d(description="14 October 2024").click()
    
    # Seleccionar fecha de fin (18 de octubre 2024)
    context.d(description="18 October 2024").click()
    
    # Hacer clic en el botón "Select dates"
    context.d(resourceId="com.booking:id/facet_date_picker_confirm").click()

    # Hacer clic en el selector de habitaciones y huéspedes
    context.d.click(800, 940)
    
    # Agregar 
    context.d.click(978, 1882)
    
    # Hacer clic en "Apply"
    context.d.click(677, 2049)
    context.d.click(677, 2049)

    # Hacer clic en "Search"
    context.d.click(730, 1131)

@when('selecciono el segundo hotel disponible')
def step_impl(context):

    # Definir el selector para el elemento
    selector = {
        "resourceId": "com.booking:id/facet_search_box_basic_field_label_3",
        "text": "1 room ? 2 adults ? 0 children",
        "className": "android.widget.TextView"
    }

    # Esperar a que el elemento esté presente y hacer clic
    context.d(**selector).wait(timeout=10)  # Espera hasta 10 segundos
    context.d(**selector).click()

    """
    # Esperar a que la lista de hoteles se cargue
    context.d(resourceId="com.booking:id/results_list_facet").wait(timeout=30)

    # Seleccionar el segundo hotel de la lista
    hotels = context.d(className="android.view.ViewGroup")
    if len(hotels) >= 2:
        hotels[1].click()
    else:
        context.d.click(876, 1801)

    # Esperar a que la página de detalles del hotel se cargue
    context.d(resourceId="com.booking:id/property_section_content_layout").wait(timeout=30)

    # Intentar seleccionar la opción recomendada
    try:
        context.d(resourceId="com.booking:id/facet_price_view").click(timeout=10)
    except u2.exceptions.UiObjectNotFoundError:
        # Si no se encuentra, intenta hacer scroll y buscar de nuevo
        context.d(scrollable=True).scroll.to(resourceId="com.booking:id/facet_price_view")
        context.d(resourceId="com.booking:id/facet_price_view").click(timeout=10)

    # Esperar a que la página de selección de habitación se cargue
    context.d(resourceId="com.booking:id/rooms_item_select_text_view").wait(timeout=30)

    # Seleccionar la opción de habitación
    context.d(resourceId="com.booking:id/rooms_item_select_text_view").click()

    # Esperar a que el botón de reserva esté disponible
    context.d(resourceId="com.booking:id/main_action").wait(timeout=30)
    context.d(resourceId="com.booking:id/main_action").click()
    """
@when('ingreso informacion personal')
def step_impl(context):
    # First Name
    context.d(resourceId="com.booking:id/bui_input_container_content").set_text("Jose")

    # Last Name
    context.d(resourceId="com.booking:id/bui_input_container_content_2").set_text("Hurtado")

    # Aquí puedes agregar más campos si es necesario

@when('ingreso credit card information')
def step_impl(context):
    # Implementa esto si es necesario
    pass

@then('deberia ver el booking')
def step_impl(context):
    print("Recuperar precio.")
    # Implementa la verificación del booking aquí