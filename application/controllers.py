from flask import Flask,render_template,request,redirect
from flask import current_app as app   #refers to the app.py object
from .models import *
import datetime
from matplotlib.pyplot as plt
matplotlib.use("Agg")  # used to work with backend
# http://127.0.0.1:5000 base url

# Transaction One
def raw(text):
    result= text.split()
    srch_word=''
    for word in result:
        srch_word+=word.lower()



@app.route('/userlogin',methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        u_name=request.form.get("u_name")
        pwd=request.form.get('pwd')
        this_user=User.query.filter_by(username=u_name).first()       #or .all()
        if this_user:
            if this_user.password==pwd:
                if this_user.type=="admin":
                    return redirect('/admin')
                else:
                    return redirect(f'/user/{this_user.id}') # can user urlfor instead of f string
            else:
                return 'Incorrect Passswod'
        else:
            return "USER DNE"
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def user_register():
    if request.method=='POST':
        u_name=request.form.get("u_name")
        pwd=request.form.get('pwd')
        this_user=User.query.filter_by(username=u_name).first() 
        if this_user:
            return "User Already Exists"
        else:
            new_user=User(username=u_name,password=pwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/userlogin')

    return render_template('register.html')


@app.route('/admin',methods=['GET','POST'])
def admin_login():
    admin=User.query.filter_by(type='admin').first()
    requsted_trans= Transaction.query.filter_by(internal_status="requested").all()
    quoted_trans= Transaction.query.filter_by(internal_status="quoted").all()
    paid_trans= Transaction.query.filter_by(internal_status="paid").all()
    return render_template("admin_dash.html",requested_trans=requsted_trans,
                                            quaoted_trans=quoted_trans,
                                            paid_trans=paid_trans)


@app.route('/user/<int:user_id>',methods=['GET','POST'])
def user(user_id):
    user=User.query.get(user_id)
    transactions= user.trans # objects trans related to specific user
    return render_template("user_dash.html",u_name=user,transactions=transactions)


@app.route('/transaction_create/<int:user_id>' , methods=['GET','POST'])
def trans_create(user_id):
    user=User.query.get(user.id)
    if request.method=='POST':
        t_name=request.form.get('t_name')
        t_type=request.form.get('t_type')
        s_city=request.form.get('s_city')
        d_city=request.form.get('d_city')
        description=request.form.get('description')
        new_trans=Transaction(t_name=t_name,t_search_name=raw(t_name),t_type=t_type,t_date=datetime.datetime.now(),s_city=s_city,d_city=d_city,user_id=user.id)
        db.session.add(new_trans)
        db.session.commit()
        return redirect(f'/user/{user.id}')
    return render_template('create_transc.html',user=user)



@app.route('/review/<int:trans_id>',methods=['GET','POST'])
def review_trans(trans_id):
    this_trans=Transaction.query.get(trans_id)
    if request.method=='POST':
        d_date= request.form.get('d_date')
        this_trans.delivery_date=d_date
        amt=request.form.get('amt')
        this_trans.amount=amt
        this_trans.internal_status='quoted'
        db.session.commit()
        return redirect('/admin')
    return render_template('review.html',this_trans=this_trans)


@app.route('/delete/<int:id>')
def cancel_trans(id):
    del_trans=Transaction.query.get(id)
    del_trans.interna_status='cancelled'
    db.session.commit()
    return redirect('/admin')

@app.route('/search')
def text_search():
    t_names=Transaction.query.all() # all transactions
    srch_word=request.args.get('srch_word')
    search_word="%"+raw(srch_word)+"%"
    search_city="%"+srch_word.lower+"%"
    search_type="%"+srch_word.lower+"%"
    t_names=Transaction.query.filter(Transaction.t_search_name.like(search_word)).all()
    t_s_city=Transaction.query.filter(Transaction.s_city.like(search_city.lower)).all()
    t_d_city=Transaction.query.filter(Transaction.d_city.like(search_city.lower)).all()
    t_types=Transaction.query.filter(Transaction.t_type.like(search_city.lower)).all()
    search_results=t_names+t_s_city+t_d_city+t_types
    return render_template('srch_result.html',search_results=search_results)

@app.route('/stats')
def stats():
    transactions=Transaction.query.all()
    types=[]
    for trans in transactions:
        types.append(trans.t_type)
    plt.clf()   #clears previous fig
    plt.hist(types)
    plt.savefig('static/img.png')
    return render_template('summary.html')
