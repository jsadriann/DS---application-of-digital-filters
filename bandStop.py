import numpy as np
from scipy.signal import butter, lfilter
import soundfile as sf
import matplotlib.pyplot as plt

def calcular_snr(signal_power, noise_power):
    """
    Calcula a Relação Sinal-Ruído (SNR) em decibéis (dB).
    
    :param signal_power: Potência do sinal útil.
    :param noise_power: Potência do ruído.
    :return: SNR em decibéis.
    """
    return 10 * np.log10(signal_power / noise_power)


def potencia_sinal(sinal):
    return np.mean(np.square(sinal))

def butter_bandstop(lowcut, highcut, fs, order=4):

    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a

def bandstop_filter(data, lowcut, highcut, fs, order=4):

    b, a = butter_bandstop(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Caminho para o arquivo de áudio com ruído
input_audio_noisy_path = 'audio_ruido.wav'
output_audio_filtered_path = 'audio_bandstop_filtered.wav'

# Carregar o sinal de áudio com ruído
audio_noisy, sr = sf.read(input_audio_noisy_path)

# Definir a faixa de frequências para o filtro rejeita-banda (4000 Hz a 8000 Hz)
lowcut = 2200.0  # Frequência de corte inferior
highcut = 10000.0  # Frequência de corte superior

# Aplicar o filtro rejeita-banda para remover o ruído nessa faixa
audio_filtered = bandstop_filter(audio_noisy, lowcut, highcut, sr, order=15)

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

# Calcular a potência do sinal útil (usando o sinal completo)
potencia_sinal_util = potencia_sinal(audio_noisy)

# Calcular a potência do ruído antes da filtragem
potencia_ruido_antes = potencia_sinal(ruido_est)

# Calcular a potência do ruído depois da filtragem
potencia_ruido_depois = potencia_sinal(audio_filtered[inicio_ruido:fim_ruido])

# Calcular SNR antes e depois da filtragem
snr_antes = calcular_snr(potencia_sinal_util, potencia_ruido_antes)
snr_depois = calcular_snr(potencia_sinal_util, potencia_ruido_depois)

# Mostrar as potências e SNR calculadas
print(f"Frequencia de Amostragem: {sr:.2f}")
print(f"Potência do ruído antes da filtragem: {potencia_ruido_antes:.6f}")
print(f"Potência do ruído depois da filtragem: {potencia_ruido_depois:.6f}")
print(f"SNR antes da filtragem: {snr_antes:.2f} dB")
print(f"SNR depois da filtragem: {snr_depois:.2f} dB")

# Plotar espectros e formas de onda
plot_spectrum(audio_noisy, sr, "Espectro de Frequências - Áudio com Ruído")
plot_spectrum(audio_filtered, sr, "Espectro de Frequências - Áudio Filtrado")
plot_audio_waveforms(audio_noisy, audio_filtered, sr)
plot_audio_waveformsZoom(audio_noisy, audio_filtered, sr)

print(f"Áudio filtrado salvo em: {output_audio_filtered_path}")

