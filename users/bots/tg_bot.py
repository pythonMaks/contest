from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from users.models import User
from telegram import Bot

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Введите ваш секретный код', reply_markup=ForceReply())

def send_telegram_message(chat_id, text):
    bot = Bot(token="6503653218:AAEq4laa7R5Zf7pQUYJhrEWcmf7HrVriGnE")
    bot.send_message(chat_id, text)
    
def handle_code(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id
    # Get user from database using user_message as access code
    # I use Django's ORM for database interactions, but you can use your preferred method.
    try:
        user = User.objects.get(access_code=user_message)
        user.chat_id = chat_id
        user.save()
        update.message.reply_text(f'Добро пожаловать, {user.username}! Вы успешно подписались на оповещения!')
    except User.DoesNotExist:
        update.message.reply_text('Введен не корректный код! Проверьте код в вашем профиле http://13.50.99.201:8000/profile/')

def change(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Введите новый секретный код', reply_markup=ForceReply())
    
def main() -> None:
    updater = Updater("6503653218:AAEq4laa7R5Zf7pQUYJhrEWcmf7HrVriGnE", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("change", change))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, handle_code))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
