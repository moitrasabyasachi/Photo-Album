from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
import mysql.connector as sql
import db
from kivymd.toast import toast


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    pass


class ChangePasswordScreen(Screen):

    def on_enter(self, *args):
        self.ids.box_layout.clear_widgets()

        self.textfield1 = MDTextField(hint_text="Current Password", password=True, icon_right="key-variant",
                                      pos_hint={"center_x": 0.5}, size_hint_x=None, width=200)
        self.textfield2 = MDTextField(hint_text="New Password", password=True, icon_right="key-variant",
                                      pos_hint={"center_x": 0.5}, size_hint_x=None, width=200)
        self.textfield3 = MDTextField(hint_text="Confirm New Password", password=True, icon_right="key-variant",
                                      pos_hint={"center_x": 0.5}, size_hint_x=None, width=200)

        self.ids.box_layout.add_widget(MDLabel(text="Change Password", halign="center", font_style="H5"))
        self.ids.box_layout.add_widget(self.textfield1)
        self.ids.box_layout.add_widget(self.textfield2)
        self.ids.box_layout.add_widget(self.textfield3)
        self.ids.box_layout.add_widget(
            MDRaisedButton(text="Change Password", pos_hint={"center_x": 0.5}, on_release=self.change_password))

    def change_password(self, obj):
        current_pwd = self.textfield1.text
        new_pwd = self.textfield2.text
        confirm_new_pwd = self.textfield3.text
        if current_pwd == '' or new_pwd == '' or confirm_new_pwd == '':
            msg = "Empty entry"
            self.show_toast(msg)
        else:
            conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
            cur = conn.cursor()

            # current password
            uname = self.ids.label2.text[1:]
            query = "SELECT * FROM user WHERE uname = %s"
            val = (uname,)
            cur.execute(query, val)
            results = cur.fetchall()
            for row in results:
                pwd = row[4]
            if current_pwd == pwd:
                if new_pwd == confirm_new_pwd:
                    if new_pwd == current_pwd:
                        msg = "New Password and Current Password must be different"
                        self.show_toast(msg)
                    else:
                        # change password
                        query = "UPDATE user SET pwd = %s WHERE uname = %s"
                        val = (new_pwd, uname)
                        cur.execute(query, val)
                        conn.commit()
                        if cur.rowcount >= 1:
                            msg = "Password changed. Login with new password"
                            self.show_toast(msg)

                            conn.close()

                            self.index_screen()
                        else:
                            msg = "Password updation failed"
                            self.show_toast(msg)
                else:
                    msg = "New Password and Confirm New Password must be same"
                    self.show_toast(msg)
            else:
                msg = "Not the Current Password"
                self.show_toast(msg)

            conn.close()

    def clear_all(self):
        self.textfield1.text = ''
        self.textfield2.text = ''
        self.textfield3.text = ''

    def close_dialog(self, obj):
        self.clear_all()
        self.dialog.dismiss()

    def show_toast(self, msg):
        self.clear_all()
        toast(msg)

    def index_screen(self):
        self.manager.current = "index"
        self.manager.get_screen("index").ids.tab1textfield2.text = ''

    def home_screen(self):
        fname = self.ids.label1.text
        uname = self.ids.label2.text
        self.ids.nav_drawer.set_state("close")
        self.manager.current = "home"
        self.manager.get_screen("home").ids.label1.text = fname.title()
        self.manager.get_screen("home").ids.label2.text = '@' + uname[1:]

    def edit_profile_screen(self):
        fname = self.ids.label1.text
        uname = self.ids.label2.text
        self.ids.nav_drawer.set_state("close")
        self.manager.current = "edit_profile"
        self.manager.get_screen("edit_profile").ids.label1.text = fname.title()
        self.manager.get_screen("edit_profile").ids.label2.text = '@' + uname[1:]
