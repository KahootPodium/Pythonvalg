import network, socket, ujson

symbols = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"
candidates = []

tokens = []
votes = [""] * len(tokens)

main = """
<!DOCTYPE html>
<html>
  <head>
    <title>Valgomat</title>
  </head>
</html>
"""
results = """
<!DOCTYPE html>
<html>
  <head>
    <title>Valgresultat</title>
  </head>
</html>
"""

ssid = "Valgomat"
password = "Valg2025"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ip = "192.168.1.50"
subnet = "255.255.255.0"
gateway = "192.168.1.1"
dns = "8.8.8.8"

wlan.ifconfig((ip, subnet, gateway, dns))
wlan.connect(ssid, password)

print("Connecting to Wi-Fi...")

while not wlan.isconnected():
    pass

print("Connected with wlantic IP:", wlan.ifconfig()[0])

listener = socket.socket()
listener.bind(("0.0.0.0", 80))
listener.listen(5)

print("Listening on port 80")

while True:
    try:
        client, address = listener.accept()
        request = client.recv(1024).decode()

        path = request.split("\n")[0].split(" ")[1]

        if path == "/":
            client.send("HTTP/1.1 200 OK" + "\n\n" + main)

        elif path == "/results":
            client.send("HTTP/1.1 200 OK" + "\n\n" + result)

        elif path == "/token":
            try:
                body = request.split("\n")[-1]
                data = ujson.loads(body)

                if data["token"] in tokens:
                    status = "HTTP/1.1 200 OK"

                else:
                    status = "HTTP/1.1 401 Unauthorized"
                  
            except:
                status = "HTTP/1.1 400 Bad Request"

            client.send("\n".join([status, "Access-Control-Allow-Origin: *", "Access-Control-Allow-Headers: *"]))

        elif path == "/vote":
            try:
                body = request.split("\n")[-1]
                data = ujson.loads(body)

                token = data["token"]
                candidate = data["candidate"]

                group = (symbols.index(token[-1]) - symbols.index(token[-2])) % (len(symbols) - 1) - 1

                if votes[tokens.index(token)] == "":
                    if token in tokens and candidate in candidates[group]:
                        votes[tokens.index(token)] = candidate

                        status = "HTTP/1.1 200 OK"

                    else:
                        status = "HTTP/1.1 401 Unauthorized"

                else:
                    status = "HTTP/1.1 409 Conflict"

            except:
                status = "HTTP/1.1 400 Bad Request"

            client.send("\n".join([status, "Access-Control-Allow-Origin: *", "Access-Control-Allow-Headers: *"]))

        elif path == "/statistics":
            names = sorted(candidate for group in candidates for candidate in group)
            response = ujson.dumps({name: votes.count(name) for name in names})

            client.send("\n".join(["HTTP/1.1 200 OK", "Access-Control-Allow-Origin: *", "Access-Control-Allow-Headers: *", "", response]))

        client.close()

    except:
        pass
