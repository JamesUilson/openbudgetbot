from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import json
import asyncio
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import urllib.parse

# --- Asosiy sozlamalar ---
bot_token = "8411094844:AAEnCiLApVlWPl59bb8V4YZgsgOVP1NvOkU"
bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()

Admin_Id = 2110945697
REQUIRED_CHANNEL = "@BaxaTech2025"
REFERRAL_FILE = "referrals.json"
bot_link = "https://t.me/OpenBudget025Bot"
REFERRAL_BONUS = 7000
MIN_WITHDRAW = 30000

# --- JSON bilan ishlash ---
def load_referrals():
    if not os.path.exists(REFERRAL_FILE):
        return {}
    with open(REFERRAL_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_referrals(data):
    with open(REFERRAL_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
    referrer_id, new_user_id = str(referrer_id), str(new_user_id)
    if referrer_id not in data:
        data[referrer_id] = {"balance": 0, "referrals": []}
    if new_user_id not in data[referrer_id]["referrals"]:
        data[referrer_id]["referrals"].append(new_user_id)
        data[referrer_id]["balance"] += REFERRAL_BONUS
    save_referrals(data)

# --- Kanal obuna tekshiruv ---
async def check_channel_subscription(user_id: int):
    try:
        member = await bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["creator", "administrator", "member"]
    except:
        return False

# --- Klaviaturalar ---
def main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗳 Ovoz berish")],
            [KeyboardButton(text="🔗 Havola"), KeyboardButton(text="💳 Balans"), KeyboardButton(text="💰 Pul yechish")],
            [KeyboardButton(text="📝 Qo'llanma"), KeyboardButton(text="🤖 Bot haqida")],
            [KeyboardButton(text="💸 To‘lovlar")]
        ],
        resize_keyboard=True
    )
    return keyboard

def subscribe_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Kanalga obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL.strip('@')}")
    return builder.as_markup()

# --- START ---
@dp.message(Command("start"))
async def start(message: Message, command: Command):
    user_id = message.from_user.id
    args = command.args

    if not await check_channel_subscription(user_id):
        await message.reply("⚠️ Botdan foydalanish uchun avvalo kanalga obuna bo‘ling:", reply_markup=subscribe_button())
        return

    if args and args.isdigit():
        ref_id = int(args)
        if ref_id != user_id:
            add_referral(ref_id, user_id)

    user_name = message.from_user.first_name
    await message.reply(
        f"Assalomu alaykum {user_name}. Xush kelibsiz!\n👇 Quyidagi tugmalardan foydalaning:",
        reply_markup=main_keyboard()
    )

# --- Tugma handlerlari ---
@dp.message(lambda m: m.text == "🤖 Bot haqida")
async def about_bot(message: Message):
    await message.answer("🤖 Ushbu bot BaxaTech tomonidan yaratilgan.\n\n"
            "💰 Har bir ovoz uchun foydalanuvchilarga 30 000 so'm to‘lanadi. Har bir referall uchun esa 7000 so`m !\n\n"
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

@dp.message(lambda m: m.text == "💳 Balans")
async def balance(message: Message):
    bal = get_balance(message.from_user.id)
    await message.answer(f"💳 Sizning balansingiz: {bal} so‘m")

@dp.message(lambda m: m.text == "🗳 Ovoz berish")
async def vote(message: Message):
    url1 = "https://openbudget.uz/boards/initiatives/initiative/52/993f621d-34f0-4ce0-8ae5-8e0421ae6bdc"
    builder = InlineKeyboardBuilder()
    builder.button(text="👉 Ovoz berish", url=url1)
    builder.button(text="✅ Ovoz berdim", callback_data="ovoz_berdim")
    await message.answer("📌 Havolaga kirib ovoz bering. Screenshot olishni unnutmang(Ovoz tasdiqlangan bo`lishi kerak yoki tasdiqlanishini kutib tasdiqlanganlik togrisidagi sms habaringizni screenshoti ham kifoya qiladi)\n✅ Keyin 'Ovoz berdim' tugmasini bosing.", reply_markup=builder.as_markup())

@dp.message(lambda m: m.text == "🔗 Havola")
async def send_referral(message: Message):
    user_id = message.from_user.id
    share_text = "👥 Do‘stlaringizni taklif qilib 7 000 so‘m bonus oling!"
    referral_link = f"https://t.me/OpenBudget025Bot?start={user_id}"
    
    # 🔗 ulashish havolasi
    share_url = f"https://t.me/share/url?url={urllib.parse.quote(referral_link)}&text={urllib.parse.quote(share_text)}"

    referral_button = InlineKeyboardButton(
        text=f"👤 Do'stlarni taklif qilish (ID: {user_id})",
        url=share_url
    )
    referral_keyboard = InlineKeyboardMarkup(inline_keyboard=[[referral_button]])
    
    photo_path = os.path.join(os.path.dirname(__file__), "OpenPhoto.jpg")
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo, caption=share_text, reply_markup=referral_keyboard)
    else:
        await message.answer("❌ Rasm topilmadi!")

@dp.message(lambda m: m.text == "📝 Qo'llanma")
async def guide(message: Message):
    video_path = "openbudget.mp4"
    if os.path.exists(video_path):
        video = FSInputFile(video_path)
        await message.answer_video(video, caption="📹 Botdan foydalanish bo‘yicha video ko‘rsatma.")
    else:
        await message.answer("❌ Video topilmadi!")

@dp.message(lambda m: m.text == "💸 To‘lovlar")
async def payments(message: Message):
    channel_url = "https://t.me/Tolovlar2025"
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 To‘lovlar kanali", url=channel_url)
    await message.answer("📢 To‘lovlarni ko‘rish uchun:", reply_markup=builder.as_markup())

@dp.message(lambda m: m.text == "💰 Pul yechish")
async def withdraw(message: Message):
    user_id = message.from_user.id
    bal = get_balance(user_id)
    username = f"@{message.from_user.username}" if message.from_user.username else "username yo‘q"
    
    if bal < MIN_WITHDRAW:
        await message.answer(f"❌ Balansingiz yetarli emas. Pul yechish uchun kamida {MIN_WITHDRAW} so‘m bo‘lishi kerak.")
    else:
        await message.answer("✅ So‘rovingiz yuborildi. Tez orada admin siz bilan bog‘lanadi.")
        await bot.send_message(
            Admin_Id,
            f"💸 Pul yechish so‘rovi!\n👤 Foydalanuvchi: {username}\n🆔 ID: {user_id}\n💳 Balans: {bal} so‘m"
        )

# --- Callback handler ---
@dp.callback_query(lambda c: c.data == "ovoz_berdim")
async def process_vote_done(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    username = f"@{user.username}" if user.username else "username yo‘q"
    builder = InlineKeyboardBuilder()
    builder.button(text="📸 Screenshot va karta yuborish", url="https://t.me/Open_admin025Bot")
    await callback_query.message.answer("✅ Rahmat! Ovoz berganingiz tasdiqlash uchun screenshot va karta raqamingizni adminga yuboring:", reply_markup=builder.as_markup())
    await bot.send_message(Admin_Id, f"📢 {username} ovoz berdi. ID: {user.id}")

# --- Bot ishga tushurish ---
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
