from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///glossary.db'
app.config['SECRET_KEY']= 'This is my first flask web api'
db= SQLAlchemy(app)


class Words(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    word= db.Column(db.String(50), nullable= False)
    definition= db.Column(db.String(200), nullable= False)
    source= db.Column(db.String(100), nullable= False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Vocabulary: {self.word}'

@app.route('/')
def index():
    words= Words.query.order_by(Words.date_created).all()
    return render_template('index.html', words= words)

@app.route('/add', methods= ['GET', 'POST'])
def addWord():    
    if request.method == 'POST':
        word= request.form['word']
        w= Words.query.filter_by(word= word).first()
        if not w:
            definition= request.form['definition']
            source= request.form['source']
            newword= Words(word= word, definition= definition, source=source)
            db.session.add(newword)
            db.session.commit()
            return redirect('/')
    return render_template('add.html')

@app.route('/delete', methods= ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        for num in request.form.getlist('deleteclick'):
            word= Words.query.get_or_404(num)
            db.session.delete(word)
            db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods= ['GET', 'POST'])
def update(id):
    word= Words.query.get_or_404(id)
    if request.method == 'POST':
        word.word= request.form['word']
        word.definition= request.form['definition']
        word.source= request.form['source']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('update.html', word= word)


if __name__ == "__main__":
    app.run(debug= True)