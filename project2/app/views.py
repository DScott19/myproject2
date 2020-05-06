import datetime
from app import app, db,login_manager
from flask import render_template, request, redirect, url_for, flash,session, abort
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import ProfileForm, PostForm
from app.login_form import LoginForm
from app.models import Users,Posts,Likes,Follows
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os


def format_date_joined():
    date_joined = datetime.datetime.now()
    return date_joined.strftime("%B %d, %Y") 



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/secure-page')
@login_required
def secure_page():
    return render_template('secure_page.html')

##@app.route('/profiles')
##def profiles():
##    users = db.session.query(UserProfile).all() 
##    ##image_list=get_uploaded_images();
##    return render_template('profiles.html',users=users)
##
##@app.route('/profile/<userid>')
##def user_profile(userid):
##    users=db.session.query(UserProfile).filter_by(userid=userid).all()
##    return render_template('user_profile.html',users=users)
##



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        username=form.username.data
        password=form.password.data
            # Get the username and password values from the form.
        user=Users.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            # using your model, query database for a user based on the username
            # and password submitted. Remember you need to compare the password hash.
            # You will need to import the appropriate function to do so.
            # Then store the result of that query to a `user` variable so it can be
            # passed to the login_user() method below.
            # get user id, load into session
            login_user(user)
            # remember to flash a message to the user
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            
            return redirect(next_page or url_for('profiles'))
        else:
            flash('Username or Password is incorrect.', 'danger')
    return render_template("login.html", form=form)
##NEED FIXING. NEED TO PIN POINT CURRENT USER IN PROFILES.HTML
@app.route('/users')
def profiles():
    users = db.session.query(Users).all() 
    ##image_list=get_uploaded_images();
    return render_template('profiles.html',users=users)

@app.route('/users/<user_id>')
def user_profile(user_id):
    users=db.session.query(Users).filter_by(id=user_id).all()
    return render_template('user_profile.html',users=users)



##THIS NEEDS FIXING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CANNOT USE CURRENT_USER IN RENDER_ TEMPLATE
@app.route('/users/<user_id>/posts',methods=['GET','POST'])
def posts(user_id):
    print(user_id)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    post=PostForm()
    if request.method == "POST" and post.validate_on_submit():
        caption=post.caption.data
        photo=post.photo.data
        filename=secure_filename(photo.filename)
        photo.save(os.path.join(app.config['POSTS_FOLDER'], filename))
        posts=Posts(user_id=int(user_id),photo=filename,caption=caption,created_on=format_date_joined())
        db.session.add(posts)
        db.session.commit()
        flash('Post was successfully added','success')
        return redirect(url_for('profiles'))
    else:
        
        return render_template('posts.html',form=post,userid=current_user)
        

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.','success')
    return redirect(url_for("home"))


@app.route('/users/register',methods=['GET','POST'])
def profile():
    form=ProfileForm()
    if request.method == "POST" and form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        firstname=form.firstname.data
        lastname=form.lastname.data
        email=form.email.data
        location=form.location.data
        biography=form.biography.data
        profile_photo=form.profile_photo.data
        filename=secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        user=Users(username=username,password=password,firstname=firstname,lastname=lastname,email=email,location=location,biography=biography,profile_photo=filename,joined_on=format_date_joined())
        db.session.add(user)
        db.session.commit()
        flash('Profile was successfully added','success')
        return redirect(url_for('home'))
    else:
        
        return render_template('profile.html',form=form)

        


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")


    
    


