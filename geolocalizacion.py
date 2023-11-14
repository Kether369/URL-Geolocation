from flask import Flask, request, render_template
import requests
from user_agents import parse
from datetime import datetime

from flask import Flask, request, render_template
from correo import enviar_correo  

app = Flask(__name__)

# Almacenar los tokens generados en un diccionario (esto es solo para ejemplo)
tokens = {}

# Función para obtener la dirección IP pública del usuario
def obtener_direccion_ip_publica():
    try:
        url = 'https://api.ipify.org?format=json'
        response = requests.get(url)
        data = response.json()
        return data['ip']
    except Exception as e:
        print(f"Error al obtener la dirección IP pública: {str(e)}")
        return None

# Función para obtener la información de geolocalización de una dirección IP utilizando la API de ip-api.com
def obtener_geolocalizacion(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pais = data.get('country', 'Desconocido')
            ciudad = data.get('city', 'Desconocido')
            direccion = data.get('regionName', 'Desconocido')
            codigo_postal = data.get('zip', 'Desconocido')
            zona_horaria = data.get('timezone', 'Desconocido')
            organizacion = data.get('org', 'Desconocido')
            codigo_as = data.get('as', 'Desconocido')
            nombre_as = data.get('asname', 'Desconocido')
            proxy = data.get('proxy', 'Desconocido')
            hosting = data.get('hosting', 'Desconocido')
            latitud = data.get('lat', 'Desconocido')
            longitud = data.get('lon', 'Desconocido')
            privacidad = 'Desconocido'  # ip-api.com no proporciona información de privacidad
            dispositivo, navegador = obtener_info_dispositivo_navegador()
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return pais, ciudad, direccion, codigo_postal, zona_horaria, organizacion, codigo_as, nombre_as, proxy, hosting, latitud, longitud, privacidad, dispositivo, navegador, ip, fecha_hora
    except Exception as e:
        print(f"Error al obtener información de geolocalización: {str(e)}")
    return 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido', 'Desconocido'

    email = token_info['email']
    mensaje = "Esto es un mensaje de prueba enviado desde la URL generada."
    asunto = "Mensaje desde la URL generada"
    enviar_correo(email, asunto, mensaje)

# Función para obtener la información de dispositivo y navegador del usuario
def obtener_info_dispositivo_navegador():
    user_agent = request.headers.get('User-Agent')
    ua = parse(user_agent)
    dispositivo = ua.device.family
    navegador = ua.browser.family
    return dispositivo, navegador

# Ruta para la página principal donde se generará el token
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token = request.form['token']
        email = request.form['email']
        # Guardar el token y el correo en el diccionario (puedes almacenarlo en una base de datos en futuras versiones)
        tokens[token] = {'email': email}
        # Generar la URL basada en el token (esto es solo para ejemplo)
        url_generada = f"/mi_URL/{token}"
        return render_template('url_generada.html', url_generada=url_generada)
    return render_template('index.html')

# Ruta para acceder al token generado y mostrar la geolocalización del amigo
@app.route('/mi_URL/<string:token>')
def canary_token(token):
    # Obtiene la información asociada al token desde el diccionario
    token_info = tokens.get(token)
    if not token_info:
        return "Token no válido."

    email = token_info['email']
    
    

    # Obtiene la dirección IP del dispositivo del amigo que accedió al token
    direccion_ip_amigo = request.headers.get('X-Forwarded-For')
    if not direccion_ip_amigo:
        direccion_ip_amigo = obtener_direccion_ip_publica()

    if direccion_ip_amigo:
        # Obtener geolocalización del amigo utilizando la API de ip-api.com
        pais, ciudad, direccion, codigo_postal, zona_horaria, organizacion, codigo_as, nombre_as, proxy, hosting, latitud, longitud, privacidad, dispositivo, navegador, ip, fecha_hora = obtener_geolocalizacion(direccion_ip_amigo)

        # Mostrar la geolocalización en la terminal
        print("País:", pais)
        print("Ciudad:", ciudad)
        print("Dirección:", direccion)
        print("Código Postal:", codigo_postal)
        print("Zona Horaria:", zona_horaria)
        print("Organización:", organizacion)
        print("Código AS:", codigo_as)
        print("Nombre AS:", nombre_as)
        print("Proxy:", proxy)
        print("Hosting:", hosting)
        print("Latitud:", latitud)
        print("Longitud:", longitud)
        print("Privacidad:", privacidad)
        print("Dispositivo:", dispositivo)
        print("Navegador:", navegador)
        print("IP:", direccion_ip_amigo)
        print("Fecha y Hora:", fecha_hora)

        # Redirigir al amigo a una página diferente (por ejemplo, Google)
        return '<script>window.location.href = "https://www.google.com";</script>'
    else:
        return "Error al obtener la geolocalización. Por favor, inténtalo de nuevo más tarde."

# ...

if __name__ == '__main__':
    app.run(port=8080)
