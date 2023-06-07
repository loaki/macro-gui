import customtkinter


class IndexFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        self.label = customtkinter.CTkLabel(self, text="Macros")
        self.label.pack()

        button = customtkinter.CTkButton(
            self,
            text="Go to the macro page",
            command=lambda: controller.show_frame("NewMacroFrame"),
        )
        button.pack()
