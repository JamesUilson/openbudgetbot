from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils import executor
from aiogram.types import ParseMode
import json
import os
import urllib.parse
import logging
import sys
import asyncio as ancynio

# --- Asosiy sozlamalar ---
bot_token = "8411094844:AAEnCiLApVlWPl59bb8V4YZgsgOVP1NvOkU"
bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot)

Admin_Id = "2110945697"
REQUIRED_CHANNEL = "@BaxaTech2025"  # Kanal username
REFERRAL_FILE = "referrals.json"
bot_link = "https://t.me/OpenBudget025Bot"

referral_counts = {}

# --- JSON fayl bilan ishlash ---
def load_referrals():
    if not os.path.exists(REFERRAL_FILE):
        return {}
    with open(REFERRAL_FILE, "r") as f:
        return json.load(f)

def save_referrals(data):
    with open(REFERRAL_FILE, "w") as f:
        json.dump(data, f)

def get_balance(user_id):
    data = load_referrals()
    return data.get(str(user_id), {}).get("balance", 0)

def add_balance(user_id, amount):
    data = load_referrals()
    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"balance": 0, "referrals": []}
    data[user_id]["balance"] += amount
    save_referrals(data)

def add_referral(referrer_id, new_user_id):
    data = load_referrals()
    referrer_id = str(referrer_id)
    new_user_id = str(new_user_id)

    if referrer_id not in data:
        data[referrer_id] = {"balance": 0, "referrals": []}

    # Bir xil odamni ikki marta qo‘shmaslik
    if new_user_id not in data[referrer_id]["referrals"]:
        data[referrer_id]["referrals"].append(new_user_id)
        data[referrer_id]["balance"] += 2000
        save_referrals(data)


# --- Kanal tekshiruv ---
async def check_channel_subscription(user_id: int):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
        return False
    except:
        return False

# --- Tugmalar dizayni ---
def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('🗳 Ovoz berish'))
    keyboard.row(
        types.KeyboardButton('🔗 Havola'),
        types.KeyboardButton('💳 Balans'),
        types.KeyboardButton('💰 Pul yechish')
    )
    keyboard.row(
        types.KeyboardButton("📝 Qo'llanma"),
        types.KeyboardButton("🤖 Bot haqida")
    )
    keyboard.add(types.KeyboardButton("💸 To‘lovlar"))
    return keyboard

def subscribe_button():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text="📢 Kanalga obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL.strip('@')}"
    ))
    return keyboard


# --- START ---
@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()

    # Kanal tekshiruv
    subscribed = await check_channel_subscription(user_id)
    if not subscribed:
        await message.reply(
            "⚠️ Botdan foydalanish uchun avvalo kanalga obuna bo‘ling:",
            reply_markup=subscribe_button()
        )
        return

    # Agar referal orqali kelsa
    if args.isdigit() and int(args) != user_id:
        add_referral(args, user_id)
        await bot.send_message(
            args,
            f"🎉 Siz yangi do‘stni taklif qildingiz!\n"
            f"💵 Balansingizga *2000 so‘m* qo‘shildi.\n"
            f"💳 Joriy balans: {get_balance(args)} so‘m",
            parse_mode=ParseMode.MARKDOWN
        )

    user_name = message.from_user.first_name.upper()
    await message.reply(
        f"Assalomu alaykum {user_name}. Xush kelibsiz!\n👇 Quyidagi tugmalardan foydalaning:",
        reply_markup=main_keyboard()
    )


