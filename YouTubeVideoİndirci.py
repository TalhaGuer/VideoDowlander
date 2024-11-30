import os
import yt_dlp
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar
from ttkbootstrap import Style
from ttkbootstrap.widgets import Combobox, Frame

def cozunurlukleri_goster():
    link = link_giris.get()
    
    if not link:
        messagebox.showerror("Hata", "Lütfen geçerli bir link girin!")
        return
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(os.path.expanduser("~"), "Desktop", "İndirilenlerYT", '%(title)s.%(ext)s'), 
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)  
            title = info.get('title', 'Video Başlığı Bulunamadı')
            formats = info.get('formats', [])
            
           
            cozunurlukler = [
                f"{f.get('format_note', 'Bilinmiyor')} - {f.get('resolution', 'Bilinmiyor')}" 
                for f in formats if f.get('resolution')
            ]
            
           
            cozunurlukler = [coz for coz in cozunurlukler if "p" in coz]
            
            if cozunurlukler:
                cozunurluk_secenekleri.set(cozunurlukler[0])  
                cozunurluk_menu['values'] = cozunurlukler
                messagebox.showinfo("Çözünürlük Seçenekleri", "\n".join(cozunurlukler))
            else:
                cozunurluk_secenekleri.set("Mevcut değil")
                cozunurluk_menu['values'] = []

            messagebox.showinfo("Video Bilgisi", f"Video Başlığı: {title}")
    
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")


def video_indir():
    link = link_giris.get()
    
    if not link:
        messagebox.showerror("Hata", "Lütfen geçerli bir link girin!")
        return
    
    try:
        ydl_opts = {
            'format': 'best', 
            'outtmpl': os.path.join(os.path.expanduser("~"), "Desktop", "İndirilenlerYT", '%(title)s.%(ext)s'), 
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(link, download=True) 
        messagebox.showinfo("Başarılı", f"Video başarıyla indirildi!\n\n{os.path.join(os.path.expanduser('~'), 'Desktop', 'İndirilenlerYT')}")
    
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

style = Style(theme="superhero")

root = style.master
root.title("YouTube Video İndirici")
root.geometry("600x400")  

frame = Frame(root, padding=20)
frame.pack(fill="both", expand=True)

Label(frame, text="YouTube Video Linki:", font=("Arial", 12)).pack(pady=10)
link_giris = Entry(frame, width=50, font=("Arial", 12))  #
link_giris.pack(pady=10)

Label(frame, text="Çözünürlük Seç:", font=("Arial", 12)).pack(pady=5)
cozunurlukler = []
cozunurluk_secenekleri = StringVar(value="Seçim yapılmadı")
cozunurluk_menu = Combobox(frame, textvariable=cozunurluk_secenekleri, state="readonly", width=50, font=("Arial", 12)) 
cozunurluk_menu.pack(pady=10)

btn_goster = Button(frame, text="Çözünürlükleri Göster", command=cozunurlukleri_goster, width=20, font=("Arial", 12))
btn_goster.pack(pady=10)

btn_indir = Button(frame, text="Video İndir", command=video_indir, width=20, font=("Arial", 12))
btn_indir.pack(pady=20)

root.mainloop()
