from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt
from googletrans import Translator
from languages import LANGUAGES, LANGCODES

# Class Build
class Home(QWidget):
    # Constructor
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.initUI()
        self.settings()
        # Connect buttons to their functions here
        self.button_events()

    # App Object and Design
    def initUI(self):
        self.setWindowTitle("The Babel Fish")

        # --- UI Elements ---
        # Input/Output text boxes
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("Enter text to translate...")
        self.output_box = QTextEdit()
        self.output_box.setPlaceholderText("Translation will appear here...")
        self.output_box.setReadOnly(True)

        # Buttons
        self.reverse_button = QPushButton("Reverse")
        self.reset = QPushButton("Reset")
        self.submit = QPushButton("Translate Now")

        # Language selection
        self.input_option = QComboBox()
        self.output_option = QComboBox()
        self.title = QLabel("The\n Babel\n Fish")
        self.title.setAlignment(Qt.AlignCenter)

        # Populate the language dropdowns
        sorted_languages = sorted(lang.title() for lang in LANGUAGES.values())
        self.input_option.addItem("Auto Detect")
        self.input_option.addItems(sorted_languages)
        self.output_option.addItems(sorted_languages)
        
        # Set default selections
        self.input_option.setCurrentText("English")
        self.output_option.setCurrentText("Spanish")

        # --- Layouts ---
        # Master layout
        self.master = QHBoxLayout()

        # Column 1 (Controls)
        col1 = QVBoxLayout()
        col1.addWidget(self.title)
        
        # Add a frame around the controls for better visual separation
        control_frame = QFrame()
        control_frame.setFrameShape(QFrame.StyledPanel)
        
        control_layout = QVBoxLayout(control_frame)
        control_layout.addWidget(QLabel("Source Language:"))
        control_layout.addWidget(self.input_option)
        control_layout.addWidget(QLabel("Destination Language:"))
        control_layout.addWidget(self.output_option)
        control_layout.addSpacing(15)
        control_layout.addWidget(self.submit)
        control_layout.addWidget(self.reset)
        
        col1.addWidget(control_frame)
        col1.addStretch(1)

        # Column 2 (Text areas and reverse button)
        col2 = QVBoxLayout()
        col2.addWidget(self.input_box)
        col2.addWidget(self.reverse_button, alignment=Qt.AlignCenter)
        col2.addWidget(self.output_box)

        # Set stretch factors for the main layout
        self.master.addLayout(col1, 33)
        self.master.addLayout(col2, 66)

        self.setLayout(self.master)
        
        # --- Dark Theme Styling with Gradients ---
        # Main widget background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #131221, stop:1 #3a1c71);
                color: #e0b0ff;
                font-family: Arial;
            }
            QLabel {
                color: #e0b0ff;
                font-size: 25px;
                font-weight: 800;
            }
            #QuickTranslate {
                color: #ecf0f1;
            }
            QPushButton {
                background: #5d429a;
                color: #e0b0ff;
                border: 2px solid #e0b0ff;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8e2de2, stop:1 #4a00e0);
                color: #ffffff;
            }
            QComboBox, QTextEdit {
                background-color: #262130;
                color: #e0b0ff;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                padding: 5px;
            }
            QFrame {
                background-color: rgba(30, 20, 50, 0.5);
                border: 2px solid #5d429a;
                border-radius: 10px;
            }
            QTextEdit {
                color: #e0b0ff;
                border: 1px solid #7f8c8d;
                background-color: rgba(30, 20, 50, 0.7);
            }
        """)

    # App Settings
    def settings(self):
        self.setGeometry(250,250,800,600)

    # Button Events
    def button_events(self):
        self.submit.clicked.connect(self.translate_text)
        self.reset.clicked.connect(self.reset_app)
        self.reverse_button.clicked.connect(self.reverse)

    #Translate Text
    def translate_text(self):
        text_to_translate = self.input_box.toPlainText()
        if not text_to_translate:
            self.output_box.setText("Please enter text to translate.")
            return

        # Get language codes from the text of the combo boxes
        src_lang = LANGCODES.get(self.input_option.currentText().lower(), "auto")
        dest_lang = LANGCODES.get(self.output_option.currentText().lower(), "en")
        
        try:
            translation = self.translator.translate(text_to_translate, dest=dest_lang, src=src_lang)
            self.output_box.setText(translation.text)
        except Exception as e:
            self.output_box.setText(f"An error occurred: {e}. Please check your internet connection or try again later.")
            
    # Reset App
    def reset_app(self):
        self.input_box.clear()
        self.output_box.clear()

    #Reverse Translation
    def reverse(self):
        s1, l1 = self.input_box.toPlainText(),self.input_option.currentText()
        s2, l2 = self.output_box.toPlainText(),self.output_option.currentText()

        self.input_box.setText(s2)
        self.output_box.setText(s1)

        self.input_option.setCurrentText(l2)
        self.output_option.setCurrentText(l1)
        self.translate_text()


# Main Run
if __name__ == "__main__":
    app = QApplication([])
    main = Home()
    main.show()
    app.exec()
