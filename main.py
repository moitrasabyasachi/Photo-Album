from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from index_screen import IndexScreen
from home_screen import HomeScreen
from create_album_screen import CreateAlbumScreen
from photo_gallery_screen import PhotoGalleryScreen
from file_chooser_screen import FileChooserScreen
from view_photo_screen import ViewPhotoScreen
from edit_album_screen import EditAlbumScreen
from edit_profile_screen import EditProfileScreen
from change_password_screen import ChangePasswordScreen
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import fonts
from kivy.lang import Builder
from helper import screen_helper

Window.size = (320, 568)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(IndexScreen(name="index"))
sm.add_widget(HomeScreen(name="home"))
sm.add_widget(CreateAlbumScreen(name="create_album"))
sm.add_widget(PhotoGalleryScreen(name="photo_gallery"))
sm.add_widget(FileChooserScreen(name="file_chooser"))
sm.add_widget(ViewPhotoScreen(name="view_photo"))
sm.add_widget(EditAlbumScreen(name="edit_album"))
sm.add_widget(EditProfileScreen(name="edit_profile"))
sm.add_widget(ChangePasswordScreen(name="change_password"))


class PhotoAlbumApp(MDApp):

    @property
    def storage(self):
        return self.user_data_dir

    def on_start(self):
        # index screen
        self.root.get_screen("index").ids.toolbar.ids.label_title.text = \
            f"[size=25sp][font={fonts[-1]['fn_regular']}]{md_icons['camera-image']}[/size][/font] " \
            f"PHOTO ALBUM"
        self.root.get_screen("index").ids.toolbar.ids.label_title.font_name = 'data/font/FREESCPT.ttf'
        self.root.get_screen("index").ids.toolbar.ids.label_title.font_size = '25sp'
        self.root.get_screen("index").ids.toolbar.ids.label_title.bold = True
        # home screen
        self.root.get_screen("home").ids.toolbar.ids.label_title.text = \
            f"[size=25sp][font={fonts[-1]['fn_regular']}]{md_icons['camera-image']}[/size][/font] " \
            f"PHOTO ALBUM"
        self.root.get_screen("home").ids.toolbar.ids.label_title.font_name = 'data/font/FREESCPT.ttf'
        self.root.get_screen("home").ids.toolbar.ids.label_title.font_size = '25sp'
        self.root.get_screen("home").ids.toolbar.ids.label_title.bold = True
        # edit profile screen
        self.root.get_screen("edit_profile").ids.toolbar.ids.label_title.text = \
            f"[size=25sp][font={fonts[-1]['fn_regular']}]{md_icons['camera-image']}[/size][/font] " \
            f"PHOTO ALBUM"
        self.root.get_screen("edit_profile").ids.toolbar.ids.label_title.font_name = 'data/font/FREESCPT.ttf'
        self.root.get_screen("edit_profile").ids.toolbar.ids.label_title.font_size = '25sp'
        self.root.get_screen("edit_profile").ids.toolbar.ids.label_title.bold = True
        # change password screen
        self.root.get_screen("change_password").ids.toolbar.ids.label_title.text = \
            f"[size=25sp][font={fonts[-1]['fn_regular']}]{md_icons['camera-image']}[/size][/font] " \
            f"PHOTO ALBUM"
        self.root.get_screen("change_password").ids.toolbar.ids.label_title.font_name = 'data/font/FREESCPT.ttf'
        self.root.get_screen("change_password").ids.toolbar.ids.label_title.font_size = '25sp'
        self.root.get_screen("change_password").ids.toolbar.ids.label_title.bold = True

    def build(self):
        screen = Builder.load_string(screen_helper)

        return screen


PhotoAlbumApp().run()
