from django.shortcuts import render
# Create your views here.
from telegram.ext import CallbackContext
from telegram import Update
import aspose.words as aw


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"""🇦🇺 - Hi {user.first_name}, send me docx or doc to convert it into pdf""")


def received_document(update: Update, context: CallbackContext):
    user = update.effective_user
    file = update.message.document
    if file.file_name.endswith('.doc' or '.docx'):
        update.message.reply_text('Input the file name')

    doc = aw.Document(file)
    doc.save('Pdf.pdf')
