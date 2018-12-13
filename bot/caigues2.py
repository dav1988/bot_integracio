#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Codi bàsic de bot que realitza enquestes per gestionar el personal que atent als pacients que han caigut.
 
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

llista=[]
count=0
 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
 
 
def start(bot, update):
    global llista
    global count
    #identificador avi
    #localització caiguda
    count = 0
    llista=[]
    keyboard = [[InlineKeyboardButton("Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("No puc atendre'l", callback_data='2')],   [InlineKeyboardButton("algo més", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Ha caigut el iaio 'xxxxxx' al 'lloc caiguda', qui pot atendre'l?", reply_markup=reply_markup)

 
def button(bot, update):
    global llista
    global count
    query = update.callback_query
    #print query
    nom=str(query)
    comes=nom.split(",")
    nom=nom.split("'")
    #obtenim la id de l'usuari
    comes=comes[3].split(" ")
    iduser=comes[2]
    print iduser
    print " opcio "+str(query.data)
    if str(query.data)=="1" iduser not in llista:        
        llista.append(iduser)
        count=count+1
        print "portem "+str(count) +" assistents diferents"
        if count==2:
            #falta afegir identificador caiguda
            bot.editMessageText(text="Els usuaris " + llista[0] + " i " + llista[1] + " van a socorrer el iaio caigut" , chat_id=query.message.chat_id, message_id=query.message.message_id)
    if str(query.data)=="2":
        if iduser in llista:
            llista.remove(iduser)
        bot.editMessageText(text="Ha caigut el iaio 'xxxxxx' al 'lloc caiguda', qui pot atendre'l? /n \u274c", chat_id=query.message.chat_id, message_id=query.message.message_id)
        keyboard = [[InlineKeyboardButton("Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("No puc atendre'l", callback_data='2')],   [InlineKeyboardButton("algo més", callback_data='3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
    
def stop(bot, update):
    query = update.callback_query
    bot.editMessageText(text="Enquesta cancelada" , chat_id=query.message.chat_id, message_id=query.message.message_id)

def help(bot, update):
    update.message.reply_text("Use /query to test this bot.")
 
 
def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))
 
 
# Create the Updater and pass it your bot's token.
updater = Updater("697741163:AAEIsJnN3fQehIhrXI_TjgzgwM0jMJlD7FE")
 
updater.dispatcher.add_handler(CommandHandler('query', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
#updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_error_handler(error)
 
# Start the Bot
updater.start_polling()
 
# Stop the Bot 
updater.idle()

########################################################
################### Tasques pendents ###################
########################################################
# Relació de id's i noms de treballadors. ->BD
# Agafar directament els noms pot donar problemes de coincidencies. Millors utilitzar els id's i establir un nom per a cada treballador.-> BD
# Definir funció que mitjançant una senyal pel port serie realitzi l'enquesta
# Editar missatge ajuda. Afegir estat dels pacients.
# Opció stop per parar l'enquesta
# Temporitzador 5 min?

