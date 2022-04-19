'''this file contains all route it it likethe controller that determines what happens when a user visits our app'''
import math, random, os,requests
from unicodedata import category
from sqlalchemy import desc,asc
from werkzeug.security import generate_password_hash, check_password_hash
from flask import  render_template ,request,redirect,flash,make_response,session,jsonify,json

#imporing all we need 
from shopeaseapp import app,db   #imporing the instantate flask (app)
from shopeaseapp.mymodel import User,Vendor,Admin,Order,Payment,Product,Category,Orderdeet,Newsletter#writing nt raw we firs import the class post which is in the mode.py
#from conferenceapp.forms import LoginForm




@app.route('/')
def home():
    id = session.get('loggedin')
    
    userdeets = User.query.get(id)
    productdeets=Product.query.order_by(desc(Product.product_id)).limit(12).all()
    product1k=Product.query.filter(Product.product_price == 1000).order_by(desc(Product.product_id)).limit(12).all()
    productchopchop=Product.query.filter(Product.product_categoryid == 7).order_by(desc(Product.product_id)).limit(12).all()
    productelectronics=Product.query.filter(Product.product_categoryid == 1).order_by(desc(Product.product_id)).limit(12).all()

    categorydeets=Category.query.all()
    return render_template('user/fpreal.html',userdeets=userdeets,productdeets=productdeets,categorydeets=categorydeets,product1k=product1k, productchopchop= productchopchop,productelectronics=productelectronics)

@app.route('/signup')
def user_signup():
    return render_template('user/fpsignup.html')


@app.route('/signup/submit',methods=['GET','POST'])
def user_signup_submit():
    if request.method=='GET':
        return redirect('/signup')
    else:
        fname=request.form.get('firstname')
        lname=request.form.get('lastname')
        email=request.form.get('email')
        address=request.form.get('address')
        phoneno=request.form.get('phoneno')
        pwd=request.form.get('password')
        cpwd=request.form.get('passwordconf')
        if email=="" or pwd=="" or cpwd=="" or fname=="" or lname=="" or address=="" or phoneno=="":
            message="please fill up all fields" 
            flash(message)
            return redirect('/signup')
        elif pwd!=cpwd:
            message=" password mismatch"
            flash(message)
            return redirect('/signup')
        else:
            formated=generate_password_hash(pwd)
            #instantiate  a class oftable User
            u=User(user_email=email,user_passwrd=formated,user_fname=fname,user_lname=lname,user_phoneno=phoneno,user_address=address)
            db.session.add(u)
            db.session.commit()
            return redirect('/login' )


        
@app.route('/login')
def user_login():
    id=session.get('loggedin')
    userdeets=User.query.get(id)
    return render_template('user/fplogin.html',userdeets=userdeets)


@app.route('/login/submit',methods=['POST'])
def user_logsub():
    if request.method=="GET":
        return redirect('/login')
    else:
        a=request.form.get('email')
        b=request.form.get('password')
        deets=User.query.filter(User.user_email==a).first()
        if a=='' or b=='':
            message='please fill all fields'
            flash(message)
            return redirect('/login')
        else:
            if deets:
                formattedpassword=deets. user_passwrd
                chk=check_password_hash(formattedpassword,b)
                if chk:
                    id=deets.user_id
                    session['loggedin']=id#creating a session
                    userdeets = User.query.get(id)
                    return redirect('/')
                else:
                    message="invalid credentials"
                    flash(message)
                    return redirect('/login')

            else:
                message="invalid credentials"
                flash(message)
                return redirect('/login')


@app.route('/user/edit/profile/')
def edit_profile():
    id=session.get('loggedin')
    userdeets = User.query.get(id)
    categorydeets=Category.query.all()
    if id == None:
        return redirect('/login')
    else:
        return render_template('user/edit_profile.html', userdeets= userdeets, categorydeets= categorydeets)

