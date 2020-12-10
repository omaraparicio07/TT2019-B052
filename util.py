import logging
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(level=logging.DEBUG)

def send_email(email_user,password_user, name_user,subject=False ,forget_pass=False):

  msg = MIMEMultipart('alternative')
  msg['Subject'] = 'Recovery Pass' if subject else 'Welcome'
  msg['From'] = "Scheme Converter Tool"
  msg['To'] = email_user

  html_new = """\
  <html>
  <head></head>
  <body>
    <p>Hola! <b>Como te encuentras el día de hoy?</b><br><br>
      Te damos la bienvenida al trabajo terminal 2019-B052<br><br>
      &nbsp;&nbsp;&nbsp;&nbsp;Usuario : %s<br>
      &nbsp;&nbsp;&nbsp;&nbsp;Contraseña : %s
    </p>
  </body>
  </html>
  """ %(name_user,str(password_user))

  html_recoverypass = """\
  <html>
  <head></head>
  <body>
    <p>Hola! <b>Bienvenido de vuelta </b><br><br>
    ¿Has cambiado tu contraseña??<br><br>
    &nbsp;&nbsp;&nbsp;&nbsp;Usuario : %s<br>
    &nbsp;&nbsp;&nbsp;&nbsp;Nueva contraseña : %s
    </p>
  </body>
  </html>
  """ %(name_user,str(password_user))

  message = MIMEText(html_recoverypass, 'html')if forget_pass else MIMEText(html_new, 'html')
  msg.attach(message)

  try:
    username = 'omaraparicio07@gmail.com'
    password = 'rxazsvxafzjspevx'
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail('trabajo_terminal@ipn.mx',email_user, msg.as_string())
    smtp.quit()
    logging.info("Correo enviado corrrectamente a la dirección : %s", email_user)
    return 200
  except Exception as e:
    logging.error("Ocurrio un error al enviar correo a la dirección : %s", email_user)
    logging.error(e)
    return 500

def validate_email(email_address):
  # Regex para validar correo, puede probar la expresion regular en el sitio https://pythex.org/
  regex = re.compile('[a-z]([\w\+-]?\.?)+[a-z0-9]@[a-z]\w{2,}\.[a-z]{2,}')
  email_valid = regex.match(email_address)
  return bool(email_valid)
