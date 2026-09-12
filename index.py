import logging
import json
import subprocess
import sys

# Auto-install correct package (first remove wrong one)
def install_correct_package():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "telegram", "-y", "--quiet"], stderr=subprocess.DEVNULL)
    except:
        pass
    
    # Need v22.7+ for icon_custom_emoji_id + style support
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot>=22.7", "--upgrade", "--quiet"])

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application, ChatJoinRequestHandler, CommandHandler,
        ContextTypes, CallbackQueryHandler, MessageHandler, filters
    )
except ImportError:
    print("Installing python-telegram-bot...")
    install_correct_package()
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application, ChatJoinRequestHandler, CommandHandler,
        ContextTypes, CallbackQueryHandler, MessageHandler, filters
    )

# ------------------ CONFIG ------------------

BOT_TOKEN        = "8910821109:AAHDM02E2SYogk-I7Sumj9I9V9_6tHHmQ7w"
ADMIN_ID         = 8599018764
SOURCE_CHANNEL   = "@kpbot98"
APK_MESSAGE_ID   = 11  # APK message ID
VIDEO_MESSAGE_ID = 7  # Video message ID
VOICE_MESSAGE_ID = 12  # Voice message ID
USERS_FILE       = "londa.json"

VIP_CHANNEL_LINK = "https://t.me/King_Bhaiya1?text=KING%20SIR%2C%20PLEASE%20ADD%20ME%20TO%20THE%20%24100%20%E2%9E%9C%20%241000%20VIP%20CHALLENGE%20GROUP%20%F0%9F%9A%80"
REGISTRATION_LINK = "https://u3.shortink.io/register?utm_campaign=860305&utm_source=affiliate&utm_medium=sr&a=DZaqxgiIGmAknf&al=1794680&ac=aipannel&cid=979048"
HACK_BOT_LINK = "http://t.me/king_ai_signal_bot"

# ------------------ PREMIUM EMOJI IDs ------------------
EMOJI_VIDEO = "6147617184479711380"      # First - Video emoji
EMOJI_APK   = "5767209624675553166"      # Second - APK emoji
EMOJI_VOICE = "6124902618574625426"      # Third - Voice emoji

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ------------------ COLORED BUTTONS ------------------
VIDEO_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="VIP CHANNEL",
            url=VIP_CHANNEL_LINK,
            icon_custom_emoji_id=EMOJI_VIDEO,
            style="primary"
        ),
        InlineKeyboardButton(
            text="LOSS RECOVER",
            url=LOSS_RECOVER_LINK,
            icon_custom_emoji_id=EMOJI_APK,
            style="danger"
        )
    ],
    [
        InlineKeyboardButton(
            text="REGISTRATION LINK",
            url=REGISTRATION_LINK,
            icon_custom_emoji_id=EMOJI_VOICE,
            style="success"
        )
    ]
])

APK_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="DM FOR LOSS RECOVERY",
            url=LOSS_RECOVER_LINK,
            icon_custom_emoji_id=EMOJI_APK,
            style="danger"
        )
    ]
])

VOICE_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="Join VIP Now Limited Spots",
            url=VIP_CHANNEL_LINK,
            icon_custom_emoji_id=EMOJI_VIDEO,
            style="warning"
        )
    ]
])

# ------------------ START TEXT ------------------
START_MESSAGE = (
    "𝗛𝗘𝗟𝗟𝗢\n\n"
    "𝗔𝗔𝗣𝗞𝗜 𝗥𝗘𝗤𝗨𝗘𝗦𝗧 𝗝𝗔𝗟𝗗𝗜 𝗛𝗜 𝗔𝗣𝗣𝗥𝗢𝗩𝗘 𝗛𝗢 𝗝𝗔𝗬𝗘𝗚𝗜 \n\n"
    "𝗦𝗘𝗧𝗨𝗣 𝗩𝗜𝗗𝗘𝗢 & 𝗛𝗔𝗖𝗞 𝗔𝗣𝗞 𝗡𝗘𝗘𝗖𝗛𝗘 𝗗𝗜𝗬𝗔 𝗚𝗔𝗬𝗔 𝗛𝗔𝗜"
)

# ------------------ USERS SAVE / LOAD ------------------

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

users = load_users()

# ------------------ HELPER FUNCTION ------------------

