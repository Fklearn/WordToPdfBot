from django.core.management import BaseCommand
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from TgBotApp.views import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        updater = Updater('5028779716:AAEWI_822MoMa8GKg2wADRNKkTBvI0eujA4')
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.document, received_document))

        updater.start_polling()
        updater.idle()
