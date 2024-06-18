
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

      # Edit Customer, Item, and Reviews to inherit from SerializerMixin.
    # Add serialization rules to avoid errors involving recursion depth (be careful about tuple commas).
    # Customer should exclude reviews.customer
    serialize_rules = ("-reviews.customer",)# Exclude reviews.customer to avoid recursion

    # a relationship named reviews that establishes a relationship with the Review model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review.
    reviews = db.relationship('Review', back_populates='customer')
    
    #Update Customer to add an association proxy named items to get a list of items through the customer's reviews relationship. 
    # # Association proxy to get items for this project through assignments
    items = association_proxy(
        'reviews', 'item', creator=lambda item_obj: Review(item=item_obj)
    )

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>' 
    

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items' 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    # Exclude reviews.item to avoid recursion
    serialize_rules = ('-reviews.item',) 

    # a relationship named reviews that establishes a relationship with the Review model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review.
    reviews = db.relationship('Review', back_populates='item')
   
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    
    # exclude customer.reviews and item.reviews
    # tuple only one comma
    serialize_rules = ('-customer.reviews', '-item.reviews')

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))



    # Relationship mapping the review to related customer
    # Use plural names ('reviews') for relationships that represent collections (one-to-many). Customer has many reviews
    customer = db.relationship('Customer', back_populates='reviews') #singular customers inverse to plural reviews
    item = db.relationship('Item', back_populates='reviews') #singular item inverse to plural reviews


    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, {self.customer.name}, {self.item.name}>'