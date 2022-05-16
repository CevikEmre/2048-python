#Tkinter GUI(Arayüzü) projeye eklendi.
from __future__ import print_function
try:
    import tkinter as tk
    import tkinter.messagebox as messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

import random

class Pencere:
    def __init__(self,size): #constructor(yapıcı) fonksiyon tanımlandı.
        self.size = size
        self.hucreler = self.bos_pencere_olustur()
        self.sikisma = False
        self.birlesme = False
        self.hareket = False
        self.puan = 0

    def random_hucre(self): #rastgele yeni hücre oluşumu
        hucre = random.choice(self.bosHucre_geri_al())
        i = hucre[0]
        j = hucre[1]
        self.hucreler[i][j] = 2 if random.random() < 0.9 else 4

    def bosHucre_geri_al(self): #2 sayı birleşince artan hücre silindi
        bosHucre = []
        for i in range (self.size):
            for j in range(self.size):
                if self.hucreler[i][j] == 0:
                    bosHucre.append((i,j))
        return bosHucre

    def bos_pencere_olustur(self): #hareketten sonra yeni boş bir pencere(grid) oluştu.
        return [[0] * self.size for i in range (self.size)]

    def birlestirme(self): #transpoze metodu
        self.hucreler = [list(t) for t in zip(*self.hucreler)] #zip metodu:  listelerdeki aynı index değerine sahip elamanları aynı indextte birleştirir.

    def ters_cevirme(self):
        for i in range(self.size):
            baslangic = 0
            bitis = self.size - 1
            while baslangic < bitis:
                self.hucreler[i][baslangic], self.hucreler[i][bitis] = self.hucreler[i][bitis], self.hucreler[i][baslangic]
                baslangic += 1
                bitis -= 1

    def temizle_bayrak(self): #bayrak programın tamamının ya da belirli bir bölümünün çalışacağını anlatmak için programa sinyal yollar
        # gerekli nesnelerin False yapılması için bu işlem yapılır.
        self.sikisma = False
        self.birlesme = False
        self.hareket = False

    def artik_sikisma(self): #artık(kalan) sayıları sıkıştırma metodu tanımlandı.
        self.sikisma = False
        yeni_pencere = self.bos_pencere_olustur()
        for i in range(self.size):
            sayac  = 0
            for j in range(self.size):
                if self.hucreler[i][j] != 0:
                    yeni_pencere[i][sayac]  = self.hucreler[i][j]
                    if sayac!= j:
                        self.sikisma = True
                    sayac += 1
        self.hucreler = yeni_pencere

    def artik_birlesme(self): #artık sayıları birleştiren metod
        self.birlesme = False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.hucreler[i][j]== self.hucreler[i][j+1] and  self.hucreler[i][j] != 0:
                    self.hucreler[i][j] *=2
                    self.hucreler[i][j+1] = 0
                    self.birlesme = True

    def ulasmak_2048(self): #2048 oldu mu diye kontrol eder.
        for i in range(self.size):
            for j in range(self.size):
                if self.hucreler[i][j]>=2048:
                    return True
        return False

    def bos_hucre_varsa(self): #boş hücre var mı diye kontrol eder.
        for i in range(self.size):
            for j in range(self.size):
                if self.hucreler[i][j]== 0:
                    return True
        return False

    def birlesebilir(self): # birleşebilir durumda olup olmadığını kontrol eder.
        for i in range(self.size):
            for j in range(self.size-1):
                if self.hucreler[i][j] == self.hucreler[i][j+1]:
                    return True
        for j in range(self.size):
            for i in range(self.size-1):
                if self.hucreler[i][j] == self.hucreler[i+1][j]:
                    return True
        return False

    def set_hucre(self,hucreler): #hücre nesnesine setter işlemi
        self.hucreler=hucreler


class OyunPaneli: #Oyunun görünen yüzünü ayarlama sınıfı

    ARKAPLAN_RENGI = '#2f4f4f'
    BOS_HUCRE_RENGI = '#ffffe0'
    HUCRE_ARKAPLAN_RENGI_KILAVUZ = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#f2b179',
        '16': '#f59563',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#edc850',
        '1024': '#edc53f',
        '2048': '#edc22e',
        'beyond': '3c3a32'
    }
    HUCRE_RENGI_KILAVUZ = {
        '2': '#776e65',
        '4': '#776e65',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#f9f6f2',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
        'beyond': '#f9f6f2'
    }
    FONT = ('Times New Roman',40,'bold')
    YUKARI_TUS = ('Up')
    ASAGI_TUS = ('Down')
    SOLA_TUS = ('Left')
    SAGA_TUS = ('Right')

    def __init__(self,grid): #constructor(yapıcı) metod tanımlandı.
        self.grid = grid
        self.kaynak = tk.Tk()
        self.kaynak.title('2048')
        self.arkaplan = tk.Frame(self.kaynak, bg=OyunPaneli.ARKAPLAN_RENGI)
        self.hucre_etiketi = []
        for i in range(self.grid.size):
            satir_etiketi = []
            for j in range(self.grid.size):
                label = tk.Label(self.arkaplan,text='',
                                   bg= OyunPaneli.BOS_HUCRE_RENGI,
                                   justify=tk.CENTER, font=OyunPaneli.FONT,
                                   width= 4 , height = 2)
                label.grid(row = i,column = j, padx=10,pady=10)
                satir_etiketi.append(label)
            self.hucre_etiketi.append(satir_etiketi)
        self.arkaplan.grid()


    def renk(self):   #gerekli renk işlemleri yapıldı.
        for i in range(self.grid.size):
            for j in range (self.grid.size):
                if self.grid.hucreler[i][j] == 0:
                    self.hucre_etiketi[i][j].configure(
                        text = '',
                        bg = OyunPaneli.BOS_HUCRE_RENGI)
                else:
                    hucre_text = str(self.grid.hucreler[i][j])
                    if self.grid.hucreler[i][j] > 2048:
                        bg_rengi = OyunPaneli.HUCRE_ARKAPLAN_RENGI_KILAVUZ.get('beyond')
                        fg_rengi = OyunPaneli.HUCRE_RENGI_KILAVUZ.get('beyond')
                    else:
                        bg_rengi = OyunPaneli.HUCRE_ARKAPLAN_RENGI_KILAVUZ.get(hucre_text)
                        fg_rengi = OyunPaneli.HUCRE_RENGI_KILAVUZ.get(hucre_text)
                    self.hucre_etiketi[i][j].configure(
                        text = hucre_text,
                        bg = bg_rengi,
                        fg = fg_rengi)

