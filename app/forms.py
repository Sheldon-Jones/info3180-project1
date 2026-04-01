from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (StringField, TextAreaField, SelectField,
                     DecimalField, IntegerField, SubmitField)
from wtforms.validators import DataRequired, NumberRange, Length


class PropertyForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired()]
    )
    no_of_bedrooms = IntegerField(
        'Number of Bedrooms',
        validators=[DataRequired(), NumberRange(min=1, message='Must be at least 1')]
    )
    no_of_bathrooms = IntegerField(
        'Number of Bathrooms',
        validators=[DataRequired(), NumberRange(min=1, message='Must be at least 1')]
    )
    location = StringField(
        'Location',
        validators=[DataRequired(), Length(max=255)]
    )
    price = DecimalField(
        'Price',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, message='Price must be positive')]
    )
    property_type = SelectField(
        'Property Type',
        choices=[('House', 'House'), ('Apartment', 'Apartment')],
        validators=[DataRequired()]
    )
    photo = FileField(
        'Property Photo',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
        ]
    )
    submit = SubmitField('Add Property')
