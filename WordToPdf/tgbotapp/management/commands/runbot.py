from django.core.management import BaseCommand
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
from tgbotapp.views import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater('5028779716:AAEWI_822MoMa8GKg2wADRNKkTBvI0eujA4')
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.document, received_document))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, received_message))

        updater.start_polling()
        updater.idle()
