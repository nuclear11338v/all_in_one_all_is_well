import telebot
import os
import subprocess
import threading

API_TOKEN = '7685491877:AAGCya_bYave_CQm0cyEUNG0hnhRYt1oCsA'
bot = telebot.TeleBot(API_TOKEN)

ADMIN_ID = 7858368373  # Replace with your admin ID
USER_IDS_FILE = "user_id.txt"

# Function to save user IDs
def save_user(user_id):
    with open(USER_IDS_FILE, "a+") as file:
        file.seek(0)
        users = file.read().splitlines()
        if str(user_id) not in users:
            file.write(f"{user_id}\n")

# Start command handler
@bot.message_handler(commands=['start'])
def start_command(message):
    save_user(message.from_user.id)
    bot.reply_to(message, "👋 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚝𝚘 𝚅𝚒𝚍𝚎𝚘 𝚝𝚘 𝙰𝚞𝚍𝚒𝚘 𝙲𝚘𝚗𝚟𝚎𝚛𝚝𝚎𝚛 𝙱𝚘𝚝!\n\n𝚂𝚎𝚗𝚍 𝚊 𝚟𝚒𝚍𝚎𝚘 𝚊𝚗𝚍 𝙸'𝚕𝚕 𝚌𝚘𝚗𝚟𝚎𝚛𝚝 𝚒𝚝 𝚝𝚘 𝚊𝚞𝚍𝚒𝚘 𝚏𝚘𝚛 𝚢𝚘𝚞.")

# Help command handler
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🛠 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 :\n"
        "⦿ /start - 𝚆𝚎𝚕𝚌𝚘𝚖𝚎 𝚖𝚎𝚜𝚜𝚊𝚐𝚎\n"
        "⦿ /help - 𝙻𝚒𝚜𝚝 𝚘𝚏 𝚊𝚟𝚊𝚒𝚕𝚊𝚋𝚕𝚎 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜\n"
        "⦿ /support - 𝙶𝚎𝚝 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 𝚒𝚗𝚏𝚘𝚛𝚖𝚊𝚝𝚒𝚘𝚗\n"
        "⦿ /users - 𝚂𝚑𝚘𝚠 𝚊𝚕𝚕 𝚞𝚜𝚎𝚛𝚜 (𝙰𝚍𝚖𝚒𝚗 𝙾𝚗𝚕𝚢)\n"
        "⦿ /broadcast - 𝚂𝚎𝚗𝚍 𝚖𝚎𝚜𝚜𝚊𝚐𝚎 𝚝𝚘 𝚊𝚕𝚕 𝚞𝚜𝚎𝚛𝚜 (𝙰𝚍𝚖𝚒𝚗 𝙾𝚗𝚕𝚢)\n"
        "⦿ ᴤɪᴍᴘʟʏ ᴤᴇɴᴅ ᴀ ᴠɪᴅᴇᴏ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ɪᴛ ɪɴᴛᴏ ᴀᴜᴅɪᴏ!"
    )
    bot.reply_to(message, help_text)

# Support command handler
@bot.message_handler(commands=['support'])
def support_command(message):
    bot.reply_to(message, "📞 𝙁𝙤𝙧 𝙨𝙪𝙥𝙥𝙤𝙧𝙩, 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 @MR_ARMAN_OWNER  @ARMANTEAMVIP")

