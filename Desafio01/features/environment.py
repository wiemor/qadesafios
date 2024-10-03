from behave import fixture, use_fixture

@fixture
def booking_fixture(context):
    context.booking_id = None
    context.booking_details = {}
    context.new_booking_details = {}
    yield


def before_all(context):
    context.shared_data = {}
    context.base_url = "https://restful-booker.herokuapp.com"
    context.endpoints = {
        "auth": f"{context.base_url}/auth",
        "booking": f"{context.base_url}/booking",
        "ping": f"{context.base_url}/ping"
    }

def before_scenario(context, scenario):
    use_fixture(booking_fixture, context)

def after_scenario(context, scenario):
    attributes_to_share = ["booking_details", "new_booking_details", "booking_id", "token"]
    
    for attr in attributes_to_share:
        if hasattr(context, attr):
            context.shared_data[attr] = getattr(context, attr)

def after_feature(context, feature):
    if hasattr(context, "token"):
        context.shared_data["token"] = context.token