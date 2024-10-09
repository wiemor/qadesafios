import requests
from behave import given, when, then

def auth_request(context, credentials):
    try:
        response = requests.post(context.endpoints['auth'], json=credentials, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error en la solicitud de autenticación: {str(e)}")
        raise

@given('I have valid credentials')
def step_impl(context):
    context.credentials = {"username": "admin", "password": "password123"}

@when('I authenticate in the API with valid credentials')
def step_impl(context):
    context.response = auth_request(context, context.credentials)

@then('I should receive a valid token')
def step_impl(context):
    assert context.response.status_code == 200, f"Código de estado esperado 200, pero se recibió {context.response.status_code}"
    response_json = context.response.json()
    assert "token" in response_json, "No se encontró 'token' en la respuesta"
    context.token = response_json["token"]

@given('I have invalid credentials')
def step_impl(context):
    context.credentials = {"username": "invalid", "password": "invalid"}

@when('I authenticate in the API with invalid credentials')
def step_impl(context):
    context.response = auth_request(context, context.credentials)

@then('I should receive an error message')
def step_impl(context):
    assert context.response.status_code == 200, f"Código de estado esperado 200, pero se recibió {context.response.status_code}"
    response_json = context.response.json()
    assert "reason" in response_json, "No se encontró 'reason' en la respuesta"
    assert response_json["reason"] == "Bad credentials", f"Mensaje de error esperado 'Bad credentials', pero se recibió '{response_json['reason']}'"