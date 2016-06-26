from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

import sys
import time
import pprint
import telepot

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print (content_type, chat_type, chat_id, msg['chat']['username'])
    print(msg['text'])

    if content_type == 'text':
        if msg['text'] == '/start':
              bot.sendMessage(chat_id, """Type your code...\n
Note that python language is case sensitive!\n
Try these commands:
    print('Hello World')
    x = 2
    print(x)
    for i in range(10): print(i)
or any desired code!""")
        elif msg['text'] == '/stop':
            bot.sendMessage(chat_id, 'Bye :(')
        else:
            #bot.sendMessage(chat_id, "Python Code:\n" + msg['text'])
            code = msg['text']
            flag = True;
            with stdoutIO() as screen:
                try:
                    exec(code)
                except Exception as exception:
                    flag = False
                    error = str(exception)
                    print(error)

            result = screen.getvalue()
            if ((result.find('name') != -1) and (result.find('is not defined') != -1) and result != result.lower()):
                result += '\n' + '-May help you: Python language is case sensitive!'
            if flag:
                output = '>>> Result\n'
            else:
                output = '>>> Error\n'

            #max_line = max([len(line) for line in result.split('\n')])
            #if max_line < 12:
            #    max_line = 12
            #elif max_line > 40:
            #    max_line = 40
            #for i in range(max_line):
            #    output = output + '_'
            output += '\n' + result
            bot.sendMessage(chat_id, output)

    if content_type != 'text':
        bot.sendMessage(chat_id, """It is not even a text, let alone a python code!\n
Please send a TEXT content!""")


# Getting the token from command-line is better than embedding it in code,
# because tokens are supposed to be kept secret.
TOKEN = '196858157:AAEwHOS5hTgqt1vF9C04B9ma6IXv6dvB0GU'

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(1)

