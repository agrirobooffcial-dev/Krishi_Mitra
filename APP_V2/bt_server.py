import socket

def bluetooth_server(on_command):
    server = socket.socket(
        socket.AF_BLUETOOTH,
        socket.SOCK_STREAM,
        socket.BTPROTO_RFCOMM
    )

    server.bind(("54:9A:8F:19:7A:EE", 1))   # RFCOMM channel 1
    server.listen(1)

    print("🔵 Bluetooth RFCOMM socket listening on channel 1")

    client, addr = server.accept()
    print("✅ Connected to", addr)

    try:
        while True:
            data = client.recv(1024)
            if not data:
                break

            command = data.decode().strip()
            print("📩 Received:", command)
            on_command(command)

    except Exception as e:
        print("❌ Bluetooth error:", e)

    finally:
        client.close()
        server.close()
