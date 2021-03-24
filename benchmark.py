import tkinter as tk
import threading
import time
import random

class CPS_Tester:
    """This class will create a tkinter toplevel that allows the user to test their CPS.
    Requires a toplevel window to be passed."""
    def __init__(self, root):
        self.is_running = True
        self.currently_threading = False
        self.clicks = 0
        self.current_time = 10
        self.start_time = self.current_time
        self.root = root

        root.title("CPS Tester")
        root.geometry("400x400")
        root.resizable(0, 0)

        self.main_frame = tk.Frame(root, bg="turquoise")
        self.main_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.stats_frame = tk.Frame(root, bg="turquoise")
        self.stats_frame.pack(padx=5, pady=5)

        tk.Label(self.main_frame, text="CPS Tester", bg="light blue").pack(padx=2, pady=2)

        self.main_button = tk.Button(self.main_frame, text="Click me to start!", command=self.test_clicks, bg="light blue", activebackground="light blue")
        self.main_button.pack(padx=2, pady=2, expand=True, fill=tk.BOTH)

        self.timer_label = tk.Label(self.stats_frame, text="Timer", bg="light blue")
        self.timer_label.grid(row=0, column=0, padx=5, pady=10)

        self.average_label = tk.Label(self.stats_frame, text="Average", bg="light blue")
        self.average_label.grid(row=0, column=1, padx=5, pady=10)

    def thread_timer(self):
        """Start a thread that calls the timer function to begin - we have to do this
        due to the button freezing if we use any other delay method."""
        thread = threading.Thread(target=self.timer)
        thread.start()

    def thread_interval(self):
        """Begin the thread to call the interval_wait function"""
        thread = threading.Thread(target=self.interval_wait)
        thread.start()

    def interval_wait(self):
        """freeze and unfreeze the button after the interval, not
         allowing the user to instantly start another test and not see their score
         accidentally."""

        wait_interval = 2

        self.main_button.config(state=tk.DISABLED)
        time.sleep(wait_interval)
        self.main_button.config(text="Click me to go again!", state=tk.ACTIVE)

    def test_clicks(self):
        """The main logic for getting the player's clicks and storing in a
        variable."""

        if not self.currently_threading:
            self.thread_timer()
            self.currently_threading = True

        if self.is_running:
            self.clicks += 1
            self.main_button.config(text="Clicks: " + str(self.clicks))

    def timer(self):
        """Run the timer that counts down from click_time, then call the
        appropriate functions once the time is up."""

        # The interval that the time counts down in
        time_interval = 0.25

        while self.current_time > 0:
            time.sleep(time_interval)
            self.current_time -= time_interval
            self.update_timer()

        self.main_button.config(text="You got " + str(self.clicks) + " clicks!")
        self.average_label.config(text="Average: " + self.get_average())

        self.thread_interval()
        self.reset_stats()

    def update_timer(self):
        """Update the timer label with the current time."""
        self.timer_label.config(text="Time: " + str(self.current_time))

    def reset_stats(self):
        """Reset all global variables as well as the timer_label to the correct
        time"""

        self.is_running = True
        self.currently_threading = False
        self.clicks = 0
        self.current_time = 10

        self.timer_label.config(text="Time: " + str(self.current_time))

    def get_average(self):
        return str(self.clicks / self.start_time)


class WPS_Tester:
    """This class will create a tkinter toplevel that allows the user to test their CPS.
    Requires a toplevel window to be passed."""
    def __init__(self, root):
        self.got_word = False
        self.word = ""
        self.current_time = 0
        self.interval = 0.25

        # The phrases that the user will have to type - add or remove at your leisure!
        self.phrase_list = ["Once there was a guy who could count to five", "Don’t tell people your plans. Show them your results",
                            "We can do anything we want to if we stick to it long enough", "Try Again. Fail again. Fail better.",
                            "A bird in the hand is worth two in the bush!", "A horse, a horse, my kingdom for a horse",
                            "All limitations are self-imposed.", "One day the people that don’t even believe in you will tell everyone how they met you.",
                            "If you tell the truth you don’t have to remember anything.", "Have enough courage to start and enough heart to finish.",
                            "Oh, the things you can find, if you don’t stay behind.", "Never let your emotions overpower your intelligence.",
                            "Reality is wrong, dreams are for real.", "To live will be an awfully big adventure."]

        root.title("WPS Tester")
        root.geometry("600x400")
        root.resizable(0, 0)

        self.word_label = tk.Label(root, text="Ready?", bg="light blue", font=("Caladea", 12))
        self.word_label.pack(pady=15)

        self.word_entry = tk.Entry(root, width=85, bg="light blue")
        self.word_entry.pack(pady=15)

        self.main_button = tk.Button(root, text="Start", command=self.start_test, bg="light blue", font=main_font)
        self.main_button.pack(pady=15)

        self.timer_label = tk.Label(root, text="Timer: ", bg="light blue")
        self.timer_label.pack()

    def thread_timer(self):
        """Begin the thread that calls the timer function"""
        thread = threading.Thread(target=self.timer)
        thread.start()

    def update_timer(self):
        """Update the timer label with the current time."""
        self.timer_label.config(text="Time: " + str(self.current_time))

    def timer(self):
        """Begin the timer, and stop it when the word is typed. Also calls appropriate functions
        once timer stops."""
        while self.word_entry.get() != self.word_label["text"] and self.word_label["text"] != "Ready?":
            time.sleep(self.interval)
            self.current_time += self.interval
            self.update_timer()

        self.word_label.config(text="Well done!")
        self.timer_label.config(text="You took " + str(self.current_time) + " seconds")
        time.sleep(2)
        self.reset_stats()

    def get_rand_phrase(self):
        """Get a random phrase from phrase_list, and return it"""
        choice = random.choice(self.phrase_list)
        self.phrase_list.remove(choice)
        return choice

    def start_test(self):
        """Start the wps test"""
        if not self.got_word:
            self.word = self.get_rand_phrase()
            self.word_label.config(text=self.word)
            self.main_button.config(text="Go!", state=tk.DISABLED)
            self.thread_timer()
            self.got_word = True

    def reset_stats(self):
        self.word = ""
        self.current_time = 0
        self.word_label.config(text="Ready?")
        self.main_button.config(text="Start", state=tk.ACTIVE)
        self.word_entry.delete(0, "end")
        self.got_word = False


def open_cps_window():
    cps_window = tk.Toplevel()
    cps_window.config(bg="turquoise")
    CPS_Tester(cps_window)
    cps_window.mainloop()


def open_wps_window():
    wps_window = tk.Toplevel()
    wps_window.config(bg="turquoise")
    WPS_Tester(wps_window)
    wps_window.mainloop()


title_font = ("Caladea", 40)
main_font = ("Caladea", 30)

root = tk.Tk()
root.title("main")
root.geometry("500x350")
root.resizable(0, 0)
root.config(bg="turquoise")

title_frame = tk.Frame(root, bg="turquoise")
title_frame.pack(pady=5)
button_frame = tk.Frame(root, bg="turquoise")
button_frame.pack(pady=5)

tk.Label(title_frame, text="CPS/WPS Benchmark", font=title_font, bg="light blue").pack()

cps_button = tk.Button(button_frame, text="CPS Tester", command=open_cps_window, font=main_font, bg="light blue")
cps_button.grid(row=0, column=0, padx=10, pady=10)

cps_button = tk.Button(button_frame, text="WPS Tester", command=open_wps_window, font=main_font, bg="light blue")
cps_button.grid(row=1, column=0, padx=10, pady=10)


root.mainloop()
