import imaplib
    import email
    import re
    import datetime

    # Configurações do Outlook
    EMAIL_ACCOUNT_OUTLOOK = "seuemail@outlook.com"
    PASSWORD_OUTLOOK = "suasenhaoutlook"
    IMAP_SERVER_OUTLOOK = "outlook.office365.com" # ou o servidor IMAP correto do outlook

    # Configurações do Gmail
    EMAIL_ACCOUNT_GMAIL = "seuemail@gmail.com"
    PASSWORD_GMAIL = "suasenhagmail"
    IMAP_SERVER_GMAIL = "imap.gmail.com"

    # Data de corte
    DATA_CORTE = datetime.datetime(2024, 3, 15) # Exemplo: 15 de março de 2024

    def obter_recibos_email(servidor, conta, senha, data_inicio=None, data_fim=None):
        """Obtém recibos de um determinado email."""
        # Código para acessar o email (Outlook ou Gmail) e buscar os recibos
        # Incluir filtros de data se data_inicio e data_fim forem fornecidos
        # Extrair dados (data e valor) e retornar lista de tuplas
        pass

    # Obter recibos do Outlook
    recibos_outlook = obter_recibos_email(IMAP_SERVER_OUTLOOK, EMAIL_ACCOUNT_OUTLOOK, PASSWORD_OUTLOOK, data_fim=DATA_CORTE)

    # Obter recibos do Gmail
    recibos_gmail = obter_recibos_email(IMAP_SERVER_GMAIL, EMAIL_ACCOUNT_GMAIL, PASSWORD_GMAIL, data_inicio=DATA_CORTE)

    # Combinar os recibos
    recibos = recibos_outlook + recibos_gmail

    # Processar e analisar os dados (usando Pandas, por exemplo)
    # ...

    # Exibir resultados
    print(recibos)