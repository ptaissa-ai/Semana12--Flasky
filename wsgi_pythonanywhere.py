"""Exemplo: copie o conteúdo para o arquivo WSGI no painel PythonAnywhere."""
import os
import sys
PROJECT_DIR = '/home/SEU_USUARIO/semana_12_Flasky'
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)
# Produção: configurações e chave API devem existir no ambiente do processo WSGI.
os.environ['FLASK_CONFIG'] = 'production'
from flasky import app as application
