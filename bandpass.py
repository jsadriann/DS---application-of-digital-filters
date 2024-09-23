# import numpy as np
# import librosa
# from scipy.signal import butter, lfilter
# import soundfile as sf
# import matplotlib.pyplot as plt
# from moviepy.editor import VideoFileClip

# # Função para calcular a potência de um sinal (usando np.square para garantir o cálculo correto)
# def potencia_sinal(sinal):
#     return np.mean(np.square(sinal))

# # Definir o filtro passa-banda
# def butter_bandpass(lowcut, highcut, fs, order=5):
#     nyq = 0.5 * fs  # Frequência de Nyquist
#     low = lowcut / nyq
#     high = highcut / nyq
#     b, a = butter(order, [low, high], btype='band', analog=False)
#     return b, a

# def bandpass_filter(data, lowcut, highcut, fs, order=5):
#     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
#     y = lfilter(b, a, data)
#     return y

# # Função para plotar o espectro de frequências
# def plot_spectrum(audio, sr):
#     freqs = np.fft.rfftfreq(len(audio), 1/sr)
#     fft_values = np.fft.rfft(audio)
#     magnitude = np.abs(fft_values)
    
#     plt.figure(figsize=(10, 6))
#     plt.plot(freqs, magnitude)
#     plt.title("Espectro de Frequências do Áudio")
#     plt.xlabel("Frequência (Hz)")
#     plt.ylabel("Magnitude")
#     plt.xlim(0, sr/2)  # Limite até a frequência de Nyquist
#     plt.grid(True)
#     plt.show()

# # Extrair áudio de arquivo MP4
# def extract_audio_from_mp4(mp4_file, output_wav_file):
#     video = VideoFileClip(mp4_file)
#     audio = video.audio
#     audio.write_audiofile(output_wav_file, codec='pcm_s16le')

# # Caminho para o arquivo de vídeo
# arquivo_video = 'teste.mp4'
# arquivo_audio_extraido = 'audio_extraido.wav'

# # Extrair o áudio do arquivo MP4
# extract_audio_from_mp4(arquivo_video, arquivo_audio_extraido)

# # Carregar o arquivo de áudio extraído
# audio, sr = librosa.load(arquivo_audio_extraido, sr=None)

# # Verificar valores de amplitude para garantir que não estão muito baixos
# print(f"Valor máximo do sinal: {np.max(audio)}")
# print(f"Valor mínimo do sinal: {np.min(audio)}")

# # Exibir a taxa de amostragem
# print(f'Taxa de amostragem: {sr} Hz')

# # Aplicar Filtro Passa-Banda
# lowcut = 10.0  # Ajuste a frequência de corte inferior
# highcut = 20000.0  # Frequência de corte superior
# audio_filtrado_bandpass = bandpass_filter(audio, lowcut, highcut, sr, order=5)

# # Salvar o áudio filtrado final
# sf.write('audio_filtrado_final.wav', audio_filtrado_bandpass, sr)

# # Estimar o ruído usando os primeiros 0.5 segundos do áudio original
# inicio_ruido = 0
# fim_ruido = int(.5 * sr)  # 0.5 segundos de áudio para estimar o ruído
# ruido_est = audio[inicio_ruido:fim_ruido]
# ruido_filted = audio_filtrado_bandpass[inicio_ruido:fim_ruido]

# # Calcular a potência do sinal e do ruído antes da filtragem
# potencia_ruido_antes = potencia_sinal(ruido_est)

# # Calcular a potência do sinal e do ruído depois da filtragem
# potencia_ruido_depois = potencia_sinal(audio_filtrado_bandpass[inicio_ruido:fim_ruido])

# # Mostrar as potências calculadas
# print(f"Potência do ruído antes da filtragem: {potencia_ruido_antes:.6f}")
# print(f"Potência do ruído depois da filtragem: {potencia_ruido_depois:.6f}")

# # Visualizar o espectro de frequências do áudio filtrado e do original
# plot_spectrum(audio, sr)
# plot_spectrum(audio_filtrado_bandpass, sr)




# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal import butter, lfilter
# import soundfile as sf
# from moviepy.editor import VideoFileClip

# # Função para plotar o espectro de frequências
# def plot_spectrum(audio, sr):
#     freqs = np.fft.rfftfreq(len(audio), 1/sr)
#     fft_values = np.fft.rfft(audio)
#     magnitude = np.abs(fft_values)
    
#     plt.figure(figsize=(10, 6))
#     plt.plot(freqs, magnitude)
#     plt.title("Espectro de Frequências do Áudio")
#     plt.xlabel("Frequência (Hz)")
#     plt.ylabel("Magnitude")
#     plt.xlim(0, sr/2)  # Limite até a frequência de Nyquist
#     plt.grid(True)
#     plt.show()


# # Função para criar um filtro rejeita-banda
# def butter_bandstop(lowcut, highcut, fs, order=4):
#     nyquist = 0.5 * fs
#     low = lowcut / nyquist
#     high = highcut / nyquist
#     b, a = butter(order, [low, high], btype='bandstop')
#     return b, a

# def bandstop_filter(data, lowcut, highcut, fs, order=4):
#     b, a = butter_bandstop(lowcut, highcut, fs, order=order)
#     y = lfilter(b, a, data)
#     return y

# # Extrair áudio de arquivo MP4
# def extract_audio_from_mp4(mp4_file, output_wav_file):
#     video = VideoFileClip(mp4_file)
#     audio = video.audio
#     audio.write_audiofile(output_wav_file, codec='pcm_s16le')

# # Carregar o arquivo de áudio
# def load_audio(file_path):
#     data, sample_rate = sf.read(file_path)
#     # Se for estéreo, converter para mono para simplificar
#     if len(data.shape) > 1:
#         data = np.mean(data, axis=1)
#     return data, sample_rate