@app.route ('/user/update/submit/<ids>',methods=['GET','POST'])  
def user_edit(ids):
   
    if request.method=='GET':
        return redirect('/') 
    else:
         id=session.get('loggedin')
         fname=request.form.get('firstname')
         lname=request.form.get('lastname')
         email=request.form.get('email')
         phoneno=request.form.get('phoneno')
         address=request.form.get('address')
         password=request.form.get('password')
         check=request.form.get('passwordconf')
         if check != password:
             message='check that your password matches the confirm password'
             flash(message)
             return redirect('/user/edit/profile')
        
         elif int(id)==int(ids):

             user=User.query.get(id)
             user.user_fname=fname
             user.user_lname=lname
             user.user_email=email
             user.user_phoneno=phoneno
             user.user_address=address
             user.user_passwrd=password
             db.session.commit()
             message='profile updated sucessfully'
             flash(message)
             return redirect('/user/edit/profile')

         else:
             return redirect('/')

@app.route('/user/order/history',methods=['GET','POST'])
def userorder_history():
    id=session.get('loggedin')
    userdeets = User.query.get(id)
    list1=[]
    list2=[]
    if id == None:
        return redirect('/login')
    else:
        
        orders=Order.query.filter(Order.order_userid == id).order_by(desc(Order.order_id)).all()
        for i in orders:
            a=i.order_id
            list1.append(a)
        for i in list1:
            details = Orderdeet.query.filter(Orderdeet.orderdeet_orderid==i).order_by(desc(Orderdeet.orderdeet_id)).all()
            list2.append(details)
       
            
        
        #return render_template('user/f.html',orders=orders,list2=list2,zip=zip)
        
            
        return render_template('user/userorder_history.html', userdeets= userdeets,orders=orders,list2=list2,zip=zip)


@app.route('/user/order/history/<ids>',methods=['GET','POST'])
def userorder_showdeethistory(ids):
    id=session.get('loggedin')
    userdeets = User.query.get(id)
    list1=[]
    list2=[]
    if id == None:
        return redirect('/login')
    elif request.method=='GET':
         return redirect('/login')
    else:
        list2 = Orderdeet.query.filter(Orderdeet.orderdeet_orderid==ids).all()
        return render_template('user/fpshowdeet.html', userdeets= userdeets,list2=list2)
            
@app.route('/newsletter/submit',methods=['GET', 'POST'])
def newsletter_submit():
    if request.method=='GET':
        return redirect('/')
    else:
        a=request.form.get('mail')
        if a == '':
            message='please fill a valid email while subcribing to newsletter'
            flash(message)
            return redirect('/')
        else:
            news=Newsletter(newsletter_email=a)
            db.session.add(news)
            db.session.commit()
            message='Succesfully Subcribed to our Newsletter'
            flash(message)
            return redirect('/')









@app.route('/user/category/<ids>')
def show_category(ids):
    id = session.get('loggedin')
    userdeets=User.query.get(id)
    categorydeets=Category.query.all()
    categoryproducts=Product.query.filter(Product.product_categoryid == ids).all()
    return render_template('user/categorypage.html',categoryproducts=categoryproducts,userdeets=userdeets,categorydeets=categorydeets)


@app.route('/user/product/order/submit/<ids>',methods=['POST'])
def order_submit(ids):
    id = session.get('loggedin')
    if id == None:
        return redirect('/login')
    else:
        
        quantity=request.form.get('quantity')
        userid=request.form.get('userid')
        vendorid=request.form.get('vendorid')
        categoryid=request.form.get('categoryid')
        productid=request.form.get('productid')
        order_ref = int(random.random() * 10000000)
        if int(quantity) <= 0:
            message='quantity cant be zero'
            flash(message)
            return redirect('/user/product/<ids>')
        else:
        
            ord=Order(order_quantity=quantity,order_userid=userid,order_vendorid=vendorid,order_categoryid=categoryid,order_productid=productid,order_ref=order_ref)
            db.session.add(ord)
            db.session.commit()
            return redirect('/')

