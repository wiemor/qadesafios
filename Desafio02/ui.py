from uiautomator import Device

# Connect to the device
print("device")
d = Device('emulador-5554')

# Find a UI element
print("ui")

ui_element = d(text='')

print("ui_element", ui_element)

print("ui_element.info", ui_element.info)

print("properties")

# Print properties
print(f"Text: {ui_element.text}")
print(f"Resource ID: {ui_element.info['resourceId']}")
print(f"Class Name: {ui_element.info['className']}")
print(f"Description: {ui_element.info['contentDescription']}")
print(f"Bounds: {ui_element.info['bounds']}")