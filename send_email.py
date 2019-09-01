from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    from_email="matburauto@gmail.com"
    from_password="Bonzai12"
    to_email = email

    subject="Dane odnośnie Twojego wzrostu"
    message="Hej twój wzrost to <strong>%s</strong>. <br> Średni wzrost wszystkich respondentów to %s, do tej pory wzięło udział ,%s osób." \
            "<br> Dziękuje za Twój udział w ankiecie!" % (height, average_height, count)

    msg=MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail=smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)


