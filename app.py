import logging
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '514089417:AAEIvJE2fRpjdRr28GXsMo2MAcXHs4c8u4M'


def start(bot, update):
    update.message.reply_text('Underc0de Grupo oficial de la comunidad Underc0de.org Unete => https://t.me/underc0deoficial')


def help(bot, update):
    update.message.reply_text('La ayuda es para los debiles.')

def test(bot, update):
    update.message.reply_text('testinit')
    update.message.reply_text(update.message.chat.id)
    update.message.reply_text(update.message.chat.type)
    update.message.reply_text('testend')


def echo(bot, update):
    update.message.reply_text('%s: %s' % (update.message.from_user.username ,update.message.text))


def error(bot, update, error):
    logger.warning('No puedo afirmar ni denegar que ha sucedido un error.')

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("test", test))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