# Notify admin about user conversion
def notify_admin(user, status):
    try:
        bot.send_message(
            ADMIN_ID,
            f"*New user convert*\n"
            f"User name: @{user.username if user.username else 'No Username'}\n"
            f"User ID: {user.id}\n"
            f"User converts: Yes\n"
            f"User converting: {status}",
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin notification failed: {e}")

# Process video
def process_video(message, video_file_id):
    user = message.from_user
    video = bot.get_file(video_file_id)
    video_file_path = f'{video_file_id}.mp4'

    try:
        downloaded_file = bot.download_file(video.file_path)
        with open(video_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "🔄 ᴾʳᵒᶜᵉˢˢⁱⁿᵍ ʸᵒᵘʳ ᵛⁱᵈᵉᵒ, ᵖˡᵉᵃˢᵉ ʷᵃⁱᵗ...")

        if os.path.getsize(video_file_path) > 18 * 1024 * 1024:
            bot.reply_to(message, "❌ 𝚂𝚘𝚛𝚛𝚢, 𝚝𝚑𝚎 𝚟𝚒𝚍𝚎𝚘 𝚜𝚒𝚣𝚎 𝚎𝚡𝚌𝚎𝚎𝚍𝚜 18𝙼𝙱.")
            os.remove(video_file_path)
            notify_admin(user, "failed")
            return

        audio_file_path = f'{video_file_id}.mp3'
        command = f'ffmpeg -i "{video_file_path}" -q:a 0 -map a "{audio_file_path}" -threads 4 -preset fast'
        subprocess.run(command, shell=True)

        bot.send_chat_action(message.chat.id, 'upload_audio')
        with open(audio_file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="ᴰᴼᵂᴺᴸᴼᴬᴰᴱᴰ ᴮʸ @Sidgkdigdjgzigdotxotbot")

        os.remove(video_file_path)
        os.remove(audio_file_path)

        bot.send_message(message.chat.id, "👉 ᴾᴸᴱᴬˢᴱ ᴶᴼᴵᴺ : @ARMANTEAMVIP")
        notify_admin(user, "successfully")

    except Exception as e:
        bot.reply_to(message, "̶⚠̶️̶ ̶A̶n̶ ̶e̶r̶r̶o̶r̶ ̶o̶c̶c̶u̶r̶r̶e̶d̶ ̶d̶u̶r̶i̶n̶g̶ ̶p̶r̶o̶c̶e̶s̶s̶i̶n̶g̶.̶ ̶P̶l̶e̶a̶s̶e̶ ̶t̶r̶y̶ ̶a̶g̶a̶i̶n̶ ̶l̶a̶t̶e̶r̶.")
        print(f"Error: {e}")
        notify_admin(user, "failed")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    save_user(message.from_user.id)
    video_file_id = message.video.file_id
    threading.Thread(target=process_video, args=(message, video_file_id)).start()

# Show all users (Admin Only)
@bot.message_handler(commands=['users'])
def show_users(message):
    if message.from_user.id == ADMIN_ID:
        try:
            with open(USER_IDS_FILE, "r") as file:
                user_ids = file.read().splitlines()

            if user_ids:
                user_list = "\n".join([f"ID: {uid}" for uid in set(user_ids)])
                bot.send_message(message.chat.id, f"👥 *Users List:*\n\n{user_list}", parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "No users found.")
        except FileNotFoundError:
            bot.send_message(message.chat.id, "No users found.")
    else:
        bot.reply_to(message, "̶❌̶ ̶Y̶o̶u̶ ̶a̶r̶e̶ ̶n̶o̶t̶ ̶a̶u̶t̶h̶o̶r̶i̶z̶e̶d̶ ̶t̶o̶ ̶u̶s̶e̶ ̶t̶h̶i̶s̶ ̶c̶o̶m̶m̶a̶n̶d.")

# Broadcast message (Admin Only)
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "📢 Please enter your message to broadcast.")
        bot.register_next_step_handler(message, send_broadcast)
    else:
        bot.reply_to(message, "̶❌̶ ̶Y̶o̶u̶ ̶a̶r̶e̶ ̶n̶o̶t̶ ̶a̶u̶t̶h̶o̶r̶i̶z̶e̶d̶ ̶t̶o̶ ̶u̶s̶e̶ ̶t̶h̶i̶s̶ ̶c̶o̶m̶m̶a̶n̶d")

def send_broadcast(message):
    try:
        with open(USER_IDS_FILE, "r") as file:
            user_ids = file.read().splitlines()

        success, failed = 0, 0
        for user_id in set(user_ids):
            try:
                bot.send_message(user_id, f"📢 *Broadcast Message:*\n\n{message.text}", parse_mode="Markdown")
                success += 1
            except Exception:
                failed += 1

        bot.send_message(message.chat.id, f"✅ Message sent to {success} users.\n❌ Failed: {failed}")

    except FileNotFoundError:
        bot.send_message(message.chat.id, "No users found.")

# Start polling
bot.polling(non_stop=True)
                               
