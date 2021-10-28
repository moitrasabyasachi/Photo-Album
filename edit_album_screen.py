from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
import mysql.connector as sql
import db


class EditAlbumScreen(Screen):

    def on_enter(self, *args):
        self.ids.box_layout.clear_widgets()

        self.textfield1 = MDTextField(hint_text="Album Name", icon_right="folder",
                                      pos_hint={"center_x": 0.5}, size_hint_x=None, width=200)

        self.ids.box_layout.add_widget(self.textfield1)
        self.ids.box_layout.add_widget(
            MDRaisedButton(text="Edit Album", pos_hint={"center_x": 0.5}, on_release=self.edit_album))

        self.textfield1.text = self.manager.get_screen("photo_gallery").ids.toolbar.title

    def edit_album(self, obj):
        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()
        new_aname = self.textfield1.text
        aid = self.manager.get_screen('photo_gallery').aid
        query = "UPDATE album SET aname = %s WHERE aid = %s"
        val = (new_aname, aid)
        cur.execute(query, val)
        conn.commit()
        if cur.rowcount == 1:
            msg = "Album updated"
            self.show_toast(msg)
        else:
            msg = "Album updation failed"
            self.show_toast(msg)

        conn.close()

        self.manager.get_screen("photo_gallery").ids.toolbar.title = new_aname
        self.photo_gallery_screen()

    def show_toast(self, msg):
        toast(msg)

    def photo_gallery_screen(self):
        self.manager.current = "photo_gallery"
