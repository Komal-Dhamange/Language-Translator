import customtkinter as ctk
from tkinter import messagebox
from utils.translator import translate_text
from gtts import gTTS
import pygame
import os
import threading
from PIL import Image, ImageTk  # Dono ko import kiya hai icon aur logo ke liye

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI Language Translator")
app.geometry("900x750")  # Logo ke liye height thodi aur badhayi hai
app.resizable(False, False)

# --- 1. WINDOW ICON SET KARNA ---
try:
    icon_path = os.path.join("assets", "icon.png")
    # Window icon (Jo taskbar aur corner mein dikhta hai)
    img = Image.open(icon_path)
    window_icon = ImageTk.PhotoImage(img)
    app.wm_iconphoto(False, window_icon)
except Exception as e:
    print(f"Icon load nahi ho paya: {e}")

# --- 2. UI KE ANDAR LOGO ADD KARNA ---
try:
    logo_img = ctk.CTkImage(light_image=Image.open("assets/icon.png"),
                            dark_image=Image.open("assets/icon.png"),
                            size=(100, 100)) # Size aap adjust kar sakte hain
    
    logo_label = ctk.CTkLabel(app, image=logo_img, text="")
    logo_label.pack(pady=(20, 0)) 
except Exception as e:
    print(f"Logo display error: {e}")

# --- Title ---
title = ctk.CTkLabel(
    app,
    text="🌍 AI Language Translator",
    font=("Arial", 32, "bold"),
    text_color="#3B8ED0"
)
title.pack(pady=(10, 20))

# --- New Audio Function ---
def play_audio():
    text = output_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Warning", "Please translate some text first!")
        return
    
    def speak():
        try:
            lang_code = languages[selected_language.get()]
            tts = gTTS(text=text, lang=lang_code)
            filename = "temp_voice.mp3"
            tts.save(filename)
            
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                continue
                
            pygame.mixer.quit()
            os.remove(filename)
        except Exception as e:
            messagebox.showerror("Error", f"Voice error: {e}")

    threading.Thread(target=speak).start()

# --- Input Section ---
input_label = ctk.CTkLabel(app, text="Enter Text", font=("Arial", 14, "italic"))
input_label.pack()

input_text = ctk.CTkTextbox(app, width=700, height=120, corner_radius=15, border_width=2)
input_text.pack(pady=10)

# --- Language Options ---
languages = {
    "Hindi": "hi", "English": "en", "French": "fr", "German": "de",
    "Spanish": "es", "Japanese": "ja", "Chinese": "zh-cn"
}

selected_language = ctk.StringVar(value="Hindi")

language_menu = ctk.CTkOptionMenu(
    app,
    values=list(languages.keys()),
    variable=selected_language,
    width=200,
    corner_radius=10,
    dynamic_resizing=True
)
language_menu.pack(pady=10)

# --- Output Section ---
output_label = ctk.CTkLabel(app, text="Translated Text", font=("Arial", 14, "italic"))
output_label.pack()

output_text = ctk.CTkTextbox(app, width=700, height=120, corner_radius=15, border_width=2, fg_color="#2B2B2B")
output_text.pack(pady=10)

# --- Translation Logic ---
def perform_translation():
    text = input_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter text")
        return

    translate_btn.configure(text="Translating...")
    app.update_idletasks()

    lang_code = languages[selected_language.get()]
    translated = translate_text(text, lang_code)

    output_text.delete("1.0", "end")
    output_text.insert("end", translated)
    translate_btn.configure(text="Translate")

def copy_text():
    translated = output_text.get("1.0", "end").strip()
    if translated:
        app.clipboard_clear()
        app.clipboard_append(translated)
        copy_btn.configure(text="✅ Copied!", fg_color="green")
        app.after(2000, lambda: copy_btn.configure(text="Copy Text", fg_color=["#3B8ED0", "#1F6AA5"]))

# --- Modern Button Frame ---
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.pack(pady=20)

translate_btn = ctk.CTkButton(
    button_frame,
    text="Translate",
    command=perform_translation,
    width=160,
    height=45,
    font=("Arial", 16, "bold"),
    corner_radius=20,
    hover_color="#1F6AA5"
)
translate_btn.grid(row=0, column=0, padx=15)

listen_btn = ctk.CTkButton(
    button_frame,
    text="🔊 Listen",
    command=play_audio,
    width=160,
    height=45,
    font=("Arial", 16, "bold"),
    fg_color="#5D6D7E",
    hover_color="#34495E",
    corner_radius=20
)
listen_btn.grid(row=0, column=1, padx=15)

copy_btn = ctk.CTkButton(
    button_frame,
    text="Copy Text",
    command=copy_text,
    width=160,
    height=45,
    font=("Arial", 16, "bold"),
    corner_radius=20
)
copy_btn.grid(row=0, column=2, padx=15)

app.mainloop()