@app.route('/user/product/<ids>')
def user_prodord(ids):
    
        id = session.get('loggedin')
        userdeets=User.query.get(id)
        productdeets=Product.query.get(ids)
        
        return render_template('user/stupid.html',productdeets=productdeets,userdeets=userdeets)

@app.route('/user/order/history')
def user_orderhist():
    id=session.get('loggedin')


@app.route('/product/<ids>')
def prod(ids):
    categorydeets=Category.query.all()
    id = session.get('loggedin')
    userdeets=User.query.get(id)
    productdeets=Product.query.get(ids)
    prodi=productdeets.product_vendorid
    productvendsame=Product.query.filter(Product.product_vendorid==prodi, Product.product_id != ids).order_by(desc(Product.product_id)).limit(4).all()
    catdi=productdeets.product_categoryid
    productcatsame=Product.query.filter(Product.product_categoryid==catdi, Product.product_id != ids).all()

    
   
    return render_template('user/fpproduct.html',categorydeets=categorydeets,userdeets=userdeets,productdeets=productdeets,productvendsame=productvendsame,productcatsame=productcatsame)

#dicts marger for add to cart
def MagerDicts(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1 + dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items())+ list(dict2.items()))
    return False



#adding to cart
@app.route('/addcart',methods=['POST'])
def addcart():
    try:
        productid=request.form.get('productid')
        quantity=request.form.get('quantity')
        product=Product.query.filter_by(product_id=productid).first()
        
        
        
        if productid and quantity and request.method == 'POST':

            DictItems={productid:{'name':product.product_name,'price':product.product_price,'quantity':quantity,'image':product.product_image,'id':product.product_id}}
            if 'shoppingcart' in session:
                print(session['shoppingcart'])
                if productid in session['shoppingcart']:
                    for key,item in session['shoppingcart'].items():
                        if int(key) == int(productid):
                            session.modified= True
                            item['quantity']+=1
                else:
                    session['shoppingcart']=MagerDicts(session['shoppingcart'],DictItems)
                    return redirect(request.referrer)
            else:
                session['shoppingcart']=DictItems
                return redirect(request.referrer)
    except Exception as e:

        print(e)
    finally:

        return redirect(request.referrer)



@app.route('/cart')
def usercat():
    id = session.get('loggedin')
    userdeets=User.query.get(id)
    categorydeets=Category.query.all()
    

    if id==None:
        return redirect('/login')
    if 'shoppingcart' not in session:

        return redirect('/')
        #request.referrer
    SubTotal=0
    grandtotal=0
    vat=0
    for key ,prod in session['shoppingcart'].items():
        SubTotal+=(float(prod['price'])*float(prod['quantity']))
        vat=('%.2f'%(0.075*float(SubTotal)))
        grandtotal=float(vat) + float(SubTotal)
    return  render_template('user/cart.html',userdeets=userdeets,vat=vat,grandtotal=grandtotal,categorydeets=categorydeets)



#emptying a cart
@app.route('/empty/cart')
def empty_cart():
    try:
        session.clear()
        return redirect('/')
    except Exception as e:
        print(e)
        return 'a'

@app.route('/update/cart/<int:id>',methods=['POST'])
def update_cart(id):
    if 'shoppingcart' not in session or len(session['shoppingcart'])<=0:
        return redirect('/')
    if request.method=='POST':
        quantity=request.form.get('quantity')
        try:
            session.modified=True
            for key,item in session['shoppingcart'].items():
                if int(key)==id:
                    item['quantity']=quantity
                    flash('cart updated')
                    return redirect('/cart')
        except Exception as e:
            print(e)
            return redirect('/cart')

"""removing a item from cart"""
@app.route('/remove/cart/<int:id>')
def remove_cart(id):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect('/')
    
    try:
        session.modified = True
        for key, item in session['shoppingcart'].items():
            if int(key)==id:
                session['shoppingcart'].pop(key, None)
                return redirect('/cart')
    except Exception as e:
        print(e)
        return redirect('/cart')

