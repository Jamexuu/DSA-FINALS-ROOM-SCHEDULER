import json
from collections import deque

class QueueManager:
    def __init__(self):
        self.queue_data = self.load_queue_data()

    def load_queue_data(self):
        try:
            with open('queue_data.json', 'r') as file:
                data = json.load(file)
                return {room: deque(entries) for room, entries in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_queue_data(self):
        with open('queue_data.json', 'w') as file:
            json.dump({room: list(entries) for room, entries in self.queue_data.items()}, file, indent=4)

    def add_to_queue(self, room_name, start_time, end_time, program, year_section):
        if room_name not in self.queue_data:
            self.queue_data[room_name] = deque()
        self.queue_data[room_name].append((start_time, end_time, program, year_section))
        self.save_queue_data()

    def get_queue(self, room_name):
        return list(self.queue_data.get(room_name, deque()))
    