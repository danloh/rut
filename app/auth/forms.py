# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL

class EditProfileForm(FlaskForm):    
    nickname = StringField('Change Public Nickname',
                          render_kw={"placeholder":"Max 64 characters"})
    location = StringField('Location')
    avatar = StringField('Profile Image URL, Max length 256')
    about = TextAreaField("About me")
    links = StringField('Blog/Social Page Link',
                        render_kw={"placeholder":"Valid URL, Max length 120"})
    submit = SubmitField('submit')
