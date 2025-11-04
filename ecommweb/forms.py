from flask_wtf import FlaskForm
from wtforms import FileField, StringField,IntegerField,FloatField,PasswordField,EmailField,BooleanField,SubmitField, SelectField
from wtforms.validators import DataRequired,length,NumberRange
from flask_wtf.file import FileRequired

class SignupForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired(), length(min=2)])
    password1=PasswordField('Enter your password',validators=[DataRequired(), length(min=8)])
    password2=PasswordField('Confirm your password',validators=[DataRequired(), length(min=8)])
    submit=SubmitField('Signup')

class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

class PasswordChangeForm(FlaskForm):
    current_password=PasswordField('Current Password',validators=[DataRequired(),length(min=8)])
    new_password=PasswordField('New Password',validators=[DataRequired(),length(min=8)])
    confirm_new_password=PasswordField('Confirm New Password',validators=[DataRequired(),length(min=8)])
    change_password=SubmitField('Change Password')

class ShopItemsForm(FlaskForm):
    product_name=StringField('Name of Product', validators=[DataRequired()])
    current_price=StringField('Current Price', validators=[DataRequired()])
    prev_price=FloatField('Previous Price', validators=[DataRequired()])
    in_stock=IntegerField('instock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture=FileField('Picture', validators=[FileRequired()])
    flash_sale=BooleanField('Flash Sale')

    add_product=SubmitField('Add Product')
    update_product=SubmitField('Update Product')

class UpdateForm(FlaskForm):
    order_status=SelectField('Order status', choices=[('Pending', 'Pending'),('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')])
    update_status=SubmitField('Update Status')