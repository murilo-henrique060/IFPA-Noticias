# That module is used to send html emails.
def sendEmail(message_html):
    from decouple import config
    from smtplib import SMTP
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    host = config('host')
    port = config('port', cast=int)
    user = config('user')
    password = config('password')
    to = config('to')
    title = config('title')

    server = SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(user, password)

    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = to
    email_msg['Subject'] = title

    email_msg.attach(MIMEText(message_html, 'html'))

    server.sendmail(email_msg['From'], to.split(', '), email_msg.as_string())

    server.quit()