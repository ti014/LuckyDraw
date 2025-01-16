import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime
from audio_handler import AudioHandler
from ui_components import UIComponents
from file_operations import FileOperations
from PIL import Image, ImageTk

class ModernLuckyDraw:
    def __init__(self, root):
        self.root = root
        self.root.title("Lucky Draw FIS DT")
        self.root.attributes('-fullscreen', True)  # Set to full screen by default
        
        # Initialize modules
        self.audio_handler = AudioHandler(root)
        self.file_operations = FileOperations()
        self.ui_components = UIComponents(root, self.get_colors())
        
        # Set background image
        self.set_background_image()
        
        # Setup audio
        self.audio_handler.setup_audio()
        
        # State variables
        self.is_drawing = False
        self.animation_speed = 50
        self.current_participant = None
        
        # Setup UI
        self.ui_components.setup_styles()
        self.ui_components.create_ui()
        self.load_previous_winners()
        
        # Bind buttons to methods
        self.ui_components.file_btn.config(command=self.load_excel_file)
        self.ui_components.start_btn.config(command=self.start_draw)
        self.ui_components.stop_btn.config(command=self.stop_draw)
        self.ui_components.next_btn.config(command=self.next_round)
        
        # Bind ESC key to exit
        self.root.bind("<Escape>", self.exit_program)
        
    def get_colors(self):
        """Return color scheme"""
        return {
            'bg': '#1a1a2e',
            'primary': '#0f3460',
            'secondary': '#16213e',
            'accent': '#e94560',
            'text': '#ffffff',
            'gold': '#FFD700',
            'silver': '#C0C0C0'
        }
        
    def load_excel_file(self):
        """Load participants from Excel file"""
        num_participants = self.file_operations.load_excel_file()
        if num_participants > 0:
            self.ui_components.file_label.config(
                text=f"✅ Loaded {num_participants} participants"
            )
            self.ui_components.start_btn.config(state='normal')
        
    def start_draw(self):
        """Start the drawing process with music"""
        if not self.file_operations.participants:
            messagebox.showwarning("Warning", "Please load participants first!")
            return
        self.is_drawing = True
        self.ui_components.start_btn.config(state='disabled')
        self.ui_components.stop_btn.config(state='normal')
        self.animation_speed = 50
        self.audio_handler.play_background_music()
        self.animate_selection()
        
    def stop_draw(self):
        """Stop the drawing process and music"""
        self.ui_components.stop_btn.config(state='disabled')
        self.audio_handler.reduce_volume()
        self.root.after(3000, self.finish_selection)
        
    def finish_selection(self):
        """Complete drawing process"""
        self.is_drawing = False
        winner_record = next(
            x for x in self.file_operations.participants 
            if x['Name'] == self.current_participant_name
        )
        self.file_operations.winners.append(winner_record)
        self.file_operations.participants.remove(winner_record)
        self.audio_handler.stop_background_music()
        self.ui_components.name_label.config(
            text=f"{winner_record['Name']}\n{winner_record['Group']} - {winner_record['Department']}",
            fg=self.ui_components.colors['gold']
        )
        self.ui_components.winners_list.insert(
            0,
            f"🏆 {datetime.now().strftime('%Y-%m-%d %H:%M')} - {winner_record['Name']}\n{winner_record['Group']} - {winner_record['Department']}"
        )
        self.file_operations.update_excel_file(winner_record)
        self.ui_components.next_btn.config(state='normal')
        self.audio_handler.announce_winner(winner_record)
        self.audio_handler.cleanup_winner_audio()
        
    def next_round(self):
        """Prepare for next round"""
        self.ui_components.name_label.config(
            text="Ready for Next Draw",
            fg=self.ui_components.colors['text']
        )
        self.ui_components.start_btn.config(state='normal')
        self.ui_components.next_btn.config(state='disabled')
        self.audio_handler.stop_background_music()
        
    def animate_selection(self):
        """Animate the name selection with visual effects"""
        if not self.is_drawing:
            return
        name_only_list = [p['Name'] for p in self.file_operations.participants]
        self.current_participant_name = random.choice(name_only_list)
        self.ui_components.name_label.config(
            text=self.current_participant_name,
            fg=self.ui_components.colors['text']
        )
        self.root.after(self.animation_speed, self.animate_selection)
        
    def load_previous_winners(self):
        """Load previously saved winners"""
        winners = self.get_winners_from_file()
        if winners is None:
            winners = []
        for winner in winners:
            self.ui_components.winners_list.insert(
                0,
                f"🏆 {winner}"
            )
            
    def get_winners_from_file(self):
        """Get winners from file"""
        try:
            winners = self.file_operations.load_previous_winners()
            return winners
        except FileNotFoundError:
            return None
            
    def set_background_image(self):
        """Set the background image"""
        self.background_image = Image.open("assets/backGround.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        self.background_label.lower()
        
    def exit_program(self, event):
        """Exit the program"""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernLuckyDraw(root)
    root.mainloop()