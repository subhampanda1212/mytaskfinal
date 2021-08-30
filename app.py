from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy  
from werkzeug.utils import secure_filename
from datetime import datetime
import os
#import magic
import urllib.request
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Dell/3D Objects/My_Python/my_task/blog.db'+'?check_same_thread=False'
app.config['SECRET_KEY'] = 'cairocoders-ednalan'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
 
UPLOAD_FOLDER = 'C:/Users/Dell/3D Objects/My_Python/my_task/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
  
ALLOWED_EXTENSIONS = set(['png', 'jpeg'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
db = SQLAlchemy(app) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True) 
    profile_pic = db.Column(db.String(150))
    last_seen=db.Column(db.DateTime, default=datetime.utcnow)
    

@app.route('/')
def index():
    our_users = User.query.order_by(User.last_seen) 
    return render_template('index.html',our_users=our_users)


@app.route('/upload', methods=['GET','POST'])
def upload():
    file = request.files['inputFile']
    rs_username = request.form['txtusername']
    filename = secure_filename(file.filename)
    
    if file and allowed_file(file.filename):
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  
       newFile = User(profile_pic=file.filename, username=rs_username, email='subhampanda1212@gmail.com')
       db.session.add(newFile)
       db.session.commit()
       flash('File successfully uploaded ' + file.filename + ' to the database!')
       
       return redirect('/')
    else:
       flash('Invalid Uplaod only png or jpeg')
    
    
    return redirect('/')  
  
if __name__ == '__main__':
    app.run(debug=True)