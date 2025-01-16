import pandas as pd
import json
from pathlib import Path
from tkinter import filedialog, messagebox

class FileOperations:
    def __init__(self):
        self.excel_path = None
        self.participants = []
        self.winners = []

    def load_excel_file(self):
        """Load and validate Excel file"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx")]
            )
            if not file_path:
                return
            # Only load necessary columns
            df = pd.read_excel(file_path, usecols=['STT', 'Name', 'Group', 'Department'])
            if not all(col in df.columns for col in ['STT', 'Name', 'Group', 'Department']):
                raise ValueError("Required columns 'STT', 'Name', 'Group' and 'Department' not found")
            self.excel_path = file_path
            self.participants = df.to_dict('records')
            return len(self.participants)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error loading file: {str(e)}"
            )
            return 0

    def update_excel_file(self, winner):
        """Update Excel file and save winners"""
        try:
            df = pd.read_excel(self.excel_path)
            df = df[df['STT'] != winner['STT']]
            df.to_excel(self.excel_path, index=False)
            self.save_winners()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error updating Excel file: {str(e)}"
            )

    def save_winners(self):
        """Save winners to JSON file"""
        try:
            with open('winners.json', 'w') as f:
                json.dump(self.winners, f)
        except Exception as e:
            print(f"Error saving winners: {e}")

    def load_previous_winners(self):
        """Load previously saved winners"""
        try:
            if Path('winners.json').exists():
                with open('winners.json', 'r') as f:
                    self.winners = json.load(f)
                    return self.winners
        except Exception as e:
            print(f"Error loading winners: {e}")
            return []
