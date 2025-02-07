import telebot
import threading
import time 
import logging
import re
import os
import requests
from instaloader import Instaloader, Post
from telebot import types
import subprocess
import yt_dlp
from bs4 import BeautifulSoup
import json

# Logging setup
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TOKEN = "8056603811:AAH32j_hunSJEHTzwaFzB1b8rbybVlVbzWg"  # Set this in your environment variables

bot = telebot.TeleBot(TOKEN)

# Instagram credentials (set in environment variables)
INSTAGRAM_USERNAME = "rjfjfndjdjfndnfnfnfjfndn"
INSTAGRAM_PASSWORD = "your_instagram_password_here"

ADMIN_ID = "7858368373"

loader = Instaloader()
SESSION_FILE = f"{os.getcwd()}/session-{INSTAGRAM_USERNAME}"
session_lock = threading.Lock()

# Dictionary to store users and their downloads
user_downloads = {}

# Load or create Instagram session
def load_or_create_session():
    with session_lock:
        if os.path.exists(SESSION_FILE):
            loader.load_session_from_file(INSTAGRAM_USERNAME, filename=SESSION_FILE)
        else:
            loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            loader.save_session_to_file(SESSION_FILE)

load_or_create_session()

# Helper functions
def extract_shortcode(url):
    """Extract shortcode from Instagram URL."""
    match = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?#&]+)", url)
    return match.group(1) if match else None

def is_valid_instagram_url(url):
    """Validate Instagram URL."""
    return bool(re.match(r"https?://(www\.)?instagram\.com/(p|reel|tv)/", url))

def fetch_instagram_reel(shortcode):
    """Fetch Instagram reel media URL and caption."""
    try:
        post = Post.from_shortcode(loader.context, shortcode)
        if post.is_video:
            return post.video_url, post.caption
        else:
            return None, None
    except Exception as e:
        logger.error(f"Error fetching Instagram reel: {e}")
        return None, None

def download_file(url, file_name, retries=3):
    """Download a file with retry mechanism."""
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Download failed (attempt {attempt+1}): {e}")
            time.sleep(5)
    return False

#_&________

