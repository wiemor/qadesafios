from appium import webdriver
from appium.options.android import UiAutomator2Options

def before_all(context):
    capabilities = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'adbExecTimeout': 250000,
        "platformVersion": "11",  
        'deviceName': 'emulador-5554', 
        'app': 'C:\\codes\\qadesafios\\Desafio02\\app\\booking-com-32-9.apk',
        'appPackage': 'com.booking',
        'appActivity': 'com.booking.startup.HomeActivity',
        'noReset': True,
        'fullReset': False,
        'autoGrantPermissions': True,
        'allowTestPackages': True,
        'ignoreHiddenApiPolicyError': True,
    }

    options = UiAutomator2Options().load_capabilities(capabilities)

    try:
        print("Attempting to connect to Appium server...")
        context.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        print("Connection successful, setting implicit wait...")
        context.driver.implicitly_wait(30)
        print("Driver setup complete")
    except Exception as e:
        print(f"Failed to set up driver: {e}")
        raise e

def after_all(context):
    if hasattr(context, 'driver'):
        context.driver.quit()
    else:
        print("No driver to quit")