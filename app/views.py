from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User

@app.before_request 	# se izvede preden so klicane view funkcije
def before_request():
	g.user = current_user 	# nastavimo vrednost g.user na trenutnega uporabnika iz Flask-Login
	# sedaj imamo dostop do trenutnega uporabnika znotraj view-ov

@app.route('/')
@app.route('/index')
@login_required 			# ce pred klicom nisi vpisan, te poslje na /login
def index():
	user = g.user
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
							
'''
In Flask-Login you can protect views against non logged in users by adding the login_required decorator. 
If the user tries to access one of the affected URLs then it will be redirected to the login page 
(lm.login_view v __init__) automatically. Flask-Login will store the original URL as the next page, 
and it is up to us to return the user to this page once the login process completed.
'''

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index')) 	# url_for() -> Flask vrne url za view 'index'
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data 	# Flask session - shranjeni podatki so na voljo za vse requeste tega userja
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email']) # poslje podatke iz openid form do openid providerja,
		#od njega dobi podatke o 'nickname' in 'email' uporabnika. Ce je login uspese, poslje response funkciji oid.after_login
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.email).first() 	# iscemo email userja v bazi podatkov
	if user is None: 				# ce userja se ni v bazi, ustvarimo novega
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname=nickname, email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me= False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me) 	#funkcija modula Flas_Login, potrdi da uporabnik vpisan
	return redirect(request.args.get('next') or url_for('index')) 	#nadaljuj na naslednjo stran ali index, ce ni naslednje v requestu

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

						   
#funkcija, ki nalozi uporabnika iz database:
@lm.user_loader 	#povezava s Flask-Login - dfiniraj funkcijo, ko nalozi uporabnika iz DB
def load_user(id):
	return User.query.get(int(id)) #user id in Flask-Login is a string, we need int for database