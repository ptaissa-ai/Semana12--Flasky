from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NameForm(FlaskForm):
    username = StringField('Nome do usuário', validators=[DataRequired(), Length(min=2, max=80)])
    submit = SubmitField('Cadastrar usuário')
