import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
import os

class CalendarApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calendar with Events")
        self.master.configure(bg='#F0F0F0')  # Set a light gray background

        # Colors for different elements
        self.header_bg = '#6495ED'  # Cornflower Blue
        self.weekday_bg = 'white'  # Weekdays background
        self.weekend_bg = '#FFCCCB'  # Weekends background
        self.event_bg = '#ADD8E6'  # Light Blue for event days

        # Initialize current year, month, and day
        self.current_year = tk.IntVar(value=2024)
        self.current_month = tk.IntVar(value=4)
        self.current_day = tk.IntVar(value=1)

        # Title Label
        self.calendar = tk.Label(master, text="Calendar", font=('Helvetica', 16), bg=self.header_bg, fg='white')
        self.calendar.grid(row=0, column=0, columnspan=7, sticky="ew")

        # Navigation buttons
        self.prev_button = tk.Button(master, text="< Prev Month", command=self.prev_month, bg=self.header_bg, fg='white')
        self.prev_button.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.next_button = tk.Button(master, text="Next Month >", command=self.next_month, bg=self.header_bg, fg='white')
        self.next_button.grid(row=1, column=5, columnspan=2, sticky="ew")

        # Month and year label
        self.month_year_label = tk.Label(
            master,
            textvariable=self.get_month_year(),
            font=('Helvetica', 12),
            bg=self.header_bg,
            fg='white'
        )
        self.month_year_label.grid(row=1, column=2, columnspan=3)

        # Day headers (Sun, Mon, Tue, etc.)
        self.days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(self.days):
            tk.Label(
                master,
                text=day,
                bg=self.header_bg,
                fg='white'
            ).grid(row=2, column=i, sticky="ew")

        # Calendar cells for the dates
        self.cells = []
        for i in range(6):
            for j in range(7):
                bg_color = self.weekend_bg if j == 0 or j == 6 else self.weekday_bg
                cell = tk.Button(
                    master,
                    text="",
                    bg=bg_color,
                    command=lambda i=i, j=j: self.show_events(i, j)
                )
                cell.grid(row=i + 3, column=j, sticky="nsew")
                self.cells.append(cell)

        # Load existing events and update the calendar
        self.events = self.load_events()
        self.update_calendar()

    def get_month_year(self):
        return tk.StringVar(value=f"{calendar.month_name[self.current_month.get()]} {self.current_year.get()}")

    def update_calendar(self):
        for cell in self.cells:
            cell.config(text="", bg=self.weekday_bg)  # Reset background to weekday color

        month_events = self.events.get((self.current_year.get(), self.current_month.get()), {})
        month_range = range(1, calendar.monthrange(self.current_year.get(), self.current_month.get())[1] + 1)

        first_weekday = calendar.weekday(self.current_year.get(), self.current_month.get(), 1)

        for day in month_range:
            index = first_weekday + (day - 1)
            row = index // 7
            column = index % 7
            cell_index = row * 7 + column
            
            if day in month_events:
                # Color for days with events
                self.cells[cell_index].config(text=str(day), bg=self.event_bg)
            else:
                # Set appropriate background color for weekdays/weekends
                bg_color = self.weekend_bg if column == 0 or column == 6 else self.weekday_bg
                self.cells[cell_index].config(text=str(day), bg=bg_color)

    def prev_month(self):
        # Navigate to the previous month
        current_month = self.current_month.get()
        if current_month == 1:
            self.current_month.set(12)
            self.current_year.set(self.current_year.get() - 1)
        else:
            self.current_month.set(current_month - 1)
        self.update_calendar()
        self.month_year_label.config(text=self.get_month_year().get())

    def next_month(self):
        # Navigate to the next month
        current_month = self.current_month.get()
        if current_month == 12:
            self.current_month.set(1)
            self.current_year.set(self.current_year.get() + 1)
        else:
            self.current_month.set(current_month + 1)
        self.update_calendar()
        self.month_year_label.config(text=self.get_month_year().get())

    def show_events(self, row, col):
        day_text = self.cells[row * 7 + col].cget("text")
        if not day_text:
            return

        day = int(day_text)
        event_date = (self.current_year.get(), self.current_month.get(), day)
        if event_date in self.events:
            events_str = "\n".join(self.events[event_date])
            messagebox.showinfo(
                "Events",
                f"Events on {self.current_month.get()}/{day}/{self.current_year.get()}:\n{events_str}"
            )
        else:
            messagebox.showinfo(
                "Events",
                f"No events on {self.current_month.get()}/{day}/{self.current_year.get()}"
            )

    def add_event(self):
        day = simpledialog.askinteger("Add Event", "Enter day:")
        if not day:
            return

        event = simpledialog.askstring("Add Event", "Enter event:")
        if not event:
            return

        event_date = (self.current_year.get(), self.current_month.get(), day)
        if event_date in self.events:
            self.events[event_date].append(event)
        else:
            self.events[event_date] = [event]

        self.update_calendar()
        self.save_events()

    def edit_event(self):
        day = simpledialog.askinteger("Edit Event", "Enter day:")
        if not day:
            return

        event_date = (self.current_year.get(), self.current_month.get(), day)
        if event_date in self.events:
            events_str = "\n".join(self.events[event_date])
            new_events_str = simpledialog.askstring(
                "Edit Event",
                f"Current events on {self.current_month.get()}/{day}/{self.current_year.get()}:\n{events_str}\nEnter new events:"
            )
            if new_events_str:
                self.events[event_date] = new_events_str.split('\n')
                self.update_calendar()
                self.save_events()
        else:
            messagebox.showinfo(
                "Edit Event",
                f"No events on {self.current_month.get()}/{day}/{self.current_year.get()}"
            )

    def delete_event(self):
        day = simpledialog.askinteger("Delete Event", "Enter day:")
        if not day:
            return

        event_date = (self.current_year.get(), self.current_month.get(), day)
        if event_date in self.events:
            del self.events[event_date]
            self.update_calendar()
            self.save_events()
            messagebox.showinfo(
                "Delete Event",
                f"Events on {self.current_month.get()}/{day}/{self.current_year.get()} deleted."
            )
        else:
            messagebox.showinfo(
                "Delete Event",
                f"No events on {self.current_month.get()}/{day}/{self.current_year.get()}"
            )

    def load_events(self):
        events = {}
        if os.path.exists("events.txt"):
            with open("events.txt", "r") as file:
                for line in file:
                    year, month, day, *event = line.strip().split(",")
                    event_date = (int(year), int(month), int(day))
                    events[event_date] = event
        return events

    def save_events(self):
        with open("events.txt", "w") as file:
            for event_date, events in self.events.items():
                year, month, day = event_date
                events_str = ",".join(events)
                file.write(f"{year},{month},{day},{events_str}\n")


def main():
    root = tk.Tk()
    app = CalendarApp(root)

    add_button = tk.Button(root, text="Add Event", command=app.add_event)
    add_button.grid(row=10, column=1, pady=10)

    edit_button = tk.Button(root, text="Edit Event", command=app.edit_event)
    edit_button.grid(row=10, column=2, pady=10)

    delete_button = tk.Button(root, text="Delete Event", command=app.delete_event)
    delete_button.grid(row=10, column=3, pady=10)

    root.mainloop()

main()
