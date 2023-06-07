import mouse
import keyboard
import customtkinter
import tkinter as tk


class NewMacroFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.recording = False
        self.hook = False
        self.sequence = []

        self.label = customtkinter.CTkLabel(self, text='New Macro')
        self.label.pack()

        name_label = customtkinter.CTkLabel(self, text='Name :')
        name_label.pack()

        name_var = tk.StringVar(value="")
        name_input = customtkinter.CTkEntry(self, textvariable=name_var, width=100, height=25)
        name_input.pack()

        self.record_var = tk.StringVar(value="Record")
        record_button = customtkinter.CTkButton(self, textvariable=self.record_var,
                           command=lambda: self.record_km())
        record_button.pack()

        self.sequence_text = customtkinter.CTkTextbox(self, height = 100, width = 250)
        self.sequence_text.configure(state=tk.DISABLED)
        self.sequence_text.pack()

        reset_button = customtkinter.CTkButton(self, text="Reset",
                           command=lambda: self.reset_record())
        reset_button.pack()
        
        cancel_button = customtkinter.CTkButton(self, text="Cancel",
                           command=lambda: self.cancel())
        cancel_button.pack()

        save_button = customtkinter.CTkButton(self, text="Save",
                           command=lambda: self.save())
        save_button.pack()


    def event_key(self, e):
        if type(e) == mouse._mouse_event.ButtonEvent and e.event_type == "down" or \
            type(e) == keyboard._keyboard_event.KeyboardEvent and e.event_type == "down":
            self.hook = True
        if type(e) == mouse._mouse_event.MoveEvent:
            self.position = (e.x, e.y)
        if self.hook and type(e) == mouse._mouse_event.ButtonEvent and e.event_type == "up":
            self.sequence.append((e.button, self.position))
            self.sequence_text.configure(state=tk.NORMAL)
            self.sequence_text.insert(tk.END, str(((e.button, self.position))))
            self.sequence_text.configure(state=tk.DISABLED)
            self.sequence_text.see(tk.END)
            self.update_idletasks()
        if self.hook and type(e) == keyboard._keyboard_event.KeyboardEvent and e.event_type == "up":
            if e.name =="esc":
                self.record_km()
                return
            self.sequence.append((e.name, self.position))
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
            self.update_idletasks()
        else:
            self.recording = True
            self.position = None
            mouse.hook(self.event_key)
            keyboard.hook(self.event_key)
            self.record_var.set("Recording..")
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
        self.reset_record()
        self.controller.show_frame("IndexFrame")
