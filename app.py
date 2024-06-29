from flask import Flask, request, render_template, redirect, url_for, send_file
from flask_excel import make_response
from datetime import datetime ,  timezone
from flask_sqlalchemy import SQLAlchemy
import flask_excel as excel
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.DateTime , nullable = False ,default=lambda: datetime.now(timezone.utc))   

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/qr')
def qr():
    return render_template('qr.html') 

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    if email:
        new_email = Email(email=email)
        db.session.add(new_email)
        db.session.commit() 
    return redirect(url_for('index'))

@app.route('/download')
def download():
    # Query all UserEmail records
    emails = Email.query.all() 
    # Create a list of lists to be used by flask_excel
    email_list = [['ID', 'Email']] + [[e.id, e.email] for e in emails]
    # Use flask_excel to create an Excel response
    response = excel.make_response_from_array(email_list, "xlsx")
    response.headers["Content-Disposition"] = "attachment; filename=emails.xlsx"
    return response 

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('emails.db'):
            db.create_all()
    app.run(debug=True)







