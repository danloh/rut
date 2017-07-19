from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL



class EditProfileForm(FlaskForm):    
    nickname = StringField('nickname')
    location = StringField('location')
    about = TextAreaField("About me")
    links = StringField('Blog/Socail Page Links',
                        render_kw={"placeholder":"REQUIRED VALID URL"})
    submit = SubmitField('submit')
