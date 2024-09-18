#!/usr/bin/python3

import os
import io
from pydub import AudioSegment
from pydub.playback import play

def play_audio_file(audio_path, fator):
    if os.path.exists(audio_path):
        # Carregar o arquivo de áudio
        audio = AudioSegment.from_file(audio_path)
        
        # Ajustar a velocidade sem alterar o pitch
        audio_modificado = audio.speedup(playback_speed=fator)
        
        # Exportar o áudio para um buffer em memória
        audio_buffer = io.BytesIO()
        audio_modificado.export(audio_buffer, format="wav")
        
        # Reposicionar o cursor no início do buffer
        audio_buffer.seek(0)
        
        # Reproduzir o áudio modificado diretamente do buffer
        play(AudioSegment.from_wav(audio_buffer))

import tempfile
from gtts import gTTS

def text_to_audio_file(text,language):
    tts = gTTS(text=text, lang=language)
    tmp_filename = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_filename.name)
    return tmp_filename.name;

'''
import tempfile
import os    
def play_audio_file_old(audio_path, fator):
    # Carregar o arquivo de áudio
    audio = AudioSegment.from_file(audio_path)
    
    # Ajustar a velocidade sem alterar o pitch
    audio_modificado = audio.speedup(playback_speed=fator)
    
    # Salvar o áudio modificado em um arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_file.close()
    audio_modificado.export(temp_file.name, format="wav")
    
    # Reproduzir o áudio modificado
    with open(temp_file.name, 'rb') as f:
        play(AudioSegment.from_wav(f))
    
    # Remover o arquivo temporário
    os.remove(temp_file.name)
'''

