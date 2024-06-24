from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db
from app.forms import ContactForm, RecommendationForm, SongForm, PostForm
from app.models import User, Song, Post
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
        current_user.recommendations = "Recommended music list based on mood, genre, and generation"
        db.session.commit()
        flash('Recommendations updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('recommend.html', title='Recommendations', form=form)

@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash('Your message has been sent!', 'success')
        return redirect(url_for('main.home'))
    return render_template('contact.html', title='Contact', form=form)

@main.route("/library", methods=['GET', 'POST'])
@login_required
def library():
    form = SongForm()
    if form.validate_on_submit():
        song = Song(title=form.title.data, artist=form.artist.data, album=form.album.data, genre=form.genre.data, owner=current_user)
        db.session.add(song)
        db.session.commit()
        flash('Song added to your library!', 'success')
        return redirect(url_for('main.library'))
    user_songs = Song.query.filter_by(user_id=current_user.id).all()
    return render_template('library.html', title='My Library', form=form, songs=user_songs)

@main.route("/blog", methods=['GET', 'POST'])
@login_required
def blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.blog'))
    posts = Post.query.all()
    return render_template('blog.html', title='Blog', form=form, posts=posts)

