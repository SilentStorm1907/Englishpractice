import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QTableWidget, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt

# Veritabanına bağlanma
conn = sqlite3.connect('Englishpractice.db')
cursor = conn.cursor()

# Veritabanı Tablosu (eğer yoksa)
cursor.execute('''CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turkish_word TEXT,
                    english_word TEXT,
                    pronunciation TEXT,
                    example_sentence TEXT,
                    collocations TEXT,
                    synonyms TEXT,
                    category TEXT,
                    level TEXT)''')

# Flashcard Ekleme Fonksiyonu
def add_flashcard(turkish, english, pronunciation, sentence, collocations, synonyms, category, level):
    cursor.execute('''INSERT INTO flashcards (turkish_word, english_word, pronunciation, example_sentence, 
                                               collocations, synonyms, category, level)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (turkish, english, pronunciation, sentence, collocations, synonyms, category, level))
    conn.commit()

# Flashcard'ları Listeleme Fonksiyonu
def get_flashcards():
    cursor.execute("SELECT * FROM flashcards")
    return cursor.fetchall()

class FlashcardApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flashcard Uygulaması")
        self.setGeometry(100, 100, 800, 600)
        
        self.layout = QVBoxLayout()

        self.add_flashcard_button = QPushButton('Flashcard Ekle')
        self.add_flashcard_button.clicked.connect(self.open_add_flashcard_dialog)
        self.layout.addWidget(self.add_flashcard_button)

        self.show_flashcards_button = QPushButton('Flashcard Listele')
        self.show_flashcards_button.clicked.connect(self.display_flashcards)
        self.layout.addWidget(self.show_flashcards_button)

        self.study_flashcards_button = QPushButton('Kartları Çalıştır')
        self.study_flashcards_button.clicked.connect(self.study_flashcards)
        self.layout.addWidget(self.study_flashcards_button)

        self.setLayout(self.layout)

        self.flashcards = []  # Başlangıçta boş flashcard listesi
        self.current_card_index = 0
        self.card_widget = None  # Kart widget'ını dışarıda tanımlıyoruz

    def study_flashcards(self):
        if not self.flashcards:  # Eğer flashcards listesi boşsa
            print("Flashcard listesi boş. Lütfen önce flashcard ekleyin.")
            return  # Flashcard'lar olmadan devam etme
        
        if self.card_widget is None:
            self.show_card(self.current_card_index)  # İlk kartı göster
        else:
            self.update_card(self.current_card_index)  # Kartı güncelle

    def show_card(self, index):
        if index >= len(self.flashcards):  # Eğer index listeden büyükse, döngüye devam etme
            print("Geçersiz kart indeksi.")
            return

        card = self.flashcards[index]
        self.card_widget = QWidget()
        self.card_layout = QVBoxLayout()

        # Kartın ön yüzü (Türkçe kelime)
        self.card_front_label = QLabel(f"Türkçe: {card[1]}")
        self.card_front_label.setAlignment(Qt.AlignCenter)  # Ortaya hizalama
        self.card_layout.addWidget(self.card_front_label)

        # Kartın arka yüzü (İngilizce kelime ve diğer bilgiler)
        self.card_back_label = QLabel(f"İngilizce: {card[2]}\nTelaffuz: {card[3]}\nÖrnek Cümle: {card[4]}\nCollocations: {card[5]}\nSynonyms: {card[6]}\nKategori: {card[7]}\nSeviye: {card[8]}")
        self.card_back_label.setAlignment(Qt.AlignCenter)  # Ortaya hizalama
        self.card_back_label.setVisible(False)  # Başlangıçta arka yüz gizli olacak
        self.card_layout.addWidget(self.card_back_label)

        # Kartı çevirmek için buton
        self.toggle_button = QPushButton("Kartı Çevir")
        self.toggle_button.clicked.connect(self.toggle_card)
        self.card_layout.addWidget(self.toggle_button)

        # Önceki ve sonraki kartlara geçiş için butonlar
        self.prev_button = QPushButton("Önceki Kart")
        self.prev_button.clicked.connect(self.prev_card)
        self.card_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Sonraki Kart")
        self.next_button.clicked.connect(self.next_card)
        self.card_layout.addWidget(self.next_button)

        self.card_widget.setLayout(self.card_layout)
        self.setLayout(self.card_layout)
        self.card_widget.show()

    def update_card(self, index):
        card = self.flashcards[index]

        # Kartı güncelleme
        self.card_front_label.setText(f"Türkçe: {card[1]}")
        self.card_back_label.setText(f"İngilizce: {card[2]}\nTelaffuz: {card[3]}\nÖrnek Cümle: {card[4]}\nCollocations: {card[5]}\nSynonyms: {card[6]}\nKategori: {card[7]}\nSeviye: {card[8]}")

        # Başlangıçta sadece ön yüzü gösterelim
        self.card_back_label.setVisible(False)
        self.card_front_label.setVisible(True)

    def toggle_card(self):
        # Kartı çevir
        if self.card_back_label.isVisible():
            self.card_back_label.setVisible(False)
            self.card_front_label.setVisible(True)
        else:
            self.card_back_label.setVisible(True)
            self.card_front_label.setVisible(False)

    def prev_card(self):
        # Önceki karta git
        if self.current_card_index > 0:
            self.current_card_index -= 1
            self.update_card(self.current_card_index)

    def next_card(self):
        # Sonraki karta git
        if self.current_card_index < len(self.flashcards) - 1:
            self.current_card_index += 1
            self.update_card(self.current_card_index)

    def open_add_flashcard_dialog(self):
        self.dialog = AddFlashcardDialog(self)
        self.dialog.show()

    def display_flashcards(self):
        flashcards = get_flashcards()
        self.flashcards = flashcards
        
        self.table = QTableWidget()
        self.table.setRowCount(len(flashcards))
        self.table.setColumnCount(9)
        
        for row, flashcard in enumerate(flashcards):
            for col, data in enumerate(flashcard[1:]):  # flashcard[1:] 1. index'ten itibaren
                self.table.setItem(row, col, QTableWidgetItem(str(data)))
        
        self.table.setHorizontalHeaderLabels(["Türkçe Kelime", "İngilizce Kelime", "Telaffuz", "Örnek Cümle", 
                                              "Collocations", "Synonyms", "Kategori", "Seviye"] )
        
        self.table.show()

class AddFlashcardDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Flashcard Ekle")
        self.setGeometry(150, 150, 400, 300)
        
        self.layout = QFormLayout()

        self.turkish_input = QLineEdit()
        self.layout.addRow("Türkçe Kelime:", self.turkish_input)

        self.english_input = QLineEdit()
        self.layout.addRow("İngilizce Kelime:", self.english_input)

        self.pronunciation_input = QLineEdit()
        self.layout.addRow("Telaffuz:", self.pronunciation_input)

        self.sentence_input = QLineEdit()
        self.layout.addRow("Örnek Cümle:", self.sentence_input)

        self.collocations_input = QLineEdit()
        self.layout.addRow("Collocations:", self.collocations_input)

        self.synonyms_input = QLineEdit()
        self.layout.addRow("Synonyms:", self.synonyms_input)

        self.category_input = QLineEdit()
        self.layout.addRow("Kategori:", self.category_input)

        self.level_input = QLineEdit()
        self.layout.addRow("Seviye:", self.level_input)

        self.submit_button = QPushButton('Kaydet')
        self.submit_button.clicked.connect(self.submit_flashcard)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit_flashcard(self):
        turkish = self.turkish_input.text()
        english = self.english_input.text()
        pronunciation = self.pronunciation_input.text()
        sentence = self.sentence_input.text()
        collocations = self.collocations_input.text()
        synonyms = self.synonyms_input.text()
        category = self.category_input.text()
        level = self.level_input.text()

        # Veritabanına yeni flashcard ekle
        add_flashcard(turkish, english, pronunciation, sentence, collocations, synonyms, category, level)

        # Dialogu kapat
        self.close()

# Uygulamayı başlat
app = QApplication([])
window = FlashcardApp()
window.show()
app.exec_()
