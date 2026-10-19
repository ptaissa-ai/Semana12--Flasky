import unittest
from unittest.mock import patch
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
        self.assertEqual(self.client.get('/').status_code, 200)

    @patch('app.main.views.send_email')
    def test_cadastro_notifica_ambos(self, mock_email):
        cfg = self.app.config
        mock_email.return_value = ([cfg['STUDENT_EMAIL'], cfg['FLASKY_ADMIN']], '[Flask] Novo usuário')
        response = self.client.post('/', data={'username': 'estudante01'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(EmailEnviado.query.count(), 2)
        recipients = mock_email.call_args.args[0]
        self.assertEqual(recipients, [cfg['STUDENT_EMAIL'], cfg['FLASKY_ADMIN']])

    @patch('app.main.views.send_email')
    def test_duplicidade_nao_envia(self, mock_email):
        role = Role.query.filter_by(name='User').first()
        db.session.add(User(username='existente', role=role))
        db.session.commit()
        self.client.post('/', data={'username': 'existente'})
        mock_email.assert_not_called()
        self.assertEqual(User.query.count(), 1)

    @patch('app.main.views.send_email')
    def test_falha_envio_impede_cadastro(self, mock_email):
        from app.email import EmailDeliveryError
        mock_email.side_effect = EmailDeliveryError('falha')
        self.client.post('/', data={'username': 'falha'})
        self.assertEqual(User.query.count(), 0)
        self.assertEqual(EmailEnviado.query.count(), 0)
