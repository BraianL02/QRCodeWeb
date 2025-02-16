from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from QRcode_functions import generate_qr, verify_link, get_dir

app = Flask(__name__)

colors = [
    "black", "white","red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "magenta", 
    "brown", "gray", "gold", "lime", "navy", "teal", "maroon",
    "violet", "indigo", "turquoise", "salmon", "coral", "khaki", "plum"
]
# logos = os.listdir(os.path.abspath(f"{get_dir()}/static/Logos/"))
logos = [logo.replace(".png", "") for logo in os.listdir(os.path.abspath(f"{get_dir()}/static/Logos/"))]
@app.route("/", methods=["GET","POST"])
def home():
    qr_name=""
    if request.method == "POST": # verifica si se está enviando un formulario con datos
        # Obtengo los datos del formulario
        qr_type = request.form["qr_type"]
        color1 = request.form["color1"]
        color2 = request.form["color2"]
        logo = request.form["logo"]     


        if qr_type == "link":
            data = request.form["url"]
            qr_name, valid = verify_link(data)
            if not valid:
                return render_template("index.html", error="El enlace no es válido")
        
        elif qr_type == "wifi":
            ssid = request.form["ssid"]
            password = request.form["password"]
            security = request.form["security"]
            hidden = request.form["hidden"]
            data = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;"
            qr_name = ssid

        generate_qr(data, get_dir(), color1, color2, logo, qr_name)
        print(f"QR generado en: {get_dir()}")
        qr_path = f"static/Output/{qr_name}.png"
        return redirect(url_for("show_qr", qr_path=qr_path))
    return render_template("index.html", qr_path=f"static/Output/{qr_name}.png", colors=colors, logos=logos)


@app.route("/generated")
def show_qr():
    qr_path = request.args.get("qr_path")  # Obtiene la imagen desde la URL
    return render_template("generated.html", qr_path=qr_path)

# if __name__ == "__main__":
#     app.run(debug=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render asigna un puerto automáticamente
    app.run(host="0.0.0.0", port=port, debug=False)