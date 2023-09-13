""" 
App que permite introducir un texto o url en español o ingles y lo convierte a formato voz

@author Ivan Pascual
"""

# Importamos bibliotecas externas
from newspaper import Article
from gtts import gTTS
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import pygame


# Opciones del lenguaje
opcion_language = {
    "Español": "es",
    "Inglés": "en",
}

# Opciones de la voz
option_voice = {
    "Masculino": "male",
    "Femenino": "femele",
}

class TextToSpeech(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversor de un texto/url a voz") # Titulo de la app
        # Definir las variables language_var y voice_var
        self.window_definition()

    def window_definition(self):
        """
        Defino la ventana al completo de la app
        """
        # Menú desplegable para elegir la opción (Texto o URL)
        self.option_label = ttk.Label(self, text="Elige una opción:")
        self.option_label.pack(side=tk.TOP, pady=5)
        self.option_var = tk.StringVar()  # Variable para almacenar la opción seleccionada
        self.option_combobox = ttk.Combobox(self, state="readonly", textvariable=self.option_var, values=["URL", "TEXTO"])
        self.option_combobox.pack(side=tk.TOP)

        # Menu desplegable para elegir el idioma (Ingles o español)
        self.language_label = ttk.Label(self, text="Selecciona el idioma:")
        self.language_label.pack(side=tk.TOP, pady=5)
        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(self, state="readonly", textvariable=self.language_var, values=["Inglés", "Español"])
        self.language_combobox.pack(side=tk.TOP)

        # Área de entrada de texto para el usuario o para introducir la url
        self.input_text_label = ttk.Label(self, text="Ingresa el texto o URL en el idioma que haya indicado:")
        self.input_text_label.pack(padx=10, pady=5)
        self.input_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=10, width=50)
        self.input_text.pack(pady=5)

        # Botón para reproducir el texto o la pagina a voz
        self.play_button = ttk.Button(self, text="Reproducir", command=self.play_audio)
        self.play_button.pack(side=tk.LEFT, padx=10, pady=10)  # Alineado a la izquierda

        # Botón para salir
        self.quit_button = ttk.Button(self, text="Salir", command=self.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=10, pady=10)  # Alineado a la derecha
        
    def play_audio(self):
        try:
            text = self.input_text.get("1.0", "end-1c")

            # Mensale de error si no introduce texto para reproducir
            if not text:
                messagebox.showerror("Error", "Por favor ingresa un texto para convertir en voz.")
                return
            
            selected_option = self.option_var.get()  # Obtén la opción seleccionada (Texto o URL)
            language = opcion_language[self.language_var.get()]  # Obtén el código de idioma
            
            if selected_option == "URL":
                article = Article(text)
                article.download()
                article.parse()
                text = article.text  # Obtén el contenido de la URL

            # Convertir el texto a voz
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save("audio.mp3")

            # Reproducir el audio usando pygame
            pygame.mixer.init()
            pygame.mixer.music.load("audio.mp3")
            pygame.mixer.music.play()

            # Mantener la aplicación en espera hasta que termine de reproducirse el audio
            while pygame.mixer.music.get_busy():
                continue
            
            # Finalizo el proceso de audio
            pygame.mixer.quit()

        except Exception as e:
            # Mostrar mensaje de error en caso de problemas
            messagebox.showerror("Error", f"Hubo un problema: {str(e)}")

app = TextToSpeech()
app.mainloop()


