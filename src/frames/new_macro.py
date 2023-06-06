import customtkinter
import tkinter as tk

class NewMacroFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        # add widgets onto the frame...
        self.label = customtkinter.CTkLabel(self, text='New Macro')
        self.label.pack()

        name_input = tk.StringVar(value="")
        name_input = customtkinter.CTkEntry(self, textvariable=name_input, width=100, height=25)
        name_input.pack()

        cancel_button = customtkinter.CTkButton(self, text="Cancel",
                           command=lambda: controller.show_frame("IndexFrame"))
        cancel_button.pack()

        save_button = customtkinter.CTkButton(self, text="Save",
                           command=lambda: controller.show_frame("IndexFrame"))
        save_button.pack()