@app.route('/empty/cart')
def emptyCart():
    try:
        session.clear()
        return redirect('/')
    except Exception as e:
        print(e)

@app.route('/clear/cart')
def clear_cart():
    try:
        session.pop('shoppingcart', None)
        return redirect('/')
    except Exception as e:
        print(e)

@app.route('/checkout',methods=['GET','POST'])   
def checkout():
    id = session.get('loggedin')
    userdeets=User.query.get(id)
  
    grandtotal=request.form.get('grandtotal')
   
    if request.method=='GET' or id==None:

        return redirect('/login')
    else:
        order_ref = int(random.random() * 10000000)
        mo=Order(order_ref=order_ref,order_userid=id)
        db.session.add(mo)
        db.session.commit()
        orderdeets_orderid=mo.order_id
        #ref for payment
        ref= int(random.random() * 10000000)
        session['refno']=ref
        subtotal=0
        vat=0
        for x,y in session['shoppingcart'].items():
            subtotal=subtotal+(float(y['price'])*float(y['quantity']))
            vat=("%.2f"% (0.075*float(subtotal)))
            grandtotal=float(vat)+ float(subtotal)
            quantity=y['quantity']
            prodiddeets=Product.query.get(x)
            prodvendid=prodiddeets.product_vendorid
            productid=x
            prodcategoryid=prodiddeets.product_categoryid
            od=Orderdeet(orderdeet_quantity=quantity,orderdeet_amt=grandtotal,orderdeet_orderid=orderdeets_orderid,orderdeet_vendorid=prodvendid,orderdeet_productid=productid,orderdeet_categoryid=prodcategoryid)
            db.session.add(od)
            #always use YOUR commit outside the loop to aviiod repetition
        db.session.commit()
        p=Payment(payment_amount=grandtotal,payment_userid=id,payment_orderid=orderdeets_orderid,payment_ref=ref)
        db.session.add(p)
        db.session.commit()
        return redirect('/confirm/pay')


@app.route('/confirm/pay',methods=['GET' ,'POST'])
def confirm_pay():
     id = session.get('loggedin')
     ref=session.get('refno')
     if id == None or ref == None:
         return redirect('/')
     userdeets=User.query.get(id)
     deets=Payment.query.filter(Payment.payment_ref == ref).first()
     if request.method=='GET':
         return render_template('user/confirmpay.html',userdeets=userdeets,deets=deets)
     else:
         data={"email":userdeets.user_email,"amount":deets.payment_amount,"reference":deets.payment_ref}
         headers={"Content-Type":'application/json',"Authorization":"Bearer sk_test_cba23255fcc0206b36b07013cb8dd028d0c2f534"}
         response= requests.post("https://api.paystack.co/transaction/initialize",headers=headers,data=json.dumps(data))
         rspjson=json.loads(response.text)
         if rspjson.get('status')==True:
             authur1=rspjson['data']['authorization_url']
             session.pop('shoppingcart',None)
             return redirect(authur1)
         else:
             message='Please check your internet '
             flash(message)
             return redirect('/cart')


@app.route('/user/payverify')
def paystack_verf():
    #gettting the seeeion of the ref 
    ref=session.get('refno')
    #trying to update your payment table with the reponse from paystack
    headers={"Content-Type":'application/json',"Authorization":"Bearer sk_test_cba23255fcc0206b36b07013cb8dd028d0c2f534"}
    response= requests.get(f"https://api.paystack.co/transaction/verify/{ref}",headers=headers)
    rsp=response.json()#in json formatting
    if rsp['data']['status'] == 'success':
        amt=rsp['data']['amount']
        ipaddress=rsp['data']['ip_address']
        p=Payment.query.filter(Payment.payment_ref == ref).first()
        p.payment_status='paid'
        db.session.add(p)
        db.session.commit()
        message=f' Your payment of {p.payment_amount} Naira was Successful with ref no {p.payment_ref}. Kindly visit your profile to view your order history'
        flash(message)
        return redirect('/result/pay')
    else:
        p=Payment.query.filter(Payment.pay_ref == ref).first()
        p.payment_status='failed'
        db.session.add(p)
        db.session.commit
        message='Your payment was Unsuccesful.'
        flash(message)
        return redirect('/result/pay')