class Oyun:     #asıl oyum mekaniginin bulundugu sınıf
    def __init__(self,grid,panel):
        self.grid = grid
        self.panel = panel
        self.baslangic_hucre_sayisi = 2
        self.bitis = False
        self.galibiyet = False
        self.oyuna_devam = False

    def oyun_sonlandi_mi(self): #yapılacak hamle var mı yok mu kontrol eder.
        return self.bitis or (self.galibiyet and (not self.oyuna_devam))

    def start(self): #programın baslama fonksiyonu
        self.baslangic_hucre_ekle()
        self.panel.renk()
        self.panel.kaynak.bind('<Key>',self.tus_isleyici)       #bind fonksiyonu görsel bileşenler ile olaylar arasında bağlantı sağlar
        self.panel.kaynak.mainloop()

    def baslangic_hucre_ekle(self): #pencereye eklenecek hucreleri belirleyen metod
        for i in range(self.baslangic_hucre_sayisi):
            self.grid.random_hucre()

    def hareket_edebilme(self): #sayıların hareket edip edemedigini kontrol eder.
        return self.grid.bos_hucre_varsa() or self.grid.birlesebilir()

    def tus_isleyici(self,event):      #programdaki sayıların hareketini saglamak icin klavye ile baglantı kurar.

        if self.oyun_sonlandi_mi():
            return

        self.grid.temizle_bayrak()
        tus_degeri = event.keysym
        print('{} tuş basıldı.'.format(tus_degeri))
        if tus_degeri in OyunPaneli.YUKARI_TUS:
            self.up()
        elif tus_degeri in OyunPaneli.SOLA_TUS:
            self.left()
        elif tus_degeri in OyunPaneli.ASAGI_TUS:
            self.down()
        elif tus_degeri in OyunPaneli.SAGA_TUS:
            self.right()
        else:
            pass

        self.panel.renk()
        print('Skor: {}'.format(self.grid.puan))
        if self.grid.ulasmak_2048():
            self.kazandin()
            if not self.oyuna_devam:
                return
        if self.grid.hareket:
            self.grid.random_hucre()

        self.panel.renk()
        if not self.hareket_edebilme():
            self.bitis = True
            self.oyun_bitti()

    def kazandin(self):
        if not self.galibiyet:
            self.galibiyet = True
            print('Kazandın! :)')
            if messagebox.askyesno('2048','KAZANDIN!'):
                self.oyuna_devam = True

    def oyun_bitti(self):
        print('Oyun Bitti :( ')
        messagebox.showinfo('2048','Oyun Bitti :(')

    def up(self):               #yukari gitme hareket mekanigi
        self.grid.birlestirme()
        self.grid.artik_sikisma()
        self.grid.artik_birlesme()
        self.grid.hareket = self.grid.sikisma or self.grid.birlesme
        self.grid.artik_sikisma()
        self.grid.birlestirme()
    def left(self):            #sola gitme hareket mekanigi
        self.grid.artik_sikisma()
        self.grid.artik_birlesme()
        self.grid.hareket = self.grid.sikisma or self.grid.birlesme
        self.grid.artik_sikisma()
    def down(self):             #asagi gitme hareket mekanigi
        self.grid.birlestirme()
        self.grid.ters_cevirme()
        self.grid.artik_sikisma()
        self.grid.artik_birlesme()
        self.grid.hareket = self.grid.sikisma or self.grid.birlesme
        self.grid.artik_sikisma()
        self.grid.ters_cevirme()
        self.grid.birlestirme()
    def right(self):            #saga gitme hareket mekanigi
        self.grid.ters_cevirme()
        self.grid.artik_sikisma()
        self.grid.artik_birlesme()
        self.grid.hareket = self.grid.sikisma or self.grid.birlesme
        self.grid.artik_sikisma()
        self.grid.ters_cevirme()

if __name__ == '__main__':
    size = 4
    grid = Pencere(size)
    panel = OyunPaneli(grid)
    oyun_2048 = Oyun(grid,panel)
    oyun_2048.start()
