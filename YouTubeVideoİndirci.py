import os
import yt_dlp
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar
from ttkbootstrap import Style
from ttkbootstrap.widgets import Combobox, Frame

# Çözünürlükleri göstermek için kullanılan fonksiyon
def cozunurlukleri_goster():
    link = link_giris.get()
    
    if not link:
        messagebox.showerror("Hata", "Lütfen geçerli bir link girin!")
        return
    
    try:
        ydl_opts = {
            'format': 'best',  # En yüksek çözünürlükteki video
            'outtmpl': os.path.join(os.path.expanduser("~"), "Desktop", "İndirilenlerYT", '%(title)s.%(ext)s'),  # İndirilenlerYT klasörüne kaydet
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)  # Video bilgilerini al
            title = info.get('title', 'Video Başlığı Bulunamadı')
            formats = info.get('formats', [])
            
            # Sadece video çözünürlüklerini seçiyoruz
            cozunurlukler = [
                f"{f.get('format_note', 'Bilinmiyor')} - {f.get('resolution', 'Bilinmiyor')}" 
                for f in formats if f.get('resolution')
            ]
            
            # Çok fazla seçenek varsa, yalnızca yüksek çözünürlükleri gösterelim
            cozunurlukler = [coz for coz in cozunurlukler if "p" in coz]
            
            if cozunurlukler:
                cozunurluk_secenekleri.set(cozunurlukler[0])  # Varsayılan çözünürlük
                cozunurluk_menu['values'] = cozunurlukler
                messagebox.showinfo("Çözünürlük Seçenekleri", "\n".join(cozunurlukler))
            else:
                cozunurluk_secenekleri.set("Mevcut değil")
                cozunurluk_menu['values'] = []

            messagebox.showinfo("Video Bilgisi", f"Video Başlığı: {title}")
    
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# Video indirme fonksiyonu
def video_indir():
    link = link_giris.get()
    
    if not link:
        messagebox.showerror("Hata", "Lütfen geçerli bir link girin!")
        return
    
    try:
        ydl_opts = {
            'format': 'best',  # En yüksek çözünürlükteki video
            'outtmpl': os.path.join(os.path.expanduser("~"), "Desktop", "İndirilenlerYT", '%(title)s.%(ext)s'),  # İndirilenlerYT klasörüne kaydet
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(link, download=True)  # Videoyu indir
        messagebox.showinfo("Başarılı", f"Video başarıyla indirildi!\n\n{os.path.join(os.path.expanduser('~'), 'Desktop', 'İndirilenlerYT')}")
    
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# Tkinter yerine ttkbootstrap stili kullanarak arayüzü oluşturuyoruz
style = Style(theme="superhero")

# Ana pencereyi oluştur
root = style.master
root.title("YouTube Video İndirici")
root.geometry("600x400")  # Ekran boyutunu büyütüyoruz

# Ana çerçeve
frame = Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Video linki girişi
Label(frame, text="YouTube Video Linki:", font=("Arial", 12)).pack(pady=10)
link_giris = Entry(frame, width=50, font=("Arial", 12))  # Giriş alanı daha geniş oldu
link_giris.pack(pady=10)

# Çözünürlük seçenekleri
Label(frame, text="Çözünürlük Seç:", font=("Arial", 12)).pack(pady=5)
cozunurlukler = []
cozunurluk_secenekleri = StringVar(value="Seçim yapılmadı")
cozunurluk_menu = Combobox(frame, textvariable=cozunurluk_secenekleri, state="readonly", width=50, font=("Arial", 12))  # Menü genişliği arttırıldı
cozunurluk_menu.pack(pady=10)

# Çözünürlükleri Göster Butonu
btn_goster = Button(frame, text="Çözünürlükleri Göster", command=cozunurlukleri_goster, width=20, font=("Arial", 12))
btn_goster.pack(pady=10)

# Video indirme butonu
btn_indir = Button(frame, text="Video İndir", command=video_indir, width=20, font=("Arial", 12))
btn_indir.pack(pady=20)

# Uygulamayı başlat
root.mainloop()
