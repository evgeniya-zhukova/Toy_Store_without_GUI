# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 2020

Evgeniya Zhukova
ID: 101239316
"""
#database-related functions


import sys
import os
import sqlite3
from contextlib import closing

#import classes
from objects import Category
from objects import Toy

conn = None

#connect with database
def connect():
    global conn
    if not conn:
        if sys.platform == "win32":
            DB_FILE = "toys.sqlite"
        else:
            HOME = os.environ["HOME"]
            DB_FILE = HOME + "toys.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

#close connection       
def close():
    if conn:
        conn.close()
 
#create an object of class Category with data from database  
def make_category(row):
    try:
        return Category(row["categoryID"], row["categoryName"])
    except:
        print("You entered an invalid input. Please try again.") 

#create an object of class Toy with data from database 
def make_toy(row):
    try:
        return Toy(row["toyID"], row["name"], row["for_age"],
            row["price"], make_category(row))
    except:
        print("You entered an invalid input. Please try again.") 

#get all categories from database
def get_categories():
    query = '''SELECT categoryID, name as categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()       
    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories

#get certain category from database
def get_category(category_id):
    query = '''SELECT categoryID, name AS categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()        
    category = make_category(row)
    return category

#get info about all toys from database
def get_toys():
    query = '''SELECT toyID, Toys.name, for_age, price,
                      Toys.categoryID as categoryID,
                      Category.name as categoryName
               FROM Toys JOIN Category
                      ON Toys.categoryID = Category.categoryID'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()
    toys = []
    for row in results:
        toys.append(make_toy(row))
    return toys

#get info about certain toy from database
def get_toy(toy_id):
    query = '''SELECT toyID, Toys.name, for_age, price,
                      Toys.categoryID as categoryID,
                      Category.name as categoryName
               FROM Toys JOIN Category
                      ON Toys.categoryID = Category.categoryID
               WHERE toyID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (toy_id,))
        row = c.fetchone()        
    toy = make_toy(row)
    return toy

#get info about all toys from certain category from database
def get_toys_by_category(category_id):
    query = '''SELECT toyID, Toys.name, for_age, price,
                      Toys.categoryID as categoryID,
                      Category.name as categoryName
               FROM Toys JOIN Category
                      ON Toys.categoryID = Category.categoryID
               WHERE Toys.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()
    toys = []
    for row in results:
        toys.append(make_toy(row))
    return toys