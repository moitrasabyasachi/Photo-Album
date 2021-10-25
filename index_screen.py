from kivymd.toast import toast
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import Screen
import mysql.connector as sql
import db


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    pass


class IndexScreen(Screen):

    def user_signin(self):
        uname = self.ids.tab1textfield1.text
        pwd = self.ids.tab1textfield2.text
        if uname == '' or pwd == '':
            msg = "Empty credentials"
            self.show_toast(msg)
        else:
            conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
            cur = conn.cursor()

            # user authentication
            query = "SELECT * FROM user WHERE uname = %s AND pwd = %s"
            val = (uname, pwd)
            cur.execute(query, val)
            results = cur.fetchall()
            if len(results) > 0:
                for row in results:
                    fname = row[2]

                conn.close()

                self.manager.current = "home"
                self.manager.get_screen("home").ids.label1.text = fname.title()
                self.manager.get_screen("home").ids.label2.text = '@' + uname
            else:
                msg = "Invalid credentials"
                self.show_toast(msg)

                conn.close()

    def user_signup(self):
        fname = self.ids.tab2textfield1.text
        uname = self.ids.tab2textfield2.text
        pwd = self.ids.tab2textfield3.text
        confirm_pwd = self.ids.tab2textfield4.text
        if fname == '' or uname == '' or pwd == '' or confirm_pwd == '':
            msg = "Empty entry"
            self.show_toast(msg)
        else:
            if pwd != confirm_pwd:
                msg = "Password & Confirm pwd must be same"
                self.show_toast(msg)
            else:
                conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
                cur = conn.cursor()

                # auto user-id generation
                query = "SELECT * FROM user ORDER BY slno ASC"
                cur.execute(query)
                results = cur.fetchall()
                if len(results) > 0:
                    for row in results:
                        slno = row[0]
                    slno = slno + 1
                else:
                    slno = 1
                uid = 'U' + str(slno)

                # registration
                query = "INSERT INTO user (slno, uid, fname, uname, pwd) VALUES (%s, %s, %s, %s, %s)"
                val = (slno, uid, fname, uname, pwd)
                cur.execute(query, val)
                conn.commit()
                if cur.rowcount == 1:
                    msg = "Account created"
                    self.show_toast(msg)
                else:
                    msg = "Account creation failed"
                    self.show_toast(msg)

                conn.close()

    def clear_all(self):
        self.ids.tab1textfield1.text = ''
        self.ids.tab1textfield2.text = ''
        self.ids.tab2textfield1.text = ''
        self.ids.tab2textfield2.text = ''
        self.ids.tab2textfield3.text = ''
        self.ids.tab2textfield4.text = ''

    def show_toast(self, msg):
        self.clear_all()
        toast(msg)
