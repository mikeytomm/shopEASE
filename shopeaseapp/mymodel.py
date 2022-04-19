import datetime
from sqlalchemy.orm import backref,relationship

from shopeaseapp import db




class User(db.Model): 
    user_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_phoneno = db.Column(db.String(255), nullable=True)
    user_passwrd = db.Column(db.String(255), nullable=False)
    user_address = db.Column(db.Text(), nullable=True)
    user_regdt = db.Column(db.DateTime(), default=datetime.datetime.utcnow())

    #setup the relationships
    userpayment = db.relationship('Payment', back_populates ='paymentuserobj')
    
  
class Newsletter(db.Model): 
    newsletter_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    
    newsletter_email = db.Column(db.String(255), nullable=False)   
    


class Vendor(db.Model):
    vendor_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    vendor_fname = db.Column(db.String(255), nullable=False)
    vendor_lname = db.Column(db.String(255), nullable=False)
    vendor_email = db.Column(db.String(255), nullable=False)
    vendor_phoneno = db.Column(db.String(255), nullable=False)
    vendor_storename = db.Column(db.String(255), nullable=False)
    vendor_address = db.Column(db.Text(), nullable=False)
    vendor_passwrd = db.Column(db.String(255), nullable=False)



    #create the relationship
    vendproduct = db.relationship('Product', back_populates ='productvendobj')
   
   




class Admin(db.Model):
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_email = db.Column(db.String(255), nullable=False)
    admin_passwrd = db.Column(db.String(255), nullable=False)



   



class Product(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_quantity = db.Column(db.String(255), nullable=False)
    product_price = db.Column(db.Integer(), nullable=False)
    product_image = db.Column(db.String(255),nullable=True)
    product_description = db.Column(db.Text(255), nullable=False)

    #create the foreign key
    product_vendorid = db.Column(db.Integer(), db.ForeignKey("vendor.vendor_id")) 
    product_categoryid = db.Column(db.Integer(), db.ForeignKey("category.category_id")) 


    #create the relationship
    productcateobj = db.relationship('Category', back_populates ='cateproduct')
    productvendobj = db.relationship('Vendor', back_populates ='vendproduct')
   
   
   
    
    



class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    order_status=db.Column(db.Enum("pending","settled"), default="pending")
   
    order_datetime =db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    order_ref = db.Column(db.String(255), nullable=False)
 
    #create the foreign keys for orders
    order_userid = db.Column(db.Integer(), db.ForeignKey("user.user_id")) 
   
    #relationship
    orderpayment = db.relationship('Payment', back_populates ='paymentorderobj')
   
   


class Orderdeet(db.Model):
    orderdeet_id= db.Column(db.Integer(), primary_key=True,autoincrement=True)
    orderdeet_quantity=db.Column(db.Integer(), nullable=False)
    orderdeet_amt=db.Column(db.Float(), nullable=False)
    #set up foreign key
    
    orderdeet_orderid = db.Column(db.Integer(), db.ForeignKey("order.order_id")) 
    orderdeet_productid = db.Column(db.Integer(), db.ForeignKey("product.product_id"))

    orderdeet_vendorid = db.Column(db.Integer(), db.ForeignKey("vendor.vendor_id"))
    orderdeet_productid= db.Column(db.Integer(), db.ForeignKey("product.product_id"))
    orderdeet_categoryid= db.Column(db.Integer(), db.ForeignKey("category.category_id"))


    #set up relationship
    orderdeet_order=db.relationship('Order',backref='order_orderdetails')
    orderdeet_product=db.relationship('Product',backref='order_productdetails')
    orderdeet_vendor = db.relationship('Vendor', backref ='vendorder')
    orderdeet_cat = db.relationship('Category', backref ='cateorder')

class Payment(db.Model):
    payment_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    payment_amount = db.Column(db.String(255), nullable=False)
    payment_status=db.Column(db.Enum("pending","paid","failed"), default="pending")
    payment_datetime = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    payment_ref=db.Column(db.Integer(),nullable=False)

    #create the foreign keys
    payment_userid = db.Column(db.Integer(), db.ForeignKey("user.user_id"))
   
   
    payment_orderid = db.Column(db.Integer(), db.ForeignKey("order.order_id"))

    #create the relationship
    paymentuserobj = db.relationship('User', back_populates ='userpayment')
  
   
    paymentorderobj = db.relationship('Order', back_populates ='orderpayment')

class Category(db.Model):
    category_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False)

    #create the relationship
    cateproduct = db.relationship('Product', back_populates ='productcateobj')
    
   
    
  

    











