import networkx as nx

class RotaGorsellestirici:
    """Graf veri yapısını PyQt5 Canvas ekseni (ax) üzerine çizer."""
    
    @staticmethod
    def harita_ciz(graf, ax, yol=None):
        ax.clear()
        pos = nx.spring_layout(graf, seed=42, k=2.0)
        
        # Düğüm Renklerini Ayarla
        renk_haritasi = []
        cizgi_renkleri = []
        for dugum in graf.nodes:
            if "Depo" in dugum:
                renk_haritasi.append("#3b82f6") # Profesyonel Mavi
                cizgi_renkleri.append("#1e3a8a") # Koyu Mavi Çerçeve
            else:
                renk_haritasi.append("#ef4444") # Profesyonel Kırmızı
                cizgi_renkleri.append("#7f1d1d") # Koyu Kırmızı Çerçeve

        # Düğümler ve Etiketler
        dugumler = nx.draw_networkx_nodes(graf, pos, ax=ax, node_color=renk_haritasi, node_size=2500, edgecolors=cizgi_renkleri, linewidths=2.5)
        dugumler.set_picker(5)
        nx.draw_networkx_labels(graf, pos, ax=ax, font_color="#11111b", font_weight="bold", font_size=11)
        
        # Rota varsa vurgula, yoksa standart çiz
        if yol:
            yol_kenarlari = list(zip(yol, yol[1:]))
            nx.draw_networkx_edges(graf, pos, ax=ax, edge_color="#45475a", alpha=0.3, width=1)
            nx.draw_networkx_edges(graf, pos, ax=ax, edgelist=yol_kenarlari, edge_color="#f38ba8", width=4)
        else:
            nx.draw_networkx_edges(graf, pos, ax=ax, edge_color="#94A3B8", width=2)
            
        # Ağırlıkları (Mesafe) yaz
        edge_labels = nx.get_edge_attributes(graf, 'weight')
        nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels, ax=ax, font_color="#1E3A8A", font_weight="bold", font_size=10)
        ax.axis('off')