from flask import Blueprint, render_template, flash, redirect, url_for
from ecommweb.forms import LoginForm, SignupForm, PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint('auth',__name__)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():   
    form=SignupForm()      
    if form.validate_on_submit():
        email=form.email.data
        username=form.username.data
        password1=form.password1.data
        password2=form.password2.data

        if password1==password2:
            new_customer=Customer()
            new_customer.email=email
            new_customer.username=username
            new_customer.password=password2  # This will use the password setter to hash it

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account created successfully! You may Login now')
                return redirect('/auth/login')
            except Exception as e:
                print(e)
                flash('Account already exist !')

            form.email.data=''    
            form.username.data=''    
            form.password1.data=''    
            form.password2.data=''

    return render_template("signup.html", form=form) #Defining route for signup page    

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data

        customer = Customer.query.filter_by(email=email).first()
        
        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                flash('Logged in successfully!')
                return redirect('/')
            else:   
                flash('Incorrect password!,Try again')
                # flash('Email does not exist!')
        else:
            flash("User Not Registered")
        
    return render_template("login.html",form=form) #Defining route for login page


@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect('/')


@auth.route('/profile/<int:id>')
@login_required
def profile(id):
    if id != current_user.id:
        flash('You can only view your own profile')
        return redirect('/')
    customer = Customer.query.get(id)
    if not customer:
        flash('Profile not found')
        return redirect('/')
    return render_template('profile.html', customer=customer)

@auth.route('/change-password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
    if id != current_user.id:
        flash('You can only change your own password')
        return redirect('/')
    
    form = PasswordChangeForm()
    if form.validate_on_submit():
        customer = Customer.query.get(id)
        if customer.verify_password(form.current_password.data):
            customer.password = form.new_password.data
            db.session.commit()
            flash('Password changed successfully!')
            return redirect(url_for('auth.profile', id=id))
        else:
            flash("Password donot match")
    else:
        flash('Current password is incorrect')
    
    return render_template('change_password.html', form=form)