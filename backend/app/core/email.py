import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
SMTP_USERNAME = settings.SMTP_USERNAME
SMTP_PASSWORD = settings.SMTP_PASSWORD

def enviar_email(destinatario: str, assunto: str, mensagem: str):
    
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(mensagem, "html"))

    try:
        print(SMTP_USERNAME + " / " + SMTP_PASSWORD)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, destinatario, msg.as_string())
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")