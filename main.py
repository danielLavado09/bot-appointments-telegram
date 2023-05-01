#from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
import sqlite3
from DBManager import DBManager
from RegisterHandler import RegisterHandler
from AppointmentHandler import AppointmentHandler


def main():
    TOKEN = 'TOKEN'
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Configuración de la base de datos
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()

    db_manager = DBManager(conn)
    db_manager.create_users_table()
    db_manager.create_appointments_table()
    db_manager.create_doctors_table()

    # Conversación de registro
    RegisterHandler(dispatcher, db_manager)

    # Conversación de cita
    AppointmentHandler(dispatcher, db_manager)

    # Iniciar el bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
