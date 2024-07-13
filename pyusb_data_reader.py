import usb.core
import usb.util
import time

# Define the vendor and product ID
VENDOR_ID = 0x303a  # Replace with your actual Vendor ID
PRODUCT_ID = 0x0002  # Replace with your actual Product ID

# Find the USB device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError("Device not found")

# Set the active configuration
dev.set_configuration()

# Claim the interface (assuming interface 0)
interface = 0
try:
    dev.detach_kernel_driver(interface)
except Exception as e:
    pass  # If detaching fails, we continue

usb.util.claim_interface(dev, interface)

# Use the correct IN endpoint (e.g., 0x81)
endpoint = dev[0][(0, 0)][0]
# HID key code to character mapping for non-modified keys
HID_KEYCODES = {
    0x04: 'a', 0x05: 'b', 0x06: 'c', 0x07: 'd',
    0x08: 'e', 0x09: 'f', 0x0A: 'g', 0x0B: 'h',
    0x0C: 'i', 0x0D: 'j', 0x0E: 'k', 0x0F: 'l',
    0x10: 'm', 0x11: 'n', 0x12: 'o', 0x13: 'p',
    0x14: 'q', 0x15: 'r', 0x16: 's', 0x17: 't',
    0x18: 'u', 0x19: 'v', 0x1A: 'w', 0x1B: 'x',
    0x1C: 'y', 0x1D: 'z', 0x1E: '1', 0x1F: '2',
    0x20: '3', 0x21: '4', 0x22: '5', 0x23: '6',
    0x24: '7', 0x25: '8', 0x26: '9', 0x27: '0',
    0x28: '\n', 0x2C: ' ', 0x2D: '-', 0x2E: '=',
    0x2F: '[', 0x30: ']', 0x33: ';', 0x34: '\'',
    0x36: ',', 0x37: '.', 0x38: '/', 0x2A: '[BACKSPACE]'
}

# Function to decode and print HID keyboard reports
def decode_hid_report(report):
    chars = []
    for i in range(2, 8):
        key_code = report[i]
        if key_code in HID_KEYCODES:
            chars.append(HID_KEYCODES[key_code])
    return ''.join(chars)
# Function to read data from the HID device
def read_hid_data():
    d=""
    while True:
        try:
            # Read data (adjust endpoint address and size as needed)
            data = dev.read(endpoint.bEndpointAddress, 64, timeout=5000)
            temp=decode_hid_report(data)
            if(temp!='\n'):
                d+=temp
            else:
                print(d)
                d=""
        except usb.core.USBError as e:
            if e.args == ('Operation timed out',):
                continue
            print(f"USB Error: {e}")
            break

try:
    read_hid_data()
except KeyboardInterrupt:
    print("Measurement stopped by user")
finally:
    # Release the interface
    usb.util.release_interface(dev, interface)
    usb.util.dispose_resources(dev)

