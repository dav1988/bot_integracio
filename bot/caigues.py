#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Codi bàsic de bot que realitza enquestes per gestionar el personal que atent als pacients que han caigut.
 
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from fitxer import id_users, personal

llista=[]
nollista=[]
count=0
personal=personal()
query_text="Ha caigut el iaio 'xxxxxx' al 'lloc caiguda', necessita l'assistencia de 2 infermers/es"
 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
 
 
def start(bot, update):
    global query_text
    #identificador avi
    #localització caiguda
    keyboard = [[InlineKeyboardButton("✅ Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("❌ No puc atendre'l", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(query_text, reply_markup=reply_markup)

 
def button(bot, update):
    global llista
    global nollista
    global count
    query = update.callback_query
    #print query
    nom=str(query)

    ### Obtenció ID user ###
    comes=nom.split("from")
    #print comes[2]
    #print comes[1]    
    nom=comes[1].split("'")
    #print nom
    #print len(nom)
    x=0
    for n in nom:
        if n == 'id':
            nom=nom[x+1]
            nom=nom.split(" ")
            nom=nom[1].split(",")
            iduser=nom[0]
        else:
            x=x+1
    #print iduser
    
    #obtenim la id de l'usuari. Metode obsolet, donava error amb el josep.
    #comes=comes[3].split(" ")
    #iduser=comes[2]
    #print iduser
    iduser=id_users(str(iduser),personal)

    print " opcio "+str(query.data)
    if str(query.data)=="1" and iduser not in llista:        
        llista.append(iduser)
        print "l'infermer/a "+ iduser +" va a socorrer a l'avi, fa falta un/a segon/a infermer/a"
        #editar missatge enquesta (ha de ser com el print)

        keyboard = [[InlineKeyboardButton("✅ Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("❌ No puc atendre'l", callback_data='2')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.editMessageText(text=query_text+ '\n ✅' + iduser , chat_id=query.message.chat_id, message_id=query.message.message_id,reply_markup=reply_markup)

        print llista

        if len(llista)==2:
            #falta afegir identificador caiguda
            bot.editMessageText(text="Els/Les infermers/es " + llista[0] + " i " + llista[1] + " van a socorrer l'avi (fulanito) que ha caigut" , chat_id=query.message.chat_id, message_id=query.message.message_id)
            llista=[]
            nollista=[]
        
    elif str(query.data)=="2":
        if iduser not in nollista:
            nollista.append(iduser)
            keyboard = [[InlineKeyboardButton("✅ Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("❌ No puc atendre'l", callback_data='2')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.editMessageText(text=query_text +'\n ❌' + iduser, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

        else:
            print iduser + " ja sabem que no hi vas"
        if iduser in llista:
            llista.remove(iduser)
            count=count-1
            print "l'infermer/a "+ iduser +" ja NO va a socorrer a l'avi, fan falta dos infermers/es"
            #editar missatge enquesta (com el print)
    else:
        print "l'usuari "+ iduser +" és un cansino"
def stop(bot, update):
    #error AttributeError: 'NoneType' object has no attribute 'message'
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

try:
	# Start the Bot
	print "inicialitzant bot [...]"	
	updater.start_polling()
	print "bot actiu"

	# Stop the Bot 
	updater.idle()
except Exception as error:
	print ("Connectant amb el Bot de Telegram -> ERROR")
	print (error) # <- Error de connexió
	sys.exit(1)	
	
		
########################################################
################### Tasques pendents ###################
########################################################
# Relació de id's i noms de treballadors. ->BD
# Agafar directament els noms pot donar problemes de coincidencies. Millors utilitzar els id's i establir un nom per a cada treballador.-> BD
# Definir funció que mitjançant una senyal pel port serie realitzi l'enquesta
# Editar missatge ajuda. Afegir estat dels pacients.
# Opció stop per parar l'enquesta
# Temporitzador 5 min?
# Repassar ID. Amb el Josep no m'agafa la seva id, em retorna false.
# Falla funció identificació. Cosa rara amb el iduser.
