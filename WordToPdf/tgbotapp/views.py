from django.shortcuts import render
# Create your views here.
from telegram.ext import CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import aspose.words as aw
from .models import Log


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    log = Log.objects.filter(user_id=user.id).first()
    if not log:
        log = Log()
        log.user_id = user.id
        log.log = {"state": 0}
        log.save()
    state = log.log
    state['state'] = 1
    update.message.reply_text(f"""🇺🇿Tilni tanlang\n\n🇷🇺Выбирай язык\n\n🇫🇰Choose the language""", reply_markup=keyboard_buttons(type='lang'))
    log.log = state
    log.save()


def received_message(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.message.text
    log = Log.objects.filter(user_id=user.id).first()
    info = log.log
    if info['state'] == 1:
        if msg == '🇺🇿 Uzb':
            update.message.reply_text(dictionary(user, 'uzb', 'start'))
            info['lang'] = msg
            info['state'] = 2
        elif msg == '🇷🇺 Rus':
            update.message.reply_text(dictionary(user, 'rus', 'start'))
            info['lang'] = msg
            info['state'] = 2
        elif msg == '🇫🇰 En':
            update.message.reply_text(dictionary(user, 'en', 'start'))
            info['lang'] = msg
            info['state'] = 2
    log.log = info
    log.save()


def received_document(update: Update, context: CallbackContext):
    file = update.message.document.file_name
    with open(f"files/{file}", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    user = update.effective_user
    log = Log.objects.filter(user_id=user.id).first()
    state = log.log
    if state['state'] == 2:
        if file.endswith('.docx'):
            doc = aw.Document(f'files/{file}')
            if (doc.watermark.type == aw.WatermarkType.TEXT):
                doc.watermark.remove()
            doc.save(f'files/{file}.pdf')
            context.bot.sendDocument(document=open(f'files/{file}.pdf', 'rb'), chat_id=user.id)

    log.log = state
    log.save()


def keyboard_buttons(type=None):
    btn = []
    if type == 'lang':
        btn = [
            [KeyboardButton('🇺🇿 Uzb'), KeyboardButton('🇷🇺 Rus')],
            [KeyboardButton('🇫🇰 En')],
        ]
    return ReplyKeyboardMarkup(btn, resize_keyboard=True, one_time_keyboard=True)


def dictionary(user, language, method):
    dict = {
        'uzb': {
            'start': f"Assalomu alaykum {user.first_name}. doc, docx yoki rasm jo'nating pdf ga aylantirish uchun",
        },
        'en': {
            'start': f"""🇦🇺 - Hi {user.first_name}. send me docx or doc to convert it into pdf""",
        },
        'rus': {
            'start': ''
        }
    }
    return dict[language][method]


