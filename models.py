# -*- coding: UTF-8 –*-
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
     __tablename__ = 'users'
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(64), unique=True, index=True)  # index=True表示为这列创建索引，提升查询效率
     password = db.Column(db.String(64),unique=True)
     
     def __repr__(self):
          return '<User %r>' % self.username
     #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 定义外键，说明该列的值是roles表中行的id值
     # Flask-Login integration
     def get_id(self):
        return str(self.id)

     def is_authenticated(self):
        return True

     def is_active(self):
        return True

     def is_anonymous(self):
        return False
     # TypeError: ObjectId('552f41e56a85f00dd043406b') is not JSON serializable
     
     def __unicode__(self):
        return self.name
 
     def verify_password(self, pwdata):
          if self.password == pwdata:
               return True
          else:
               return False



class Post(db.Model):
     __tablename__ = 'posts'
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(128), unique=True)
     article = db.Column(db.String)
     #modify_time = db.Column(db.DateTime, unique=True)
     Tags1 = db.Column(db.String, index=True)
     Tags2 = db.Column(db.String, index=True)
     Tags3 = db.Column(db.String, index=True)
     create_time = db.Column(db.DateTime, unique=True)


     def __repr__(self):
          return '<Post %r>' % self.title

'''class Role(db.Model):
     __tablename__ = 'roles'     # 定义数据库中使用的表名
     id = db.Column(db.Integer, primary_key=True)  # 模型属性，被定义为db.Column类的实例
     name = db.Column(db.String(64), unique=True)  # 模型属性，uinque=True表示这一列不允许出现重复的值

     def __repr__(self):  # 定义__repr__()方法，返回一个具有可读性的字符串表示的模型，可在调试和测试时使用
          return '<Role %r>' % self.name
     users = db.relationship('User', backref='role')  # 表示两个模型间的关系，backref定义反向关系

'''