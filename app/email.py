"""Envio por HTTPS via SendGrid, sem SMTP (compatível com PythonAnywhere)."""
import requests
from flask import current_app, render_template

class EmailConfigurationError(Exception):
    pass
class EmailDeliveryError(Exception):
    pass

def send_email(to, subject, template, **context):
    cfg = current_app.config
    required = ('API_KEY', 'API_FROM', 'API_URL', 'STUDENT_EMAIL', 'FLASKY_ADMIN')
    missing = [k for k in required if not cfg.get(k)]
    if missing:
        raise EmailConfigurationError('Variáveis ausentes: ' + ', '.join(missing))
    recipients = list(dict.fromkeys([to] if isinstance(to, str) else to))
    html_body = render_template(template + '.html', **context)
    full_subject = cfg['FLASKY_MAIL_SUBJECT_PREFIX'] + subject
    payload = {
        'personalizations': [{'to': [{'email': address} for address in recipients]}],
        'from': {'email': cfg['API_FROM'], 'name': 'Flask - Semana 12'},
        'subject': full_subject,
        'content': [{'type': 'text/html', 'value': html_body}],
    }
    try:
        response = requests.post(cfg['API_URL'], headers={
            'Authorization': 'Bearer ' + cfg['API_KEY'],
            'Content-Type': 'application/json',
        }, json=payload, timeout=15)
    except requests.RequestException as exc:
        raise EmailDeliveryError('Falha de comunicação com o serviço de e-mail.') from exc
    if response.status_code != 202:
        raise EmailDeliveryError(f'SendGrid não aceitou o envio (HTTP {response.status_code}).')
    return recipients, full_subject
