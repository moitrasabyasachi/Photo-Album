from kivy.uix.screenmanager import Screen
import mysql.connector as sql
import db
from kivymd.uix.imagelist import SmartTileWithLabel
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
import os
from kivymd.toast import toast


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
                                            on_release=self.view_photo_screen)
                self.ids.md_grid_layout.add_widget(images)
                
            if len(results) < self.ids.md_grid_layout.cols:
                diff = self.ids.md_grid_layout.cols - len(results)
                for i in range(diff):
                    images = SmartTileWithLabel(source='', box_color=(0, 0, 0, 0))
                    self.ids.md_grid_layout.add_widget(images)
        else:
            pass

        conn.close()

    def dropdown_menu(self):
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
        else:
            pass

        self.menu.dismiss()

    def add_photo(self):
        self.file_chooser_screen()

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

    def view_photo_screen(self, obj):
        path = obj.source
        pname = path.split('/')[-1]
        pid = pname.split('.')[0]
        self.slno = pid.split('P')[-1]

        self.manager.current = "view_photo"
        self.manager.get_screen("view_photo").ids.toolbar.title = self.ids.toolbar.title
