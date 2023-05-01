from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from util import *


class AppointmentHandler:
    def __init__(self, dispatcher, db_manager):
        self.dispatcher = dispatcher
        self.db_manager = db_manager
        self.temp_dates = []
        self.temp_specialties = []
        self.temp_doctors = []

        appointment_handler = ConversationHandler(
            entry_points=[CommandHandler('nueva_cita', self.start)],
            states={
                'specialty': [MessageHandler(Filters.regex("^[1-9]*$"), self.get_specialty)],
                'doctor': [MessageHandler(Filters.regex("^[1-9]*$"), self.get_doctor)],
                'date_due': [MessageHandler(Filters.regex("^[1-9]*$"), self.get_date_due)],
            },
            fallbacks=[MessageHandler(Filters.text, self.echo)]
        )

        self.dispatcher.add_handler(appointment_handler)

    def start(self, update, context):
        self.temp_dates.clear()
        self.temp_specialties.clear()
        self.temp_doctors.clear()

        if self.db_manager.validate_user(update.effective_chat.id):
            context.user_data['nueva_cita'] = {}
            context.user_data['nueva_cita']['specialty'] = None
            context.user_data['nueva_cita']['doctor'] = None
            context.user_data['nueva_cita']['date_due'] = None

            # Obteniendo las epecialidades
            self.temp_specialties = self.db_manager.get_specialties()

            enumerated_list = [f"{i + 1}. {element}" for i, element in enumerate(self.temp_specialties)]

            # Unimos los elementos de la lista con un salto de línea
            result_string = '\n'.join(enumerated_list)

            update.message.reply_text("Elige la especialidad médica. \n\n" + result_string)

            return 'specialty'
        else:
            update.message.reply_text("Primero debes registrarte. /registro")

            return ConversationHandler.END

    def get_specialty(self, update, context):
        specialty = update.message.text

        context.user_data['nueva_cita']['specialty'] = self.temp_specialties[int(specialty) - 1]

        # Obteniendo los doctores segun la especialidad
        self.temp_doctors = self.db_manager.get_doctors_by_specialties(self.temp_specialties[int(specialty) - 1])

        # Imprimiendo nombres
        names = [name[0] for name in self.temp_doctors]

        enumerated_list = [f"{i + 1}. Dr/Dra {element}" for i, element in enumerate(names)]

        # Unimos los elementos de la lista con un salto de línea
        result_string = '\n'.join(enumerated_list)

        update.message.reply_text("Elige alguno de los siguientes doctores: \n\n" +
                                  result_string)

        return 'doctor'

    def get_doctor(self, update, context):
        doctor = update.message.text

        context.user_data['nueva_cita']['doctor'] = self.temp_doctors[int(doctor) - 1]

        # Obteniendo las fechas para mostrar
        self.temp_dates = get_random_date()

        enumerated_list = [f"{i + 1}. {element}" for i, element in enumerate(self.temp_dates)]

        # Unimos los elementos de la lista con un salto de línea
        result_string = '\n'.join(enumerated_list)

        update.message.reply_text("Elige alguna de las siguientes fechas: \n\n" +
                                  result_string)

        return 'date_due'

    def get_date_due(self, update, context):
        date_due = update.message.text

        context.user_data['nueva_cita']['date_due'] = str(self.temp_dates[int(date_due) - 1])

        temp_doctor_id = context.user_data['nueva_cita']['doctor'][1]
        temp_doctor_name = context.user_data['nueva_cita']['doctor'][0]

        temp_date = str(self.temp_dates[int(date_due) - 1])

        # Se verifica si el usuario tiene cita para ese día
        if not self.db_manager.validate_user_date(update.effective_chat.id, temp_date):
            if not self.db_manager.validate_doctor_agenda(temp_doctor_id, temp_date):
                try:
                    # Registro de la cita
                    self.register_appointment(update, context)

                    msg = "Cita asignada con éxito. \nDoctor/a: {}\nFecha: {}".format(temp_doctor_name, temp_date)
                    update.message.reply_text(msg)
                except:
                    update.message.reply_text("No se pudo asignar la cita.")
            else:
                update.message.reply_text("El/la doctor/a elegido tiene la agenda ocupada para esa fecha.\n/nueva_cita")
        else:
            update.message.reply_text("Ya tienes una cita asignada para esa fecha.\n/nueva_cita")

        return ConversationHandler.END

    def echo(self, update, context):
        update.message.reply_text(
            "Lo siento, no entiendo lo que quieres decir. Por favor, inténtalo de nuevo.")

    def register_appointment(self, update, context):
        user_id = update.effective_chat.id
        doctor_id = context.user_data['nueva_cita']['doctor'][1]
        specialty = context.user_data['nueva_cita']['specialty']
        date_due = context.user_data['nueva_cita']['date_due']
        appointment_id = str(user_id) + str(date_due.replace('-', '_'))

        print(str(user_id) + " " + str(doctor_id) + " " + str(specialty) + " "
              + str(date_due) + " " + str(appointment_id))

        self.db_manager.register_appointment(appointment_id, user_id, doctor_id, specialty, date_due)
