""" 
Programa que convierte un archivo en formato texto a un archivo en formato audio

@author Ivan Pascual
"""

# Importamos bibliotecas externas
import nltk
from newspaper import Article
from gtts import gTTS

fichero = open("texto_a_convertir.txt", "r")
tts = gTTS(fichero.read(), lang="es-es")
tts.save("audio.mp3")
