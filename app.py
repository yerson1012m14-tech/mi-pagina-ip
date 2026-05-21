from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Registro de Key e IP</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    body {
      margin: 0;
      background: #090909;
      color: white;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }

    .box {
      width: 92%;
      max-width: 420px;
      background: #151515;
      padding: 25px;
      border-radius: 18px;
      box-shadow: 0 0 25px rgba(255, 0, 0, 0.35);
      border: 1px solid #ff1a1a;
    }

    h1 {
      text-align: center;
      color: #ff1a1a;
      margin-bottom: 20px;
      font-size: 24px;
    }

    label {
      font-size: 14px;
      margin-top: 14px;
      display: block;
    }

    input {
      width: 100%;
      padding: 13px;
      border-radius: 10px;
      border: 1px solid #333;
      background: #050505;
      color: white;
      margin-top: 6px;
      box-sizing: border-box;
      font-size: 15px;
    }

    button {
      width: 100%;
      padding: 14px;
      border: none;
      border-radius: 10px;
      margin-top: 15px;
      background: #ff1a1a;
      color: white;
      font-weight: bold;
      font-size: 16px;
      cursor: pointer;
    }

    button:hover {
      background: #cc0000;
    }

    .msg {
      margin-top: 15px;
      text-align: center;
      font-size: 14px;
      color: #00ff88;
    }
  </style>
</head>

<body>
  <div class="box">
    <h1>JASON XIT</h1>

    <label>KEY</label>
    <input id="key" placeholder="Pega tu key aquí">

    <label>Dirección IP</label>
    <input id="ip" placeholder="Pulsa buscar IP" readonly>

    <button onclick="buscarIP()">BUSCAR IP</button>
    <button onclick="registrar()">REGISTRAR KEY E IP</button>

    <div class="msg" id="msg"></div>
  </div>

<script>
async function buscarIP() {
  const msg = document.getElementById("msg");
  msg.textContent = "Buscando IP...";

  try {
    const res = await fetch("/api/ip", { cache: "no-store" });
    const data = await res.json();

    document.getElementById("ip").value = data.ip || "";
    msg.textContent = "IP detectada correctamente";
  } catch (e) {
    msg.textContent = "No se pudo buscar la IP";
  }
}

async function registrar() {
  const key = document.getElementById("key").value.trim();
  const ip = document.getElementById("ip").value.trim();
  const msg = document.getElementById("msg");

  if (!key) {
    msg.textContent = "Falta la key";
    return;
  }

  if (!ip) {
    msg.textContent = "Primero busca la IP";
    return;
  }

  const res = await fetch("/api/register", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({key, ip})
  });

  const data = await res.json();
  msg.textContent = data.message || "Registrado";
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/updateip")
def updateip():
    return render_template_string(HTML)

@app.route("/api/ip")
def obtener_ip():
    ip = (
        request.headers.get("X-Real-IP")
        or request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For")
        or request.remote_addr
    )

    if ip and "," in ip:
        ip = ip.split(",")[0].strip()

    return jsonify({"ip": ip})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(force=True)

    key = data.get("key", "").strip()
    ip = data.get("ip", "").strip()

    if not key or not ip:
        return jsonify({"ok": False, "message": "Falta key o IP"}), 400

    print(f"KEY REGISTRADA: {key} | IP: {ip}")

    return jsonify({
        "ok": True,
        "message": f"Key registrada con IP {ip}"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)