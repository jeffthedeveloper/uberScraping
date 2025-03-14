import imaplib
import email
import re

# Configurações do email
EMAIL_ACCOUNT = "seuemail@gmail.com"
PASSWORD = "suasenha"
IMAP_SERVER = "imap.gmail.com"

def obter_recibos_uber():
    """Obtém recibos da Uber do email."""

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.select("inbox")

    _, data = mail.search(None, '(FROM "uber" SUBJECT "Recibo da Uber")')  # Adaptar para o assunto exato

    recibos = []

    for num in data[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                for part in msg.walk():
                    if part.get_content_type() == "text/plain": # ou "text/html"
                        body = part.get_payload(decode=True).decode()
                        data_viagem = re.search(r'\d{2} de \w+ de \d{4}', body) # Usar regex para buscar a data
                        valor_viagem = re.search(r'R\$ ([\d,]+)', body) # Regex para buscar o valor
                        if data_viagem and valor_viagem:
                            recibos.append((data_viagem.group(0), valor_viagem.group(1).replace(',', '.'))) # Adiciona em formato (data, valor)

    mail.close()
    mail.logout()

    return recibos

recibos = obter_recibos_uber()

# Agora você tem uma lista de tuplas com (data, valor). Use Pandas para organizar e calcular os gastos.

print(recibos)