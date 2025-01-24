import pandas as pd
import json
from pathlib import Path
from tkinter import filedialog, messagebox
import threading

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
            # Load necessary columns, handle missing columns
            df = pd.read_excel(file_path, dtype=str)
            if 'STT' not in df.columns or 'Name' not in df.columns:
                raise ValueError("Required columns 'STT' and 'Name' not found")
            self.excel_path = file_path
            self.participants = df.to_dict('records')
            return len(self.participants)
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error loading file: {str(e)}"
            )
            return 0

    def load_excel_file_async(self, on_complete):
        """Load Excel in a background thread, then invoke on_complete."""
        def worker():
            num_participants = self.load_excel_file()
            on_complete(num_participants)
        threading.Thread(target=worker, daemon=True).start()

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
            with open('winners.json', 'w', encoding='utf-8') as f:
                json.dump(self.winners, f, ensure_ascii=False, indent=4)
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

    def clear_winners_file(self):
        with open('winners.json', 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    def save_participants_to_excel(self):
        if not self.excel_path:
            return
        df = pd.DataFrame(self.participants)
        df.to_excel(self.excel_path, index=False)