# --- Xabarlar handler ---
@dispatcher.message_handler()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name.upper()

    if not await check_channel_subscription(user_id):
        await message.reply(
            "⚠️ Botdan foydalanish uchun avvalo kanalga obuna bo‘ling:",
            reply_markup=subscribe_button()
        )
        return

    url1 = "https://openbudget.uz/boards/initiatives/initiative/52/993f621d-34f0-4ce0-8ae5-8e0421ae6bdc"
    Admin_url = "https://t.me/Open_admin025Bot"
    Channel_url = "https://t.me/Tolovlar2025"

    if message.text == "🤖 Bot haqida":
        bot_info_text = (
            "🤖 Ushbu bot BaxaTech tomonidan yaratilgan.\n\n"
            "💰 Har bir ovoz uchun foydalanuvchilarga 30 000 so'm to‘lanadi.\n\n"
            "📌 Loyihaning tavsifi:\n"
            "Ички йўлларни (пиёдалар йўлакчаси, йўл ўтказгичлар) таъмирлаш билан боғлиқ тадбирлар.\n\n"
            "🆔 ID: 052400055011\n"
            "🏗 Лойиҳа тури: Қурилиш ва таьмирлаш\n\n"
            "🛣 Ishlar tafsiloti:\n"
            "- BOG KO'CHASINI 250 METRIGA ASFALT QOPLAMASINI YOTQIZISH\n"
            "- BODOMZOR KO'CHASINI 600 METRIGA ASFALT QOPLAMASINI YOTQIZISH\n"
            "- XUMOR KO'CHASINI 700 METRIGA ASFALT QOPLAMASINI YOTQIZISH\n"
            "- CHINOR KO'CHASINI 800 METRIGA ASFALT QOPLAMASINI YOTQIZISH\n"
            "- YANGI QO'RG'ONCHA KO'CHASINI 250 METRIGA ASFALT QOPLAMASINI YOTQIZISH\n"
            "- QO'RG'ONCHA KO'CHASINI 200 METRIGA ASFALT QOPLAMASINI YOTQIZISH\n\n"
            "📏 Йўлнинг узунлиги: 2 683 M\n\n"
            "📞 Loyihani qo‘llab-quvvatlash markazi: [BaxaTechBot](https://t.me/BaxaTechBot)"
        )
        await bot.send_message(chat_id, bot_info_text, parse_mode=ParseMode.MARKDOWN)

    elif message.text == "💳 Balans":
        balance = get_balance(user_id)
        await bot.send_message(chat_id, f"💳 Sizning balansingiz: {balance} so‘m")

    elif message.text == "🗳 Ovoz berish":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="👉 Ovoz berish", url=url1))
        keyboard.add(types.InlineKeyboardButton(text="✅ Ovoz berdim", callback_data="ovoz_berdim"))
        await bot.send_message(
            chat_id,
            "📌 Havolaga kirib ovoz bering.\n✅ Keyin 'Ovoz berdim' tugmasini bosing.",
            reply_markup=keyboard
        )

    elif message.text == '🔗 Havola':
        share_text = (
            "👥 Iltimos do'stlaringizga quyidagi linkni ulashing,\n"
            "ular ham pul ishlashda yordam beradi:"
        )

        # Referal link (asl link)
        raw_referral = f"https://t.me/OpenBudget025Bot?start={user_id}"

        # Telegram share uchun to‘g‘rilangan (URL encoded)
        referral_link = f"https://t.me/share/url?url={urllib.parse.quote(raw_referral)}"

        referral_button = types.InlineKeyboardButton(
            text=f"👤 Do'stlarni taklif qilish (ID: {user_id})",
            url=referral_link
        )

        referral_keyboard = types.InlineKeyboardMarkup().add(referral_button)

        await bot.send_photo(
            chat_id,
            photo=open("OpenPhoto.jpg", "rb"),
            caption=share_text,
            reply_markup=referral_keyboard
        )

    elif message.text == "📝 Qo'llanma":
        html = '📹 Quyida botdan qanday foydalanish haqida qisqacha video ko‘rsatma keltirilgan.'
        await bot.send_video(chat_id, video=open("openbudget.mp4", "rb"), caption=html)

    elif message.text == "💰 Pul yechish":
        balance = get_balance(user_id)
        if balance < 30000:
            await bot.send_message(chat_id, f"❌ Pul yechish uchun kamida 30 000 so‘m kerak.\n"
                                            f"📊 Sizning balans: {balance} so‘m")
            return
        withdrawal_message = (
            f"Assalomu alaykum {user_name}!\n"
            "Pulni olish uchun pastdagi tugmani bosing va adminga karta raqamingizni yuboring."
        )
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(types.InlineKeyboardButton(text="Adminga yozish", url=Admin_url))
        await bot.send_message(chat_id, text=withdrawal_message, reply_markup=inline_keyboard)

        # Adminni ogohlantirish
        await bot.send_message(
            Admin_Id,
            f"💸 Foydalanuvchi pul yechmoqchi.\n"
            f"👤 Foydalanuvchi: {user_name} (@{message.from_user.username})\n"
            f"🆔 ID: {user_id}\n"
            f"Balansi: {balance} so‘m")

    elif message.text == "💸 To‘lovlar":
        await bot.send_message(
            chat_id,
            "📢 To‘lovlarni ko‘rish uchun:",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(text="📢 To‘lovlar kanali", url=Channel_url)
            )
        )


# --- Ovoz berishni tasdiqlash ---
@dispatcher.callback_query_handler(lambda c: c.data == "ovoz_berdim")
async def process_vote_done(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user 
    user_id = callback_query.from_user.id

    Admin_url = "https://t.me/Open_admin025Bot"

    # Foydalanuvchiga admin linkini yuborish
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton(text="📸 Screenshot va karta yuborish", url=Admin_url))

    await bot.send_message(
        chat_id,
        "✅ Rahmat! Ovoz berganingiz tasdiqlandi.\nIltimos, screenshot va karta raqamingizni adminga yuboring:",
        reply_markup=inline_keyboard
    )

    # Adminga ogohlantirish
    await bot.send_message(
        Admin_Id,
        f"📢 Yangi foydalanuvchi ovoz berdi!\n"
        f"👤 Foydalanuvchi: {user.first_name} (@{user.username})\n"
        f"🆔 ID: {user.id}\n" 
        "Tekshirishni unutmang."
    )


# --- BOTNI ISHGA TUSHURISH ---
if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)

    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
