from telegram.ext import CommandHandler


class ListAppointmentsHandler:
    def __init__(self, dispatcher, db_manager):
        self.dispatcher = dispatcher
        self.db_manager = db_manager

        self.dispatcher.add_handler(CommandHandler("lista_citas", self.start))

    def start(self, update, context):
        data = self.db_manager.get_appointments(update.effective_chat.id)

        enum_results = "\n".join([f"{i + 1}. {result[0]} - {result[1]}" for i, result in enumerate(data)])

        update.message.reply_text("Tienes las siguientes citas asignadas: \n\n" + enum_results)
