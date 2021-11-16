# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 2020

Evgeniya Zhukova
ID: 101239316
"""
#main and functions

#import module with database-related functions
import db

#import classes
from objects import Cart


#display title
def display_title():
    print()
    print("***ONLINE TOY STORE***")
    print()    
    display_menu()

 
#display command menu
def display_menu():
    print("Command Menu:")
    print("view - View Toys by category")
    print("add  - Add Toys into shopping cart")
    print("del  - Delete Toys from shopping cart")
    print("cart - View shopping cart") 
    print("pay  - View the receipt")   
    print("exit - Exit program") 
 
    
#display all categories
def display_categories():
    print()
    print("CATEGORIES")
    categories = db.get_categories()    
    for category in categories:
        print(str(category.id) + ". " + category.name)


#display all toys    
def display_toys(toys, title_term):
    print()
    print("Kids Play Sets: " + title_term)
    line_format = "{:3s} {:12s} {:33s} {:6s} {:8s}"
    print(line_format.format("ID", "Category", "Name", "Age", "Price"))
    print("-" * 65)
    for toy in toys:
        print(line_format.format(str(toy.id), toy.category.name,
                                 toy.name,
                                 str(toy.age), 
                                 str(toy.price)))
    print() 
 
    
#display shopping cart
def display_cart(cart):
    print()
    line_format = "{:3s} {:12s} {:33s} {:6s} {:8s} {:8s}"
    print(line_format.format("ID", "Category", "Name", "Age", "Price", "Discount Price"))
    print("-" * 81)
    i = 1
    for toy in cart.cart_list:
        print(line_format.format(str(i),
                                toy.category.name,
                                toy.name,
                                str(toy.age), 
                                str(toy.price),
                                str(round(toy.discount_price, 2))))
        i += 1
    print()


#function for return variable discount_price for sorting
def byPrice_key(toy):
    return toy.discount_price 


#count discounts
def count_discounts(cart):
    #define variables
    lego = 0; play_doh = 0; art_craft = 0
    #count how many toys of each category in shopping cart
    for toy in cart.cart_list:
        #count sum of toys in shopping cart
        cart.sum += toy.price
        if toy.category.name == "Lego":
            lego +=1
        elif toy.category.name == "Play-Doh":
            play_doh +=1 
        elif toy.category.name == "Art & Craft":
            art_craft +=1
    #assign a discount price for toys are two or more from the same category
    for toy in cart.cart_list:
        if lego >=2 and toy.category.name == "Lego":
            toy.discount_price = toy.price * 0.85
        elif play_doh >=2 and toy.category.name == "Play-Doh":
            toy.discount_price = toy.price * 0.85 
        elif art_craft >=2 and toy.category.name == "Art & Craft":
            toy.discount_price = toy.price * 0.85 
        else:
            toy.discount_price = toy.price
        #count sum of discount prices for toys in shopping cart
        cart.sum_discount += toy.discount_price         
    #count how many free toys client have in receipt
    cart.free_toys = len(cart.cart_list) // 4
    #define list for sorting shopping cart by discount_price
    cart_sort_price = []
    if cart.free_toys > 0:
        #sort cart by discount_price
        cart_sort_price = sorted(cart.cart_list, key = byPrice_key)
        i = 0
        for toy in cart_sort_price:
            #count sum of free toys
            cart.sum_free += cart_sort_price[i].discount_price
            cart_sort_price[i].discount_price = 0
            i += 1
            if (cart.free_toys == i):
                break
    return cart


#view all toys by category    
def view_toys_by_category():
    display_categories()
    #asking ID of category what user would like to see
    category_id = None
    while True:
        try:
            category_id = int(input("Category ID: "))
        except:
            print("You entered an invalid input. Please try again.") 
        if (category_id != None):
            break
    #get category from database using category id
    category = db.get_category(category_id)
    if category == None:
        print("There is no category with that ID.\n")
    else:
        #display toys from this category
        toys = db.get_toys_by_category(category_id)
        display_toys(toys, category.name.upper())


#add toys into shopping cart         
def add_toy(cart):
    #display all toys
    toys = db.get_toys()
    display_toys(toys, "")
    #print discount options
    print("*" * 29 + "DISCOUNTS" + "*" * 27)
    print("Buy TWO Toys from ONE category - get 15% discount for all Toys from that category")
    print("Buy THREE ANY Toys - get FOURTH (with the lowest price) for FREE")
    print("-" * 65)
    #asking ID of toys what user would like to add
    print("What would you like to add to the shopping cart?")
    choice = "y"
    while choice.lower() == "y":    
        toy_id = None   
        while True:
            try:
                toy_id = int(input("Toy ID: "))
            except:
                print("You entered an invalid input. Please try again.\n")
            if (toy_id != None):
                break 
        #get toy from database using toy id
        toy = db.get_toy(toy_id)    
        if toy == None:
            print("There is no toy with this ID.")
        else:
            #add toy to shopping cart
            cart.cart_list.append(toy)  
            print(toy.name + " was added.")
        #asking if the user would like to continue
        choice = input("Continue add? (y/n): ")
    print()  
    return cart       


#delete toys from shopping cart        
def delete_toy(cart):
    if len(cart.cart_list) == 0:
        print("There are no items in the shopping cart.\n")
        return
    else:
        print("What would you like to delete from the shopping cart?")           
        choice = "y"
        while choice.lower() == "y": 
            #display shopping cart
            view_cart(cart)
            #asking ID of toys what user would like to delete     
            number = None   
            while True:
                try:
                    number = int(input("Toy ID: "))
                except:
                    print("You entered an invalid input. Please try again.\n")
                if (number != None):
                    break 
            try:
                #delete toy with that ID
                toy = cart.cart_list.pop(number-1)
                print(toy.name + " was deleted.")
            except:
                print("There is no item with this ID in the shopping cart.")
                #asking if the user would like to continue
            choice = input("Continue delete? (y/n): ")
        print()  
        return cart 


#view shopping cart    
def view_cart(cart):
    if len(cart.cart_list) == 0:
        print("There are no items in the shopping cart.\n")
        return
    else:
        #count discounts and display cart
        count_discounts(cart)
        display_cart(cart)
        cart.zero_sum()
    return cart


#view receipt    
def view_receipt(cart):
    #print receipt title
    print("\n\n\n" + "*" * 33 + "ONLINE TOY STORE" + "*" * 32)
    print("*" * 38 + "RECEIPT" + "*" * 36)
    print("Cashier: Evgeniya Zhukova")
    #view cart
    count_discounts(cart)
    display_cart(cart)
    print("Number of items: " + str(len(cart.cart_list)))  
    #print discounts and total price
    print("*" * 36 + "DISCOUNTS" + "*" * 36)
    print("Buy TWO Toys from ONE category - get 15% discount for all Toys from that category")
    print("You Saved: " + str(round((cart.sum - cart.sum_discount), 2)))
    print()
    print("Buy THREE ANY Toys - get FOURTH (with the lowest price) for FREE") 
    print("You Received " + str(cart.free_toys) + " Free Toys!")
    print("You Saved: " + str(round(cart.sum_free, 2)))
    print("*" * 81)   
    print("Price:                   " + str(round(cart.sum, 2)))
    print("Price with Discounts:    " + str(round(cart.sum_discount - cart.sum_free, 2)))
    print("HST 13%:                 " + str(round(((cart.sum_discount - cart.sum_free) * 0.13), 2)))
    print("TOTAL PRICE:             " + str(round(((cart.sum_discount - cart.sum_free) + (cart.sum_discount - cart.sum_free) * 0.13), 2)))    
    print("*" * 81)
    cart.zero_sum()
    print()  


#main function    
def main():
    db.connect()
    display_title()
    #creating Cart object
    cart = Cart()
    #accepting user`s choice of command
    while True:        
        command = input("Command: ")
        if command == "view":
            view_toys_by_category()
        elif command == "add":
            add_toy(cart)
        elif command == "del":
            delete_toy(cart)
        elif command == "cart":
            view_cart(cart)
        elif command == "pay":
            view_receipt(cart)
        elif command == "exit":
            break
        else:
            print("Not a valid command. Please try again.\n")
        display_menu()    
    db.close()
    print("Bye!")
    
if __name__ == "__main__":
    main()