import telepot
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import DBHelper


class Register:

    def __init__(self, sender):

        self.sender = sender
        self._subState = "start"
        self._msgContent = ""
        self.cnx = DBHelper.connection()
        self.cursor = DBHelper.setup_cursor(self.cnx)
        key1 = KeyboardButton(text='مرد', callback_data='male')
        key2 = KeyboardButton(text='زن', callback_data='female')

        f1 = KeyboardButton(text='فنی مهندسی', callback_data='Engineering')
        f2 = KeyboardButton(text='علوم پایه', callback_data='Science')
        f3 = KeyboardButton(text='علوم انسانی', callback_data='Humanities')
        f4 = KeyboardButton(text='پزشکی', callback_data='Medical')
        f5 = KeyboardButton(text='هنر', callback_data='Art')

        reset = KeyboardButton(text='شروع مجدد')
        login = KeyboardButton(text='ورود')
        reg = KeyboardButton(text='ثبت نام')

        sharePhone = KeyboardButton(text='اشتراک شماره تلفن', request_contact=True)
        notShare = KeyboardButton(text='سیکتیر')
        finishKey = KeyboardButton(text='ثبت نهایی')
        self.sharePhoneKeys = [[sharePhone,notShare],[reset]]
        self.finish = [[finishKey],[reset]]

        self.fieldKeys = [[f1, f2], [f3, f4], [f5],[reset]]
        self.keyboard = [[key1, key2],[reset]]

        self.userInfo = {
            'name': "",
            'age': "",
            'sex': "",
            'field': "",
            'phone': ""
        }

    def register(self, msg, content_type):


        if content_type == "contact":

            self.userInfo['phone'] = msg['contact']['phone_number']
            self._msgContent = "برای تکمیل ثبت نام \"ثبت نهایی\" را انتخاب کنید"
            reply = ReplyKeyboardMarkup(keyboard=self.finish, one_time_keyboard=True)
            self.sender.sendMessage(self._msgContent,reply_markup=reply)

            self._subState = 'endRegister'
            return "register"

        elif msg['text'] == "/start":

            self._subState = self._subState

        elif msg['text'] == "شروع مجدد":

            self._msgContent = "برای شروع مجدد /start را بزنید"
            self.sender.sendMessage(self._msgContent)


            self._subState = "start"

            return "start"

        elif self._subState == "start":
            # self.sender.sendMessage("شما هنوز ثبت نام نکرده اید لطفا نام خود را وارد کنید")
            self._msgContent = " لطفا نام کاربری خود را وارد کنید"

            self.sender.sendMessage(self._msgContent)
            self._subState = "enterName"
            return "register"


        elif self._subState == "enterName":

            self.userInfo['name'] = msg['text']
            self._msgContent = "لطفا سن خود را وارد کنید"
            self.sender.sendMessage(self._msgContent)
            self._subState = "enterAge"
            return "register"

        elif self._subState == "enterAge":

            a = int(msg['text'])
            self.userInfo['age'] = a

            self._msgContent = "لطفا جنسیت خود را انتخاب کنید"
            reply = ReplyKeyboardMarkup(keyboard=self.keyboard, one_time_keyboard=True)
            self.sender.sendMessage(self._msgContent, reply_markup=reply)
            self._subState = "enterSex"
            return "register"

        elif self._subState == "enterSex":

            self.userInfo['sex'] = msg['text']
            self._msgContent = "لطفا گروه تحصیلی خود را انتخاب کنید"
            reply = ReplyKeyboardMarkup(keyboard=self.fieldKeys, one_time_keyboard=True)
            self.sender.sendMessage(self._msgContent, reply_markup=reply)
            self._subState = "enterField"
            return "register"

        elif self._subState == "enterField":

            self.userInfo['field'] = msg['text']

            self._msgContent = "در صورت تمایل شماره تلفن خود را با ما به اشتراک بگذارید"
            reply = ReplyKeyboardMarkup(keyboard=self.sharePhoneKeys, one_time_keyboard=True)
            self.sender.sendMessage(self._msgContent, reply_markup=reply)

            self._subState = "endRegister"

            return "register"

        elif self._subState == "endRegister":

            self._msgContent = "ثبت نام شما با موفقیت انجام شد"



            query = "INSERT INTO users(name,age, field, sex,phone) " \
                    "VALUES(%(name)s,%(age)s,%(field)s,%(sex)s,%(phone)s)"

            self.cursor.execute(query, self.userInfo)

            self.cnx.commit()

            self.sender.sendMessage(self._msgContent)

            self._subState = "endRegistration"
            return "loggedIn"


        # elif self._subState == "endRegistration":
        #
        #     self._msgContent = "سلام {} عزیز اطلاعات شما به صورت زیر است\n"
        #     self.lastid = self.cursor.lastrowid
        #


        print("subState = "+self._subState)


#-----------------ignored code------------------#


# query1 = ("SELECT * FROM users"
#           "WHERE id IS %s")



# print(self.lastid)
#
# # self.cursor.execute(query1 , self.lastid)
#
# for name in self.cursor:
#     print(name)

#####################

# query = ("INSERT INTO users"
#          "(name , age , field , sex)"
#          "VALUES(%s , %s, %s, %s)")
#


        # query = ("SELECT name FROM users")
        # DBHelper.executeQuery(query , self.cursor)
        # for userName in self.cursor:
        #     print(userName[0])

        # elif self._subState == "enterName":
        #     self._msgContent = "لطفا سن خود را وارد کنید"
        #     self.sender.sendMessage(self._msgContent)
        #     self._subState = "enterAge"