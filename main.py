#
# import time
# import telepot
# from telepot.loop import MessageLoop
# import DBHelper
#
# cnx = DBHelper.connection()
# cursor = DBHelper.setup_cursor(cnx.cursor())
# state = ""
# counter = 1
#
# RegParam = {'id':"", 'name':"", 'age':"", 'field':"", 'sex':""}
#
# def handle(msg):
#
#
#     content_type, chat_type, chat_id = telepot.glance(msg)
#     print(content_type, chat_type, chat_id)
#
#
#     if content_type == 'text':
#
#         if msg['text'] == '/start':
#             bot.sendMessage(chat_id, 'شما در سایت ثبت نام نشده اید لطفا نام خود را وارد کنید')
#
#
#
#
#                 # DBHelper.executeQuery(query,cursor)
#                 # bot.sendMessage(chat_id , 'نام شما با موفقیت ثبت شد')
#
#
#
#
# TOKEN = "537967601:AAFhqCoQKZSuKMBQhq7SHdlEr1hM_rRLctM"
#
# bot = telepot.Bot(TOKEN)
# MessageLoop(bot, handle).run_as_thread()
# print ('Listening ...')
#
# # Keep the program running.
# while 1:
#     time.sleep(10)

import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open
import DBHelper
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        self._state = "start"
        self.lastid = 0
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0
        self._msgContent = ""
        self.cnx = DBHelper.connection();
        self.cursor = DBHelper.setup_cursor(self.cnx)
        key1 = KeyboardButton(text='مرد', callback_data='male')
        key2 = KeyboardButton(text='زن', callback_data='female')

        f1 = KeyboardButton(text='فنی مهندسی', callback_data='Engineering')
        f2 = KeyboardButton(text='علوم پایه', callback_data='Science')
        f3 = KeyboardButton(text='علوم انسانی', callback_data='Humanities')
        f4 = KeyboardButton(text='پزشکی', callback_data='Medical')
        f5 = KeyboardButton(text='هنر', callback_data='Art')


        login = KeyboardButton(text='ورود')
        reg = KeyboardButton(text='ثبت نام')



        self.fieldKeys = [[f1, f2], [f3, f4], [f5]]
        self.keyboard = [[key1, key2]]

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
                    self._state = "enterName"

                    # query = ("SELECT name FROM users")
                    # DBHelper.executeQuery(query , self.cursor)
                    # for userName in self.cursor:
                    #     print(userName[0])

                    # elif self._state == "enterName":
                    #     self._msgContent = "لطفا سن خود را وارد کنید"
                    #     self.sender.sendMessage(self._msgContent)
                    #     self._state = "enterAge"
            else:



                if self._state == "enterName":

                    self.userInfo['name'] = msg['text']
                    self._msgContent = "لطفا سن خود را وارد کنید"
                    self.sender.sendMessage(self._msgContent)
                    self._state = "enterAge"

                elif self._state == "enterAge":

                    a = int(msg['text'])
                    self.userInfo['age'] = a


                    self._msgContent = "لطفا جنسیت خود را انتخاب کنید"
                    reply = ReplyKeyboardMarkup(keyboard=self.keyboard, one_time_keyboard=True)
                    self.sender.sendMessage(self._msgContent, reply_markup=reply)
                    self._state = "enterSex"

                elif self._state == "enterSex":

                    self.userInfo['sex'] = msg['text']
                    self._msgContent = "لطفا گروه تحصیلی خود را انتخاب کنید"
                    reply = ReplyKeyboardMarkup(keyboard=self.fieldKeys, one_time_keyboard=True)
                    self.sender.sendMessage(self._msgContent, reply_markup=reply)
                    self._state = "enterField"

                elif self._state == "enterField":

                    self._msgContent = "ثبت نام شما با موفقیت انجام شد"
                    self.userInfo['field'] = msg['text']

                    # query = ("INSERT INTO users"
                    #          "(name , age , field , sex)"
                    #          "VALUES(%s , %s, %s, %s)")
                    #

                    query = "INSERT INTO users(name,age, field, sex) " \
                            "VALUES(%(name)s,%(age)s,%(field)s,%(sex)s)"

                    self.cursor.execute(query,self.userInfo)

                    self.cnx.commit()

                    self.sender.sendMessage(self._msgContent)

                    self._state = "endRegistration"

                elif self._state == "endRegistration":

                    self._msgContent = "سلام {} عزیز اطلاعات شما به صورت زیر است\n"
                    self.lastid = self.cursor.lastrowid

                    # query1 = ("SELECT * FROM users"
                    #           "WHERE id IS %s")



                    print(self.lastid)

                    # self.cursor.execute(query1 , self.lastid)

                    for name in self.cursor:

                        print(name)




                    # print(msg['from']['first_name'])
                    # self.sender.sendMessage(self._count)
            print(msg['text'])
            print(self._state)



    def on__idle(self, event):
        text = ' timeout'
        # self.editor.editMessageText(
        #     text + '\n\nThis message will disappear in 5 seconds to test deleteMessage',
        #     reply_markup=None)

        time.sleep(5)
        # self.editor.deleteMessage()

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
