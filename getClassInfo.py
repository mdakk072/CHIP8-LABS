import numpy as np
import matplotlib.pyplot as plt

def square_wave(t, T):
    return np.where(np.mod(t, T) < T/2, 1, -1)

def rectangular_pulse_train(t, T, duty_cycle):
    t_mod = np.mod(t, T)
    return np.where(t_mod < T * duty_cycle, 1, 0)

def sawtooth_wave(t, T):
    return 2 * (t/T - np.floor(0.5 + t/T))

def triangular_pulse_train(t, T, duty_cycle):
    t_mod = np.mod(t, T)
    return np.where(t_mod < T * duty_cycle/2, t_mod * 2 / (T * duty_cycle), (T - t_mod) * 2 / (T * (1 - duty_cycle)))

def fourier_series(signal_name, num_terms, T, num_points):
    # Définition du signal
    if signal_name == 'squareWave':
        signal = square_wave
    elif signal_name == 'rectangularpulseTrain':
        signal = rectangular_pulse_train
    elif signal_name == 'SawtoothWave':
        signal = sawtooth_wave
    elif signal_name == 'triangularpulseTrain':
        signal = triangular_pulse_train
    else:
        raise ValueError("Nom de signal invalide")

    # Calcul de la série de Fourier
    a0 = 1 / T * np.trapz(signal(np.linspace(0, T, 1000)), np.linspace(0, T, 1000))
    a = np.zeros(num_terms)
    b = np.zeros(num_terms)
    for n in range(1, num_terms+1):
        a[n-1] = 1 / (T * n) * np.trapz(signal(np.linspace(0, T, 1000)) * np.cos(2*np.pi*n*np.linspace(0, T, 1000)/T), np.linspace(0, T, 1000))
        b[n-1] = 1 / (T * n) * np.trapz(signal(np.linspace(0, T, 1000)) * np.sin(2*np.pi*n*np.linspace(0, T, 1000)/T), np.linspace(0, T, 1000))

    # Calcul de la fonction approximée
    t = np.linspace(0, T, num_points)
    ft = np.zeros(num_points)
    for n in range(1, num_terms+1):
        ft += a[n-1] * np.cos(2*np.pi*n*t/T) + b[n-1] * np.sin(2*np.pi*n*t/T)
    ft += a0 / 2

    # Retourne les tableaux de x et f(x)
    return t, ft


def plot_signal(t, ft):
    plt.plot(t, ft)
    plt.xlabel('Temps')
    plt.ylabel('Signal')
    plt.grid(True)
    plt.show()

# Exemple d'utilisation avec un signal carré
t, ft = fourier_series('squareWave', 100, 5,200)
plot_signal(t, ft)
