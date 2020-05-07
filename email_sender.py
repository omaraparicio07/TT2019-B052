import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, filename='server.log')

def send_email(email_user,password_user, name_user,forget_pass=False):

  msg = MIMEMultipart('alternative')
  msg['Subject'] = "Test Email"
  msg['From'] = "Scheme Converter Tool"
  msg['To'] = email_user

  html_new = """\
  <html>
  <head></head>
  <body>
    <p>Hi! Welcome tt - 2019 - b052<br>
       How are you?<br>
       name:%s<br>
       password:%s
    </p>
  </body>
  </html>
  """ %(name_user,str(password_user))

  html_recoverypass = """\
  <html>
  <head></head>
  <body>
    <p>Hi! Recovery password <br>
       How are you? <br>
       New password ...<br>
       name:%s<br>
       password:%s
    </p>
  </body>
  </html>
  """ %(name_user,str(password_user))

  message = MIMEText(html_recoverypass, 'html') if forget_pass else MIMEText(html_new, 'html')
  msg.attach(message)

  try:
    username = 'omaraparicio07@gmail.com'
    password = 'rxazsvxafzjspevx'
    smtp = smtplib.SMTP('smtp.gmail.com:587')
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail("OMAR",email_user, msg.as_string())
    smtp.quit()
    logging.info("Correo enviado corrrectamente a la dirección : %s", email_user)
    return 200
  except:
    logging.error("Ocurrio un error al enviar correo a la dirección : %s", email_user)
    return 500
