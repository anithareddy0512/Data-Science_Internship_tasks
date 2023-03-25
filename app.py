import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,render_template,request, session, flash, redirect
import pyshorteners

app = Flask(__name__)
  
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

############# creating a tabel model
class URL(db.Model):
      __tablename__ = 'URL_Shortening_Data'
      id = db.Column(db.Integer, primary_key = True)
      long_url = db.Column(db.Text)
      short_url = db.Column(db.Text)

      def __init__(self,long_url,short_url):
          self.long_url = long_url
          self.short_url = short_url 
          
      def __repr__(self):
          return "{}----------{}".format(self.long_url,self.short_url)
        
        
        
@app.before_first_request
def table_creation():
    db.create_all()
    

############# End of the table ##############################
# s = 4
@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        long_url = request.form.get('in_1')
        if long_url:
            short = pyshorteners.Shortener()
            short_url = short.tinyurl.short(long_url)
            new_url = URL(long_url,short_url)
            db.session.add(new_url)
            db.session.commit() 
            db.session.close()
        return render_template('home.html', shortened=short_url, original = long_url)
    return render_template('home.html')

@app.route('/history')
def hist():
    urls = URL.query.all()
    return render_template('history.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)