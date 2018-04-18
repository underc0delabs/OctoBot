import os
import html
import _thread
import logging
import http.server
import socketserver
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '514089417:AAEIvJE2fRpjdRr28GXsMo2MAcXHs4c8u4M'

chatlog = []


web_dir = os.path.join(os.path.dirname(__file__), 'data')
os.chdir(web_dir)


def initServer(serverName):
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("serving at port", PORT)
    httpd.serve_forever()

def start(bot, update):
    update.message.reply_text('Unete al Grupo oficial de la comunidad Underc0de.org => https://t.me/underc0deoficial')

def help(bot, update):
    update.message.reply_text('La ayuda es para los debiles.')

def echo(bot, update):
    if update.message.chat.type=='group':
        print(update.message.chat.title)
        if 'Underc0de' in update.message.chat.title:
            profilepic = 'none'
            if len(update.message.from_user.get_profile_photos().photos) > 0:
                profilepic = update.message.from_user.get_profile_photos().photos[0][0].file_id
            mensaje = update.message.text
            if len(update.message.photo) > 0:
                mensaje = 'IMG_TG123' + update.message.photo[0].file_id
            if mensaje != 'None':
              chatlog.append('%s#|~#&@#%s#|~#&@#%s' % (profilepic, update.message.from_user.username ,mensaje))
              while len(chatlog) > 300:
                  del chatlog[0]
              with open('log.txt', 'w+') as f:
                  for msg in chatlog:
                      f.write('%s;<^¡] ¬¬\n' % (msg));
                

                
def error(bot, update, error):
    logger.warning('No puedo afirmar ni denegar que ha sucedido un error.')

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling..."""
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
        
        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.all, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    print ('Inicializando hilo del WebServer')
    print ('Inicializando hilo del Bot')
    _thread.start_new_thread( initServer, ("HTTP/SERVER", ) )
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