# # Caminho para o arquivo de vídeo
# arquivo_video = 'teste.mp4'
# arquivo_audio_extraido = 'audio_extraido.wav'

# # Extrair o áudio do arquivo MP4
# extract_audio_from_mp4(arquivo_video, arquivo_audio_extraido)

# # Carregar o arquivo de áudio extraído
# audio, sr = load_audio(arquivo_audio_extraido)

# # Definir a faixa de frequências para atenuar (frequências típicas da voz humana)
# lowcut = 200.0  # Frequência de corte inferior
# highcut = 4000.0  # Frequência de corte superior

# # Aplicar o filtro rejeita-banda para remover a voz
# audio_vocal_removed = bandstop_filter(audio, lowcut, highcut, sr, order=4)

# # Salvar o áudio com a voz removida
# sf.write('musica_sem_voz_filtrada.wav', audio_vocal_removed, sr)

# plot_spectrum(audio, sr)
# plot_spectrum(audio_vocal_removed, sr)



import numpy as np
from scipy.signal import butter, lfilter
import soundfile as sf
import matplotlib.pyplot as plt

def potencia_sinal(sinal):
    return np.mean(np.square(sinal))

def butter_bandpass(lowcut, highcut, fs, order=6):

    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=6):

    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Caminho para o arquivo de áudio com ruído
input_audio_noisy_path = 'audio_ruido.wav'
output_audio_filtered_path = 'audio_bandpass_filted.wav'

# Carregar o sinal de áudio com ruído
audio_noisy, sr = sf.read(input_audio_noisy_path)

# Definir a faixa de frequências para o filtro passa-banda
lowcut = 300.0  # Frequência de corte inferior
highcut = 3000.0  # Frequência de corte superior

# Aplicar o filtro passa-banda para recuperar o áudio
audio_filtered = bandpass_filter(audio_noisy, lowcut, highcut, sr, order=5)

# Salvar o áudio filtrado
sf.write(output_audio_filtered_path, audio_filtered, sr)

# Plotar o espectro de frequências do áudio com ruído e do áudio filtrado
def plot_spectrum(audio, sr, title):
    freqs = np.fft.rfftfreq(len(audio), 1/sr)
    fft_values = np.fft.rfft(audio)
    magnitude = np.abs(fft_values)
    
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, magnitude)
    plt.title(title)
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.show()

def plot_audio_waveforms(original_audio, noisy_audio, sr):
    """
    Plota as formas de onda do áudio original e do áudio com ruído.

    :param original_audio: numpy array do áudio original.
    :param noisy_audio: numpy array do áudio com ruído.
    :param sr: Taxa de amostragem do áudio.
    """
    # Gerar o eixo do tempo para os dois sinais
    times = np.arange(len(original_audio)) / sr

    # Plotar a forma de onda do áudio original
    plt.figure(figsize=(14, 6))
    
    # Áudio original
    plt.subplot(2, 1, 1)
    plt.plot(times, original_audio)
    plt.title("Áudio com ruido")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    
    # Áudio com ruído
    plt.subplot(2, 1, 2)
    plt.plot(times, noisy_audio)
    plt.title("Áudio filtrado")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

def plot_audio_waveformsZoom(original_audio, noisy_audio, sr, start_time=0, duration=5):
    """
    Plota as formas de onda do áudio original e do áudio com ruído com zoom.

    :param original_audio: numpy array do áudio original.
    :param noisy_audio: numpy array do áudio com ruído.
    :param sr: Taxa de amostragem do áudio.
    :param start_time: Tempo de início (em segundos) para o zoom.
    :param duration: Duração (em segundos) para o zoom.
    """
    # Índices para a seleção do segmento
    start_sample = int(start_time * sr)
    end_sample = start_sample + int(duration * sr)
    
    # Gerar o eixo do tempo para os dois sinais
    times = np.arange(len(original_audio)) / sr

    # Plotar a forma de onda do áudio original (com zoom)
    plt.figure(figsize=(14, 6))
    
    # Áudio original
    plt.subplot(2, 1, 1)
    plt.plot(times[start_sample:end_sample], original_audio[start_sample:end_sample])
    plt.title("Áudio com ruído (Zoom)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    
    # Áudio com ruído (com zoom)
    plt.subplot(2, 1, 2)
    plt.plot(times[start_sample:end_sample], noisy_audio[start_sample:end_sample])
    plt.title("Áudio  filtrado (Zoom)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()



# Estimar o ruído usando os primeiros 0.5 segundos do áudio original
inicio_ruido = 0
fim_ruido = int(.5 * sr)  # 0.5 segundos de áudio para estimar o ruído
ruido_est = audio_noisy[inicio_ruido:fim_ruido]
ruido_filted = audio_filtered[inicio_ruido:fim_ruido]

# Calcular a potência do sinal e do ruído antes da filtragem
potencia_ruido_antes = potencia_sinal(ruido_est)

# Calcular a potência do sinal e do ruído depois da filtragem
potencia_ruido_depois = potencia_sinal(audio_filtered[inicio_ruido:fim_ruido])

# Mostrar as potências calculadas
print(f"Potência do ruído antes da filtragem: {potencia_ruido_antes:.6f}")
print(f"Potência do ruído depois da filtragem: {potencia_ruido_depois:.6f}")

plot_spectrum(audio_noisy, sr, "Espectro de Frequências - Áudio com Ruído")
plot_spectrum(audio_filtered, sr, "Espectro de Frequências - Áudio Passa-Banda Filtrado")
plot_audio_waveforms(audio_noisy, audio_filtered, sr)
plot_audio_waveformsZoom(audio_noisy, audio_filtered, sr)
print(f"Áudio filtrado salvo em: {output_audio_filtered_path}")
