import os
import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# توکن تلگرام شما
TOKEN = '8845228023:AAG544VITXBB-AnsY4gr3451xDQ_uZW9gB0'
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

# چیدمان کیبوردهای بازی
main_menu_keyboard = [[{"text": "سنگ, کاغذ, قیچی 🎮"}, {"text": "شیر یا خط 🪙"}]]
rps_keyboard = [[{"text": "سنگ ✊"}, {"text": "کاغذ ✋"}, {"text": "قیچی ✌️"}], [{"text": "بازگشت به منوی اصلی 🔙"}]]
coin_keyboard = [[{"text": "شیر 🦁"}, {"text": "خط 📜"}], [{"text": "بازگشت به منوی اصلی 🔙"}]]

rps_choices = ["سنگ ✊", "کاغذ ✋", "قیچی ✌️"]
coin_choices = ["شیر 🦁", "خط 📜"]

def send_message(chat_id, text, keyboard_layout=None):
    url = BASE_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if keyboard_layout:
        payload["reply_markup"] = {"keyboard": keyboard_layout, "resize_keyboard": True}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Error sending message:", e)

@app.route('/', methods=['GET'])
def home():
    return "Bot is Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if update and "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        user_text = update["message"]["text"].strip()
        user_name = update["message"]["from"].get("first_name", "دوست")

        if user_text == "/start" or user_text == "بازگشت به منوی اصلی 🔙":
            welcome_text = f"سلام {user_name} عزیز! 🌟\nبه ربات بازی خوش آمدی.\n\nلطفاً یکی از بازی‌ها رو انتخاب کن: 👇"
            send_message(chat_id, welcome_text, main_menu_keyboard)
        
        elif user_text == "سنگ, کاغذ, قیچی 🎮":
            send_message(chat_id, "وارد بازی سنگ، کاغذ، قیچی شدی! یکی از گزینه‌های زیر رو انتخاب کن: 👇", rps_keyboard)
        
        elif user_text == "شیر یا خط 🪙":
            send_message(chat_id, "وارد بازی شیر یا خط شدی! پیش‌بینی کن که سکه چطوری میفته؟ 👇", coin_keyboard)
        
        elif user_text in rps_choices:
            bot_choice = random.choice(rps_choices)
            if user_text == bot_choice:
                result = "مساوی شدیم! 🤝 دستان مثل هم بود."
            elif (user_text == "سنگ ✊" and bot_choice == "قیچی ✌️") or \
                 (user_text == "کاغذ ✋" and bot_choice == "سنگ ✊") or \
                 (user_text == "قیچی ✌️" and bot_choice == "کاغذ ✋"):
                result = "بارک‌الله! شما برنده شدی! 🎉 🏆"
            else:
                result = "من برنده شدم! 😜 🦾"
            send_message(chat_id, f"انتخاب شما: {user_text}\nانتخاب ربات: {bot_choice}\n\nنتیجه: {result}", rps_keyboard)
        
        elif user_text in coin_choices:
            bot_choice = random.choice(coin_choices)
            result = f"درست حدس زدی! 🎉 سکه {bot_choice} اومد و برنده شدی! 🪙" if user_text == bot_choice else f"ای‌بابا! اشتباه حدس زدی. 😜 سکه {bot_choice} اومد."
            send_message(chat_id, result, coin_keyboard)
        
        else:
            send_message(chat_id, "لطفاً فقط از دکمه‌های پایین صفحه استفاده کن! 👇", main_menu_keyboard)

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
