from app import db
from hashlib import md5 # md5 hash to get avatars from gravatar.com

# Followers - followed table - NOT a class, it only contains foreign keys (relationships)
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                                secondary=followers,        # indicates relationship table
                                primaryjoin=(followers.c.follower_id == id),    # condition that links the primary (follower) user with relationship table
                                secondaryjoin=(followers.c.followed_id == id),  # condition that links the secundary (followed) user with relationship table
                                backref=db.backref('followers', lazy='dynamic'), #defines how this will be accessed from the 'followed' side (list of followers)
                                lazy='dynamic')
	
	#True, razen ce se ne sme vpisat:
    def is_authenticated(self):
        return True

    #True, razen ce ne sme biti aktiven (BAN):
    def is_active(self):
        return True

    #True le za tiste, ki se naj ne bi vpisali
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
            
    def avatar(self, size): #get avatar from gravatar.com (if not, mistery man (d=mm) avatar)
        return 'http://gravatar.com/avatar/%s?d=mm&s=%d' %(md5(self.email.encode('utf-8')).hexdigest(), size)
        
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self         # Returns new ("updated") user object to be added to db
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
    
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
        
    #Metoda, ki poišče poste uporabnikov, ki jim sledimo:
    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
        '''
        http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers-contacts-and-friends
        '''
    def __repr__(self):
        return '<User %r>' % (self.nickname)
        
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname
	

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
        
