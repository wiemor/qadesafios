from appium import webdriver
from appium.options.android import UiAutomator2Options

def before_scenario(context, scenario):
    capabilities = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'emulator-5554', 
        'app': 'C:\\codes\\qadesafios\\Desafio02\\app\\booking-com-32-9.apk',
        "appPackage": "com.booking",
        "appActivity": "com.booking.activities.MainActivity",
        'noReset': True
    }

    options = UiAutomator2Options().load_capabilities(capabilities)

    try:
        context.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        context.driver.implicitly_wait(10)
        print("Driver setup successful")
    except Exception as e:
        print(f"Failed to set up driver: {e}")
        raise

def after_scenario(context, scenario):
    print("Tearing down the driver after scenario:", scenario.name)
    if hasattr(context, 'driver'):
        context.driver.quit()
    else:
        print("No driver to quit")