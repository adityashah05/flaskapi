"""
This is module is used to create the database with the defined tables and the schemas.
Once the database is created, it leverages pandas to read the csv provided in the challenge and inserts the data
That's how the eshop_data.db was created
"""


from marshmallow import Schema, fields
import os
import pandas as pd
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flaskapi import app

CREATE_DB = False

if CREATE_DB:

    db = SQLAlchemy(app)

    class Orders(db.Model):
        __tablename__ = 'orders'
        id = db.Column(db.Integer, primary_key=True)
        created_at = db.Column(db.DateTime)
        vendor_id = db.Column(db.Integer)
        customer_id = db.Column(db.Integer)
        order_lines = db.relationship(
                    'OrderLines', backref="order", lazy="select")


    class Products(db.Model):
        __tablename__ = 'products'
        id = db.Column(db.Integer, primary_key=True)
        description = db.Column(db.String)
        product_promotion = db.relationship(
                    'ProductPromotions', backref="product", lazy="select")
        order_lines = db.relationship(
                    'OrderLines', backref="product", lazy="select")


    class Promotions(db.Model):
        __tablename__ = 'promotions'
        id = db.Column(db.Integer, primary_key=True)
        description = db.Column(db.String)
        product_promotion = db.relationship(
                    'ProductPromotions', backref="promotion", lazy="select")


    class ProductPromotions(db.Model):
        __tablename__ = 'product_promotions'
        date = db.Column(db.Date, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
        promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'))


    class Commissions(db.Model):
        __tablename__ = 'commissions'
        date = db.Column(db.Date, primary_key=True)
        vendor_id = db.Column(db.Integer, primary_key=True)
        rate = db.Column(db.Numeric)


    class OrderLines(db.Model):
        __tablename__ = 'order_lines'
        order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
        product_description = db.Column(db.String)
        product_price = db.Column(db.Numeric)
        product_vat_rate = db.Column(db.Numeric)
        discount_rate = db.Column(db.Numeric)
        quantity = db.Column(db.Integer)
        full_price_amount = db.Column(db.Numeric)
        discounted_amount = db.Column(db.Numeric)
        vat_amount = db.Column(db.Numeric)
        total_amount = db.Column(db.Numeric)

    if os.path.exists('eshop_data.db'):
        os.remove('eshop_data.db')

    db.create_all()

    filepath = os.getcwd()+'/data/'
    files = os.listdir(filepath)
    conn = sqlite3.connect('eshop_data.db')

    for file in files:
        filename = filepath+file
        data = pd.read_csv(filename)
        data.to_sql(file.split('.')[0], conn, if_exists='append', index=False)



