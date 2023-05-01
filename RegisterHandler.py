from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters


class RegisterHandler:
    def __init__(self, dispatcher, db_manager):
        self.dispatcher = dispatcher
        self.db_manager = db_manager

        register_handler = ConversationHandler(
            entry_points=[CommandHandler('registro', self.start)],
            states={
                'id': [MessageHandler(Filters.regex("^[0-9]*$"), self.get_id)],
                'name': [MessageHandler(Filters.text, self.get_name)],
                'age': [MessageHandler(Filters.regex("^\d*$"), self.get_age)],
                'email': [
                    MessageHandler(Filters.regex("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"), self.get_email)],
                'cellphone': [MessageHandler(Filters.regex("^\d{10}$"), self.get_cellphone)]
            },
            fallbacks=[MessageHandler(Filters.text, self.echo)]
        )

        self.dispatcher.add_handler(register_handler)

    def start(self, update, context):
        if self.db_manager.validate_user(update.effective_chat.id):
            update.message.reply_text("Ya se encuentra registrado.")

            return ConversationHandler.END

        else:
            context.user_data['registro'] = {}
            context.user_data['registro']['id'] = None
            context.user_data['registro']['name'] = None
            context.user_data['registro']['age'] = None
            context.user_data['registro']['email'] = None
            context.user_data['registro']['cellphone'] = None

            update.message.reply_text("Por favor, ingresa tu documento.")

            return 'id'

    def get_id(self, update, context):
        id = update.message.text

        context.user_data['registro']['id'] = id

        update.message.reply_text("Por favor, ingresa tu nombre.")

        return 'name'

    def get_name(self, update, context):
        name = update.message.text

        context.user_data['registro']['name'] = name

        update.message.reply_text("Por favor, ingresa tu edad.")

        return 'age'

    def get_age(self, update, context):
        age = update.message.text

        context.user_data['registro']['age'] = age

        update.message.reply_text("Por favor, ingresa tu correo electrónico.")

        return 'email'

    def get_email(self, update, context):
        email = update.message.text

        context.user_data['registro']['email'] = email

        update.message.reply_text(
            "Por favor, ingresa tu número de teléfono celular.")

        return 'cellphone'

    def get_cellphone(self, update, context):
        cellphone = update.message.text

        context.user_data['registro']['cellphone'] = cellphone

        try:
            self.register_user(update, context)
            update.message.reply_text("¡Gracias por registrarte!")

        except :
            update.message.reply_text("No se realizo el registro.")

        return ConversationHandler.END

    def echo(self, update, context):
        update.message.reply_text(
            "Lo siento, no entiendo lo que quieres decir. Por favor, inténtalo de nuevo.")

    def register_user(self, update, context):
        self.db_manager.register_user(
            update.effective_chat.id, context.user_data['registro']['id'], context.user_data['registro']['name'],
            context.user_data['registro']['age'], context.user_data['registro']['email'],
            context.user_data['registro']['cellphone'])
