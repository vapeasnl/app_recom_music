from flask import Blueprint, render_template, url_for, flash, redirect
from app import db
from app.forms import ContactForm, RecommendationForm
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html', title='Home')

@main.route("/recommend", methods=['GET', 'POST'])
@login_required
def recommend():
    form = RecommendationForm()
    if form.validate_on_submit():
        current_user.mood = form.mood.data
        current_user.genre = form.genre.data
        current_user.generation = form.generation.data
        # Here you would implement the recommendation logic based on user's input
        current_user.recommendations = "Recommended music list based on mood, genre, and generation"
        db.session.commit()
        flash('Recommendations updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('recommend.html', title='Recommendations', form=form)

@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Here you would handle the contact form submission (e.g., send an email)
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.home'))
    return render_template('contact.html', title='Contact', form=form)

