import socket
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

class LudoApp(App):
    def build(self):
        self.socket = None
        self.active_player = 0 
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.status_label = Label(text="Status: Disconnected", size_hint_y=0.1, color=(1,0,0,1))
        main_layout.add_widget(self.status_label)
        
        connect_btn = Button(text="Connect to Game", size_hint_y=0.15, background_color=(0,1,0,1))
        connect_btn.bind(on_press=self.connect_game)
        main_layout.add_widget(connect_btn)
        
        player_label = Label(text="Select Player:", size_hint_y=0.1)
        main_layout.add_widget(player_label)
        
        player_layout = GridLayout(cols=4, size_hint_y=0.15)
        for i in range(4):
            btn = Button(text=f"P{i+1}")
            btn.bind(on_press=lambda instance, p=i: self.select_player(p))
            player_layout.add_widget(btn)
        main_layout.add_widget(player_layout)
        
        dice_label = Label(text="Select Dice Number:", size_hint_y=0.1)
        main_layout.add_widget(dice_label)
        
        dice_layout = GridLayout(cols=3, size_hint_y=0.4)
        for i in range(1, 7):
            btn = Button(text=str(i), font_size='20sp')
            btn.bind(on_press=lambda instance, d=i: self.send_command(d))
            dice_layout.add_widget(btn)
        main_layout.add_widget(dice_layout)
        
        return main_layout

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

    def connect_game(self, instance):
        self.status_label.text = "Status: Connecting..."
        self.status_label.color = (1,1,0,1)
        
        TARGET_IP = "192.168.43.1" 
        TARGET_PORT = 8888
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((TARGET_IP, TARGET_PORT))
            
            self.status_label.text = f"Status: Connected! ✅"
            self.status_label.color = (0,1,0,1)
            self.show_popup("Success", "Game se connect ho gaya!")
            
        except Exception as e:
            self.socket = None
            self.status_label.text = "Status: Failed ❌"
            self.status_label.color = (1,0,0,1)
            self.show_popup("Error", "Connect nahi hua. Check Hotspot & Game.")

    def select_player(self, player_id):
        self.active_player = player_id
        self.show_popup("Player Selected", f"Ab tu Player {player_id + 1} ko control kar raha hai.")

    def send_command(self, dice_num):
        if not self.socket:
            self.show_popup("Error", "Pehle Connect toh kar le bhai!")
            return
        
        try:
            command = f"SET {self.active_player} {dice_num}\n"
            self.socket.sendall(command.encode('utf-8'))
            
            Clock.schedule_once(lambda dt: self.reset_dice(), 0.5)
            
            self.show_popup("Success", f"Command Sent: {command.strip()}")
            
        except Exception as e:
            self.show_popup("Error", f"Command fail: {e}")
            self.socket = None
            self.status_label.text = "Status: Disconnected ❌"
            self.status_label.color = (1,0,0,1)

    def reset_dice(self):
        if self.socket:
            try:
                reset_command = f"SET {self.active_player} 6\n"
                self.socket.sendall(reset_command.encode('utf-8'))
            except:
                pass

if __name__ == '__main__':
    LudoApp().run()


