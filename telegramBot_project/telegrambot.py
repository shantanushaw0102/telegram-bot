import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Define the initial state of the cart
cart = {}
products = {"Dabur Honey(200 g)": 382.00,
            "Sunfeast Dark Fantasy Coco Fills(5 piece)": 50.00,
            "Zeta Tea(250 g)": 118.00,
            "Zeta Coffee(150 g)": 205.00,
            "Rice Bran Oil(2 liters)": 450.00,
            "Assure Hair Conditioner(75 g)": 245.00,
            "Assure Arctic Perfume Spray (100 ml)": 275.00,
            "Assure Hand Wash(250 ml)": 145.00,
            "Enerva Breakfast Cereal(350 g)": 299.00,
            "Hyvest Ultra Matic Detergent Powder(500 g)": 185.00,
            "Flax oil ":515.00,
            }

# Define the functions to be executed when each button is pressed


def welcome(update, context):
    # Send a welcome message and show the main menu
    message = "Welcome to ONE STOP GROCERY SHOP !!!!! How may I help you ?"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, reply_markup=main_menu())


def view_products(update, context):
    # Show a list of products and their prices
    products = {    "Dabur Honey(200 g)": 382.00,
                    "Sunfeast Dark Fantasy Coco Fills(5 piece)": 50.00,
                    "Zeta Tea(250 g)": 118.00,
                    "Zeta Coffee(150 g)": 205.00,
                    "Rice Bran Oil(2 liters)": 450.00,
                    "Assure Hair Conditioner(75 g)": 245.00,
                    "Assure Arctic Perfume Spray (100 ml)": 275.00,
                    "Assure Hand Wash(250 ml)": 145.00,
                    "Enerva Breakfast Cereal(350 g)": 299.00,
                    "Hyvest Ultra Matic Detergent Powder(500 g)": 185.00,
                    "Flax oil ":515.00,
            }
    message = "Here are the available products:\n\n"
    for product, price in products.items():
        message += f"{product} - ₹{price:.2f}\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, reply_markup=add_to_cart_menu())


def add_to_cart(update, context):
    # Add the selected product to the cart
    query = update.callback_query
    product = query.data.split(':')[1]
    if product in cart:
        cart[product] += 1
    else:
        cart[product] = 1
    context.bot.answer_callback_query(callback_query_id=query.id)
    context.bot.edit_message_reply_markup(
        chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=add_to_cart_menu())
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"{product} added to your cart.")


def view_cart(update, context):
    # Show the current contents of the cart
    if len(cart) == 0:
        message = "Your cart is empty."
    else:
        message = "Your Cart Items Are:\n\n"
        for product, quantity in cart.items():
            message += f"{product} x {quantity}\n"
        message += f"\nTotal: ₹{get_total():.2f}"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, reply_markup=checkout_menu())


def checkout(update, context):
    # Show the final status of the order and clear the cart
    message = "Your Final Order Status:\n\n"
    for product, quantity in cart.items():
        message += f"{product} x {quantity}\n"
    message += f"\nTotal: ₹{get_total():.2f}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    message = "Thank you for your Order !!! Keep Visiting !!\n\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    cart.clear()

# Define the helper functions to generate the menus


def main_menu():
    keyboard = [[InlineKeyboardButton("View Products", callback_data='view_products')],
                [InlineKeyboardButton("View Cart", callback_data='view_cart')]]
    return InlineKeyboardMarkup(keyboard)


def add_to_cart_menu():
    keyboard = []
    products = ["Dabur Honey(200 g)", "Sunfeast Dark Fantasy Coco Fills(5 piece)", "Zeta Tea(250 g)", "Zeta Coffee(150 g)", "Rice Bran Oil(2 liters)", "Assure Hair Conditioner(75 g)",
                "Assure Arctic Perfume Spray (100 ml)", "Assure Hand Wash(250 ml)", "Enerva Breakfast Cereal(350 g)", "Hyvest Ultra Matic Detergent Powder(500 g)","Flax oil"]
    for product in products:
        keyboard.append([InlineKeyboardButton(
            f"Add {product}", callback_data=f'add_to_cart:{product}')])
    keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
    return InlineKeyboardMarkup(keyboard)


def checkout_menu():
    keyboard = [[InlineKeyboardButton("Confirm Order", callback_data='checkout')],
                [InlineKeyboardButton("Cancel", callback_data='cancel')]]
    return InlineKeyboardMarkup(keyboard)


def get_total():
    products = {"Dabur Honey(200 g)": 382.00,
            "Sunfeast Dark Fantasy Coco Fills(5 piece)": 50.00,
            "Zeta Tea(250 g)": 118.00,
            "Zeta Coffee(150 g)": 205.00,
            "Rice Bran Oil(2 liters)": 450.00,
            "Assure Hair Conditioner(75 g)": 245.00,
            "Assure Arctic Perfume Spray (100 ml)": 275.00,
            "Assure Hand Wash(250 ml)": 145.00,
            "Enerva Breakfast Cereal(350 g)": 299.00,
            "Hyvest Ultra Matic Detergent Powder(500 g)": 185.00,
            }
    total = 0
    for product, quantity in cart.items():
        total += products[product] * quantity
    return total


# Define the Telegram bot and its handlers
updater = Updater(
    token='5707817005:AAHZyNou4F4vIC91TcIHyl_sOPbqIp7HO8w', use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', welcome)
dispatcher.add_handler(start_handler)

dispatcher.add_handler(CallbackQueryHandler(
    view_products, pattern='view_products'))
dispatcher.add_handler(CallbackQueryHandler(
    add_to_cart, pattern='add_to_cart'))
dispatcher.add_handler(CallbackQueryHandler(view_cart, pattern='view_cart'))
dispatcher.add_handler(CallbackQueryHandler(checkout, pattern='checkout'))
dispatcher.add_handler(CallbackQueryHandler(welcome, pattern='back'))

# Start the bot
updater.start_polling()
updater.idle()
