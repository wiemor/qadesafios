import requests
from behave import given, when, then

def api_request(context, method, endpoint, **kwargs):
    """Función auxiliar para realizar solicitudes a la API."""
    url = f"{context.endpoints['ping']}/{endpoint}"
    try:
        response = requests.request(method, url, **kwargs, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error en la solicitud a la API: {str(e)}")
        raise


@given('que la API está en funcionamiento')
def step_impl(context):
    pass

@when('hago ping a la API')
def step_impl(context):
    context.response = api_request(context, 'GET', '')

@then('debería recibir una respuesta OK')
def step_impl(context):
    assert context.response.status_code == 201, f"Código de estado esperado 201, pero se recibió {context.response.status_code}"
    assert context.response.text == "Created", f"Respuesta esperada 'Created', pero se recibió '{context.response.text}'"