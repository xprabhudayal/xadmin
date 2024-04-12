import subprocess as s
import os
import requests as r
from mss import mss
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.colab import userdata
# import asyncio

#This would show us that the bot is typing...
from functools import wraps

def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    return decorator
###



# Define your Telegram bot token
TOKEN = userdata.get('XADMIN')

# Define the command handlers
@send_action('typing')
def start(update, context):
    update.message.reply_html(f'''<pre class="spoiler">Hi {(update.effective_user.username).upper()}
Type help for commands</pre>
''')


@send_action('record_video_note')
def main(update, context):
  text : str = update.message.text

  if text.startswith('@'):
    file_name = text.replace("@","")

    if msg_handler(text) != str:
      return context.bot.send_document(chat_id=update.effective_chat.id, document=msg_handler(text))

    #document send remotely
    if os.path.isfile(f"./{file_name}"):
      with open(file_name, 'rb') as f:
        return context.bot.send_document(chat_id=update.effective_chat.id, document=f)

    else :
      return update.message.reply_html("<pre>the file does not exists</pre>")

  elif text.startswith("#"):
    return update.message.reply_html(random_cmd())

  else:
    try:
      return update.message.reply_html(msg_handler(text))
    except Exception as e:
      return update.message.reply_text(f"ERROR : {e}")


#directory changer
def change_dir(inp:str) -> str:
    cwd = inp.split(" ")
    os.chdir(cwd[1])
    return os.getcwd()


#for shell based functionings
def shell(inp : str) :
  if "cd" in inp:
      new_dir = change_dir(inp)
      return new_dir
      # await update.message.reply_text(new_dir)
  else:
      out = s.run(inp,text = True, shell=True, capture_output=True)
      final = out.stdout.replace("\n\n\n\n","\n\n")
      if out.returncode == 0:
          # await update.message.reply_text(final)
          return final
      else:
          return (f"ERROR : {out.stderr}")

def get_ip():
    ip_address = r.get("https://api.ipify.org").text
    return f"IP Address: {ip_address}"


##--------------------------------------------##
import random as rand
from bs4 import BeautifulSoup as b

def random_cmd():
  res = r.get(r'https://www.computerhope.com/overview.htm')
  soup = b(res.content)

  #total 143 windows commands are there
  fin = soup.find_all(class_= "tcw")

  choice = rand.randint(0,143)
  desc = fin[choice].text.split("\n")[2]
  cmd = fin[choice].a.text

  return (f"<b>{cmd}</b> : {desc}")

##--------------------------------------------##


def msg_handler(text : str):
  if text == 'ip' :
    return get_ip()
  elif text.lower() == 'help':
    return '''list of useful commands (case sensitive)

Screenshot : <pre>ss or screenshot</pre>

Remotely File Sharing : <pre>using @ before file_name(no spaces)</pre>

Random Windows Command : <pre>#</pre>

IP Address Extraction : <pre>ip</pre>

Support : https://github.com/xprabhudayal/xadmin?tab=readme-ov-file

  '''
  elif text.lower() == 'ss'  or  text.lower() == 'screenshot':
    try:
      with mss() as sct:
        ss = sct.shot()
        return
    except Exception as e:
      return e
  else :
    try:
      return shell(text)
    except Exception as e:
      return e






# Create the Updater and pass in your bot's token
updater = Updater(TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Add command handlers
dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(MessageHandler(Filters.text, main))
# dispatcher.add_handler(CommandHandler("screenshot", screenshot))
dispatcher.add_handler(CommandHandler("ip", get_ip))

# Start the Bot
updater.start_polling()
updater.idle()
