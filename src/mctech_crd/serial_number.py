import os.path
import uuid


def get_file_path():
    script_dir = os.path.expanduser('~/.cosmic')
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
    rel_path = "serial_number.txt"
    return os.path.normpath(os.path.join(script_dir, rel_path))


def create_serial_number():
    try:
        serial_number = str(uuid.uuid4())
        print("creating serial number ", serial_number)
        serial_number_file = open(get_file_path(), "w")
        serial_number_file.write(serial_number)
        serial_number_file.close()
    except Exception as e:
        print("Error:\n", e)
        raise Exception("Error: writing serial number to file")


def read_serial_number():
    try:
        serial_number_file = open(get_file_path(), "r")
        serial_number = serial_number_file.read()
        serial_number_file.close()
        return serial_number
    except Exception as e:
        print("Error:\n", e)
        raise Exception("Error: reading serial from file")


def get_MAC(interface="eth0"):
    # Return the MAC address of the specified interface
    try:
        str = open("/sys/class/net/%s/address" % interface).read()
        return str[0:17]
    except Exception as e:
        print("Could not get MAC address for ", interface, " because ", e)
        return False


def get_serial_number():
    mac = get_MAC()
    if mac != False:
        return mac
    if os.path.isfile(get_file_path()) == False:
        create_serial_number()
    return read_serial_number()
