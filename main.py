from flask import Flask, request, redirect
import cgi
import re
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True


#@app.route("/")
#def index():
    #template = jinja_env.get_template('usersignup_form.html')
    #return template.render()

@app.route('/userform')
def display_userform():
    template = jinja_env.get_template('usersignup_form.html')
    return template.render()
#    return form.format(username='', username_error='', email_address='', email_address_error='', password='', password_error='', validate_password='', validate_password_error='')

@app.route('/userform', methods=['POST'])
def validate():
    username = request.form['username']
    email_address = request.form['email_address']
    password = request.form['password']
    validate_password = request.form['verify_password']

    username_error = ""
    email_address_error = ""
    password_error = ""
    validate_password_error = ""

    if not username.isalpha():
        username_error = "Not a valid user name!"
        username = ""

    else:
        if len(username) < 3 or len(username) > 20:
            username_error = "Invalid character count. Username must be more than 3 letters and less than 20."
            username = ""
    
    if len(password) < 3 or len(password) > 20:
        password_error = "Password does not match requirements!"
        password = ""

    else:
        if not password.isalpha():
            password_error = "Password does not match requirements!"
            password = ""

    if validate_password != password:
        validate_password_error = "Passwords do not match!"
        password = ""
        validate_password = ""
        #return form.format(username_error=username_error, password_error=password_error)

    if re.match("(^$|pattern[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_address):
        email_address = ""

    else:
        if not re.fullmatch("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email_address):
            email_address_error = "This is not a valid email. Email must have '@' and '.'."
            email_address = ""
        


    if not username_error and not password_error and not validate_password_error and not email_address_error:
        name=username
        return redirect('/valid?username={0}'.format(name))

    else:
        template = jinja_env.get_template('usersignup_form.html')
        return template.render(username_error=username_error, password_error=password_error, validate_password_error=validate_password_error, email_address_error=email_address_error)

@app.route('/valid')
def valid():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(name=username)

app.run()