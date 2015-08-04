from app import db

class User(db.Model):
	id = db.Cplumn(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index0=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	
	def __repr__(self):
		return 'User %r' % (self.nickname)