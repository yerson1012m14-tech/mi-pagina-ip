from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "JASON XIT PAGINA ONLINE"

@app.route("/updateip")
def updateip():
    return "UPDATE IP FUNCIONANDO"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
