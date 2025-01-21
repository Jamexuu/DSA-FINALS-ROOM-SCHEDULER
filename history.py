import json
from datetime import datetime
from typing import Dict, List, Optional
from stack import Stack

class HistoryManager:
    """
    A class to manage and track the history of schedule-related activities.
    Integrates with the room reservation system to maintain a log of all scheduling actions.
    """
    
    def __init__(self, filename: str = "history_data.json"):
        """
        Initialize the HistoryManager with an empty stack and specified filename.
        
        Args:
            filename (str): The name of the JSON file to store history data
        """
        self.history_stack = Stack()
        self.filename = filename
        self.load_history_data()
        
    def load_history_data(self) -> None:
        """
        Load history data from the JSON file into the stack.
        Handles file operations and potential errors gracefully.
        """
        try:
            with open(self.filename, "r") as file:
                history_data = json.load(file)
                self.history_stack = Stack()  # Clear existing stack
                for entry in history_data:
                    self.history_stack.push(entry)
        except FileNotFoundError:
            print(f"Creating new history file: {self.filename}")
            self.save_history_data()  # Create empty file
        except json.JSONDecodeError:
            print(f"Error decoding {self.filename}. Creating new history file.")
            self.save_history_data()  # Create new file with empty data
            
    def add_history_entry(self, action: str, room_name: str, 
                         start_time: str, end_time: str, 
                         program: str, year_section: str) -> bool:
        """
        Add a new schedule activity entry to the history.
        
        Args:
            action (str): Type of action (e.g., "Added", "Terminated", "Modified")
            room_name (str): Name of the room
            start_time (str): Start time of the schedule
            end_time (str): End time of the schedule
            program (str): Program name
            year_section (str): Year and section information
            
        Returns:
            bool: True if entry was successfully added, False otherwise
        """
        try:
            # Validate input
            if not all([action, room_name, start_time, end_time, program, year_section]):
                raise ValueError("All fields must be non-empty")
            
            history_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "room_name": room_name,
                "start_time": start_time,
                "end_time": end_time,
                "program": program,
                "year_section": year_section,
                "day": datetime.now().strftime("%A")
            }
            
            self.history_stack.push(history_entry)
            return self.save_history_data()
            
        except Exception as e:
            print(f"Error adding history entry: {str(e)}")
            return False
            
    def save_history_data(self) -> bool:
        """
        Save the current history stack to the JSON file.
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            history_data = self.history_stack.display()
            with open(self.filename, "w") as file:
                json.dump(history_data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving history data: {str(e)}")
            return False
            
    def display_history(self, limit: Optional[int] = None) -> None:
        """
        Display the history entries in a formatted way.
        
        Args:
            limit (Optional[int]): Maximum number of entries to display
        """
        if self.history_stack.is_empty():
            print("\nNo history available.")
            return
            
        entries = self.history_stack.display()
        if limit:
            entries = entries[:limit]
            
        print("\nSchedule Activity History:")
        print("-" * 100)
        
        for entry in entries:
            print(f"""
                Timestamp: {entry['timestamp']}
                Action: {entry['action']}
                Room: {entry['room_name']}
                Schedule: {entry['start_time']} - {entry['end_time']}
                Program: {entry['program']}
                Year/Section: {entry['year_section']}
                Day: {entry['day']}
                {'-' * 100}""")
            
    def get_room_history(self, room_name: str) -> List[Dict]:
        """
        Get all history entries for a specific room.
        
        Args:
            room_name (str): Name of the room to get history for
            
        Returns:
            List[Dict]: List of history entries for the specified room
        """
        entries = self.history_stack.display()
        return [entry for entry in entries if entry['room_name'] == room_name]
    
    def get_program_history(self, program: str) -> List[Dict]:
        """
        Get all history entries for a specific program.
        
        Args:
            program (str): Program name to get history for
            
        Returns:
            List[Dict]: List of history entries for the specified program
        """
        entries = self.history_stack.display()
        return [entry for entry in entries if entry['program'] == program]
    
    def get_section_history(self, year_section: str) -> List[Dict]:
        """
        Get all history entries for a specific year and section.
        
        Args:
            year_section (str): Year and section to get history for
            
        Returns:
            List[Dict]: List of history entries for the specified year and section
        """
        entries = self.history_stack.display()
        return [entry for entry in entries if entry['year_section'] == year_section]
    
    def get_day_history(self, day: str) -> List[Dict]:
        """
        Get all history entries for a specific day.
        
        Args:
            day (str): Day to get history for
            
        Returns:
            List[Dict]: List of history entries for the specified day
        """
        entries = self.history_stack.display()
        return [entry for entry in entries if entry['day'] == day]
    
    def clear_history(self) -> bool:
        """
        Clear all history entries.
        
        Returns:
            bool: True if clearing was successful, False otherwise
        """
        try:
            self.history_stack = Stack()
            return self.save_history_data()
        except Exception as e:
            print(f"Error clearing history: {str(e)}")
            return False