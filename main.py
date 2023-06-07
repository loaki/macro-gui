import customtkinter
from pynput import keyboard

from src.frames.index import IndexFrame
from src.frames.new_macro import NewMacroFrame


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("M A Q U E R E A U")
        self.geometry("300x600")
        # self.resizable(False, False)
        self.attributes("-alpha", 0.8)
        self.iconbitmap("maquereau.ico")
        self.wm_attributes("-topmost", True)

        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (IndexFrame, NewMacroFrame):
            frame = F(master=container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F.__name__] = frame

        self.show_frame("IndexFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
