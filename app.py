from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/updateip")
def updateip():
    return render_template("index.html")

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
        return jsonify({
            "ok": False,
            "message": "Falta key o IP"
        }), 400

    print(f"KEY REGISTRADA: {key} | IP: {ip}")

    return jsonify({
        "ok": True,
        "message": f"Key registrada con IP {ip}"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
