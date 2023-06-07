import os
import json
import mouse
import keyboard
import customtkinter
import tkinter as tk
import math


class NewMacroFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.recording = False
        self.hook = False
        self.sequence = []

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
        delay_entry = customtkinter.CTkEntry(
            self, textvariable=self.delay_var, width=45, height=25
        )
        delay_entry.pack()
        delay_slider = customtkinter.CTkSlider(
            self,
            from_=0,
            to=2,
            variable=self.delay_var,
            width=100,
            command=self.set_exp_value,
        )
        delay_slider.pack()
        delay_button = customtkinter.CTkButton(
            self, text="Add Delay", command=lambda: self.append_delay()
        )
        delay_button.pack()

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

    def set_exp_value(self, val):
        self.delay_var.set(math.exp(val) - 1)

    def append_delay(self):
        self.sequence.append(
            {"key": "delay", "position": [], "delay": self.delay_var.get()}
        )
        self.sequence_text.configure(state=tk.NORMAL)
        self.sequence_text.insert(tk.END, str(("delay", self.delay_var.get())))
        self.sequence_text.configure(state=tk.DISABLED)
        self.sequence_text.see(tk.END)
        self.update_idletasks()

    def event_key(self, e):
        if (
            type(e) == mouse._mouse_event.ButtonEvent
            and e.event_type == keyboard.KEY_DOWN
            or type(e) == keyboard._keyboard_event.KeyboardEvent
            and e.event_type == keyboard.KEY_DOWN
        ):
            self.hook = True
        if type(e) == mouse._mouse_event.MoveEvent:
            self.position = [e.x, e.y]
        if (
            self.hook
            and type(e) == mouse._mouse_event.ButtonEvent
            and e.event_type == keyboard.KEY_UP
        ):
            self.sequence.append(
                {"key": e.button, "position": self.position, "delay": 0}
            )
            self.sequence_text.configure(state=tk.NORMAL)
            self.sequence_text.insert(tk.END, str((e.button, self.position)))
            self.sequence_text.configure(state=tk.DISABLED)
            self.sequence_text.see(tk.END)
            self.update_idletasks()
        if (
            self.hook
            and type(e) == keyboard._keyboard_event.KeyboardEvent
            and e.event_type == keyboard.KEY_UP
            and not keyboard.is_modifier(e.name)
        ):
            if e.name == "esc":
                self.record_km()
                return
            if mod := next(
                (k for k in keyboard.all_modifiers if keyboard.is_pressed(k)), None
            ):
                e.name = mod + "+" + e.name
            self.sequence.append({"key": e.name, "position": self.position, "delay": 0})
            self.sequence_text.configure(state=tk.NORMAL)
            self.sequence_text.insert(tk.END, str(((e.name, self.position))))
            self.sequence_text.configure(state=tk.DISABLED)
            self.sequence_text.see(tk.END)
            self.update_idletasks()

    def record_km(self):
        if self.recording:
            mouse.unhook(self.event_key)
            keyboard.unhook(self.event_key)
            self.recording = False
            self.hook = False
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
            self.controller.show_frame("IndexFrame")
