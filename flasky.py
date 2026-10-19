import os
import click
from app import create_app, db
from app.models import User, Role, EmailEnviado, create_default_roles

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'EmailEnviado': EmailEnviado}

@app.cli.command('seed-roles')
def seed_roles():
    """Cria as funções iniciais (execute após flask db upgrade)."""
    create_default_roles()
    click.echo('Funções iniciais criadas.')

@app.cli.command('test')
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Executa testes de unidade conforme Aula 080."""
    import unittest
    suite = (unittest.TestLoader().loadTestsFromNames(test_names)
             if test_names else unittest.TestLoader().discover('tests'))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)

if __name__ == '__main__':
    app.run()
