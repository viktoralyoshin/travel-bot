from telegram import Update
from telegram.ext import ContextTypes

async def attraction_detail_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    attraction_id = int(query.data.split('_')[1])