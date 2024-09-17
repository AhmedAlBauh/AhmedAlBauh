from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import json

TOKEN = '7395460695:AAEkabLwswP6KvriBgR6bdov2G7GWO7TR-k'
ADMIN_ID = 2116111813

def load_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('مرحبا! استخدم /admin للوصول إلى لوحة الإدارة.')

def admin_panel(update: Update, context: CallbackContext):
    if update.effective_user.id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("إدارة قنوات", callback_data='manage_channels')],
            [InlineKeyboardButton("إدارة رصيد زين", callback_data='manage_zen')],
            [InlineKeyboardButton("إدارة رصيد أساسي", callback_data='manage_asacell')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('لوحة الإدارة:', reply_markup=reply_markup)
    else:
        update.message.reply_text('ليس لديك صلاحيات للوصول إلى لوحة الإدارة.')

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == 'manage_channels':
        manage_channels(update, context)
    elif query.data == 'manage_zen':
        manage_zen(update, context)
    elif query.data == 'manage_asacell':
        manage_asacell(update, context)
    elif query.data.startswith('add_channel'):
        add_channel(update, context)
    elif query.data.startswith('remove_channel'):
        remove_channel(update, context)
    elif query.data.startswith('add_zen_card'):
        add_zen_card(update, context)
    elif query.data.startswith('remove_zen_card'):
        remove_zen_card(update, context)
    elif query.data.startswith('add_asacell_card'):
        add_asacell_card(update, context)
    elif query.data.startswith('remove_asacell_card'):
        remove_asacell_card(update, context)

def manage_channels(update: Update, context: CallbackContext):
    channels = load_json('channels.json')
    keyboard = [[InlineKeyboardButton(channel, callback_data=f'remove_channel_{channel}')] for channel in channels]
    keyboard.append([InlineKeyboardButton("إضافة قناة", callback_data='add_channel')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text('إدارة القنوات:', reply_markup=reply_markup)

def manage_zen(update: Update, context: CallbackContext):
    zen_cards = load_json('zen_balance.json')
    keyboard = [[InlineKeyboardButton(card, callback_data=f'remove_zen_card_{card}')] for card in zen_cards]
    keyboard.append([InlineKeyboardButton("إضافة بطاقة زين", callback_data='add_zen_card')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text('إدارة رصيد زين:', reply_markup=reply_markup)

def manage_asacell(update: Update, context: CallbackContext):
    asacell_cards = load_json('asacell_balance.json')
    keyboard = [[InlineKeyboardButton(card, callback_data=f'remove_asacell_card_{card}')] for card in asacell_cards]
    keyboard.append([InlineKeyboardButton("إضافة بطاقة أساسي", callback_data='add_asacell_card')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.edit_message_text('إدارة رصيد أساسي:', reply_markup=reply_markup)

def add_channel(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="أرسل اسم القناة لإضافته:")
    context.user_data['awaiting_channel'] = True

def remove_channel(update: Update, context: CallbackContext):
    channel_name = update.callback_query.data.replace('remove_channel_', '')
    channels = load_json('channels.json')
    if channel_name in channels:
        del channels[channel_name]
        save_json(channels, 'channels.json')
        update.callback_query.edit_message_text(f"تمت إزالة القناة: {channel_name}")
    else:
        update.callback_query.edit_message_text("القناة غير موجودة.")

def add_zen_card(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="أرسل اسم بطاقة زين لإضافتها:")
    context.user_data['awaiting_zen_card'] = True

def remove_zen_card(update: Update, context: CallbackContext):
    card_name = update.callback_query.data.replace('remove_zen_card_', '')
    zen_cards = load_json('zen_balance.json')
    if card_name in zen_cards:
        del zen_cards[card_name]
        save_json(zen_cards, 'zen_balance.json')
        update.callback_query.edit_message_text(f"تمت إزالة بطاقة زين: {card_name}")
    else:
        update.callback_query.edit_message_text("البطاقة غير موجودة.")

def add_asacell_card(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="أرسل اسم بطاقة أساسي لإضافتها:")
    context.user_data['awaiting_asacell_card'] = True

def remove_asacell_card(update: Update, context: CallbackContext):
    card_name = update.callback_query.data.replace('remove_asacell_card_', '')
    asacell_cards = load_json('asacell_balance.json')
    if card_name in asacell_cards:
        del asacell_cards[card_name]
        save_json(asacell_cards, 'asacell_balance.json')
        update.callback_query.edit_message_text(f"تمت إزالة بطاقة أساسي: {card_name}")
    else:
        update.callback_query.edit_message_text("البطاقة غير موجودة.")

def handle_message(update: Update, context: CallbackContext):
    if 'awaiting_channel' in context.user_data:
        channel_name = update.message.text
        channels = load_json('channels.json')
        channels[channel_name] = {}  # يمكنك إضافة تفاصيل القناة هنا
        save_json(channels, 'channels.json')
        update.message.reply_text(f"تمت إضافة القناة: {channel_name}")
        del context.user_data['awaiting_channel']

    elif 'awaiting_zen_card' in context.user_data:
        card_name = update.message.text
        zen_cards = load_json('zen_balance.json')
        zen_cards[card_name] = {}  # يمكنك إضافة تفاصيل البطاقة هنا
        save_json(zen_cards, 'zen_balance.json')
        update.message.reply_text(f"تمت إضافة بطاقة زين: {card_name}")
        del context.user_data['awaiting_zen_card']

    elif 'awaiting_asacell_card' in context.user_data:
        card_name = update.message.text
        asacell_cards = load_json('asacell_balance.json')
        asacell_cards[card_name] = {}  # يمكنك إضافة تفاصيل البطاقة هنا
        save_json(asacell_cards, 'asacell_balance.json')
        update.message.reply_text(f"تمت إضافة بطاقة أساسي: {card_name}")
        del context.user_data['awaiting_asacell_card']

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('admin', admin_panel))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()