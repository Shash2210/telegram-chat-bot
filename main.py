import telebot
from telebot import types

# Define the bot token and create an instance of the bot
TOKEN = "6183696542:AAFeK6RGHhu5FvYa2KaJbb5gl_nVqHS_jKY"
bot = telebot.TeleBot(TOKEN)

# Define the inventory as a dictionary with item names as keys and their attributes as values
inventory = {
    "maaza": {"price": 20, "quantity": 10, "weight": "250 ml", "type": "cold_drink", "brand": "local farm"},
    "butter": {"price": 140, "quantity": 20, "weight": "200 g", "type": "dairy", "brand": "local farm"},
    "bread": {"price": 40, "quantity": 5, "weight": "400 g", "type": "bakery", "brand": "local bakery"},
    "milk": {"price": 40, "quantity": 8, "weight": "1 lt", "type": "dairy", "brand": "local farm"},
    "salt": {"price": 35, "quantity": 12, "weight": "1 kg", "type": "salt", "brand": "local farm"},
    "cheese": {"price": 110, "quantity": 4, "weight": "300 g", "type": "dairy", "brand": "local farm"},
    "jam": {"price": 75, "quantity": 15, "weight": "200 g", "type": "snack", "brand": "local brand"},
    "ghee": {"price": 70, "quantity": 12, "weight": "350 g", "type": "dairy", "brand": "local bakery"},
    "lays": {"price": 40, "quantity": 20, "weight": "60 g", "type": "junk_chips", "brand": "local brand"},
    "water_bottle": {"price": 20, "quantity": 25, "weight": "1 lt", "type": "drink", "brand": "local brand"}
}

user_info = {}
# Define a dictionary to keep track of the user's order
order = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    user_info[user_id] = {"name": message.chat.first_name}
    bot.send_message(user_id, f"Hi {message.chat.first_name}, welcome to our store!\n\n Type /help to see available commands.")





# Define the help command
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "To view the invemtory type /inventory. To order an item, type /order <item_name>. To view your order, type /view. To confirm your order, type /confirm.")


@bot.message_handler(commands=['inventory'])
def show_inventory(message):
    inventory_str = ""
    for item_name, item in inventory.items():
        inventory_str += f"Name: {item_name}\nPrice: {item['price']}\nQuantity_Remaining: {item['quantity']}\nWeight: {item['weight']}\nType: {item['type']}\nBrand: {item['brand']}\n\n"
    bot.send_message(message.chat.id, inventory_str + "\nTo order an item, type /order <item_name>.")


# Define the order command
@bot.message_handler(commands=['order'])
def order_command(message):
    try:
        item = message.text.split()[1].lower() # Get the item name from the command
        if item in inventory: # Check if the item is in stock
            if item not in order: # If the item is not already in the order, add it
                order[item] = 0
            order[item] += 1 # Increment the quantity of the item in the order
            bot.send_message(message.chat.id, f"{item.capitalize()} added to your order. Type /view to see your order.")
        else:
            bot.send_message(message.chat.id, "Sorry, that item is not in stock.")
    except:
        bot.send_message(message.chat.id, "Please specify an item to order. Type /help for more information.")

# Define the view command
@bot.message_handler(commands=['view'])
def view_command(message):
    if order: # Check if there are any items in the order
        total_cost = 0 # Initialize the total cost of the order to zero
        message_text = "Your order:\n"
        for item, quantity in order.items():
            price = inventory[item]["price"]
            item_cost = price * quantity
            message_text += f"- {item.capitalize()} ({quantity} x {price:.2f}) = {item_cost:.2f}\n"
            total_cost += item_cost
        message_text += f"Total cost: {total_cost:.2f}\n\nType /confirm to confirm your order."
        bot.send_message(message.chat.id, message_text)
    else:
        bot.send_message(message.chat.id, "Your order is empty.")


# Define the confirm command
@bot.message_handler(commands=['confirm'])
def confirm_command(message):
    if order: # Check if there are any items in the order
        total_cost = 0 # Initialize the total cost of the order to zero
        message_text = "Your order:\n"
        for item, quantity in order.items():
            price = inventory[item]["price"]
            item_cost = price * quantity
            message_text += f"- {item.capitalize()} ({quantity} x {price:.2f}) = {item_cost:.2f}\n"
            total_cost += item_cost
        message_text += f"Total cost: {total_cost:.2f}\n\nType /delivery to choose delivery option."
        bot.send_message(message.chat.id, message_text)
        
    else:
        bot.send_message(message.chat.id, "Your order is empty.")


@bot.message_handler(commands=['delivery'])
def delivery_command(message):
    if order:
        # Create a new message with delivery options
        delivery_message = "Please choose a delivery option:"
        delivery_options = ["Home Delivery", "Store Pickup"]
        for option in delivery_options:
            delivery_message += f"\n- {option}"
        bot.send_message(message.chat.id, delivery_message)

        # Set the delivery options as a reply keyboard
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        for option in delivery_options:
            button = types.KeyboardButton(text=option)
            keyboard.add(button)
        bot.send_message(message.chat.id, "Please choose an option:", reply_markup=keyboard)

        # Set up a message handler for the delivery option
        @bot.message_handler(func=lambda message: message.text in delivery_options)
        def handle_delivery_option(message):
            option = message.text
            if option == "Home Delivery":
                bot.send_message(message.chat.id, "Please enter your address:")
                bot.register_next_step_handler(message, handle_delivery_address)
            elif option == "Store Pickup":
                bot.send_message(message.chat.id, "Your order status will be soon notified. \n\nThank you for shopping with us!")
                bot.send_message(1288513293, f"New order for delivery:\n{view_order()} \n\n select /accept to accept the order.\n\n select /decline to decline the order.  ")
                order.clear()
        

        # Set up a message handler for the delivery address
        def handle_delivery_address(message):
            address = message.text
            bot.send_message(message.chat.id, "Your order status will be soon notified. \n\nThank you for shopping with us!")
            bot.send_message(1288513293, f"New order for delivery:\n{view_order()} \n\n select /accept to accept the order.\n\n select /decline to decline the order.  ")
            order.clear()

            
    else:
        bot.send_message(message.chat.id, "Your order is empty.")

def view_order():
    order_summary = ""
    for item in order:
        quantity = order[item]
        item_price = inventory[item]["price"]
        item_cost = item_price * quantity
        order_summary += f"\n- {item}: {quantity} x {item_price:.2f} = {item_cost:.2f}"
    user_id = list(order.keys())[0] # Get the user ID from the order dictionary
    user_name = user_info.get(user_id, {}).get("name", "Unknown") # Get the user's name from user_info
    order_summary = f"Order for {user_name}:\n{order_summary}"
    return order_summary

# Handle the store owner's response to the order
@bot.message_handler(commands=['accept', 'decline'])
def handle_store_response(message):
    if message.chat.id != 1288513293: # Check that the message is from the store owner
        return
    
    if message.text == "/accept":
        # Notify the user that their order has been accepted
        for user_id in user_info:
            bot.send_message(user_id, "Your order has been accepted. Thank you have a nice day!")
        
    elif message.text == "/decline":
        # Notify the user that their order has been declined
        for user_id in user_info:
            bot.send_message(user_id, "Your order has been declined. Please try again later.")
        
    else:
        bot.send_message(message.chat.id, "Invalid command. Please type /accept or /decline to respond to the order.")
    



bot.polling(timeout=30)