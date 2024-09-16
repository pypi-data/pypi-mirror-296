import customtkinter as ctk
import os, platform, json, customtkinter as ctk
from .Theme import theme
from typing import Callable, Literal
_platform = platform.system()
if _platform == "Windows":
    from winreg import *
    from ctypes import windll
# elif _platform == "Linux":
#     pass    #! to be implemented
# elif _platform == "Darwin":
#     pass    #! to be implemented

class Chest():
    def __init__(self):
        self.userAssetsDirectory = None
        self._on_theme_change_jobs = []
        self._OS: Literal["Windows", "Linux", "Darwin"] = _platform
        if self._OS == "Windows":
            self.scaleFactor = windll.shcore.GetScaleFactorForDevice(0) / 100
        else:   #! for linux and mac (to be implemented)
            self.scaleFactor = 1
            
    def _D__Setup_Chest(self, window, frame):
        from .Tab_Page_Frame import Frame
        self.Window = window
        self.Manager : Frame = frame
        self.PageParent = self.Manager.page_frame
        self.Current_Page = "Get it using the get_current_page() method"
        self.Displayed_Pages = self.Manager.pages_dict
        self.MainPages = self.Manager.mainpages_dict
        self.SubPages = self.Manager.subpages_dict
        self.userPagesDirectory = self.Manager.U_Pages_dir
        self.toolsFrame = self.Manager.apps_frame
        self.Dialog_Manager = self.Manager.dialog_widget

        self.thread_reload_var =  ctk.StringVar()
        self.thread_reload_var.trace_add("write", lambda *args: self.reload_page(self.thread_reload_var.get()))

    def get_current_page(self):
        """Returns the Displayed Page name

        Returns:
            str: Displayed Page name
        """
        return self.Manager.page_choise

    def Switch_Page(self, Target_Page: str):
        """Closes the current page and Shows the target page (Only for Global Pages)

        Args:
            Target_Page (str): Name of the target page "case sensitive"
        """
        self.Manager.page_switcher(Target_Page)

    def reload_page(self, name: str, args: tuple = ()):
        """Reloads the page to apply any saved changes made to the code of the page

        Args:
            name (str): Name of the page "case sensitive"
            args (tuple): Arguments to be passed to the page
        """
        self.Manager.reload_page(name, args)

    def Store_a_Page(self, Target_Page: str, Switch: bool =True):
        """Constructs a new main page, so that it is ready to be opened at any moment

        Args:
            Target_Page (str): Name of the target page file (and) class "case sensitive"
            Switch (bool, optional): Switch to that page after importing it or not. Defaults to True.
        """
        self.Manager.new_page_constructor(Target_Page, Switch)

    def Remove_a_Page(self, Target_Page: str, delete_subpages: bool = False, shift_del: bool = False):
        """Deletes a Mainpage, and all its subpages if specified.
        IT DELETES THE PAGE PERMANENTLY, SO BE CAREFUL

        Args:
            Target_Page (str): Name of the mainpage tp delete "case sensitive"
            delete_subpages (bool, optional): Delete the subpages of the mainpage. Defaults to False.
            shift_del (bool, optional): When False it moves the page to the Recycle Bin, when True it deletes it PERMANENTLY. Defaults to False.
        """

        return self.Manager.delete_page(Target_Page, delete_subpages, shift_del)

    def Store_SubPage(self, Main_page: str, Sub_page, keep : bool = True, args: tuple = ()):
        """Constructs the Subpage, so that it is ready to be opened at any moment

        Args:
            Main_page (str): used to get the name of the main page class "case sensitive"
            Sub_page (Class): used to initialize the subpage class with the necessary parameters
            keep (bool, optional): keep the subpage if it already exists. Defaults to True.
            args (tuple, optional): arguments to be passed to the subpage. Defaults to ().
        """
        self.Manager.Subpage_Construction(Main_page, Sub_page, keep, args)

    def Use_SubPage(self, Main_page_name: str, Sub_page_name: str):
        """Opens the SubPage

        Args:
            Main_page (str): used to get the name of the main page class "case sensitive"
            Sub_page (str): used to get the name of the sub page class "case sensitive"
        """
        self.Manager.Subpage_init(Main_page_name, Sub_page_name)

    def Return_SubPage(self, Main_page_name: str, Sub_page_name: str):
        """Closes the SubPage

        Args:
            Main_page (str): used to get the name of the main page class "case sensitive"
            Sub_page (str): used to get the name of the sub page class "case sensitive"
        """
        self.Manager.Subpage_return(Main_page_name, Sub_page_name)

    def Get_Prefered_Theme_Mode(self):
        """Returns the prefered theme of the app

        Returns:
            str: Name of the prefered theme ["System", "Light", "Dark"]
        """
        with open(os.path.join(self.userAssetsDirectory, 'preferences.json'), 'r') as f:
            theme_data = json.load(f)
        return theme_data["theme"]["mode"]

    def Set_Prefered_Theme_Mode(self, Target_Theme: Literal["System", "Light", "Dark"]):
        """Changes the theme of the app to the target theme, and saves the preference for the next time the app is opened

        Args:
            Target_Theme (str): Name of the target theme ["System", "Light", "Dark"]
        """
        new_theme = Target_Theme.lower()

        with open(os.path.join(self.userAssetsDirectory, 'preferences.json'), 'r+') as f:
            theme_data = json.load(f)
            theme_data["theme"]["mode"] = new_theme
            f.seek(0)
            json.dump(theme_data, f, indent=4)
            f.truncate()

        try:
            #changing the color of the title bar
            if new_theme == "system":
                if self._OS == "Windows":
                    registry = ConnectRegistry(None, HKEY_CURRENT_USER)
                    key = OpenKey(registry, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                    mode = QueryValueEx(key, "AppsUseLightTheme")
                    new_theme = 'light' if mode[0] else 'dark'
                else: #! for linux and mac (to be implemented)
                    new_theme = 'dark'
            self.Window.title_bar_color(theme.TB_hex_clrs[f"{new_theme}"])
        except:
            pass

        ctk.set_appearance_mode(f'{new_theme}')
        if self._on_theme_change_jobs != []:
            for func in self._on_theme_change_jobs:
                func()

    def On_Theme_Change(self, func: Callable):
        """Registers a function to be called when the theme is changed

        Args:
            func (function): The function to be called
        """
        self._on_theme_change_jobs.append(func)

userChest = Chest() # the chest object to be used by the user