from telegram.ext import CommandHandler


class StartHandler:
    def __init__(self, dispatcher, db_manager):
        self.dispatcher = dispatcher
        self.db_manager = db_manager

        self.dispatcher.add_handler(CommandHandler("start", self.start))

    def start(self, update, context):
        if self.db_manager.validate_user(update.effective_chat.id):
            update.message.reply_text(
                "Hola " + self.db_manager.get_user_name(update.effective_chat.id) + ", bienvenid@." +
                "\n\nPara asginar una nueva cita: /nueva_cita \nVer citas: /lista_citas")
        else:
            update.message.reply_text("Hola, para empezar debes registrarte: /registro")
