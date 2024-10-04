from behave import given, when, then
from appium.webdriver.common.appiumby import AppiumBy

@given('estoy en el home')
def step_impl(context):
    assert context.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Booking.com']").is_displayed()
    assert context.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Stays']").is_displayed()
    assert context.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@text='Enter your destination']").is_displayed()

@when('busco hoteles en {city}')
def step_impl(context, city):
    search_box = context.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@text='Enter your destination']")
    search_box.click()
    search_box.send_keys(city)
    
    date_field = context.driver.find_element(AppiumBy.XPATH, "//android.view.View[@content-desc='Fri, Aug 19 - Sat, Aug 20']")
    date_field.click()
    
    start_date = context.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "14 February 2023")
    start_date.click()
    
    end_date = context.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "28 February 2023")
    end_date.click()
    
    confirm_dates = context.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Select']")
    confirm_dates.click()
    
    guests_field = context.driver.find_element(AppiumBy.XPATH, "//android.view.View[@content-desc='1 room · 2 adults · 0 children']")
    guests_field.click()
    
    add_child = context.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@content-desc='Increase number of children']")
    add_child.click()
    
    child_age_dropdown = context.driver.find_element(AppiumBy.XPATH, "//android.widget.Spinner[@content-desc='Select age of child 1']")
    child_age_dropdown.click()
    age_5 = context.driver.find_element(AppiumBy.XPATH, "//android.widget.CheckedTextView[@text='5 years old']")
    age_5.click()
    
    confirm_guests = context.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Apply']")
    confirm_guests.click()

    search_button = context.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Search']")
    search_button.click()

@when('selecciono el primer hotel disponible')
def step_impl(context):
    context.driver.implicitly_wait(10)
    first_hotel = context.driver.find_element(AppiumBy.XPATH, "(//android.view.ViewGroup[@resource-id='com.booking:id/property_card_container'])[1]")
    
    hotel_name = first_hotel.find_element(AppiumBy.XPATH, ".//android.widget.TextView[@text='Hotel Hacienda Cusco Centro Historico']")
    assert hotel_name.is_displayed()
    
    breakfast_included = first_hotel.find_element(AppiumBy.XPATH, ".//android.widget.TextView[@text='Breakfast included']")
    assert breakfast_included.is_displayed()
    
    rating = first_hotel.find_element(AppiumBy.XPATH, ".//android.widget.TextView[@text='Very Good']")
    assert rating.is_displayed()
    
    first_hotel.click()

@when('completo el proceso de booking')
def step_impl(context):
    book_button = context.driver.find_element(AppiumBy.ID, "com.booking:id/book_button")
    book_button.click()
    context.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@text='First Name *']").send_keys("Jose")
    context.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@text='Last Name *']").send_keys("Hurtado")
    context.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@text='Email Address *']").send_keys("josehurtado@gmail.com")
    context.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@text='Country/Region *']").send_keys("Colombia")
    context.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[@text='Mobile Phone *']").send_keys("930731660")
    context.driver.find_element(AppiumBy.XPATH, "//android.widget.RadioButton[@text='Leisure']").click()
    next_step_button = context.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='Next step']")
    next_step_button.click()


@then('deberia ver la confirmación')
def step_impl(context):
    context.driver.implicitly_wait(10)
    confirmation_message = context.driver.find_element(AppiumBy.ID, "com.booking:id/confirmation_message")
    assert confirmation_message.is_displayed()