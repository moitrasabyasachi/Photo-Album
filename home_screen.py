from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList, IconLeftWidget, OneLineIconListItem, ImageLeftWidget, TwoLineAvatarListItem
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
import mysql.connector as sql
import db


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    pass


class HomeScreen(Screen):

    def on_enter(self, *args):
        conn = sql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
        cur = conn.cursor()

        # user-id
        uname = self.ids.label2.text[1:]
        query = "SELECT * FROM user WHERE uname = %s"
        val = (uname,)
        cur.execute(query, val)
        results = cur.fetchall()
        for row in results:
            uid = row[1]
        self.userid = uid

        # albums
        self.ids.box_layout.clear_widgets()
        scroll = ScrollView()
        list_view = MDList()
        # create album
        icons = IconLeftWidget(icon="folder-plus")
        items = OneLineIconListItem(text="Create Album", on_release=self.create_album_screen)
        items.add_widget(icons)
        list_view.add_widget(items)
        # view albums
        query = "SELECT * FROM album WHERE uid = %s ORDER BY slno DESC"
        val = (uid,)
        cur.execute(query, val)
        results = cur.fetchall()
        if len(results) > 0:
            for row in results:
                aid = row[1]
                # no. of photos
                query2 = "SELECT * FROM photo WHERE aid = %s"
                val2 = (aid,)
                cur.execute(query2, val2)
                results2 = cur.fetchall()
                photo_num = len(results2)
                aname = row[2]
                pname = "photos/" + aid + "P1.jpg"
                images = ImageLeftWidget(source=pname)
                items = TwoLineAvatarListItem(text=aname, secondary_text=str(photo_num) + " photo(s)",
                                              on_release=self.photo_gallery_screen)
                items.add_widget(images)
                list_view.add_widget(items)
        else:
            pass
        scroll.add_widget(list_view)
        self.ids.box_layout.add_widget(scroll)

        conn.close()

    def create_album_screen(self, obj):
        self.manager.current = "create_album"

    def photo_gallery_screen(self, obj):
        if obj.text == "Create Album":
            pass
        else:
            self.manager.current = "photo_gallery"
            self.manager.get_screen("photo_gallery").ids.toolbar.title = obj.text

    def edit_profile_screen(self):
        fname = self.ids.label1.text
        uname = self.ids.label2.text
        self.ids.nav_drawer.set_state("close")
        self.manager.current = "edit_profile"
        self.manager.get_screen("edit_profile").ids.label1.text = fname.title()
        self.manager.get_screen("edit_profile").ids.label2.text = '@' + uname[1:]

    def change_password_screen(self):
        fname = self.ids.label1.text
        uname = self.ids.label2.text
        self.ids.nav_drawer.set_state("close")
        self.manager.current = "change_password"
        self.manager.get_screen("change_password").ids.label1.text = fname.title()
        self.manager.get_screen("change_password").ids.label2.text = '@' + uname[1:]

    def user_signout(self):
        self.manager.current = "index"
        self.manager.get_screen("index").ids.tab1textfield2.text = ''
