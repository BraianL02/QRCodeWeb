import qrcode
from PIL import Image
import os
import re
import validators

def clear():
    if (os.name)=='posix':
        os.system('clear')
    if (os.name)=='nt':
        os.system('cls')

def verify_link(link):
    if validators.url(link): 
        name_png = link.replace("https://","")
        name_png = re.sub(r'[<>:"/\\|?*]', '_', name_png)
        is_valid = True
    else:
        is_valid = False
        name_png = ""
    return name_png,is_valid

def create_custom_qr(data, emblem_path, output_path, frnt_color, bck_color, qr_size=300):
    print(emblem_path)
    if not os.path.exists(emblem_path):
        print(f"ERROR: No se encontró el archivo {emblem_path}")
        return  # Sale de la función si el archivo no existe
    else:
        print(f"Archivo encontrado en {emblem_path}")
    # Generar el código QR
    qr = qrcode.QRCode(
        version=3,  # Tamaño del QR, ajusta para mayor capacidad (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alto nivel de corrección
        box_size=10,
        border=4,
    )
    qr.add_data(data) # Link
    qr.make(fit=True)
    
    # Crear la imagen del QR
    qr_img = qr.make_image(fill_color = frnt_color, back_color = bck_color).convert("RGBA")  # Convierte la imagen a un formato compatible con transparencia para trabajar con el emblema
    
    # Abrir el emblema
    emblem = Image.open(emblem_path).convert("RGBA")
    
    # Redimensionar el emblema para que encaje en el centro
    qr_width, qr_height = qr_img.size
    emblem_size = qr_size // 3 # Ajusta el tamaño del emblema
    emblem = emblem.resize((emblem_size, emblem_size), Image.LANCZOS) 
    
    # Calcular la posición para centrar el emblema
    pos_x = (qr_width - emblem_size) // 2
    pos_y = (qr_height - emblem_size) // 2
    
    # Pegar el emblema en el centro del QR
    qr_img.paste(emblem, (pos_x, pos_y), emblem)
    
    # Guardar el QR personalizado
    print(f"Guardando QR en: {output_path}.png")
    qr_img.save(f"{output_path}.png")
    print(f"Código QR personalizado guardado en: {output_path}")


#############################################################

# Ruta del directorio donde está el archivo .py
def get_dir():
    return os.path.dirname(os.path.abspath(__file__))


def generate_qr(data, current_dir, frnt_color, bck_color, logo, qr_name):
    emblem_path = os.path.abspath(os.path.join(current_dir, "static", "Logos", logo + ".png"))
    output_path = os.path.abspath(os.path.join(current_dir, "static","Output",qr_name))
    create_custom_qr(data, emblem_path, output_path, frnt_color, bck_color)
  

def show_img(current_dir,qr_name):
    img = Image.open( f"{current_dir}/Output/{qr_name}.png")
    img.show()
