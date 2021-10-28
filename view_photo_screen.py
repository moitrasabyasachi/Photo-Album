from kivy.uix.screenmanager import Screen
import mysql.connector as sql
import db
from kivymd.uix.imagelist import SmartTileWithLabel
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
import os
import requests
from kivymd.toast import toast


class ViewPhotoScreen(Screen):

    def on_enter(self, *args):
        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()

        # photos
        self.ids.md_grid_layout.clear_widgets()
        # view photos
        aid = self.manager.get_screen('photo_gallery').aid
        slno = self.manager.get_screen('photo_gallery').slno
        query = "SELECT * FROM photo WHERE aid = %s AND slno <= %s ORDER BY slno ASC"
        val = (aid, slno)
        cur.execute(query, val)
        results = cur.fetchall()
        if len(results) > 0:
            for row in results:
                pname = row[2]
                images = SmartTileWithLabel(source="photos/" + pname, box_color=(0, 0, 0, 0),
                                            on_release=self.dropdown_menu)
                self.ids.md_grid_layout.add_widget(images)
        else:
            pass

        self.ids.scroll_view.scroll_to(images)

        query = "SELECT * FROM photo WHERE aid = %s AND slno > %s ORDER BY slno ASC"
        val = (aid, slno)
        cur.execute(query, val)
        results = cur.fetchall()
        if len(results) > 0:
            for row in results:
                pname = row[2]
                images = SmartTileWithLabel(source="photos/" + pname, box_color=(0, 0, 0, 0),
                                            on_release=self.dropdown_menu)
                self.ids.md_grid_layout.add_widget(images)
        else:
            pass

        conn.close()

    def dropdown_menu(self, obj):
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
        if x == "Save":
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

    def save_photo(self, y):
        # y = "https://github.com/HeaTTheatR/KivyMD-data/raw/master/gallery/previous.png"
        # save_dir = MDApp.get_running_app().storage
        save_dir = "C:\\Users\\MOITRA-L-2\\Desktop\\photoalbum"
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

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def show_toast(self, msg):
        toast(msg)

    def photo_gallery_screen(self):
        self.manager.current = "photo_gallery"