def get_moj_video(moj_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(moj_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # First try OpenGraph Meta Tag
        meta_tag = soup.find("meta", property="og:video")
        if meta_tag and meta_tag["content"]:
            return meta_tag["content"]

        # Try JSON Extraction
        return extract_moj_video_from_json(response.text)
    
    return None

def extract_moj_video_from_json(html_content):
    pattern = r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if match:
        json_data = json.loads(match.group(1))
        try:
            return json_data["videoData"]["videoUrl"]
        except KeyError:
            return None
    return None
#_____&&
@bot.message_handler(func=lambda message: message.text and "mojapp.in" in message.text)
def download_moj_video(message):
    video_url = get_moj_video(message.text)
    
    if video_url:
        bot.send_video(message.chat.id, video_url, caption="⦿ 🎥 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐌𝐨𝐣 𝐯𝐢𝐝𝐞𝐨 🪅\n\n\n☢ 𝙞𝙣𝙨𝙜𝙧𝙖𝙢 𝙧𝙚𝙚𝙡 𝙙𝙤𝙬𝙣𝙡𝙤𝙖𝙙 𝙗𝙤𝙩 🔸 @Dbdjdjdjdjdjbot ☢")
    else:
        bot.send_message(message.chat.id, "⚠̶️̶ ̶U̶n̶a̶b̶l̶e̶ ̶t̶o̶ ̶f̶e̶t̶c̶h̶ ̶t̶h̶e̶ ̶v̶i̶d̶e̶o̶.̶ ̶T̶r̶y̶ ̶a̶g̶a̶i̶n")
        
#₹________
def download_audio(instagram_url):
    try:
        ydl_opts = {
            'format': 'bestaudio/bbest',
            'outtmpl': 'BYE-@MR_ARMAN_OWNER.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([instagram_url])

        return "BYE-@MR_ARMAN_OWNER.mp3"
    
    except Exception as e:
        return None

# 🔹 Handle Audio Command
@bot.message_handler(commands=['audio'])
def handle_audio_command(message):
    url = message.text.strip().split(maxsplit=1)
    
    if len(url) < 2 or "instagram.com/reel/" not in url[1]:
        bot.send_message(message.chat.id, "̶❌̶ ̶I̶n̶v̶a̶l̶i̶d̶ ̶l̶i̶n̶k̶!̶ ̶P̶l̶e̶a̶s̶e̶ ̶s̶e̶n̶d̶ ̶a̶ ̶c̶o̶r̶r̶e̶c̶t̶ ̶I̶n̶s̶t̶a̶g̶r̶a̶m̶ ̶r̶e̶e̶l̶ ̶U̶R̶L̶.")
        return

    instagram_url = url[1]
    bot.send_message(message.chat.id, "⏳")

    audio_file = download_audio(instagram_url)

    if audio_file:
        bot.send_audio(message.chat.id, open(audio_file, 'rb'), caption="🔸📥 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐚𝐮𝐝𝐢𝐨 𝐟𝐢𝐥𝐞 🔸\n\n🔹 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈𝙴 :- @Dbdjdjdjdjdjbot")
        os.remove(audio_file)  # Delete file after sending
    else:
        bot.send_message(message.chat.id, "⚠̶️̶ ̶U̶n̶a̶b̶l̶e̶ ̶t̶o̶ ̶f̶e̶t̶c̶h̶ ̶t̶h̶e̶ ̶v̶i̶d̶e̶o̶.̶ ̶T̶r̶y̶ ̶a̶g̶a̶i̶n")


from telebot import types

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.username or "No Username"
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Unknown"

    # Step 1: Send "⌛" and delete after 2 seconds
    temp_msg = bot.send_message(chat_id, "⌛")
    time.sleep(2)
    bot.delete_message(chat_id, temp_msg.message_id)

    # Step 2: Show typing animation
    bot.send_chat_action(chat_id, "typing")
    time.sleep(0.5)  # Simulate typing delay

    # Step 3: Prepare welcome message
    caption_text = (
        f"👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ɪɴᴤᴛᴀɢʀᴀᴍ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ\n\n"
        f"⦿ 🆔 𝚈𝙾𝚄𝚁 𝙽𝙰𝙼𝙴 - `@{user_name}`\n"
        f"⦿ 🆔 𝚈𝙾𝚄𝚁 𝙸𝙳 - `{user_id}`\n"
        f"⦿ 🆔 𝚈𝙾𝚄𝚁 𝙵𝙸𝚁𝚂𝚃 𝙽𝙰𝙼𝙴 - `{first_name}`\n\n"
        "📩 𝐒𝐞𝐧𝐝 𝐦𝐞 𝐚𝐧𝐲 𝐩𝐮𝐛𝐥𝐢𝐜 𝐈𝐧𝐬𝐭𝐚𝐠𝐫𝐚𝐦 𝐥𝐢𝐧𝐤 (𝐑𝐞𝐞𝐥𝐬, 𝐏𝐨𝐬𝐭𝐬, 𝐞𝐭𝐜.), 𝐚𝐧𝐝 𝐈'𝐥𝐥 𝐡𝐞𝐥𝐩 𝐲𝐨𝐮 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐢𝐭\n\n"
        "⚠️ 𝑶𝒏𝒍𝒚 𝒑𝒖𝒃𝒍𝒊𝒄 𝒑𝒐𝒔𝒕𝒔 𝒂𝒓𝒆 𝒔𝒖𝒑𝒑𝒐𝒓𝒕𝒆𝒅 ⦿"
    )

    # Step 4: Create Inline Keyboard with Buttons
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("➕ ᴬᵈᵈ ᴹᵉ ᵗᵒ ʸᵒᵘʳ ᴳʳᵒᵘᵖ", url=f"https://t.me/{bot.get_me().username}?startgroup=true"))
    keyboard.add(types.InlineKeyboardButton("📢 J̳̿͟͞O̳̿͟͞I̳̿͟͞N̳̿͟͞", url="https://t.me/ARMANTEAMVIP"))
    keyboard.add(types.InlineKeyboardButton("👨‍💻 𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁", url="https://t.me/MR_ARMAN_OWNER"))

    # Step 5: Fetch user's profile photo (if available)
    photos = bot.get_user_profile_photos(user_id)
    if photos.total_count > 0:
        # Get the highest resolution photo
        photo = photos.photos[0][-1].file_id
        bot.send_photo(chat_id, photo, caption=caption_text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, caption_text, parse_mode="Markdown", reply_markup=keyboard)
        
   

@bot.message_handler(commands=["help"])
def help(message):
    chat_id = message.chat.id
    user_name = message.from_user.username if message.from_user.username else "No Username"
    first_name = message.from_user.first_name if message.from_user.first_name else "Unknown"

    help_text = (
        f"👋  {first_name}! 𝙷𝚎𝚕𝚕𝚘 𝙷𝚎𝚛𝚎'𝚜 𝚑𝚘𝚠 𝙸 𝚌𝚊𝚗 𝚊𝚜𝚜𝚒𝚜𝚝 𝚢𝚘𝚞🔹\n\n"
        f"⦿ 𝐔𝐬𝐞 /𝐚𝐮𝐝𝐢𝐨 <𝐫𝐞𝐞𝐥_𝐮𝐫𝐥> 𝐭𝐨 𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐚𝐮𝐝𝐢𝐨 𝐟𝐫𝐨𝐦 𝐚 𝐯𝐢𝐝𝐞𝐨.🔹\n\n"
        f"⦿ 𝐝𝐢𝐫𝐞𝐜𝐭 𝐥𝐢𝐧𝐤 𝐝𝐚𝐚𝐥𝐨 𝐯𝐢𝐝𝐞𝐨 𝐯𝐢𝐝𝐞𝐨 𝐦𝐢𝐥 𝐣𝐚𝐲𝐞𝐠𝐚 𝐭𝐡𝐮𝐦𝐞🔹\n\n"
        f"⦿ 𝙶𝙸𝚅𝙴 𝙼𝙴 𝙰𝙽𝚈 𝙼𝙾𝙹 𝚅𝙸𝙳𝙴𝙾 𝚄𝚁𝙻 𝙰𝙽𝙳 𝙸'𝙻𝙻 𝙸𝙼𝙼𝙴𝙳𝙸𝙰𝚃𝙴𝙻𝚈 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳 𝙰𝙽𝙳 𝚂𝙴𝙽𝙳 𝚈𝙾𝚄🔹\n\n"
        f"⦿ 𝙁𝙤𝙧 𝙖𝙣𝙮 𝙛𝙪𝙧𝙩𝙝𝙚𝙧 𝙦𝙪𝙚𝙨𝙩𝙞𝙤𝙣𝙨 𝙤𝙧 𝙛𝙚𝙚𝙙𝙗𝙖𝙘𝙠, 𝙛𝙚𝙚𝙡 𝙛𝙧𝙚𝙚 𝙩𝙤 𝙧𝙚𝙖𝙘𝙝 𝙤𝙪𝙩!"
    )

    # Send the help message
    bot.send_message(chat_id, help_text)
    
    
# Command: Users (Admin only)
@bot.message_handler(commands=["users"])
def list_users(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return
    
    if not user_downloads:
        bot.reply_to(message, "📂 No user data available.")
        return

    users_text = "📜 User Download List:\n\n"
    for user_id, details in user_downloads.items():
        users_text += f"👤 Username: {details['username']}\n"
        users_text += f"🆔 User ID: {user_id}\n"
        users_text += f"📥 Downloaded Videos: {len(details['downloads'])}\n"
        users_text += "_________________________\n"

    bot.send_message(message.chat.id, users_text)

# Handle: Instagram Link
@bot.message_handler(func=lambda message: is_valid_instagram_url(message.text))
def download_content(message):
    user_id = message.chat.id
    username = message.from_user.username or "Unknown"

    if user_id not in user_downloads:
        user_downloads[user_id] = {"username": username, "downloads": []}

    url = message.text.strip()
    shortcode = extract_shortcode(url)

    if not shortcode:
        bot.reply_to(message, "⚠̶️̶ ̶U̶n̶a̶b̶l̶e̶ ̶t̶o̶ ̶f̶e̶t̶c̶h̶ ̶t̶h̶e̶ ̶v̶i̶d̶e̶o̶.̶ ̶T̶r̶y̶ ̶a̶g̶a̶i̶n")
        return

    bot.send_chat_action(message.chat.id, "typing")
    progress_msg = bot.send_message(message.chat.id, "⏳")

    reel_url, caption = fetch_instagram_reel(shortcode)
    if reel_url:
        bot.send_chat_action(message.chat.id, "upload_video")

        file_name = f"reel_{message.chat.id}.mp4"
        if download_file(reel_url, file_name):
            credit_text = "\n\n⦿ @ARMAN_TEAMVIP\n⦿  𝚃𝚑𝚒𝚜 𝚟𝚒𝚍𝚎𝚘 𝚒𝚜 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍 𝚋𝚢 : @Dbdjdjdjdjdjbot\n\n\n🔹/𝚊𝚞𝚍𝚒𝚘 <𝚛𝚎𝚎𝚕_𝚞𝚛𝚕>"
            full_caption = caption + credit_text if caption else credit_text

            with open(file_name, "rb") as video:
                bot.send_video(message.chat.id, video=video, caption=full_caption)

            os.remove(file_name)
            bot.delete_message(message.chat.id, progress_msg.message_id)

            # Log successful download
            user_downloads[user_id]["downloads"].append(reel_url)

            # Notify admin
            admin_message = (
                f"📥 New Download:\n\n"
                f"👤 User: @{username}\n"
                f"🆔 User ID: {user_id}\n\n"
                f"🔗 Download Link: {url}\n\n"
                f"✅ Status: Download Success"
            )
            bot.send_message(ADMIN_ID, admin_message)
        else:
            bot.edit_message_text("⚠̶️̶ ̶U̶n̶a̶b̶l̶e̶ ̶t̶o̶ ̶f̶e̶t̶c̶h̶ ̶t̶h̶e̶ ̶v̶i̶d̶e̶o̶.̶ ̶T̶r̶y̶ ̶a̶g̶a̶i̶n.", message.chat.id, progress_msg.message_id)

            # Notify admin about failure
            admin_message = (
                f"❌ Failed Download:\n"
                f"👤 User: @{username}\n"
                f"🆔 User ID: {user_id}\n"
                f"🔗 Download Link: {url}\n"
                f"❌ Status: Download Failed"
            )
            bot.send_message(ADMIN_ID, admin_message)
    else:
        bot.edit_message_text("❌ ᶠᵃⁱˡᵉᵈ ᵗᵒ ᶠᵉᵗᶜʰ ᵗʰᵉ ʳᵉᵉˡ. ᴱⁿˢᵘʳᵉ ⁱᵗ'ˢ ᵖᵘᵇˡⁱᶜ.", message.chat.id, progress_msg.message_id)

        # Notify admin about failure
        admin_message = (
            f"❌ Failed Fetch:\n"
            f"👤 User: @{username}\n"
            f"🆔 User ID: {user_id}\n"
            f"🔗 Download Link: {url}\n"
            f"❌ Status: Fetch Failed"
        )
        bot.send_message(ADMIN_ID, admin_message)

# Support command handler
@bot.message_handler(commands=['support'])
def support_command(message):
    bot.reply_to(message, "📞 𝙵𝚘𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝, 𝚙𝚕𝚎𝚊𝚜𝚎 𝚌𝚘𝚗𝚝𝚊𝚌𝚝 @MR_ARMAN_OWNER 𝚘𝚛 𝚟𝚒𝚜𝚒𝚝 𝚘𝚞𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 𝚐𝚛𝚘𝚞𝚙 : @ARMANTEAMVIP")

# Handle Video and Process in a separate thread to speed up
def process_video(message, video_file_id):
    video = bot.get_file(video_file_id)
    video_file_path = f'{video_file_id}.mp4'

    try:
        downloaded_file = bot.download_file(video.file_path)
        with open(video_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "⦿ 🔄 ᴘʀᴏᴄᴇᴤᴤɪɴɢ ʏᴏᴜʀ ᴠɪᴅᴇᴏ, ᴘʟᴇᴀᴤᴇ ᴡᴀɪᴛ...🔹")

        if os.path.getsize(video_file_path) > 18 * 1024 * 1024:
            bot.reply_to(message, "❌ 𝙎𝙤𝙧𝙧𝙮, 𝙩𝙝𝙚 𝙫𝙞𝙙𝙚𝙤 𝙨𝙞𝙯𝙚 𝙚𝙭𝙘𝙚𝙚𝙙𝙨 18𝙈𝘽.")
            os.remove(video_file_path)
            return

        audio_file_path = f'{video_file_id}.mp3'
        command = f'ffmpeg -i "{video_file_path}" -q:a 0 -map a "{audio_file_path}" -threads 4 -preset fast'
        subprocess.run(command, shell=True)

        bot.send_chat_action(message.chat.id, 'upload_audio')
        with open(audio_file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="⦿ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏᴇ : @Sidgkdigdjgzigdotxotbot🔹")

        os.remove(video_file_path)
        os.remove(audio_file_path)

        bot.send_message(message.chat.id, "👉 ⦿ 𝙿𝙻𝙴𝙰𝚂𝙴 𝙹𝙾𝙸𝙽 : @ARMANTEAMVIP🔹")

    except Exception as e:
        bot.reply_to(message, "̶⚠̶️̶ ̶A̶n̶ ̶e̶r̶r̶o̶r̶ ̶o̶c̶c̶u̶r̶r̶e̶d̶ ̶d̶u̶r̶i̶n̶g̶ ̶p̶r̶o̶c̶e̶s̶s̶i̶n̶g̶.̶ ̶P̶l̶e̶a̶s̶e̶ ̶t̶r̶y̶ ̶a̶g̶a̶i̶n̶ ̶l̶a̶t̶e̶r̶.")
        print(f"Error: {e}")


@bot.message_handler(content_types=['video'])
def handle_video(message):
    video_file_id = message.video.file_id
    threading.Thread(target=process_video, args=(message, video_file_id)).start()  # Process video in a new thread
    
    
# Main function
if __name__ == "__main__":
    logger.info("Bot is running...")
    bot.infinity_polling()


