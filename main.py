# Network programming in general:
# 1. Choosing a device to communicate with
# 2. Figuring out hot to communicate with it
# 3. Making an outgoing connection
# 4. Accepting an incoming connection
# 5. Sending data
# 6. Receiving data


# 1. Choosing a communication partner
import bluetooth
from bluetooth import discover_devices, SERIAL_PORT_CLASS


def scan():
    print("Looking for devices...")
    nearby_devices = discover_devices(lookup_names=True)  # default scan time = 8s
    print("Found {len} devices".format(len=len(nearby_devices)))
    device_address = ""
    if len(nearby_devices) > 0:
        for addr, name in nearby_devices:
            print("Device's name: {name} - Device's address: {address}".format(name=name, address=addr))
        device_address = choose_device(nearby_devices)
    return device_address


def choose_device(nearby_devices):
    connected_device = input("Please choose a device or an address to connect: ")
    for addr, name in nearby_devices:
        if connected_device == addr or connected_device == name:
            print("Connected to {device} with the address {address}".format(device=name, address=addr))
            return addr
        else:
            print("No such device found.")
            return choose_device(nearby_devices)


# 2. Figuring out hot to communicate with it
def server():
    # 2.1. Choosing a transport protocol
    # There are 2 bluetooth protocols: RFCOMM and L2CAP.
    # RFCOMM provides the same service and reliability guarantees as TCP
    # While L2CAP is like UDP
    # host_bluetooth_address = '38:00:25:6D:BA:95'
    server_socket = bluetooth.BluetoothSocket()  # Create a socket object with the default protocol RFCOMM

    # bind to a tuple (address, port number) NOTICE: the port number must be even and between 1 to 30.
    # https://stackoverflow.com/questions/53685194/oserror-the-requested-address-is-not-valid-in-its-context
    server_socket.bind(("", 18))
    server_socket.listen(1)

    # port = server_socket.getsockname()[1]
    #
    # uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    # bluetooth.advertise_service(server_socket, "Sample server", service_id=uuid,
    #                             service_classes=[uuid, SERIAL_PORT_CLASS],
    #                             profiles=[SERIAL_PORT_CLASS])
    #
    # print("Waiting for connection on RFCOMM channel", port)

    print("Waiting for connection......")
    client_socket, client_info = server_socket.accept()
    print("Accepted connection from", client_info)

    try:
        while True:
            data = client_socket.recv(1024)  # max size of 1024kb
            if not data:
                break
            print("Received", data)
    except OSError:
        pass

    print("Disconnected.")

    client_socket.close()
    server_socket.close()
    print("All done.")


def main():
    # scan()
    server()


if __name__ == "__main__":
    main()
