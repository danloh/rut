# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL



class EditProfileForm(FlaskForm):    
    nickname = StringField('nickname')
    location = StringField('location')
    avatar = StringField('Avatar Url, max length 256')
    about = TextAreaField("About me")
    links = StringField('Blog/Socail Page Links',
                        render_kw={"placeholder":"REQUIRED VALID URL"})
    submit = SubmitField('submit')
