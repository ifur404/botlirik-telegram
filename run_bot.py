import telebot
import mysql.connector
from dotenv import dotenv_values

config = dotenv_values(".env")

mydb = mysql.connector.connect(
  host=config['host'],
  user=config['user'],
  password=config['password'],
  database=config['database']
)

mycursor = mydb.cursor()
def get_id(q):
  sql = "SELECT * FROM lirik WHERE id LIKE %(q)s limit 1"
  mycursor.execute(sql,{"q":q})
  myresult = mycursor.fetchone()
  return myresult

def search_judul(q):
  sql = "SELECT * FROM lirik WHERE judul LIKE %(q)s limit "+config['LIMIT']
  mycursor.execute(sql,{"q":q})
  myresult = mycursor.fetchall()
  return myresult

def search_artis(q):
  sql = "SELECT * FROM lirik WHERE artis LIKE %(q)s limit "+config['LIMIT']
  mycursor.execute(sql,{"q":q})
  myresult = mycursor.fetchall()
  return myresult

def search_lirik(q):
  sql = "SELECT * FROM lirik WHERE lirik LIKE %(q)s limit "+config['LIMIT']
  mycursor.execute(sql,{"q":q})
  myresult = mycursor.fetchall()
  return myresult


bot = telebot.TeleBot(config["API_KEY"], parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  mes = "Silahkan cari lirik berdasarkan \n"
  mes += "/judul Dengerin Abang\n"
  mes += "/artis Armada\n"
  # mes += "/lirik Aku Cinta Kamu :)\n"
  bot.reply_to(message,mes)

@bot.message_handler(commands=['judul'])
def send_judul(message):
  mes = message.text[7:]
  row = search_judul(mes)
  if len(row) > 0 :
    hasil = "Hasil Pencarian \n"
    for x in row :
      hasil += "/id_"+str(x[0])+" | "+x[1]+ " - "+x[2]+"\n"
    bot.reply_to(message,hasil)
  else:
    bot.reply_to(message,"tidak ada judul tersebut di data")

@bot.message_handler(commands=['artis'])
def send_artis(message):
  mes = message.text[7:]
  row = search_artis(mes)
  if len(row) > 0 :
    hasil = "Hasil Pencarian \n"
    for x in row :
      hasil += "/id_"+str(x[0])+" | "+x[1]+ " - "+x[2]+"\n"
    bot.reply_to(message,hasil)
  else:
    bot.reply_to(message,"tidak ada artis tersebut di data")

# @bot.message_handler(commands=['lirik'])
# def send_lirik(message):
#   mes = message.text[7:]
#   row = search_lirik(mes)
#   if len(row) > 0 :
#     hasil = "Hasil Pencarian \n"
#     for x in row :
#       hasil += "/id_"+str(x[0])+" | "+x[1]+ " - "+x[2]+"\n"
#     bot.reply_to(message,hasil)
#   else:
#     bot.reply_to(message,"tidak ada lirik tersebut di data")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
  if message.text[:4] == "/id_":
    q = message.text[4:]
    row = get_id(q)
    if len(row) > 0 :
      hasil = "Artis : "+row[2]+"\n"
      hasil += "Judul : "+row[1]+"\n"
      hasil += "=============================\n"
      hasil += row[3]
      bot.reply_to(message,hasil)
    else:
      bot.reply_to(message,"tidak ada data")

bot.polling()