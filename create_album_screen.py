from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
import mysql.connector as sql
import db


class CreateAlbumScreen(Screen):

    def on_enter(self, *args):
        self.ids.box_layout.clear_widgets()

        self.textfield1 = MDTextField(hint_text="Album Name", icon_right="folder",
                                      pos_hint={"center_x": 0.5}, size_hint_x=None, width=200)

        self.ids.box_layout.add_widget(self.textfield1)
        self.ids.box_layout.add_widget(
            MDRaisedButton(text="Create Album", pos_hint={"center_x": 0.5}, on_release=self.create_album))

    def create_album(self, obj):
        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()

        # auto album-id generation
        uid = self.manager.get_screen('home').userid
        query = "SELECT * FROM album WHERE uid = %s ORDER BY slno ASC"
        val = (uid,)
        cur.execute(query, val)
        results = cur.fetchall()
        if len(results) > 0:
            for row in results:
                slno = row[0]
            slno = slno + 1
        else:
            slno = 1

        # create album
        aid = uid + 'A' + str(slno)
        aname = self.textfield1.text
        if aname == '':
            aname = "Untitled"
        else:
            aname = aname
        query = "INSERT INTO album (slno, aid, aname, uid) VALUES (%s, %s, %s, %s)"
        val = (slno, aid, aname, uid)
        cur.execute(query, val)
        conn.commit()
        if cur.rowcount == 1:
            msg = "Album created"
            self.show_toast(msg)
        else:
            msg = "Album creation failed"
            self.show_toast(msg)

        conn.close()

        self.home_screen()

    def show_toast(self, msg):
        toast(msg)

    def home_screen(self):
        self.manager.current = "home"
