from app import app
from flask import render_template

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