@app.route('/result/pay')
def pay_result():
    id = session.get('loggedin')
    
    userdeets = User.query.get(id)
    productdeets=Product.query.all()
    categorydeets=Category.query.all()

    return render_template('/user/result_pay.html',userdeets=userdeets,productdeets=productdeets,categorydeets=categorydeets)


@app.route('/user/search',methods=['GET','POST'])
def search():
    id = session.get('loggedin')
    
    userdeets = User.query.get(id)
    productdeets=Product.query.all()
    categorydeets=Category.query.all()
    if request.method=='GET':
        return redirect('/')
    else:
        text=request.form.get('searchtext')
        results=Product.query.filter(Product.product_name.ilike(f'%{text}%')).order_by(desc(Product.product_id)).limit(12).all()
        return render_template('user/search.html',userdeets=userdeets,categorydeets=categorydeets,results=results)
        
            



       
        


    










@app.route('/logout')
def user_logout():
    cartid=session.get('shoppingcart')
    if cartid != None:
        session.pop('loggedin')
        session.pop('shoppingcart')
        return redirect('/')
    else:
        session.pop('loggedin')
        return redirect('/')


@app.route('/vendor')
def vendor():
    return render_template('vendor/fpvendor.html')


@app.route('/vendor/signup')
def vendor_signup():
    return render_template('vendor/fpvendorsignup.html')

@app.route('/vendor/edit_profile',methods=['GET','POST'])
def vendor_edit():
    id = session.get('logge')
    vendordeets=Vendor.query.get(id)
    if id ==None:
        return redirect('/vendor/signup')
    else:
        return render_template('vendor/vendoredit.html',vendordeets=vendordeets)
    

@app.route('/vendor/signup/submit',methods=['GET','POST'])
def vendor_signup_submit():
    if request.method=='GET':
        return redirect('/vendor/signup')
    else:
         

        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        email=request.form.get('email')
        phoneno=request.form.get('phoneno')
        vendor_address=request.form.get('vendor_address')
        vendor_storename=request.form.get('vendor_storename')
        vendor_password=request.form.get('vendor_password')
        vendor_passwordconf=request.form.get('vendor_passwordconf')
        if email=="" or firstname=="" or lastname=="" or phoneno=='' or vendor_address=='' or vendor_storename=="" or vendor_passwordconf=="" or vendor_password=="":
            message="please complete al fields"
            flash(message)
            return redirect('/vendor/signup')
        elif vendor_password != vendor_passwordconf:
            message="password mismatch"
            flash(message)
            return redirect('/vendor/signup')
        else:
            formated=generate_password_hash(vendor_password)
            a=Vendor(vendor_email=email,vendor_passwrd=formated,vendor_fname=firstname,vendor_lname=lastname,vendor_address=vendor_address,vendor_storename=vendor_storename,vendor_phoneno=phoneno)
            db.session.add(a)
            db.session.commit()
            return redirect('/vendor/login')



@app.route('/vendor/login')
def vendor_login():
    
    
    return render_template('vendor/fpvendorlogin.html')


