from flask import current_app, flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError
from . import main
from .forms import NameForm
from .. import db
from ..models import Role, User, EmailEnviado
from ..email import send_email, EmailConfigurationError, EmailDeliveryError

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        if User.query.filter_by(username=username).first():
            flash('Esse usuário já está cadastrado.', 'warning')
            return redirect(url_for('.index'))
        role = Role.query.filter_by(name='User').first()
        if role is None:
            flash('Funções não inicializadas. Execute: flask seed-roles', 'danger')
            return redirect(url_for('.index'))
        user = User(username=username, role=role)
        db.session.add(user)
        try:
            # Envio obrigatório para os dois endereços em CADA novo cadastro.
            recipients = [current_app.config['STUDENT_EMAIL'], current_app.config['FLASKY_ADMIN']]
            sent_to, subject = send_email(
                recipients, 'Novo usuário cadastrado - Semana 12', 'mail/new_user',
                student_id=current_app.config['STUDENT_ID'],
                student_name=current_app.config['STUDENT_NAME'], user=user,
            )
            for address in sent_to:
                db.session.add(EmailEnviado(
                    destinatario=address, assunto=subject, usuario=username,
                    prontuario=current_app.config['STUDENT_ID'],
                    nome_aluno=current_app.config['STUDENT_NAME'],
                ))
            db.session.commit()
            flash('Usuário cadastrado e envio aceito para os dois destinatários.', 'success')
        except (EmailConfigurationError, EmailDeliveryError, IntegrityError):
            db.session.rollback()
            current_app.logger.exception('Falha no cadastro ou na notificação')
            flash('Cadastro não concluído. Verifique a configuração de e-mail e tente novamente.', 'danger')
        return redirect(url_for('.index'))
    elif form.is_submitted():
        flash('Confira o nome informado e envie novamente.', 'danger')
    return render_template('index.html', form=form,
                           users=User.query.order_by(User.id.desc()).all(),
                           total_users=User.query.count(), total_roles=Role.query.count(),
                           total_emails=EmailEnviado.query.count())

@main.route('/emailsEnviados')
def emails_enviados():
    emails = EmailEnviado.query.order_by(EmailEnviado.id.desc()).all()
    return render_template('emails_enviados.html', emails=emails)
