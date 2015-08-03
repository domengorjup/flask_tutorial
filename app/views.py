from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Domen'}
	posts = [{
				'author':{'nickname':'Ana'},
				'body':'Domen, ki si ti!'
				},
				{
				'author':{'nickname':'Domen'},
				'body':'tule, ki si TI?!'
				},
				{
				'author':{'nickname':'David'},
				'body':'pa ti je ke?'
				}]
	return render_template('index.html',
							title='Home',
							user=user,
							posts=posts)
							
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', 
                           title='Sign In',
                           form=form)