@app.route('/vendor/login/submit',methods=['GET','POST'] )
def vendor_login_submit():
     if request.method=="GET":
         return redirect('/vendor/login')
     else:
         a=request.form.get('vendor_email')
         b=request.form.get('vendor_password')
         deets=Vendor.query.filter(Vendor.vendor_email==a).first()
         if a=='' or b=='':
             message="pls fill in all fields"
             flash(message)
             return redirect('/vendor/login')
         
         else:
             if deets:
                 formattedpassword=deets.vendor_passwrd
                 chk=check_password_hash(formattedpassword,b)
                 if chk:
                     id=deets.vendor_id
                     session['logge']=id#creating a session
                     vendordeets = Vendor.query.get(id)
                     return redirect('/vendor/home')
                 else:
                     message="invalid credentials"
                     flash(message)
                     return redirect('/vendor/login')
             else:
                 message="invalid credentials"
                 flash(message)
                 return redirect('/vendor/login')



@app.route('/vendor/home',methods=['GET','POST'])
def vendor_home():
    if request.method=='POST':
        return redirect('/vendor/login')
    else:
        id = session.get('logge')
        vendordeets = Vendor.query.get(id)
        categorydeets=Category.query.all()
        productdeets=Product.query.filter(id==Product.product_vendorid).all()
        orderdeets=Orderdeet.query.filter(id==Orderdeet.orderdeet_vendorid ).all()
        # orderno=orderdeets.orderdeet_orderid.all()
        # paymentde=Payment.query.filter(Payment.payment_orderid==orderno,Payment.payment_status=='paid').all()
        # orderdeetshistory=Orderdeet.query.filter(id==Orderdeet.orderdeet_vendorid).all()
        paystat=Payment.query.filter(Payment.payment_status=='paid').all()
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        list5=[]
  
        
        for i in paystat:

            a=i.payment_orderid
            

            list1.append(a)
        for i in list1:
            b=Orderdeet.query.filter(Orderdeet.orderdeet_orderid==i,Orderdeet.orderdeet_vendorid==id).all()
            
            #c=b.orderdeet_order.order_userid
            for i in b:
                c=i.orderdeet_order.order_userid
                list3.append(c)
                
                for i in list3:
                    d=User.query.filter(User.user_id==i).all()
                    list4.append(d)
                   
            
            list2.append(b)
        #return render_template('user/f.html',list5=list5)
        return render_template('vendor/fpvendorhome.html',vendordeets=vendordeets,categorydeets=categorydeets,productdeets=productdeets,list2=list2,list4=list4,zip=zip)
    

   
    
        

@app.route('/vendor/order/editstatus/submit/<ids>',methods=['GET','POST'])
def edit_vendorstatus(ids):
    if request.method=='GET':
        return redirect('/vendor/login')
    else:
        status=request.form .get('status')
       
        orderid=Order.query.get(ids)
        orderid.order_status=status
        db.session.commit()
        message='order status updated successfully'
        flash(message)
        return redirect('/vendor/home')











 #route for submittingproduct upload
@app.route('/vendor/addproduct', methods=['GET','POST'])
def addproduct():
    id=session.get('logge')
    if id==None:
        return redirect('/vendor/login')
    if request.method =='GET':
        
        return redirect('/vendor/home')
    else:
        #Retrieve form data (request.form....)
        product_name = request.form.get('product_name')
        
        product_quantity= request.form.get('product_quantity')
        product_price= request.form.get('product_price')
        product_description=request.form.get('product_description')
        product_vendorid=request.form.get('product_vendorid')
        product_categoryid=request.form.get('product_category')
        

        #request file
        pic_object = request.files.get('image')
        
        original_file =  pic_object.filename
        
        if product_name =='' or   product_quantity =='' or product_price =='' or product_description=='' or product_vendorid=='' or product_categoryid=='':

            message="no field can  be left empty"
            flash(message)
            #redirect('/vendor/home')
        if original_file !='': #check if file is not empty
            extension = os.path.splitext(original_file)
            
            if extension[1].lower() in ['.jpg','.png']:
               
                fn = math.ceil(random.random() * 100000000)  
                
                save_as = str(fn)+extension[1] 
                pic_object.save(f"shopeaseapp/static/uploadedimg/{save_as}")
                #insert other details into db
                b = Product(product_name=product_name,product_quantity=product_quantity,product_description=product_description,product_vendorid=product_vendorid,product_categoryid=product_categoryid,product_image=save_as,product_price=product_price)
                db.session.add(b)
                db.session.commit() 
                message='Product added succesfully' 
                flash(message)          
                return redirect("/vendor/home")
            else:
                message='file not allowed'
                flash(message)
                return redirect("/vendor/home")

