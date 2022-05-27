from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random


Builder.load_file("design.kv")
 

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_screen"
        self.ids.login_wrong.text = ""
        self.ids.username.text = ""
        self.ids.password.text = ""

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.ids.login_wrong.text = ""
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.manager.transition.direction = 'left'
            self.manager.current = "login_screen_success"
        else:
            if self.ids.login_wrong.text == "":
                self.ids.login_wrong.text = "Incorrect username or password!"
            elif self.ids.login_wrong.text == "Incorrect username or password!":
                self.ids.login_wrong.text = "Try Again!"
            elif self.ids.login_wrong.text == "Try Again!":
                self.ids.login_wrong.text = "You may need to reset your password!"
            else:
                self.ids.login_wrong.text = "Incorrect username or password!"

    def go_to_forgot_password(self):
        self.manager.current = "forgot_password"


class SignUpScreen(Screen):
    def go_back_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        if uname in users.keys():
            self.ids.feedback.text = f"Sorry! {uname} is already in use."
        elif uname == pword:
            self.ids.feedback.text = f"Password cannot be the same as Username!"
        else: 
            users[uname] = {"username": uname, "password": pword,
                "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

            with open("users.json", 'w') as file:
                json.dump(users, file)

            self.manager.current = "sign_up_screen_success"


class SignUpScreenSuccess(Screen):
    def go_back_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower() 
        feel = feel.strip() # delete the withespace at beginning
        available_feelings = glob.glob("quotes/*txt")
        
        available_feelings = [Path(filename).stem for filename in 
                                available_feelings]
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quotes.text = random.choice(quotes)
        else:
            self.ids.quotes.text = "Hmmm......."


class ForgotPassword(Screen):
    def change_password(self,user_name, new_pass):
        with open("users.json") as file:
            users = json.load(file)       
        users[user_name] = {'username':user_name, 'password':new_pass, 
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        if users[user_name]['username'] == user_name:
            with open("users.json", "w") as file:
                users[user_name]['password'] = new_pass
                json.dump(users, file)
            self.ids.password_status.text = "Password changed successfully"
        else:
            self.ids.password_status.text = "Try Again"

    def go_back_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()
        

if __name__ == '__main__':
    MainApp().run()
