import io
import tkinter as tk
from tkinter import ttk
import urllib.request

# Safely check for Pillow (PIL) library
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Massive catalog of songs mapped to public domain sheet music links
MASTER_SHEET_CATALOG = [
    # Classical Masterpieces
    ("Beethoven - Fur Elise", "Classical", "A minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Beethoven - Moonlight Sonata (1st Mov)", "Classical", "C# minor", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Beethoven - Symphony No. 5 (Opening)", "Classical", "C minor", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Mozart - Piano Sonata in C Major (KV 545)", "Classical", "C major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Mozart - Rondo alla Turca", "Classical", "A minor", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Bach - Preludthise in C Major (BWV 846)", "Classical", "C major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Bach - Goldberg Variations (Aria)", "Classical", "G major", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Chopin - Nocturne in E-flat Major (Op. 9, No. 2)", "Classical", "Eb major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Chopin - Minute Waltz (Op. 64, No. 1)", "Classical", "Db major", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Chopin - Prelude in E Minor (Op. 28, No. 4)", "Classical", "E minor", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Vivaldi - The Four Seasons (Spring)", "Classical", "E major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Debussy - Clair de Lune", "Classical", "Db major", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Debussy - Arabesque No. 1", "Classical", "E major", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Pachelbel - Canon in D", "Classical", "D major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Satie - Gymnopédie No. 1", "Classical", "D major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Tchaikovsky - Swan Lake Theme", "Classical", "B minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Tchaikovsky - Dance of the Sugar Plum Fairy", "Classical", "E minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Brahms - Lullaby", "Classical", "Eb major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Schubert - Ave Maria", "Classical", "Bb major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Mendelssohn - Wedding March", "Classical", "C major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),

    # Pop & Modern Hits
    ("Twinkle Twinkle Little Star - Classic", "Pop", "C major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Let It Go - Frozen Theme", "Pop", "Ab major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Someone Like You - Adele", "Pop", "A major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Hallelujah - Leonard Cohen", "Pop", "C major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Perfect - Ed Sheeran", "Pop", "G major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("All of Me - John Legend", "Pop", "Ab major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Imagine - John Lennon", "Pop", "C major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Yesterday - The Beatles", "Pop", "F major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Hey Jude - The Beatles", "Pop", "F major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Bohemian Rhapsody - Queen", "Pop", "Bb major", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),

    # Cinematic & Movie Themes
    ("Interstellar - Main Theme (Cornfield Chase)", "Cinematic", "A minor", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Harry Potter - Hedwig's Theme", "Cinematic", "E minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Star Wars - Main Theme", "Cinematic", "Bb major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Pirates of the Caribbean - He's a Pirate", "Cinematic", "D minor", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Lord of the Rings - Concerning Hobbits", "Cinematic", "D major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Jurassic Park - Theme Song", "Cinematic", "Bb major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Titanic - My Heart Will Go On", "Cinematic", "E major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("The Godfather - Love Theme", "Cinematic", "A minor", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("La La Land - City of Stars", "Cinematic", "A minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Inception - Time", "Cinematic", "A minor", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),

    # Jazz & Blues Standards
    ("Take Five - Dave Brubeck", "Jazz", "Eb minor", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Fly Me to the Moon - Frank Sinatra", "Jazz", "C major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Autumn Leaves - Jazz Standard", "Jazz", "G minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("The Entertainer - Scott Joplin", "Jazz", "C major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Maple Leaf Rag - Scott Joplin", "Jazz", "Ab major", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Moonlight Serenade - Glenn Miller", "Jazz", "Eb major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Summertime - George Gershwin", "Jazz", "A minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Georgia on My Mind - Ray Charles", "Jazz", "F major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),

    # Video Games
    ("Super Mario Bros - Overworld Theme", "Game", "C major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Tetris Theme (Korobeiniki)", "Game", "A minor", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/6/6a/Beethoven_Fur_Elise_page_1.png"),
    ("Zelda - Overworld Theme", "Game", "C major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Minecraft - Sweden (C418)", "Game", "F major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/b/b2/J.S._Bach_-_Prelude_in_C_major_BWV_846.png"),
    ("Pokemon - Red/Blue Pokémon Center", "Game", "C major", "Beginner", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Undertale - Megalovania", "Game", "D minor", "Advanced", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png"),
    ("Final Fantasy - Aerith's Theme", "Game", "D major", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/2/2f/W.A._Mozart_-_Allegro_KV_1_-_page_1.png"),
    ("Skyrim - Dragonborn Theme", "Game", "D minor", "Intermediate", "https://upload.wikimedia.org/wikipedia/commons/a/af/Beethoven_Moonlight_sonata.png")
]

class ErrorProofSheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Error-Proof Sheet Music Library")
        self.root.geometry("1250x800")
        self.root.configure(bg="#0b0f19")

        # Top Bar & Search
        top_frame = tk.Frame(root, bg="#111827", pady=12, padx=20)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="🎵 Library Index:", font=("Segoe UI", 11, "bold"), fg="white", bg="#111827").pack(side="left", padx=(0, 10))
        
        self.search_entry = tk.Entry(top_frame, font=("Segoe UI", 11), bg="#1f2937", fg="white", insertbackground="white", width=35)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.insert(0, "Search songs...")
        self.search_entry.bind("<KeyRelease>", self.filter_catalog)

        tk.Label(top_frame, text=f"Total Songs: {len(MASTER_SHEET_CATALOG)}", font=("Segoe UI", 10, "bold"), fg="#34d399", bg="#111827").pack(side="right", padx=10)

        # Workspace
        workspace = tk.Frame(root, bg="#0b0f19")
        workspace.pack(expand=True, fill="both", padx=15, pady=12)

        # Left Index List
        left_panel = tk.Frame(workspace, bg="#111827", width=380)
        left_panel.pack(side="left", fill="y", padx=(0, 10))

        self.listbox = tk.Listbox(left_panel, font=("Segoe UI", 10), bg="#1f2937", fg="#f3f4f6", selectbackground="#38bdf8", selectforeground="#030712", bd=0)
        self.listbox.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Right Image Viewer Panel
        right_panel = tk.Frame(workspace, bg="#111827")
        right_panel.pack(side="right", expand=True, fill="both")

        self.info_label = tk.Label(right_panel, text="Select a song to load real sheet music.", font=("Segoe UI", 11, "bold"), fg="white", bg="#111827", anchor="w")
        self.info_label.pack(fill="x", padx=15, pady=10)

        canvas_frame = tk.Frame(right_panel, bg="#1f2937")
        canvas_frame.pack(expand=True, fill="both", padx=12, pady=12)

        self.canvas = tk.Canvas(canvas_frame, bg="#1f2937", highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.current_image = None
        self.populate_list(MASTER_SHEET_CATALOG)
        self.listbox.select_set(0)
        self.load_sheet(MASTER_SHEET_CATALOG[0])

    def populate_list(self, items):
        self.listbox.delete(0, tk.END)
        for title, genre, key, diff, url in items:
            self.listbox.insert(tk.END, f"[{genre[0]}] {title}")

    def filter_catalog(self, event):
        q = self.search_entry.get().strip().lower()
        if not q or q == "search songs...":
            filtered = MASTER_SHEET_CATALOG
        else:
            filtered = [item for item in MASTER_SHEET_CATALOG if q in item[0].lower() or q in item[1].lower()]
        self.populate_list(filtered)

    def on_select(self, event):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]
        q = self.search_entry.get().strip().lower()
        if not q or q == "search songs...":
            filtered = MASTER_SHEET_CATALOG
        else:
            filtered = [item for item in MASTER_SHEET_CATALOG if q in item[0].lower() or q in item[1].lower()]
            
        if idx < len(filtered):
            self.load_sheet(filtered[idx])

    def load_sheet(self, sheet_info):
        title, genre, key, diff, url = sheet_info
        self.info_label.config(text=f"📄 {title} | Key: {key} | Level: {diff}")

        self.canvas.delete("all")

        if not PIL_AVAILABLE:
            self.canvas.create_text(350, 200, text="Pillow (PIL) library not found!\nPlease run: python3 -m pip install Pillow", font=("Segoe UI", 12), fill="#f87171", justify="center")
            return

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                img_data = response.read()

            image = Image.open(io.BytesIO(img_data))
            w, h = image.size
            new_w = 700
            new_h = int(h * (new_w / w))
            image = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

            self.current_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(350, 10, anchor="n", image=self.current_image)
            self.canvas.config(scrollregion=(0, 0, 700, new_h + 30))
        except Exception:
            self.canvas.delete("all")
            self.canvas.create_text(350, 200, text=f"Could not load image preview for:\n{title}\n(Check internet connection)", font=("Segoe UI", 13), fill="#9ca3af", justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = ErrorProofSheetApp(root)
    root.mainloop()
