# -*- coding: UTF-8 –*-
from flask.ext.wtf import Form     # 导入扩展模块
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField    # 导入需要使用的，WTFroms支持的HTML标准字段
from wtforms.validators import Required 
from models import User     # 验证函数，确保字段不为空

class NameForm(Form):
     name = StringField(u'用户名', validators=[Required()])
     password = PasswordField(u'密码', validators=[Required()])# 用户可以输入内容的文本框，值被name变量接收
     remember_me = BooleanField(u'记住我')
     submit = SubmitField(u'提交')

     def get_user(self):
          user = User.query.filter_by(username=self.name.data).first()
          return user


class PostingForm(Form):
     title = StringField(u'题目', validators=[Required()])
     tag1 = StringField(u'标签1', validators=[Required()])
     tag2 = StringField(u'标签2', validators=[Required()])
     tag3 =  StringField(u'标签3', validators=[Required()])
     content = TextAreaField(u'文章内容', validators=[Required()])
     submit = SubmitField(u'提交')


class EditForm(Form):
     edit_title = StringField(u'修改题目')
     edit_tag1 = StringField(u'修改标签1')
     edit_tag2 = StringField(u'修改标签2')
     edit_tag3 = StringField(u'修改标签3')
     edit_content = TextAreaField(u'修改博文')
     submit = SubmitField(u'提交修改')

