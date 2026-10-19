import unittest
from unittest.mock import patch
from flask import session
from app import create_app, db
from app.models import User, Role, EmailEnviado, create_default_roles

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        create_default_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_app_exists(self):
        self.assertIsNotNone(self.app)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('visitante', response.get_data(as_text=True))

    @patch('app.main.views.send_email')
    def test_cadastro_notifica_ambos(self, mock_email):
        cfg = self.app.config
        mock_email.return_value = ([cfg['STUDENT_EMAIL'], cfg['FLASKY_ADMIN']], '[Flask] Novo usuário')
        response = self.client.post('/', data={'username': 'estudante01'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(EmailEnviado.query.count(), 2)
        self.assertEqual(mock_email.call_args.args[0], [cfg['STUDENT_EMAIL'], cfg['FLASKY_ADMIN']])
        self.assertIn('Olá, estudante01!', response.get_data(as_text=True))
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['name'], 'estudante01')
            self.assertFalse(sess['known'])

    @patch('app.main.views.send_email')
    def test_duplicidade_nao_envia_e_reconhece(self, mock_email):
        role = Role.query.filter_by(name='User').first()
        db.session.add(User(username='existente', role=role))
        db.session.commit()
        response = self.client.post('/', data={'username': 'existente'}, follow_redirects=True)
        mock_email.assert_not_called()
        self.assertEqual(User.query.count(), 1)
        self.assertIn('Olá novamente, existente!', response.get_data(as_text=True))
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['name'], 'existente')
            self.assertTrue(sess['known'])

    @patch('app.main.views.send_email')
    def test_falha_envio_impede_cadastro(self, mock_email):
        from app.email import EmailDeliveryError
        mock_email.side_effect = EmailDeliveryError('falha')
        self.client.post('/', data={'username': 'falha'})
        self.assertEqual(User.query.count(), 0)
        self.assertEqual(EmailEnviado.query.count(), 0)
        with self.client.session_transaction() as sess:
            self.assertNotIn('name', sess)

    @patch('app.main.views.send_email')
    def test_usuario_existente_nao_dispara_segunda_notificacao(self, mock_email):
        cfg = self.app.config
        mock_email.return_value = ([cfg['STUDENT_EMAIL'], cfg['FLASKY_ADMIN']], '[Flask] Novo usuário')
        self.client.post('/', data={'username': 'aluno'})
        self.client.post('/', data={'username': 'aluno'})
        self.assertEqual(mock_email.call_count, 1)
        self.assertEqual(EmailEnviado.query.count(), 2)
