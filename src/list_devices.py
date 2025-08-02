# src/list_devices.py
import pyaudio

p = pyaudio.PyAudio()

print("--- Listando Dispositivos de Áudio Disponíveis ---")
print("Procure por um dispositivo com 'monitor' ou 'loopback' no nome.\n")

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0: # Filtra apenas dispositivos de ENTRADA (gravação)
        print(f"Índice do Dispositivo: {info['index']}")
        print(f"  Nome: {info['name']}")
        print("-" * 20)

p.terminate()