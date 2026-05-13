import network, socket, ujson

symbols = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"
candidates = []

tokens = []
votes = [""] * len(tokens)

main = """
<!DOCTYPE html>
<html>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width">
  <title>Valgomat</title>
  <style>
    body {
      font-family: system-ui;
      background: #f7f7f7;
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0;
    }

    main {
      width: 280px;
      padding: 2rem;
      border-radius: 12px;
      background: white;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .title {
      margin-top: 0;
      margin-bottom: 0.4rem;
      font-size: 1.2rem;
      color: #333;
    }

    .text {
      width: 100%;
      font-size: 1rem;
      border-radius: 8px;
      margin-top: 0.8rem;
      margin-bottom: 0.2rem;
      box-sizing: border-box;
    }

    input {
      padding: 0.5rem;
      border: 1px solid #ccc;
    }
    button {
      padding: 0.6rem;
      border: none;
      cursor: pointer;
      color: white;
      background: #0077ff;
    }

    button:hover {
      background: #005fcc;
    }

    select {
    padding: 0.5rem;
    }
  </style>
  <body>
    <main>
      <h1 class="title">Skriv inn engangskoden</h1>
      <form id="form" autocomplete="off">
        <input class="text" type="text" id="input" name="token">
        <button class="text" type="submit">Logg inn</button>
      </form>
    </main>
  </body>
  <script>
    document.body.style.height = /Mobi/i.test(navigator.userAgent) ? "90vh" : "100vh";

    function resize() {document.documentElement.style.zoom = Math.min(1, window.innerWidth / 420)}
    resize();

    window.addEventListener("resize", resize);

    const form = document.getElementById("form");
    const input = document.getElementById("input");

    input.oninput = () => input.style.background = "white";

    form.addEventListener("submit", async (deafult) => {
        deafult.preventDefault();

        const input = form.querySelector("input");
        const select = form.querySelector("select");
        const button = form.querySelector("button");

        if (button.disabled) return;
        button.disabled = true;

        try {
            if (input) {
                if (!input.value) return;
                const response = await fetch("http://192.168.1.50/token", {method: "POST", body: JSON.stringify({token: input.value})});

                if (response.ok) {
                    alert("Du er nå logget inn");

                    document.querySelector(".title").textContent = "Velg en kandidat";
                    document.querySelector("button").textContent = "Stem";

                    token = input.value;
                    input.remove();

                    const select = document.createElement("select");
                    select.className = "text";
                    select.name = "candidate";

                    const symbols = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!";

                    const candidates = [
                        ["Abdullah", "Einar", "Iver", "Mads"],
                        ["Ismaeel", "Maxine", "Samuel", "Sondre"],
                        ["Karim", "Kritika"],
                        ["Johannes", "Nicoline"]
                    ];

                    const group = ((symbols.indexOf(token.at(-1)) - symbols.indexOf(token.at(-2))) % (symbols.length - 1) + (symbols.length - 1)) % (symbols.length - 1) - 1;
                    candidates[group].forEach(name => select.appendChild(new Option(name, name)));

                    form.insertBefore(select, button);
                } else {input.style.backgroundColor = "#ffe8e8"}

            } else if (select) {
                const response = await fetch("http://192.168.1.50/vote", {method: "POST", body: JSON.stringify({token: token, candidate: select.value})});

                if (response.ok) {
                    alert("Stemmen din er registrert");
                    window.location.replace("/results");

                } else {alert("Du har allerede stemt")}
            }

    } catch (error) {
        console.log(error);

        if (input) input.style.backgroundColor = "#fff4e8";
        else alert("Noe gikk galt. Prøv igjen");

    } finally {button.disabled = false}
    });
  </script>
</html>
"""
results = """
<!DOCTYPE html>
<html>
  <meta name="viewport" content="width=device-width">
  <title>Valgresultat</title>
  <style>
    body {
      font-family: system-ui;
      background: #f7f7f7;
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0;
    }

    main {
      width: 280px;
      padding: 2rem 2rem 1.5rem;
      border-radius: 12px;
      background: white;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .title {
      margin-top: 0;
      margin-bottom: 1.2rem;
      font-size: 1.2rem;
      color: #333;
    }

    ul {
      padding: 0;
      margin: 0;
    }

    row {
      padding: 0.7rem 0;
      border-bottom: 1px solid #eee;

      display: flex;
      align-items: center;
      gap: 1rem;
    }

    row:last-child {
        border-bottom: none;
    }

    .container {
      flex-grow: 1;
      background: #eee;
      border-radius: 8px;
      height: 16px;
    }

    .bar {
      height: 100%;
      background: #0077ff;
      border-radius: 8px;
    }

    .votes {
      width: 1rem;
      text-align: right;
    }
  </style>
  <body>
    <main>
      <h1 class="title"></h1>
      <ul id="votes"></ul>
    </main>
  </body>
  <script type="module">
    document.body.style.height = /Mobi/i.test(navigator.userAgent) ? "90vh" : "100vh";

    function resize() {document.documentElement.style.zoom = Math.min(1, window.innerWidth / 420)}
    resize();

    window.addEventListener("resize", resize);

    try {
        const response = await fetch("http://192.168.1.50/statistics");
        const stats = await response.json();

        document.querySelector(".title").textContent = "Valgresultat";

        const list = document.getElementById("votes");
        list.innerHTML = "";

        for (const [name, votes] of Object.entries(stats)) {
          const row = document.createElement("row");
          const span = document.createElement("span");

          span.textContent = name;
          span.style.width = "70px";

          const container = document.createElement("div");
          container.className = "container";

          const bar = document.createElement("div");
          bar.className = "bar";
          bar.style.width = `${(votes / Math.max(...Object.values(stats), 1)) * 100}%`;

          container.appendChild(bar);

          const votesSpan = document.createElement("span");
          votesSpan.className = "votes";
          votesSpan.textContent = votes;

          row.appendChild(span);
          row.appendChild(container);
          row.appendChild(votesSpan);

          list.appendChild(row);
        }
      } catch (error) {document.getElementById("votes").innerHTML = "<row>Could not access statistics</li>"; console.log(error)}
  </script>
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

