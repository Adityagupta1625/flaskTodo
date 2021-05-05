from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_BINDS'] = {"register": "sqlite:///register.db"}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(200),nullable=False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Register(db.Model):
    __bind_key__ = 'register'
    username=db.Column(db.String(15), nullable=False,primary_key=True)
    password=db.Column(db.String(15), nullable=False)
    email=db.Column(db.String(15), nullable=False)

    

# @app.route('/Register',methods=['GET','POST'])
@app.route('/Register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        register=Register(username=username,email=email,password=password)

        db.session.add(register)
        db.session.commit()
        return render_template('login.html')
    return render_template('Register.html')

@app.route('/',methods=['GET','POST'])
def Login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        register=Register.query.filter_by(username=username).first()
        if register.username==username and register.password==password:
            allTodo = Todo.query.filter_by(username=username).all()
            return render_template('index.html',username=username,allTodo=allTodo)                
        else:
            return redirect("/")
    return render_template('login.html')

@app.route('/home',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        username=request.form['username']
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc,username=username)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.filter_by(username=username).all()
    return render_template('index.html',allTodo=allTodo,username=username)

@app.route('/home/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    username=todo.username
    db.session.delete(todo)
    db.session.commit()
    allTodo=Todo.query.filter_by(username=username).all()
    print(username)
    return render_template('index.html',allTodo=allTodo,username=username)


@app.route('/home/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        username=request.form['username']
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.username=username
        db.session.add(todo)
        db.session.commit()
        allTodo=Todo.query.filter_by(username=username).all()
        return render_template('index.html',allTodo=allTodo,username=username)

        
    todo= Todo.query.filter_by(sno=sno).first()
    username=todo.username
    return render_template('update.html',todo=todo,username=username)    

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':

        search=request.form['search']
        allTodo = Todo.query.filter(Todo.title.startswith(search)).all()
        
    return render_template('search.html',allTodo=allTodo)  

if __name__=="__main__":
    app.run(debug=False)

# User.query.filter(User.email.endswith('@example.com')).all()