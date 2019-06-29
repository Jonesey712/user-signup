from flask import Flask, request, redirect
import cgi
import re

#template_dir = os.path.join(os.path.dirname(__file__), 'templates')
#jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True

form = """
    <style>
        .error {{color: red;}}
    </style>
    <body>
    <h1>Signup</h1>
    <form method='post'>
        <table>
            <tr>
                <td>
                    <label for="username">Username</label>
                </td>
                <td>
                    <input name="username" type="text" value="">
                    <span class="error">{username_error}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="password">Password</label>
                </td>
                <td>
                    <input name="password" type="password" value="">
                    <span class="error">{password_error}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="verify_password">Verify Password</label>
                </td>
                <td>
                    <input name="verify_password" type="password" value="">
                    <span class="error">{validate_password_error}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <label for="email_address">E-Mail Address(optional)</label>
                <td>
                    <input name="email_address" type="text" value="">
                    <span class="error">{email_address_error}</span>
                </td>
            </tr>
            <tr>
                <input type="submit" value="Submit"
            </tr>
        </table>
    </form>
    </body>
"""

#@app.route("/")
#def index():
#    return form

@app.route('/userform')
def display_userform():
    return form.format(username='', username_error='', email_address='', email_address_error='', password='', password_error='', validate_password='', validate_password_error='')

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
        username = len(username)
        if username < 3 or username > 20:
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
        username=username
        return redirect('/valid?username={0}'.format(username))

    else:
        return form.format(username_error=username_error, password_error=password_error, validate_password_error=validate_password_error, email_address_error=email_address_error)

@app.route('/valid')
def valid():
    username=username
    form = request.args.get('form')
    return "'<h1>Welcome, ' + username + '</h1>'".format(form)

app.run()