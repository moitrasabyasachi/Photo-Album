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


class EditProfileScreen(Screen):

    def on_enter(self, *args):
        self.ids.box_layout.clear_widgets()

        self.textfield1 = MDTextField(hint_text="Full Name", icon_right="account",
                                      pos_hint={"center_x": 0.5}, size_hint_x=None, width=200)
        self.textfield2 = MDTextField(hint_text="Username", readonly=True, icon_right="account",
                                      pos_hint={"center_x": 0.5}, size_hint_x=None, width=200)

        self.ids.box_layout.add_widget(MDLabel(text="Edit Profile", halign="center", font_style="H5"))
        self.ids.box_layout.add_widget(self.textfield1)
        self.ids.box_layout.add_widget(self.textfield2)
        self.ids.box_layout.add_widget(
            MDRaisedButton(text="Update Profile", pos_hint={"center_x": 0.5}, on_release=self.update_profile))
        self.ids.box_layout.add_widget(
            MDTextField(hint_text='', pos_hint={"center_x": 0.5}, size_hint_x=None, width=200, opacity=0))

        self.textfield1.text = self.ids.label1.text
        self.textfield2.text = self.ids.label2.text[1:]

    def update_profile(self, obj):
        new_fname = self.textfield1.text
        uname = self.textfield2.text
        if new_fname == '':
            msg = "Empty entry"
            self.show_toast(msg)
        else:
            conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
            cur = conn.cursor()
            query = "UPDATE user SET fname = %s WHERE uname = %s"
            val = (new_fname, uname)
            cur.execute(query, val)
            conn.commit()
            if cur.rowcount == 1:
                msg = "Profile updated"
                self.show_toast(msg)
            else:
                msg = "Profile updation failed"
                self.show_toast(msg)

            conn.close()

            self.ids.label1.text = new_fname.title()
            self.textfield1.text = self.ids.label1.text

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_toast(self, msg):
        toast(msg)

    def user_signout(self):
        self.manager.current = "index"
        self.manager.get_screen("index").ids.tab1textfield2.text = ''

    def home_screen(self):
        fname = self.ids.label1.text
        uname = self.ids.label2.text
        self.ids.nav_drawer.set_state("close")
        self.manager.current = "home"
        self.manager.get_screen("home").ids.label1.text = fname.title()
        self.manager.get_screen("home").ids.label2.text = '@' + uname[1:]

    def change_password_screen(self):
        fname = self.ids.label1.text
        uname = self.ids.label2.text
        self.ids.nav_drawer.set_state("close")
        self.manager.current = "change_password"
        self.manager.get_screen("change_password").ids.label1.text = fname.title()
        self.manager.get_screen("change_password").ids.label2.text = '@' + uname[1:]
