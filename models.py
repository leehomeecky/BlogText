from App import db
from datetime import datetime
import re
from time import time
from sqlalchemy.orm import *
import hashlib
from uuid import uuid4

def slugify(s):
    pattern = r"[^\w+]"
    return re.sub(pattern, '-', s)

posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.Integer,
                      db.ForeignKey('post.id')),
                      db.Column('tag_id', db.Integer,
                      db.ForeignKey('tag.id'))
                      )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(128), unique=True, nullable=True)
    email = db.Column(db.String(128), nullable=False)
    _password = db.Column('password',
                        db.String(128),
                        nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    filepath = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.now())
    posts = db.relationship("Post", backref=db.backref('users'), cascade="delete")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        self.userid = str(uuid4())
        super().__init__(*args, **kwargs)
    
    # def __repr__(self):
    # return f"<User id: {self.id} Names: {self.first_name} {self.last_name}>"

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        """hashing password values"""
        self._password = hashlib.md5(pwd.encode()).hexdigest()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.String(128), unique=True, nullable=True)
    title = db.Column(db.String(140)) 
    slug = db.Column(db.String(140), unique=True) 
    body = db.Column(db.Text)
    filepath = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.userid"), nullable=True)
    tags = db.relationship('Tag', secondary='posts_tags', 
                           backref=db.backref('posts'),
                           lazy='dynamic')
    
    def __init__(self, *args, **kwargs):
        self.postid = str(uuid4())
        super().__init__(*args, **kwargs)
        self.generate_slug()
    
    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))

    def __repr__(self):
        return f"<post id: {self.id} title: {self.title} body: {self.body}>"
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140)) 
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, default=datetime.now())
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.title)
        
    def __repr__(self):
        return f"<Tag id: {self.id} title: {self.title}>"
    
    def to_dict(self):
        """return all keys and values of the objectinstance from __dict__"""
        dictcopy = self.__dict__.copy()
        return dictcopy
