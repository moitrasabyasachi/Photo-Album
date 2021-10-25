import os
import requests
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
import mysql.connector as sql
from kivymd.toast import toast
import db
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.menu import MDDropdownMenu


class PhotoGalleryScreen(Screen):

    def on_enter(self, *args):
        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()

        # album-id
        aname = self.ids.toolbar.title
        uid = self.manager.get_screen('home').userid
        query = "SELECT * FROM album WHERE aname = %s AND uid = %s"
        val = (aname, uid)
        cur.execute(query, val)
        results = cur.fetchall()
        for row in results:
            self.aid = row[1]

        # photos
        self.ids.md_grid_layout.clear_widgets()
        # view photos
        query = "SELECT * FROM photo WHERE aid = %s ORDER BY slno ASC"
        val = (self.aid,)
        cur.execute(query, val)
        results = cur.fetchall()
        if len(results) > 0:
            for row in results:
                pname = row[2]
                images = SmartTileWithLabel(source="photos/" + pname, box_color=(0, 0, 0, 0),
                                            on_release=self.dropdown_menu_photo)
                self.ids.md_grid_layout.add_widget(images)
        else:
            pass

        conn.close()

    def dropdown_menu_album(self):
        items_d = ['Edit Album', 'Delete Album']
        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}", y=self.aid: self.menu_callback(x, y),
            } for i in items_d
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.toolbar,
            items=menu_items,
            width_mult=4,
        )

        self.menu.open()

    def dropdown_menu_photo(self, obj):
        items_d = ['Save', 'Delete']
        menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "height": dp(40),
                "on_release": lambda x=f"{i}", y=obj.source: self.menu_callback(x, y),
            } for i in items_d
        ]
        self.menu = MDDropdownMenu(
            caller=obj,
            items=menu_items,
            width_mult=2,
        )

        self.menu.open()

    def menu_callback(self, x, y):
        if x == "Edit Album":
            self.edit_album_screen()
        elif x == "Delete Album":
            msg = "Delete album?"
            self.dialog = MDDialog(
                text=msg,
                buttons=[
                    MDFillRoundFlatButton(text="OK", on_release=self.delete_album),
                    MDFillRoundFlatButton(text="CANCEL", on_release=self.close_dialog)
                ]
            )
            self.dialog.open()
        elif x == "Save":
            self.save_photo(y)
        elif x == "Delete":
            pname = y.split('/')[-1]
            pid = pname.split('.')[0]

            msg = "Delete photo?"
            self.dialog = MDDialog(
                text=msg,
                buttons=[
                    MDFillRoundFlatButton(text="OK", on_release=lambda *args: self.delete_photo(pid, *args)),
                    MDFillRoundFlatButton(text="CANCEL", on_release=self.close_dialog)
                ]
            )
            self.dialog.open()
        else:
            pass

        self.menu.dismiss()

    def add_photo(self):
        self.file_chooser_screen()

    def save_photo(self, y):
        # y = "https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/previous.png"
        # save_dir = MDApp.get_running_app().storage
        save_dir = "C:\\Users\\MOITRA-D-1\\Desktop\\photoalbum"
        local_filename = y.split('/')[-1]
        local_file = os.path.join(save_dir, local_filename)
        # response = requests.get(y, stream=True)
        # with open(local_file, 'wb') as f:
        #     for chunk in response.iter_content(chunk_size=1024):
        #         if chunk:
        #             f.write(chunk)
        #             f.flush()

        with open(y, "rb") as f:
            with open(local_file, 'wb') as f1:
                for line in f:
                    f1.write(line)

        msg = "Photo saved at " + local_file
        self.show_toast(msg)

    def delete_photo(self, pid, *args):
        self.dialog.dismiss()

        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()
        query = "DELETE FROM photo WHERE pid = %s"
        val = (pid,)
        cur.execute(query, val)
        conn.commit()
        if cur.rowcount == 1:
            # remove file
            local_filename = pid + ".jpg"
            local_file = os.path.join("photos", local_filename)
            os.remove(local_file)
            msg = "Photo deleted"
            self.show_toast(msg)
        else:
            msg = "Photo deletion failed"
            self.show_toast(msg)

        conn.close()

        self.on_enter()

    def delete_album(self, obj):
        self.dialog.dismiss()

        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()

        # get photo-ids
        query = "SELECT * FROM photo WHERE aid = %s ORDER BY slno ASC"
        val = (self.aid,)
        cur.execute(query, val)
        results = cur.fetchall()
        pids = []
        if len(results) > 0:
            for row in results:
                pid = row[1]
                pids.append(pid)
        else:
            pass

        # delete album
        # delete all photos
        for i in range(len(pids)):
            query = "DELETE FROM photo WHERE pid = %s"
            val = (pids[i],)
            cur.execute(query, val)
            conn.commit()
            if cur.rowcount == 1:
                # remove file
                local_filename = pids[i] + ".jpg"
                local_file = os.path.join("photos", local_filename)
                os.remove(local_file)
            else:
                pass
        # delete album
        query = "DELETE FROM album WHERE aid = %s"
        val = (self.aid,)
        cur.execute(query, val)
        conn.commit()
        if cur.rowcount == 1:
            msg = "Album deleted"
            self.show_toast(msg)
        else:
            msg = "Album deletion failed"
            self.show_toast(msg)

        conn.close()

        self.home_screen()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_toast(self, msg):
        toast(msg)

    def home_screen(self):
        self.manager.current = "home"

    def edit_album_screen(self):
        self.manager.current = "edit_album"

    def file_chooser_screen(self):
        self.manager.current = "file_chooser"
