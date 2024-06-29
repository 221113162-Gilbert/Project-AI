import pyttsx3
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# Fungsi untuk mengonversi teks ke suara
def text_to_speech(text):
    if text:
        engine.say(text)
        engine.runAndWait()

# Fungsi untuk menangkap input suara secara real-time dan mengonversinya ke teks
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, text)
            text_to_speech(text)
            status_label.config(text="Recognition complete")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            status_label.config(text="Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            status_label.config(text=f"Could not request results; {e}")

# Fungsi untuk menyimpan teks sebagai audio
def save_audio():
    text = text_entry.get("1.0", tk.END).strip()
    if text:
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
        if file_path:
            engine.save_to_file(text, file_path)
            engine.runAndWait()
            status_label.config(text=f"Audio saved to {file_path}")

# Fungsi untuk mengubah kecepatan suara
def update_rate(val):
    engine.setProperty('rate', int(val))

# Fungsi untuk mengubah volume suara
def update_volume(val):
    engine.setProperty('volume', float(val))

# Fungsi untuk mengubah suara
def update_voice(event):
    selected_voice = voice_menu.get()
    for voice in voices:
        if voice.name == selected_voice:
            engine.setProperty('voice', voice.id)
            break

# Inisialisasi mesin TTS
engine = pyttsx3.init()

# Mengatur properti (opsional)
engine.setProperty('rate', 150)    # Kecepatan persentase (dapat melebihi 100)
engine.setProperty('volume', 0.9)  # Volume 0-1

# Mendapatkan daftar suara yang tersedia
all_voices = engine.getProperty('voices')

# Pilih satu suara laki-laki dan satu suara perempuan
male_voice = next((voice for voice in all_voices if 'male' in voice.name.lower() or 'm' in voice.id.lower()), None)
female_voice = next((voice for voice in all_voices if 'female' in voice.name.lower() or 'f' in voice.id.lower()), None)

# Jika tidak ditemukan, gunakan suara default
if not male_voice:
    male_voice = all_voices[0]
if not female_voice:
    female_voice = all_voices[1]

voices = [male_voice, female_voice]

# Membuat jendela utama aplikasi
root = tk.Tk()
root.title("Real-time Speech to Text Converter")

# Mengatur ukuran dan posisi jendela tengah layar
window_width = 600
window_height = 500
root.geometry(f"{window_width}x{window_height}")

# Menambahkan ikon aplikasi
# Note: Pastikan file icon.png ada di direktori yang sama
try:
    icon = ImageTk.PhotoImage(Image.open("icon.png"))
    root.iconphoto(False, icon)
except Exception as e:
    print("Icon file not found: ", e)

# Membuat frame utama
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Membuat dan menambahkan gambar latar belakang ke dalam frame utama jika ada
try:
    background_image = Image.open("background.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(main_frame, image=background_photo)
    background_label.pack(fill=tk.BOTH, expand=True)
    background_label.image = background_photo  # Menyimpan referensi agar gambar tetap ditampilkan
except Exception as e:
    print("Background image not found: ", e)

# Defining the style
style = ttk.Style()

# Mengatur style untuk TScale (slider)
style.configure("TScale", troughcolor="#b3d9ff", sliderlength=30, sliderthickness=20, relief="sunken", borderwidth=2, bordercolor="#b3d9ff")

# Membuat dan menempatkan widget masukan teks dengan scrollbar
text_entry_frame = ttk.Frame(main_frame)
text_entry_frame.pack(pady=20, padx=20)

text_entry = tk.Text(text_entry_frame, wrap='word', width=50, height=10, bg='#ffffff', font=('Arial', 12), relief="solid", bd=1)
text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_text_entry = ttk.Scrollbar(text_entry_frame, orient=tk.VERTICAL, command=text_entry.yview)
scrollbar_text_entry.pack(side=tk.RIGHT, fill=tk.Y)
text_entry.config(yscrollcommand=scrollbar_text_entry.set)

# Membuat dan menempatkan tombol "Speak"
speak_button = ttk.Button(main_frame, text="Speak", command=recognize_speech)
speak_button.pack(pady=10)

# Membuat dan menempatkan tombol "Save Audio"
save_button = ttk.Button(main_frame, text="Save Audio", command=save_audio)
save_button.pack(pady=10)

# Membuat label status untuk menunjukkan status pengenalan suara
status_label = ttk.Label(main_frame, text="", style="TLabel")
status_label.pack(pady=5)

# Membuat frame untuk pengaturan suara
settings_frame = ttk.Frame(main_frame)
settings_frame.pack(pady=10)

# Membuat dan menempatkan slider kecepatan suara
rate_label = ttk.Label(settings_frame, text="Speech Rate", style="TLabel")
rate_label.pack(pady=5)
rate_slider = ttk.Scale(settings_frame, from_=50, to=300, orient='horizontal', command=update_rate, style="TScale")
rate_slider.set(150)  # Set nilai default kecepatan
rate_slider.pack(pady=5)

# Membuat dan menempatkan slider volume suara
volume_label = ttk.Label(settings_frame, text="Volume", style="TLabel")
volume_label.pack(pady=5)
volume_slider = ttk.Scale(settings_frame, from_=0, to=1, orient='horizontal', command=update_volume, style="TScale")
volume_slider.set(0.9)  # Set nilai default volume
volume_slider.pack(pady=5)

# Membuat dan menempatkan dropdown untuk memilih suara
voice_label = ttk.Label(settings_frame, text="Select Voice", style="TLabel")
voice_label.pack(pady=5)
voice_menu = ttk.Combobox(settings_frame, state='readonly', font=('Arial', 10))
voice_menu['values'] = [voice.name for voice in voices]
voice_menu.current(0)
voice_menu.pack(pady=10)
voice_menu.bind("<<ComboboxSelected>>", update_voice)

# Mengikat event mouse scroll untuk mengatur scrolling pada masukan teks
def on_mouse_wheel(event):
    text_entry.yview_scroll(-1*(event.delta//120), "units")

text_entry.bind("<MouseWheel>", on_mouse_wheel)

# Menjalankan aplikasi
root.mainloop()
