import numpy as np
from scipy.signal import butter, lfilter
import soundfile as sf
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip


# Extrair áudio de arquivo MP4
def extract_audio_from_mp4(mp4_file, output_wav_file):
    video = VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(output_wav_file, codec='pcm_s16le')

# Carregar o arquivo de áudio
def load_audio(file_path):
    data, sample_rate = sf.read(file_path)
    # Se for estéreo, converter para mono para simplificar
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    return data, sample_rate

def butter_bandpass(lowcut, highcut, fs, order=4):
    """
    Cria um filtro passa-banda Butterworth.
    
    :param lowcut: Frequência de corte inferior do filtro.
    :param highcut: Frequência de corte superior do filtro.
    :param fs: Taxa de amostragem do áudio.
    :param order: Ordem do filtro.
    :return: Coeficientes do filtro.
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Aplica um filtro passa-banda a um sinal de áudio.
    
    :param data: Sinal de áudio.
    :param lowcut: Frequência de corte inferior do filtro.
    :param highcut: Frequência de corte superior do filtro.
    :param fs: Taxa de amostragem do áudio.
    :param order: Ordem do filtro.
    :return: Sinal de áudio filtrado.
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def add_band_limited_noise(audio, sr, noise_factor=0.05, lowcut=1000.0, highcut=3000.0):
    """
    Adiciona ruído a uma faixa específica de frequências em um sinal de áudio.
    
    :param audio: numpy array contendo o sinal de áudio.
    :param sr: Taxa de amostragem do áudio.
    :param noise_factor: Fator para controlar a amplitude do ruído adicionado.
    :param lowcut: Frequência de corte inferior para o ruído.
    :param highcut: Frequência de corte superior para o ruído.
    :return: Sinal de áudio com ruído adicionado.
    """
    # Gerar ruído branco
    noise = np.random.randn(len(audio))
    
    # Filtrar o ruído para restringi-lo à faixa de frequências desejada
    noise_filtered = bandpass_filter(noise, lowcut, highcut, sr, order=4)
    
    # Adicionar o ruído ao sinal
    audio_noisy = audio + noise_factor * noise_filtered
    # Normalizar para evitar clipping
    audio_noisy = np.clip(audio_noisy, -1.0, 1.0)
    return audio_noisy

# Caminho para o arquivo de vídeo
arquivo_video = 'teste.mp4'
arquivo_audio_extraido = 'audio_ruido.wav'

# Extrair o áudio do arquivo MP4
extract_audio_from_mp4(arquivo_video, arquivo_audio_extraido)

# Carregar o arquivo de áudio extraído
audio, sr = load_audio(arquivo_audio_extraido)

# Adicionar ruído à faixa de frequências específica (1000 Hz a 3000 Hz)
audio_noisy = add_band_limited_noise(audio, sr, noise_factor=0.5, lowcut=4000.0, highcut=8000.0)

# Salvar o novo áudio com ruído
sf.write(arquivo_audio_extraido,audio_noisy, sr)

# Plotar o espectro de frequências do áudio original e do áudio com ruído
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

plot_spectrum(audio, sr, "Espectro de Frequências - Áudio Original")
plot_spectrum(audio_noisy, sr, "Espectro de Frequências - Áudio com Ruído (Faixa Específica)")

print(f"Áudio com ruído adicionado salvo em: {output_audio_noisy_path}")
