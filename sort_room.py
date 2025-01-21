import json

class Room:
    def __init__(self, name, schedule=None):
        self.name = name
        self.schedule = schedule if isinstance(schedule, dict) else {}

    def is_available(self, day, start_time, end_time):
        if day not in self.schedule:
            return True
        for entry in self.schedule[day]:
            booked_start, booked_end = entry[:2]
            if not (end_time <= booked_start or start_time >= booked_end):
                return False
        return True

    def update_schedule(self, day, new_schedule):
        self.schedule[day] = new_schedule
        self.save_schedule()

    def add_schedule(self, day, start_time, end_time, program, year_section):
        if day not in self.schedule:
            self.schedule[day] = []
        self.schedule[day].append((start_time, end_time, program, year_section))
        self.save_schedule()

    def save_schedule(self):
        try:
            with open('room_scheduler_data.json', 'r+') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
                data[self.name] = self.schedule
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()  # Ensure the file is truncated to avoid leftover data
        except FileNotFoundError:
            with open('room_scheduler_data.json', 'w') as file:
                json.dump({self.name: self.schedule}, file, indent=4)


class RoomScheduler:
    def __init__(self, rooms):
        self.rooms = rooms
        self.load_schedules()

    def load_schedules(self):
        try:
            with open('room_scheduler_data.json', 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
                for room in self.rooms:
                    if room.name in data:
                        room.schedule = data[room.name] if isinstance(data[room.name], dict) else {}
        except FileNotFoundError:
            with open('room_scheduler_data.json', 'w') as file:
                json.dump({}, file)


    def sort_rooms_by_availability(self, day, start_time, end_time):
        available_rooms = [room for room in self.rooms if room.is_available(day, start_time, end_time)]
        
        # Debugging: Ensure all schedules are dictionaries
        for room in available_rooms:
            if not isinstance(room.schedule, dict):
                print(f"Error: Room {room.name} has an invalid schedule {room.schedule}")

        # Bubble sort implementation
        n = len(available_rooms)
        for i in range(n):
            for j in range(0, n-i-1):
                if len(available_rooms[j].schedule.get(day, [])) > len(available_rooms[j+1].schedule.get(day, [])):
                    available_rooms[j], available_rooms[j+1] = available_rooms[j+1], available_rooms[j]

        return available_rooms


    def update_room_schedule(self, room_name, day, new_schedule):
        for room in self.rooms:
            if room.name == room_name:
                room.update_schedule(day, new_schedule)
                break
        return self.sort_rooms_by_availability(day, new_schedule[0][0], new_schedule[-1][1])

def get_rooms():
    rooms = [
        Room("NB 101"),
        Room("NB 102"),
        Room("NB 103"),
        Room("NB 104"),
        Room("NB 203"),
        Room("NB 204"),
        Room("NB 205"),
        Room("NB 206"),
        Room("NB 301"),
        Room("NB 302"),
        Room("NB 303"),
        Room("NB 304"),
        Room("NB 305"),
        Room("NB 306"),
        Room("NB 401"),
        Room("NB 402"),
        Room("NB 403"),
        Room("NB 404"),
        Room("NB 405")
    ]
    return rooms