import time

class PerformansAnalizi:
    """Arama, Ekleme ve Silme (CRUD) performanslarını Hash ve List için kıyaslar."""
    
    @staticmethod
    def crud_testi_ciz(fig):
        boyutlar = [1000, 5000, 10000, 20000]
        hash_ekle, list_ekle = [], []
        hash_ara, list_ara = [], []
        hash_sil, list_sil = [], []
        
        for boyut in boyutlar:
            test_dict = {}
            test_list = []
            
            # 1. EKLEME TESTİ
            b = time.perf_counter()
            for i in range(boyut): test_dict[f"ID{i}"] = i
            hash_ekle.append(time.perf_counter() - b)
            
            b = time.perf_counter()
            for i in range(boyut): test_list.append(f"ID{i}")
            list_ekle.append(time.perf_counter() - b)
            
            aranan = f"ID{boyut-1}" # Worst Case
            
            # 2. ARAMA TESTİ
            b = time.perf_counter()
            _ = test_dict.get(aranan)
            hash_ara.append(time.perf_counter() - b)
            
            b = time.perf_counter()
            _ = aranan in test_list
            list_ara.append(time.perf_counter() - b)
            
            # 3. SİLME TESTİ
            b = time.perf_counter()
            del test_dict[aranan]
            hash_sil.append(time.perf_counter() - b)
            
            b = time.perf_counter()
            test_list.remove(aranan) # O(N) Maliyeti
            list_sil.append(time.perf_counter() - b)

        fig.clear()
        
        # Ekleme Grafiği
        ax1 = fig.add_subplot(131)
        ax1.plot(boyutlar, hash_ekle, 'g-o', label='Hash O(1)')
        ax1.plot(boyutlar, list_ekle, 'r-x', label='List O(N)')
        ax1.set_title("Ekleme Süresi", color="white")
        ax1.tick_params(colors='white')
        ax1.legend()

        # Arama Grafiği
        ax2 = fig.add_subplot(132)
        ax2.plot(boyutlar, hash_ara, 'g-o', label='Hash O(1)')
        ax2.plot(boyutlar, list_ara, 'r-x', label='List O(N)')
        ax2.set_title("Arama Süresi", color="white")
        ax2.tick_params(colors='white')
        ax2.legend()

        # Silme Grafiği
        ax3 = fig.add_subplot(133)
        ax3.plot(boyutlar, hash_sil, 'g-o', label='Hash O(1)')
        ax3.plot(boyutlar, list_sil, 'r-x', label='List O(N)')
        ax3.set_title("Silme Süresi", color="white")
        ax3.tick_params(colors='white')
        ax3.legend()

        # Genel figür arkaplanını ayarla
        fig.patch.set_facecolor('#1e1e2e')
        for ax in [ax1, ax2, ax3]: ax.set_facecolor('#313244')
        
        fig.tight_layout()