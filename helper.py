screen_helper = """
#: import sm kivy.uix.screenmanager
ScreenManager:
    transition: sm.NoTransition()
    IndexScreen:
    HomeScreen:
    CreateAlbumScreen:
    PhotoGalleryScreen:
    EditAlbumScreen
    FileChooserScreen
    EditProfileScreen
    ChangePasswordScreen:
            
<IndexScreen>:
    name: "index"    
    BoxLayout:
        orientation: "vertical"        
        MDToolbar:
            id: toolbar                                     
            anchor_title: "center"        
        MDTabs:            
            tab_hint_x: True
            on_tab_switch: root.clear_all()                            
            Tab:                
                title: "Sign In"                
                MDLabel:
                    text: "Log In"
                    halign: "center"
                    pos_hint: {"center_y": 0.8}                        
                    font_style: "H5"                
                MDTextFieldRound:
                    id: tab1textfield1                                        
                    hint_text: "Username"                    
                    icon_left: "account"                                         
                    pos_hint: {"center_x": 0.5, "center_y": 0.7}
                    size_hint: None, None
                    width: 200                
                MDTextFieldRound:
                    id: tab1textfield2                                      
                    hint_text: "Password"                    
                    password: True
                    icon_left: "key-variant"                                                             
                    pos_hint: {"center_x": 0.5, "center_y": 0.6}
                    size_hint: None, None
                    width: 200              
                MDFillRoundFlatButton:
                    text: "Sign In"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    on_release: root.user_signin()       
            Tab:             
                title: "Sign Up"                                
                MDLabel:
                    text: "Register"
                    halign: "center"
                    pos_hint: {"center_y": 0.8}                        
                    font_style: "H5"       
                MDTextFieldRound:
                    id: tab2textfield1                                       
                    hint_text: "Full Name"                    
                    icon_left: "account"                                         
                    pos_hint: {"center_x": 0.5, "center_y": 0.7}
                    size_hint: None, None
                    width: 200                    
                MDTextFieldRound:
                    id: tab2textfield2                                       
                    hint_text: "Username"                    
                    icon_left: "account"                                         
                    pos_hint: {"center_x": 0.5, "center_y": 0.6}
                    size_hint: None, None
                    width: 200                
                MDTextFieldRound:
                    id: tab2textfield3                                       
                    hint_text: "Password"                    
                    password: True
                    icon_left: "key-variant"                                                             
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    size_hint: None, None
                    width: 200            
                MDTextFieldRound:
                    id: tab2textfield4                                      
                    hint_text: "Confirm Password"                    
                    password: True
                    icon_left: "key-variant"                                                             
                    pos_hint: {"center_x": 0.5, "center_y": 0.4}
                    size_hint: None, None
                    width: 200                
                MDFillRoundFlatButton:
                    text: "Sign Up"
                    pos_hint: {"center_x": 0.5, "center_y": 0.3}     
                    on_release: root.user_signup()
                    
<HomeScreen>:
    name: "home"    
    MDNavigationLayout:        
        ScreenManager:            
            Screen:                
                BoxLayout:
                    orientation: "vertical"                    
                    MDToolbar:
                        id: toolbar                        
                        anchor_title: "center"                        
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                        right_action_items: [["blank"]]                  
                    BoxLayout:
                        id: box_layout
                        orientation: "vertical"                                                                                                                                                                              
        MDNavigationDrawer:
            id: nav_drawer            
            ContentNavigationDrawer:
                orientation: "vertical"
                padding: "8dp"
                spacing: "8dp"                
                AnchorLayout:
                    anchor_x: "center"
                    size_hint_y: None
                    height: avatar.height            
                    Image:
                        id: avatar
                        size_hint: None, None
                        size: "56dp", "56dp"
                        source: "data/img/blank-profile-picture.png"                
                MDLabel:
                    id: label1                    
                    font_style: "Subtitle1"
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1]                
                MDLabel:
                    id: label2
                    font_style: "Caption"
                    halign: "center"                    
                    size_hint_y: None                    
                    height: self.texture_size[1]                
                ScrollView:                
                    DrawerList:                                                
                        MDList:                            
                            OneLineIconListItem:                                
                                text: "My Albums" 
                                on_release: nav_drawer.set_state("close")                                                 
                                IconLeftWidget:
                                    icon: "folder-image"                                                              
                            OneLineIconListItem:
                                text: "Edit Profile"  
                                on_release: root.edit_profile_screen()                          
                                IconLeftWidget:
                                    icon: "account-edit"                                
                            OneLineIconListItem:
                                text: "Change Password"
                                on_release: root.change_password_screen()                            
                                IconLeftWidget:
                                    icon: "shield-edit"                           
                            OneLineIconListItem:
                                text: "Logout"                            
                                on_release: root.user_signout()
                                IconLeftWidget:
                                    icon: "logout"
                                    
<CreateAlbumScreen>:
    name: "create_album"    
    BoxLayout:        
        orientation: "vertical"        
        MDToolbar:             
            title: "Create Album"      
            left_action_items: [["close", lambda x: root.home_screen()]]
        BoxLayout:
            id: box_layout
            orientation: "vertical" 
        Widget:

<PhotoGalleryScreen>:
    name: "photo_gallery"    
    BoxLayout:
        orientation: "vertical"        
        MDToolbar:
            id: toolbar                                     
            anchor_title: "center"
            left_action_items: [["arrow-left", lambda x: root.home_screen()]]
            right_action_items: [["dots-vertical", lambda x: root.dropdown_menu_album()]]        
        BoxLayout:            
            orientation: "vertical" 
            ScrollView:
                MDGridLayout:
                    id: md_grid_layout
                    cols: 3
                    row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
                    row_force_default: True
                    adaptive_height: True
                    padding: dp(4), dp(4)
                    spacing: dp(4)
        MDBottomAppBar:
            MDToolbar:                
                icon: "image-plus"
                type: "bottom"
                on_action_button: root.add_photo()
                
<EditAlbumScreen>:
    name: "edit_album"    
    BoxLayout:        
        orientation: "vertical"        
        MDToolbar:             
            title: "Edit Album"      
            left_action_items: [["close", lambda x: root.photo_gallery_screen()]]
        BoxLayout:
            id: box_layout
            orientation: "vertical" 
        Widget:

<FileChooserScreen>:
    name: "file_chooser"    
    BoxLayout:        
        orientation: "vertical"        
        MDToolbar:
            id: toolbar 
            title: "Choose Photo(s)"      
            left_action_items: [["close", lambda x: root.photo_gallery_screen()]]               
        BoxLayout:    
            id: box_layout    
            orientation: "vertical"                                                                                                        
                                    
<EditProfileScreen>:
    name: "edit_profile"    
    MDNavigationLayout:        
        ScreenManager:            
            Screen:                
                BoxLayout:
                    orientation: "vertical"                    
                    MDToolbar:
                        id: toolbar                        
                        anchor_title: "center"                        
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                        right_action_items: [["blank"]] 
                    BoxLayout:
                        id: box_layout
                        orientation: "vertical" 
                    Widget:                                                                                                                                                                                                                          
        MDNavigationDrawer:
            id: nav_drawer            
            ContentNavigationDrawer:
                orientation: "vertical"
                padding: "8dp"
                spacing: "8dp"                
                AnchorLayout:
                    anchor_x: "center"
                    size_hint_y: None
                    height: avatar.height            
                    Image:
                        id: avatar
                        size_hint: None, None
                        size: "56dp", "56dp"
                        source: "data/img/blank-profile-picture.png"                
                MDLabel:
                    id: label1                    
                    font_style: "Subtitle1"
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1]                
                MDLabel:
                    id: label2
                    font_style: "Caption"
                    halign: "center"                    
                    size_hint_y: None                    
                    height: self.texture_size[1]                
                ScrollView:                
                    DrawerList:                                                
                        MDList:                            
                            OneLineIconListItem:                                
                                text: "My Albums"
                                on_release: root.home_screen()                                                  
                                IconLeftWidget:
                                    icon: "folder-image"                                                              
                            OneLineIconListItem:
                                text: "Edit Profile"  
                                on_release: nav_drawer.set_state("close")                          
                                IconLeftWidget:
                                    icon: "account-edit"                                
                            OneLineIconListItem:
                                text: "Change Password" 
                                on_release: root.change_password_screen()                                                  
                                IconLeftWidget:
                                    icon: "shield-edit"                           
                            OneLineIconListItem:
                                text: "Logout"                            
                                on_release: root.user_signout()
                                IconLeftWidget:
                                    icon: "logout"

<ChangePasswordScreen>:
    name: "change_password"    
    MDNavigationLayout:        
        ScreenManager:            
            Screen:                
                BoxLayout:
                    orientation: "vertical"                    
                    MDToolbar:
                        id: toolbar                        
                        anchor_title: "center"                        
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
                        right_action_items: [["blank"]] 
                    BoxLayout:
                        id: box_layout
                        orientation: "vertical" 
                    Widget:                                                                                                                                                                                                                          
        MDNavigationDrawer:
            id: nav_drawer            
            ContentNavigationDrawer:
                orientation: "vertical"
                padding: "8dp"
                spacing: "8dp"                
                AnchorLayout:
                    anchor_x: "center"
                    size_hint_y: None
                    height: avatar.height            
                    Image:
                        id: avatar
                        size_hint: None, None
                        size: "56dp", "56dp"
                        source: "data/img/blank-profile-picture.png"                
                MDLabel:
                    id: label1                    
                    font_style: "Subtitle1"
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1]                
                MDLabel:
                    id: label2
                    font_style: "Caption"
                    halign: "center"                    
                    size_hint_y: None                    
                    height: self.texture_size[1]                
                ScrollView:                
                    DrawerList:                                                
                        MDList:                            
                            OneLineIconListItem:                                
                                text: "My Albums"
                                on_release: root.home_screen()                                                  
                                IconLeftWidget:
                                    icon: "folder-image"                                                              
                            OneLineIconListItem:
                                text: "Edit Profile"  
                                on_release: root.edit_profile_screen()                          
                                IconLeftWidget:
                                    icon: "account-edit"                                
                            OneLineIconListItem:
                                text: "Change Password" 
                                on_release: nav_drawer.set_state("close")                                                           
                                IconLeftWidget:
                                    icon: "shield-edit"                           
                            OneLineIconListItem:
                                text: "Logout"                            
                                on_release: root.user_signout()
                                IconLeftWidget:
                                    icon: "logout"
"""
