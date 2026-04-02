"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for
import os
from flask import (Blueprint, render_template, redirect, url_for, flash, current_app)
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import PropertyForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Properties for sale/rent")


def allowed_file(filename):
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed



@app.route('/create/', methods=['GET', 'POST'])
def property_create():
    form = PropertyForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)

        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        photo.save(os.path.join(upload_folder, filename))

        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            no_of_bedrooms=form.no_of_bedrooms.data,
            no_of_bathrooms=form.no_of_bathrooms.data,
            location=form.location.data,
            price=form.price.data,
            property_type=form.property_type.data,
            photo=filename
        )

        db.session.add(new_property)
        db.session.commit()

        flash('Property successfully added!', 'success')
        return redirect(url_for('properties_list'))


    return render_template('create.html', form=form)


@app.route('/list/')
def properties_list():
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('list.html', properties=properties)


@app.route('/<int:propertyid>/')
def property_detail(propertyid):
    prop = Property.query.get_or_404(propertyid)
    return render_template('detail.html', property=prop)



###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
