import telebot
import requests
from bs4 import BeautifulSoup
import re
import json

TOKEN = "7786294076:AAEUMRb1Zx7iln0wWQx9rNL8s_fI1j065Mc"
bot = telebot.TeleBot(TOKEN)

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

@bot.message_handler(commands=["start"])
def start(message):
    first_name = message.from_user.first_name or "Unknown"
    bot.send_message(message.chat.id, "👋 `{first_name}`\n\n💠 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐌𝐎𝐉 𝐕𝐈𝐃𝐄𝐎 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐄𝐑 💠\n\n🔸yoυ can download any мoj vιdeo🔸\n\n🔺 𝙹𝚄𝚂𝚃 𝚂𝙴𝙽𝙳 𝚅𝙸𝙳𝙴𝙾 𝙻𝙸𝙽𝙺 🔻")

@bot.message_handler(func=lambda message: message.text and "mojapp.in" in message.text)
def download_moj_video(message):
    video_url = get_moj_video(message.text)
    
    if video_url:
        bot.send_video(message.chat.id, video_url, caption="🎥 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐌𝐨𝐣 𝐯𝐢𝐝𝐞𝐨 🪅\n\n\n☢ 𝙞𝙣𝙨𝙜𝙧𝙖𝙢 𝙧𝙚𝙚𝙡 𝙙𝙤𝙬𝙣𝙡𝙤𝙖𝙙 𝙗𝙤𝙩 🔸 @Dbdjdjdjdjdjbot ☢")
    else:
        bot.send_message(message.chat.id, "̶⚠̶️̶ ̶U̶n̶a̶b̶l̶e̶ ̶t̶o̶ ̶f̶e̶t̶c̶h̶ ̶t̶h̶e̶ ̶v̶i̶d̶e̶o̶.̶ ̶T̶r̶y̶ ̶a̶g̶a̶i̶n!")

bot.infinity_polling()