@app.route ('/vendor/update/submit/<ids>',methods=['GET','POST'])  
def vendor_update(ids):
    id=session.get('logge')
    if request.method=='GET':
        return redirect('/') 
    else:
        fname=request.form.get('firstname')
        lname=request.form.get('lastname')
        email=request.form.get('email')
        phoneno=request.form.get('phoneno')
        address=request.form.get('vendor_address')
        storename=request.form.get('vendor_storename')
        password=request.form.get('vendor_password')

        if int(id)==int(ids):
            vendor=Vendor.query.get(id)
            vendor.vendor_fname=fname
            vendor.vendor_lname=lname
            vendor.vendor_email=email
            vendor.vendor_phoneno=phoneno
            vendor.vendor_address=address
            vendor.vendor_storename=storename
            vendor.vendor_passwrd=password
            db.session.commit()
            message='profile updated sucessfully'
            flash(message)
            return redirect('/vendor/edit_profile')




@app.route('/vendor/edit/upload/<ids>')
def vend_editupload(ids):
     id=session.get('logge')
     if id=='None':
        return redirect('/') 
     else:
         productdeets=Product.query.get(ids)
         vendordeets=Vendor.query.all()
         categorydeets=Category.query.all()
         return render_template('vendor/fpproductup.html',productdeets=productdeets,vendordeets=vendordeets,categorydeets=categorydeets)


@app.route('/vendor/editupload/submit/<ids>',methods=['GET','POST'])
def vend_editupsubmit(ids): 
    if request.method=='GET':
        return redirect('/')
    else:
        product_name = request.form.get('product_name')
        product_quantity= request.form.get('product_quantity')
        product_price= request.form.get('product_price')
        product_description=request.form.get('product_description')
        product_vendorid=request.form.get('product_vendorid')
        product_categoryid=request.form.get('product_category')
        #request file
        pic_object = request.files.get('image')
        original_file =  pic_object.filename
        if product_name =='' or   product_quantity =='' or product_price =='' or product_description=='' or product_vendorid=='' or product_categoryid=='' or pic_object=='':
            
            message="no field can  be left empty"
            flash(message)
            return redirect('/vendor/home')
        if original_file !='': #check if file is not empty
            extension = os.path.splitext(original_file)
            
            
            if extension[1].lower() in ['.jpg','.png']:
               
                fn = math.ceil(random.random() * 100000000)  
                
                save_as = str(fn)+extension[1] 
                pic_object.save(f"shopeaseapp/static/uploadedimg/{save_as}")
               
        
       

                product=Product.query.get(ids)
               
                product.product_name=product_name
                product.product_quantity=product_quantity
                product.product_price=product_price
                product.product_description=product_description
                product.product_categoryid=product_categoryid
                product.product_vendorid=product_vendorid
                product.product_image=save_as
                db.session.commit()
                message='product  updated sucessfully'
                flash(message)
                return redirect('/vendor/home')
        else:
            message='check that image or category field not left empty'
            flash(message)
            return redirect('/vendor/home')
            
        





@app.route('/vendor/logout')
def vendor_logout():
    if request.method =='GET':
        return redirect('/vendor/login')
    elif id != '':
        
        session.pop('logged')
        return redirect('/vendor/login')


@app.errorhandler(404)
def pagenotfound(error):
    id = session.get('loggedin')
    
    userdeets = User.query.get(id)
    productdeets=Product.query.all()
    categorydeets=Category.query.all()

    return render_template('user/tryanderror.html',error=error,userdeets=userdeets,productdeets=productdeets,categorydeets=categorydeets)#returning the error back into it as avariable