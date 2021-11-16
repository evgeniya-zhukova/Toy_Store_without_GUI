# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 2020

Evgeniya Zhukova
ID: 101239316
"""
#classes 


class Toy:
    #constructor
    def __init__(self, id=0, name=None, age=0, 
                 price=0, category=None, discount_price=0):
        self.id = id
        self.name = name
        self.age = age
        self.price = price
        self.category = category
        self.discount_price = price
        
class Category:
    #constructor
    def __init__(self, id=0, name=None):
        self.id = id
        self.name = name
        
class Cart:
    #constructor
    def __init__(self, cart_list = [], sum=0, sum_discount=0, sum_free=0, free_toys=0):
        self.cart_list = cart_list
        self.sum = sum
        self.sum_discount = sum_discount
        self.sum_free = sum_free
        self.free_toys = free_toys
        
    #all cart sums assign zero
    def zero_sum(self):
        self.sum = 0
        self.sum_discount = 0
        self.sum_free = 0
        self.free_toys = 0