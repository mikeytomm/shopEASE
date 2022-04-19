'''this file contains all route it it likethe controller that determines what happens when a user visits our app'''
from werkzeug.security import generate_password_hash, check_password_hash
from flask import  render_template ,request,redirect,flash,make_response,session#imporing all we need 
from shopeaseapp import app,db   #imporing the instantate flask (app)
from shopeaseapp.mymodel import User,Vendor,Admin,Order,Payment,Product,Category,Orderdeet#writing nt raw we firs import the class post which is in the mode.py
#from conferenceapp.forms import LoginForm



@app.route('/admin',methods=['GET','POST'])
def admin_home():
    
    
    id = session.get('logged')
    if id== None:
        return redirect('/')
    else:
        admindeets = Admin.query.get(id)
        category=Category.query.all()
        users=User.query.all()
        vendor=Vendor.query.all()
        order=Order.query.all()
        payment=Payment.query.all()
        product=Product.query.all()
        orderdeets=Orderdeet.query.all()
        
        
    

        return render_template('admin/fpadmin.html',admindeets=admindeets,category=category,users=users,vendor=vendor,payment=payment,product=product,order=order,orderdeets=orderdeets)


@app.route('/shop/ease/admin/signup')
def admin_signup():
    return render_template('admin/fpadminsignup.html')

@app.route('/admin/signup/submit',methods=['GET','POST'])
def admin_signup_submit():
    if request.method=='GET':
        return redirect('/')
    else:
        email=request.form.get('admin_email')
        password=request.form.get('admin_password')
        confpass=request.form.get('admin_passwordconf')
        if email=="" or password=="" or confpass=="":
            message="please complete all fields"
            flash(message)
            return redirect('/shop/ease/admin/signup')
        elif password != confpass:
            message="password mismatch"
            flash(message)
            return redirect('/shop/ease/admin/signup')
        else:
            formated=generate_password_hash(password)
            a=Admin(admin_email=email,admin_passwrd=formated)
            db.session.add(a)
            db.session.commit()
            return redirect('/admin/login')



@app.route('/admin/login')
def admin_login():
    
    
    return render_template('admin/fpadminlogin.html')


@app.route('/admin/login/submit',methods=['GET','POST'])
def admin_login_submit():
     if request.method=="GET":
         return redirect('/admin/login')
     else:

         a=request.form.get('admin_email')
         b=request.form.get('admin_password')
         
         
         deets=Admin.query.filter(Admin.admin_email==a).first()
         formattedpassword=deets.admin_passwrd
         chk=check_password_hash(formattedpassword,b)
         
         if chk:

            id=deets.admin_id
            session['logged']=id#creating a session
            admindeets = Admin.query.get(id)
            return redirect('/admin')

         elif a=="" or b=="":
             message="pls fill all fields"
             flash(message)
             return redirect('/admin/login')
         else:
           
             message="invalid credentials"
             flash(message)
             return redirect('/admin/login')


@app.route('/admin/add_category',methods=['GET','POST'] )
def admin_addcat():
    if request.method == 'GET':
        return redirect('/')
    else:
        newcat=request.form .get('admin_addcatname')
        if newcat =='':
            message='please check that a field isnt left empty when trying to add a category'
            flash(message)
            return redirect('/admin')
        else:
            a=Category(category_name=newcat)
            db.session.add(a)
            db.session.commit()
            message='Category addedd successfully'
            flash(message)
            return redirect('/admin')
            





@app.route('/admin/logout')
def admin_logout():
    if request.method =='GET':
        return redirect('/admin/login')
    elif id != '':
        
        session.pop('logged')
        return redirect('/admin/login')

            
        
       



      