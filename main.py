import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

host = config('host')
port = config('port', cast=int)
user = config('user')
password = config('password')
to = config('to')
title = config('title')

message_html = """
<html>
<body>
    <div class="span10 tileContent">
		<span class="subtitle"></span>
			<h2 class="tileHeadline">
	           	<a href="/publicacoes/1290-ifpa-campus-belem-abre-selecao-para-especializacao-em-linguagens-e-artes-na-formacao-docente">IFPA Campus Belém abre seleção para Especialização em Linguagens e Artes na Formação Docente</a>
	        </h2>
	        	<span class="description">
	        		<p>O Instituto Federal de Educação, Ciência e Tecnologia do Pará - IFPA Campus Belém, por meio do Curso de Linguagens e Artes na Formação Docente, torna público o Edital nº...</p>
                </span>
  	</div>
</body>
</html>
"""

server = smtplib.SMTP(host, port)
server.ehlo()
server.starttls()
server.login(user, password)

email_msg = MIMEMultipart()
email_msg['From'] = user
email_msg['To'] = to
email_msg['Subject'] = title

email_msg.attach(MIMEText(message_html, 'html'))

server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

server.quit()

while True:
    pass