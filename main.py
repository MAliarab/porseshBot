import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open
import DBHelper
from Register import Register
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):

        self._state = "start"
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._msgContent = ""
        self.cnx = DBHelper.connection();
        self.cursor = DBHelper.setup_cursor(self.cnx)
        self.reg = Register(self.sender)

        login = KeyboardButton(text='ورود', request_contact=True)
        reg = KeyboardButton(text='ثبت نام')


        self.initial = [[login , reg]]

        self.userInfo = {
            'name': "",
            'age': "",
            'sex': "",
            'field': ""
        }



    def on_chat_message(self, msg):

        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type == 'text':
            if msg['text'] == '/start':
                if self._state == "start":

                    # self.sender.sendMessage("شما هنوز ثبت نام نکرده اید لطفا نام خود را وارد کنید")
                    self._msgContent = " عزیز سلام {} \n اگر قبلا ثبت نام کرده اید \"ورود\" و در غیر اینصورت \"ثبت نام\" را انتخاب کنید".format(
                        msg['from']['first_name'])
                    reply = ReplyKeyboardMarkup(keyboard=self.initial, one_time_keyboard=True)
                    self.sender.sendMessage(self._msgContent,reply_markup=reply)
                elif self._state == "register":

                    self._state == self.reg.register(msg, content_type)

            elif (msg['text'] == 'ثبت نام' and self._state == 'start'):

                self._state = "register"
                self._state = self.reg.register(msg, content_type)

            elif (msg['text'] == 'ورود' and self._state == 'start'):

                self._state = "login"
            else:

                if self._state == "register":

                    self._state = self.reg.register(msg, content_type)

                elif self._state == "loggedIn":
                    self._msgContent = " میتوانید پرسشنامه ی جدیدی ایجاد کنید یا با داشتن آیدی به پرسشنامه ای جواب دهید"



        elif content_type == "contact":

            self._state = self.reg.register(msg, content_type)

        print(self._state)
        # print(msg['text'])
        print(content_type)


    def on__idle(self, event):
        text = ' timeout'

        time.sleep(5)

    def on_close(self, ex):
        print('on_close() called due to %s: %s', type(ex).__name__, ex)





TOKEN = "537967601:AAFhqCoQKZSuKMBQhq7SHdlEr1hM_rRLctM"  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])
MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(10)


#-------------------------ignored

    # query = ("SELECT name FROM users")
    # DBHelper.executeQuery(query , self.cursor)
    # for userName in self.cursor:
    #     print(userName[0])

    # elif self._state == "enterName":
    #     self._msgContent = "لطفا سن خود را وارد کنید"
    #     self.sender.sendMessage(self._msgContent)
    #     self._state = "enterAge"