import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destinatario, asunto, mensaje):
    # Configura el servidor SMTP y credenciales de correo (Gmail en este ejemplo)
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    usuario_smtp = 'seguridadpacogarcia@gmail.com'
    contraseña_smtp = 'no bebas agua del lete'

    # Resto del código de la función enviar_correo...


    # Crea el mensaje de correo
    msg = MIMEMultipart()
    msg['From'] = usuario_smtp
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agrega el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    # Establece la conexión con el servidor SMTP
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()  # Iniciar el cifrado TLS
        server.login(usuario_smtp, contraseña_smtp)
        server.sendmail(usuario_smtp, destinatario, msg.as_string())

