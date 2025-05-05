import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import os

# Helper for rounded rectangles
class RoundedFrame(Canvas):
    def __init__(self, parent, width, height, radius=25, bg='#fff', **kwargs):
        Canvas.__init__(self, parent, width=width, height=height, bg=parent['bg'], highlightthickness=0, **kwargs)
        self.radius = radius
        self.bg = bg
        self.create_round_rect(0, 0, width, height, radius, fill=bg, outline=bg)
    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1,
                  x1+r, y1,
                  x2-r, y1,
                  x2-r, y1,
                  x2, y1,
                  x2, y1+r,
                  x2, y1+r,
                  x2, y2-r,
                  x2, y2-r,
                  x2, y2,
                  x2-r, y2,
                  x2-r, y2,
                  x1+r, y2,
                  x1+r, y2,
                  x1, y2,
                  x1, y2-r,
                  x1, y2-r,
                  x1, y1+r,
                  x1, y1+r,
                  x1, y1]
        self.create_polygon(points, smooth=True, **kwargs)

class ChatPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg="#a7d0f5", *args, **kwargs)
        # Content frame for prompts (top)
        content_frame = tk.Frame(self, bg="#a7d0f5")
        content_frame.pack(side="top", fill="both")
        prompt_frame = RoundedFrame(content_frame, 340, 80, radius=30, bg="#e6f2fa")
        prompt_frame.pack(pady=(40, 30), anchor="nw", padx=40)
        prompt_frame.create_text(170, 40, text="What can we do for you today?", font=("Arial", 18, "bold"), fill="#222")
        suggested_frame = tk.Frame(content_frame, bg="#a7d0f5")
        suggested_frame.pack(pady=10, anchor="nw", padx=40)
        suggested = [
            "Generate financial report",
            "Look for x skill in the cv list",
            "suggested prompts"
        ]
        for i, text in enumerate(suggested):
            f = RoundedFrame(suggested_frame, 260, 80, radius=30, bg="#e6f2fa")
            f.pack(side="left", padx=30)
            f.create_text(130, 40, text=text, font=("Arial", 16, "bold"), fill="#222")
        # Input/chatbox at the bottom center
        input_frame = tk.Frame(self, bg="#d9eaf7", height=110)
        input_frame.pack(side="bottom", pady=30, fill="x")
        input_frame.pack_propagate(False)
        circle = Canvas(input_frame, width=80, height=80, bg="#d9eaf7", highlightthickness=0)
        circle.create_oval(10, 10, 70, 70, fill="#274472", outline="#274472")
        circle.pack(side="left", padx=(30, 0), pady=10)
        input_var = tk.StringVar()
        input_entry = tk.Entry(input_frame, textvariable=input_var, font=("Arial", 22, "bold"), width=40, bd=0, relief="flat", fg="#222", bg="#d9eaf7", justify="left")
        input_entry.insert(0, "Press ‘/’ to see actions")
        input_entry.pack(side="left", padx=(20, 0), pady=28, ipady=18)
        def on_entry_click(event):
            if input_entry.get() == "Press ‘/’ to see actions":
                input_entry.delete(0, "end")
                input_entry.config(fg="#222")
        input_entry.bind("<FocusIn>", on_entry_click)
        input_entry.config(fg="#888")

class InfoPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg="#a7d0f5", *args, **kwargs)
        # Integrations/connected accounts area (placeholder)
        left_panel = tk.Frame(self, bg="#274472", width=340)
        left_panel.pack(side="left", fill="y", padx=(0, 30), pady=0)
        left_panel.pack_propagate(False)
        # Add Info Section
        add_info_frame = tk.Frame(self, bg="white")
        add_info_frame.place(relx=0.35, rely=0.6, anchor="w", width=600, height=250)
        tk.Label(add_info_frame, text="Add Info", font=("Arial", 22, "bold"), bg="white", fg="black", anchor="w").place(x=30, y=20)
        tk.Label(add_info_frame, text="Q:", font=("Arial", 18, "bold"), bg="white", fg="black").place(x=30, y=70)
        self.q_entry = tk.Entry(add_info_frame, font=("Arial", 16), width=40, bg="white")
        self.q_entry.place(x=70, y=70, height=32)
        tk.Label(add_info_frame, text="A:", font=("Arial", 18, "bold"), bg="white", fg="black").place(x=30, y=120)
        self.a_entry = tk.Entry(add_info_frame, font=("Arial", 16), width=40, bg="white")
        self.a_entry.place(x=70, y=120, height=32)
        add_btn = tk.Button(add_info_frame, text="Add", font=("Arial", 16, "bold"), bg="#274c77", fg="white", relief="groove", bd=0, padx=18, pady=4)
        add_btn.place(x=500, y=180, width=70, height=40)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Offline Assistant")
        # Set max window size to 90% of screen
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w = int(screen_w * 0.9)
        win_h = int(screen_h * 0.9)
        self.geometry(f"{win_w}x{win_h}")
        self.minsize(1000, 700)
        self.configure(bg="#a7d0f5")

        # Right Sidebar
        rightbar = tk.Frame(self, bg="#274472", width=320)
        rightbar.pack(side="right", fill="y")
        rightbar.pack_propagate(False)
        cv_lbl = tk.Label(rightbar, text="Company Vision", bg="#274472", fg="white", font=("Arial", 22, "bold"))
        cv_lbl.pack(pady=(18, 0), anchor="nw", padx=18)
        vision_text = (
            "- nu exista intrebari stupide\n"
            "- comunicare deschisa si constanta\n"
            "- feedback-ul si ideile sunt binevenite\n"
            "- tinem cont de deadline-uri – ne asumam ce promitem si comunicam daca apar obstacole\n"
            "- autonomie cu responsabilitate – aveti libertate, dar si responsabilitatea rezultatului\n"
            "- ne ajutam intre noi, pentru ca suntem o echipa"
        )
        tk.Label(rightbar, text=vision_text, bg="#274472", fg="white", font=("Arial", 13), justify="left", wraplength=300).pack(pady=(8, 8), anchor="nw", padx=18)
        Canvas(rightbar, width=300, height=2, bg="#274472", highlightthickness=0).create_line(0, 2, 300, 2, fill="#222", width=2)
        tk.Frame(rightbar, height=2, bg="#222").pack(fill="x", padx=10, pady=(0, 0))
        rem_lbl = tk.Label(rightbar, text="Reminders", bg="#274472", fg="white", font=("Arial", 20, "bold"))
        rem_lbl.pack(pady=(30, 0), anchor="nw", padx=18)
        tk.Label(rightbar, text="...", bg="#274472", fg="white", font=("Arial", 15)).pack(anchor="nw", padx=18)

        # Sidebar (left)
        sidebar = tk.Frame(self, bg="#274472", width=180)
        sidebar.pack(side="left", fill="y")
        icon_bg = "#b3d6f2"
        icon_frame = tk.Frame(sidebar, bg="#274472")
        icon_frame.pack(pady=30)
        ICON_SIZE = 80
        IMG_SIZE = 65
        img_path = "icon.png"
        if not os.path.exists(img_path):
            img_path = "R_icon.png"
        img = Image.open(img_path).resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        icon_canvas = Canvas(icon_frame, width=ICON_SIZE, height=ICON_SIZE, bg="#274472", highlightthickness=0)
        icon_canvas.create_oval(10, 10, ICON_SIZE-10, ICON_SIZE-10, fill=icon_bg, outline=icon_bg)
        icon_canvas.create_image(ICON_SIZE//2, ICON_SIZE//2, image=img_tk)
        icon_canvas.image = img_tk
        icon_canvas.pack(pady=(0, 25))
        # Menu buttons
        icons = ["💬", "💡", "⚙️"]
        self.menu_buttons = []
        for i, icon in enumerate(icons):
            c = Canvas(icon_frame, width=ICON_SIZE, height=ICON_SIZE, bg="#274472", highlightthickness=0)
            c.create_oval(10, 10, ICON_SIZE-10, ICON_SIZE-10, fill=icon_bg, outline=icon_bg)
            c.create_text(ICON_SIZE//2, ICON_SIZE//2, text=icon, font=("Arial", 38, "normal"), fill="#274472")
            c.pack(pady=(0, 25) if i < 2 else (0, 0))
            self.menu_buttons.append(c)
        history_lbl = tk.Label(sidebar, text="History", bg="#274472", fg="white", font=("Arial", 22, "bold"))
        history_lbl.pack(pady=(30, 0), anchor="nw", padx=20)

        # Container for pages
        self.container = tk.Frame(self, bg="#a7d0f5")
        self.container.pack(side="left", fill="both", expand=True)
        self.pages = {}
        self.current_page = None
        self.show_chat_page()

        # Link 💬 button to chat page
        self.menu_buttons[0].bind("<Button-1>", lambda e: self.show_chat_page())
        # Link 💡 button to info page
        self.menu_buttons[1].bind("<Button-1>", lambda e: self.show_info_page())
        # Placeholder: self.menu_buttons[2] can be linked to other pages

    def show_chat_page(self):
        if self.current_page == 'chat':
            return
        # Remove current page
        for page in self.pages.values():
            page.pack_forget()
        if 'chat' not in self.pages:
            self.pages['chat'] = ChatPage(self.container)
        self.pages['chat'].pack(fill="both", expand=True)
        self.current_page = 'chat'

    def show_info_page(self):
        if self.current_page == 'info':
            return
        for page in self.pages.values():
            page.pack_forget()
        if 'info' not in self.pages:
            self.pages['info'] = InfoPage(self.container)
        self.pages['info'].pack(fill="both", expand=True)
        self.current_page = 'info'

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 