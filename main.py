from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import time
import webbrowser
from filesharer import FileSharer


Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    def start(self):
        """
        Starts camera and change Button text
        :return:
        """
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture
        self.ids.camera.opacity = 1

    def stop(self):
        """
        Stop camera and change Button text
        :return:
        """
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture(self):
        """
        Creates a filename with the current time and captures and saves
        a photo image under that filename
        :return:
        """
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = f'files/{current_time}.png'
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    link_message = 'Create a Link First'
    def create_link(self):
        """
        Accesses the photo filepath, uploads it to the web,
        and inserts the link in the Label widget
        :return:
        """
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        file_share = FileSharer(filepath=file_path)
        self.url = file_share.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """
        Copy link to the clipboard available for pasting
        :return:
        """
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        """
        Open link with default browser
        :return:
        """
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
