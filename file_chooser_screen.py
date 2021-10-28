from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Rectangle
import mysql.connector as sql
import db
import os
from kivymd.toast import toast


class FileChooserScreen(Screen):

    def on_enter(self, *args):
        self.ids.toolbar.right_action_items = [["blank"]]
        self.ids.box_layout.clear_widgets()
        filechooser = FileChooserIconView(multiselect=True)
        with filechooser.canvas.before:
            Color(0, 0, 0)
            Rectangle(pos=self.ids.box_layout.pos, size=self.ids.box_layout.size)
        filechooser.bind(selection=self.select_photo)
        self.ids.box_layout.add_widget(filechooser)

    def select_photo(self, obj, selection):
        if len(selection) > 0:
            ext = ['jpg', 'jpeg']
            for i in range(len(selection)):
                path = str(selection[i])
                filename = path.split('\\')[-1]
                filename_ext = filename.split('.')[-1]
                if filename_ext.lower() in ext:
                    self.ids.toolbar.right_action_items = [["upload", self.upload_photo]]
                else:
                    self.ids.toolbar.right_action_items = [["blank"]]
            self.paths = selection
        else:
            self.ids.toolbar.right_action_items = [["blank"]]

    def upload_photo(self, obj):
        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()

        # auto photo-id generation
        aid = self.manager.get_screen('photo_gallery').aid
        query = "SELECT * FROM photo WHERE aid = %s ORDER BY slno ASC"
        val = (aid,)
        cur.execute(query, val)
        results = cur.fetchall()
        if len(results) > 0:
            for row in results:
                slno = row[0]
        else:
            slno = 0

        slnos = []
        pids = []
        pnames = []
        aids = []
        for i in range(len(self.paths)):
            slno = slno + 1
            pid = aid + 'P' + str(slno)
            pname = pid + '.jpg'
            slnos.append(slno)
            pids.append(pid)
            pnames.append(pname)
            aids.append(aid)

        # upload photo(s)
        dir = 'photos'
        for i in range(len(self.paths)):
            query = "INSERT INTO photo (slno, pid, pname, aid) VALUES (%s, %s, %s, %s)"
            val = (slnos[i], pids[i], pnames[i], aids[i])
            cur.execute(query, val)
            conn.commit()
            if cur.rowcount == 1:
                src = str(self.paths[i])
                dest = os.path.join(dir, pnames[i])
                with open(src, "rb") as f:
                    with open(dest, 'wb') as f1:
                        for line in f:
                            f1.write(line)
            else:
                pass

        msg = "Photo uploaded"
        self.show_toast(msg)

        conn.close()

        self.photo_gallery_screen()

    def show_toast(self, msg):
        toast(msg)

    def photo_gallery_screen(self):
        self.manager.current = "photo_gallery"
