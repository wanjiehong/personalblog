# -*-coding: UTF-8-*-
from flask import Flask, request, render_template, redirect,url_for,flash,g 
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from models import db, User, Post
from forms import NameForm, PostingForm, EditForm
from flask.ext.moment import Moment 
from flask.ext.login import LoginManager, login_required, current_user, login_user,logout_user
import os
import datetime


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "it-is-always-a-secret"
app.config['SQLALCHEMY_DATABASE_URI'] =\
     'sqlite:///'+os.path.join(basedir,'shiyang.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
db.init_app(app)  
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u'请登录账户来进入相应页面'



@app.route('/')
@app.route('/page=<int:x>')
def index(x=1):
    use = Post.query.all()
    use2 = Post.query.paginate(page=x,per_page=3,error_out=False)
    return render_template("index.html",use2=use2)


@app.route('/login', methods=['GET', 'POST'])
def login():   
    form = NameForm()
    if request.method == 'GET':
        return render_template("login.html", form=form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(u'登录成功！')
            return redirect(url_for('list')) 
        else:
            flash(u'用户名或密码错误')
            return redirect(url_for('login'))


@app.route('/post-article', methods=['GET', 'POST'])
@login_required
def post():
    if current_user.is_authenticated:
        form = PostingForm()
        if request.method == 'GET':
            return render_template("post.html", form=form)
        if request.method == 'POST' and form.validate():
            data = request.form
            add_post = Post(title=data['title'], article=data['content'],\
                Tags1=data['tag1'],Tags2=data['tag2'],
                Tags3=data['tag3'], create_time=datetime.datetime.now())
            db.session.add(add_post)
            db.session.commit()
            flash(u'您的文章已经提交成功')
            return redirect(url_for('index'))


@app.route('/editor')
@login_required
def list():
    if current_user.is_authenticated:
        use = Post.query.all()
        return render_template("editor.html",use=use)

@app.route('/editor/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):   
    if current_user.is_authenticated:
        post = Post.query.get_or_404(int(id))
        form = EditForm()    
        if request.method == 'POST' and form.validate_on_submit():
            post.title = form.edit_title.data
            post.Tags1 = form.edit_tag1.data 
            post.Tags2 = form.edit_tag2.data 
            post.Tags3 = form.edit_tag3.data 
            post.article = form.edit_content.data
            db.session.add(post)
            flash(u'博文修改提交成功！')
            return redirect(url_for('list')) 
        form.edit_title.data = post.title
        form.edit_tag1.data = post.Tags1
        form.edit_tag2.data = post.Tags2
        form.edit_tag3.data = post.Tags3
        form.edit_content.data = post.article
        return render_template("editid.html", form=form)    
    else:
        flash(u'不成功，请重试！')
        return render_template("editor.html")
    

@app.route('/test')
@login_required
def test():
    return u'只有您登录了才能打开此正常页面~'

@app.route('/delete/<id>')
@login_required
def delete(id):
    if current_user.is_authenticated():
        id=int(id)
        delete_post = Post.query.get(id)
        db.session.delete(delete_post)
        db.session.commit()
        flash(u'您的文章已经成功删除')
        return redirect(url_for('list'))

@app.route('/logout')
def logout():
    logout_user()
    flash(u'退出成功！')
    return redirect(url_for('index'))

@app.route('/<int:id>')
def show(id):
    post = Post.query.get(int(id))   
    return render_template("article.html", post=post)


@app.route('/about')
def about():
    return render_template("about.html") 


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def page_not_found(e):
     return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
     return render_template('500.html'), 500


@app.template_filter('timedeal')
def timedeal(x):
    s = x.strftime('%b-%d-%y %H:%M:%S')
    return s

@app.template_filter('limit')
def limit(s):
    return s[80:180]

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)