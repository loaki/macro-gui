import os
import json
import mouse
import keyboard
import customtkinter
import pyautogui
import tkinter as tk


class NewMacroFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.recording = False
        self.check = False
        self.prev_event = None
        self.in_frame = True
        self.sequence = []
        vcmd = (self.register(self.validate_value), '%P')

        self.label = customtkinter.CTkLabel(self, text="New Macro")
        self.label.pack()

        self.name_label = customtkinter.CTkLabel(self, text="Name :")
        self.name_label.pack()

        self.name_var = tk.StringVar(value="")
        self.name_input = customtkinter.CTkEntry(
            self, textvariable=self.name_var, width=100, height=25
        )
        self.name_input.pack()

        self.record_var = tk.StringVar(value="Record")
        self.record_button = customtkinter.CTkButton(
            self, textvariable=self.record_var, command=lambda: self.record_km()
        )
        self.record_button.pack()

        self.sequence_text = customtkinter.CTkTextbox(self, height=100, width=250)
        self.sequence_text.configure(state=tk.DISABLED)
        self.sequence_text.pack()

        self.delay_var = tk.DoubleVar(value=0)
        self.delay_var.trace("w", self.update_delay)
        delay_entry = customtkinter.CTkEntry(
            self, textvariable=self.delay_var, width=45, height=25
        )
        delay_entry.configure(validate='key', validatecommand=vcmd)
        delay_entry.pack()
        delay_slider = customtkinter.CTkSlider(
            self,
            from_=0,
            to=2,
            variable=self.delay_var or 0,
            width=100
        )
        delay_slider.pack()
        delay_button = customtkinter.CTkButton(
            self, text="Add Delay", command=lambda: self.append_delay()
        )
        delay_button.pack()

        self.check_var = tk.StringVar(value="Add a color check")
        self.check_button = customtkinter.CTkButton(
            self, textvariable=self.check_var, command=lambda: self.check_color()
        )
        self.check_button.pack()

        reset_button = customtkinter.CTkButton(
            self, text="Reset", command=lambda: self.reset_record()
        )
        reset_button.pack()

        cancel_button = customtkinter.CTkButton(
            self, text="Cancel", command=lambda: self.cancel()
        )
        cancel_button.pack()

        save_button = customtkinter.CTkButton(
            self, text="Save", command=lambda: self.save()
        )
        save_button.pack()


    def update_delay(self, *args):
        try:
            value = float(self.delay_var.get())
            self.delay_var.set(value)
        except:
            self.delay_var.set(0)


    def validate_value(self, value):
        try:
            if float(value) >= 0 and float(value) < 1000:
                return True
        except:
            pass
        return False


    def append_delay(self):
        self.sequence.append(
            {"key": "delay", "position": [], "delay": self.delay_var.get()}
        )
        self.sequence_text.configure(state=tk.NORMAL)
        self.sequence_text.insert(tk.END, str(("delay", self.delay_var.get())))
        self.sequence_text.configure(state=tk.DISABLED)
        self.sequence_text.see(tk.END)
        self.update_idletasks()


    def check_color(self):
        if self.check:
            self.check = False
            self.check_var.set("Add a color check")
        elif self.recording:
            self.check = True
            self.check_var.set("Click on the zone")


    def event_key(self, e):
        if type(e) == mouse._mouse_event.MoveEvent:
            self.position = [e.x, e.y]
        geometry = self.controller.winfo_geometry()
        if (
            self.position and
            self.position[0] > int(geometry.split("+")[1])
            and self.position[0] < int(geometry.split("x")[0]) + int(geometry.split("+")[1])
            and self.position[1] > int(geometry.split("+")[2])
            and self.position[1] < int(geometry.split("x")[1].split("+")[0]) + int(geometry.split("+")[2])
        ):
            self.in_frame = True
        elif self.position:
            self.in_frame = False
        if (not self.in_frame
            and self.check
            and type(e) == mouse._mouse_event.ButtonEvent
        ):
            self.check = False
            self.check_var.set("Add a color check")
            color = pyautogui.pixel(self.position[0], self.position[1])
            self.sequence.append(
                {"key": "check", "position": self.position, "color": color}
            )
            self.sequence_text.configure(state=tk.NORMAL)
            self.sequence_text.insert(tk.END, str(("check", self.position, color)))
            self.sequence_text.configure(state=tk.DISABLED)
            self.sequence_text.see(tk.END)
            self.update_idletasks()
            self.record_km()
            return
        if (
            not self.in_frame
            and not self.check
            and type(e) == mouse._mouse_event.ButtonEvent
        ):
            self.sequence.append(
                {"key": e.button, "type": e.event_type, "position": self.position}
            )
            self.sequence_text.configure(state=tk.NORMAL)
            self.sequence_text.insert(tk.END, str((e.button, e.event_type, self.position)))
            self.sequence_text.configure(state=tk.DISABLED)
            self.sequence_text.see(tk.END)
            self.update_idletasks()
        if (
            type(e) == keyboard._keyboard_event.KeyboardEvent
            and (not self.prev_event
            or self.prev_event != [e.name, e.event_type])
        ):
            if e.name == "esc":
                self.record_km()
                return
            self.prev_event = [e.name, e.event_type]
            self.sequence.append({"key": e.name, "type": e.event_type, "position": self.position})
            self.sequence_text.configure(state=tk.NORMAL)
            self.sequence_text.insert(tk.END, str(((e.name, e.event_type, self.position))))
            self.sequence_text.configure(state=tk.DISABLED)
            self.sequence_text.see(tk.END)
            self.update_idletasks()


    def record_km(self):
        if self.recording:
            mouse.unhook(self.event_key)
            keyboard.unhook(self.event_key)
            self.recording = False
            self.in_frame = True
            self.record_var.set("Record")
            self.name_input.configure(state=tk.NORMAL)
            self.update_idletasks()
        else:
            self.recording = True
            self.position = None
            mouse.hook(self.event_key)
            keyboard.hook(self.event_key)
            self.record_var.set("Recording..")
            self.name_input.configure(state=tk.DISABLED)
            self.update_idletasks()


    def reset_record(self):
        if self.recording:
            self.record_km()
        self.sequence = []
        self.sequence_text.configure(state=tk.NORMAL)
        self.sequence_text.delete("0.0", "end")
        self.sequence_text.configure(state=tk.DISABLED)
        self.update_idletasks()


    def cancel(self):
        self.reset_record()
        self.controller.show_frame("IndexFrame")


    def save(self):
        if self.name_var.get() and self.sequence:
            with open(
                os.path.join(os.getcwd(), f"macros/{self.name_var.get()}.json"), "w"
            ) as new_f:
                new_f.write(json.dumps(self.sequence, indent=4))
            self.reset_record()
            self.controller.show_frame("IndexFrame")
