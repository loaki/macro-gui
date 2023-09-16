import tkinter as tk
import customtkinter


class IndexFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.topmost = True

        self.label = customtkinter.CTkLabel(self, text="Macros")
        self.label.bind("<Button-1>", self.label_clicked)
        self.label.pack()

        self.topmost_var = tk.StringVar(value="Unset topmost")
        top_button = customtkinter.CTkButton(
            self,
            textvariable=self.topmost_var,
            command=lambda: self.set_topmost(),
        )
        top_button.pack()

        macro_button = customtkinter.CTkButton(
            self,
            text="Create macro",
            command=lambda: controller.show_frame("NewMacroFrame"),
        )
        macro_button.pack()


    def label_clicked(self, event):
        if self.controller.winfo_height() == 600:
            self.controller.geometry("300x20")
        else:
            self.controller.geometry("300x600")


    def set_topmost(self):
        self.controller.wm_attributes("-topmost", not self.topmost)
        self.topmost = not self.topmost
        if self.topmost:
            self.topmost_var.set("Unset topmost")
        else:
            self.topmost_var.set("Set topmost")

