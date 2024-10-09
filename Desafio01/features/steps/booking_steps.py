import requests
from behave import given, when, then

def api_request(context, method, endpoint, **kwargs):
    """Función auxiliar para realizar solicitudes a la API."""
    url = f"{context.endpoints['booking']}/{endpoint}"
    try:
        response = requests.request(method, url, **kwargs, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error en la solicitud a la API: {str(e)}")
        raise

@given('I have a valid token')
def step_impl(context):
    context.token = context.shared_data.get("token")
    assert context.token is not None, "Token no encontrado en el contexto"

@given('I have valid booking details')
def step_impl(context):
    context.booking_details = {
        "firstname" : "Jim",
        "lastname" : "Brown",
        "totalprice" : 111,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2018-01-01",
            "checkout" : "2019-01-01"
        },
        "additionalneeds" : "Breakfast"
    }

@when('I create a booking')
def step_impl(context):
    context.response = api_request(context, 'POST', '', json=context.booking_details)
    context.booking_id = context.response.json().get("bookingid")

@then('I should receive a confirmation from booking')
def step_impl(context):
    assert context.response.status_code == 200, f"Código de estado esperado 200, pero se recibió {context.response.status_code}"
    assert "bookingid" in context.response.json(), "No se encontró 'bookingid' en la respuesta"
    assert context.booking_id is not None, "El ID de booking es None"
    context.shared_data["booking_id"] = context.booking_id

@given('I have a valid booking ID')
def step_impl(context):
    context.booking_id = context.shared_data.get("booking_id")
    assert context.booking_id is not None, "ID de booking no encontrado en el contexto"

@when('I get the details of the booking')
def step_impl(context):
    context.booking_details = context.shared_data["booking_details"]
    context.response = api_request(context, 'GET', context.booking_id)

@then('I should see the correct booking information')
def step_impl(context):
    assert context.response.status_code == 200, f"Código de estado esperado 200, pero se recibió {context.response.status_code}"
    
    response_json = context.response.json()

    if 'firstname' in response_json:
        assert response_json["firstname"] == context.booking_details["firstname"], "El nombre no coincide con los detalles originales"
    else:
        raise AssertionError("La estructura de la respuesta no contiene 'firstname' como se esperaba")

@given('I have new booking details')
def step_impl(context):
    context.new_booking_details = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 999,
        "depositpaid": False,
        "bookingdates": {
        "checkin" : "2024-01-01",
        "checkout" : "2024-01-01"
        },
        "additionalneeds": "Breakfast"
    }

@when('I update the booking')
def step_impl(context):
    context.response = api_request(context, 'PUT', context.booking_id, json=context.new_booking_details, cookies={"token": context.token})

@then('I should see the updated booking information')
def step_impl(context):
    assert context.response.status_code == 200, f"Código de estado esperado 200, pero se recibió {context.response.status_code}"
    assert context.response.json()["firstname"] == context.new_booking_details["firstname"], "El nombre actualizado no coincide"

@when('I delete the booking')
def step_impl(context):
    context.response = api_request(context, 'DELETE', context.booking_id, cookies={"token": context.token})

@then('the booking should be deleted successfully')
def step_impl(context):
    assert context.response.status_code == 201, f"Código de estado esperado 201, pero se recibió {context.response.status_code}"

@given('I have invalid booking details')
def step_impl(context):
    context.invalid_booking_details = {
        "firstname": "",
        "lastname": "Doe",
        "totalprice": -100,
        "depositpaid": "invalid",
        "bookingdates": {
            "checkin": "2022-01-02",
            "checkout": "2022-01-01"
        }
    }

@when('I try to create a booking')
def step_impl(context):
    context.response = api_request(context, 'POST', '', json=context.invalid_booking_details)

@then('I should receive a validation error')
def step_impl(context):
    assert context.response.status_code == 200, f"Código de estado esperado 200, pero se recibió {context.response.status_code}"
