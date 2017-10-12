
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(2000))

    def __init__(self, title, content):
        self.title = title
        self.content = content




blog = []

@app.route('/blog', methods = ['GET'])
def index():

    id = request.args.get('id')

 
    if id != None:
         blogpost = Blog.query.get(id)
         return render_template('individual.html', blog=blogpost)
    
    else: 
        
        blogs = Blog.query.all()
        return render_template('all_blogs.html', blogs=blogs)
   

  

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == "POST":
        #check required things
        if len(request.form['title']) != 0 and len(request.form['content']) != 0:
            new_entry=Blog(request.form['title'], request.form['content'])
            db.session.add(new_entry)
            db.session.commit()
            newUrl = "/blog?id=" + str(new_entry.id)
            return redirect(newUrl)

    return render_template('newpost.html')
    

if __name__ == '__main__':
    db.create_all()
    app.run()