async def send_all_content_to_user(bot, user_id: int):
    # Sirf video, APK aur voice bhejna hai
    await bot.copy_message(
        chat_id=user_id,
        from_chat_id=SOURCE_CHANNEL,
        message_id=VIDEO_MESSAGE_ID,
        reply_markup=VIDEO_KEYBOARD
    )
    
    await bot.copy_message(
        chat_id=user_id,
        from_chat_id=SOURCE_CHANNEL,
        message_id=APK_MESSAGE_ID,
        reply_markup=APK_KEYBOARD
    )
    
    # Voice message
    try:
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=SOURCE_CHANNEL,
            message_id=VOICE_MESSAGE_ID
        )
        await bot.send_message(
            chat_id=user_id,
            text="🎤 *Click below to join VIP Channel:*",
            reply_markup=VOICE_KEYBOARD,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error sending voice to {user_id}: {e}")

# ------------------ /start ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)
    save_users(users)
    
    await update.message.reply_text(text=START_MESSAGE)
    
    try:
        await send_all_content_to_user(context.bot, user.id)
    except Exception as e:
        logger.error(f"Error sending files on /start to {user.id}: {e}")

# ------------------ ADMIN MENU ------------------

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Aap admin nahi ho")
        return
    keyboard = [
        [InlineKeyboardButton("📢 Send Text Message", callback_data="admin_text")],
        [InlineKeyboardButton("📦 Send APK File", callback_data="admin_apk")],
        [InlineKeyboardButton("🎬 Send Video", callback_data="admin_video")],
        [InlineKeyboardButton("🎤 Send Voice", callback_data="admin_voice")],
        [InlineKeyboardButton("📤 Send All Files", callback_data="admin_all")],
        [InlineKeyboardButton("📊 Users Count", callback_data="admin_stats")],
    ]
    await update.message.reply_text(
        "👑 *ADMIN MENU* 👑\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ------------------ ADMIN CALLBACKS ------------------

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "admin_stats":
        await query.edit_message_text(f"📊 *Total Registered Users:* {len(users)}", parse_mode="Markdown")

    elif data == "admin_apk":
        context.user_data['action'] = 'send_apk'
        await query.edit_message_text(
            f"📦 *Send APK to All Users*\n\nTotal users: {len(users)}\n\n"
            "Shuru karne ke liye *CONFIRM* type karein:", 
            parse_mode="Markdown"
        )

    elif data == "admin_video":
        context.user_data['action'] = 'send_video'
        await query.edit_message_text(
            f"🎬 *Send Video to All Users*\n\nTotal users: {len(users)}\n\n"
            "Shuru karne ke liye *CONFIRM* type karein:", 
            parse_mode="Markdown"
        )

    elif data == "admin_voice":
        context.user_data['action'] = 'send_voice'
        await query.edit_message_text(
            f"🎤 *Send Voice to All Users*\n\nTotal users: {len(users)}\n\n"
            "Shuru karne ke liye *CONFIRM* type karein:", 
            parse_mode="Markdown"
        )

    elif data == "admin_text":
        context.user_data['action'] = 'send_text'
        await query.edit_message_text(
            f"📢 *Broadcast Text*\n\nTotal users: {len(users)}\n\nApna message type karein:", 
            parse_mode="Markdown"
        )

    elif data == "admin_all":
        context.user_data['action'] = 'send_all'
        await query.edit_message_text(
            f"📤 *Send All Files*\n\nTotal users: {len(users)}\n\n"
            "Shuru karne ke liye *CONFIRM* type karein:", 
            parse_mode="Markdown"
        )

# ------------------ ADMIN MESSAGE HANDLER ------------------

async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    action = context.user_data.get('action')
    if not action:
        return

    msg = update.message
    text = msg.text.strip() if msg.text else ""

    if action == 'send_apk' and text.upper() == 'CONFIRM':
        await _broadcast_copy(update, context, APK_MESSAGE_ID, "📦 APK", reply_markup=APK_KEYBOARD)
        context.user_data.pop('action', None)

    elif action == 'send_video' and text.upper() == 'CONFIRM':
        await _broadcast_copy(update, context, VIDEO_MESSAGE_ID, "🎬 Video", reply_markup=VIDEO_KEYBOARD)
        context.user_data.pop('action', None)

    elif action == 'send_voice' and text.upper() == 'CONFIRM':
        await _broadcast_voice(update, context)
        context.user_data.pop('action', None)

    elif action == 'send_all' and text.upper() == 'CONFIRM':
        await send_all_files_to_all(update, context)
        context.user_data.pop('action', None)

    elif action == 'send_text':
        await send_text_broadcast(update, context, text)
        context.user_data.pop('action', None)

    else:
        await msg.reply_text("⚠️ Pehle CONFIRM type karo, ya galat action hai.")

# ------------------ BROADCAST HELPERS ------------------

async def _broadcast_copy(update, context, message_id: int, label: str, reply_markup=None):
    if len(users) == 0:
        await update.message.reply_text("❌ Koi user registered nahi hai!")
        return
        
    total = len(users)
    sm = await update.message.reply_text(f"{label} sending...\n📊 Users: {total}\n⏳ Wait...")
    success = failed = 0
    
    for uid in list(users):
        try:
            await context.bot.copy_message(
                chat_id=uid, 
                from_chat_id=SOURCE_CHANNEL, 
                message_id=message_id,
                reply_markup=reply_markup
            )
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed {uid}: {e}")
    
    rate = (success / total * 100) if total else 0
    await sm.edit_text(
        f"✅ {label} DONE!\n\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}\n"
        f"📈 Rate: {rate:.1f}%"
    )

async def _broadcast_voice(update, context):
    if len(users) == 0:
        await update.message.reply_text("❌ Koi user registered nahi hai!")
        return
        
    total = len(users)
    sm = await update.message.reply_text(f"🎤 Voice sending...\n📊 Users: {total}\n⏳ Wait...")
    success = failed = 0
    
    for uid in list(users):
        try:
            await context.bot.copy_message(
                chat_id=uid,
                from_chat_id=SOURCE_CHANNEL,
                message_id=VOICE_MESSAGE_ID
            )
            await context.bot.send_message(
                chat_id=uid,
                text="🎤 *Click below to join VIP Channel:*",
                reply_markup=VOICE_KEYBOARD,
                parse_mode="Markdown"
            )
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed {uid}: {e}")
    
    rate = (success / total * 100) if total else 0
    await sm.edit_text(
        f"✅ VOICE DONE!\n\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}\n"
        f"📈 Rate: {rate:.1f}%"
    )

async def send_all_files_to_all(update, context):
    if len(users) == 0:
        await update.message.reply_text("❌ Koi user registered nahi hai!")
        return
        
    total = len(users)
    sm = await update.message.reply_text(f"📤 All files sending...\n📊 Users: {total}\n⏳ Wait...")
    success = failed = 0
    
    for uid in list(users):
        try:
            await send_all_content_to_user(context.bot, uid)
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed {uid}: {e}")
    
    rate = (success / total * 100) if total else 0
    await sm.edit_text(
        f"✅ ALL FILES DONE!\n\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}\n"
        f"📈 Rate: {rate:.1f}%"
    )

async def send_text_broadcast(update, context, text: str):
    if len(users) == 0:
        await update.message.reply_text("❌ Koi user registered nahi hai!")
        return
        
    total = len(users)
    sm = await update.message.reply_text(f"📢 Broadcast starting...\n📊 Users: {total}")
    success = failed = 0
    
    for uid in list(users):
        try:
            await context.bot.send_message(chat_id=uid, text=text)
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed {uid}: {e}")
    
    rate = (success / total * 100) if total else 0
    await sm.edit_text(
        f"✅ BROADCAST DONE!\n\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}\n"
        f"📈 Rate: {rate:.1f}%\n\n"
        f"📝 Preview:\n{text[:100]}{'...' if len(text)>100 else ''}"
    )

# ------------------ JOIN REQUEST ------------------

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user = req.from_user
    users.add(user.id)
    save_users(users)
    
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=START_MESSAGE
        )
        
        await send_all_content_to_user(context.bot, user.id)
        
        logger.info(f"✅ All files sent to new user {user.id}")
    except Exception as e:
        logger.error(f"❌ Failed to send files to {user.id}: {e}")

# ------------------ /users ------------------

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text(f"📊 Total registered users: {len(users)}")

# ------------------ MAIN ------------------

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_menu))
    app.add_handler(CommandHandler("users", users_command))
    app.add_handler(CallbackQueryHandler(handle_admin_callback, pattern="^admin_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_message))
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    
    print("✅ Bot running successfully!")
    print(f"📊 Total users loaded: {len(users)}")
    print(f"🎬 Video Message ID: {VIDEO_MESSAGE_ID}")
    print(f"📦 APK Message ID: {APK_MESSAGE_ID}")
    print(f"🎤 Voice Message ID: {VOICE_MESSAGE_ID}")
    print(f"🔗 Channel: {SOURCE_CHANNEL}")
    print(f"✨ Premium Emojis + Colored Buttons loaded!")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()