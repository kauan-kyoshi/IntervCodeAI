import pyaudio
import google.generativeai as genai
import customtkinter as ctk
import os
import threading
from dotenv import load_dotenv
import wave
import io
from queue import Queue

# --- CONFIGURAÇÕES INICIAIS ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

INPUT_DEVICE_INDEX = None # Lembre-se de colocar o índice do seu dispositivo 'monitor' aqui

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Inicializa PyAudio para obter informações
p = pyaudio.PyAudio()
SAMPLE_WIDTH = p.get_sample_size(FORMAT)

if INPUT_DEVICE_INDEX is not None:
    try:
        device_info = p.get_device_info_by_index(INPUT_DEVICE_INDEX)
        CHANNELS = int(device_info['maxInputChannels'])
        RATE = int(device_info['defaultSampleRate'])
        print(f"Usando dispositivo: {device_info['name']} (Canais: {CHANNELS}, Taxa: {RATE})")
    except Exception as e:
        print(f"Não foi possível encontrar o dispositivo de áudio com índice {INPUT_DEVICE_INDEX}. Usando padrão. Erro: {e}")
        INPUT_DEVICE_INDEX = None
p.terminate()

model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
recording = False
audio_queue = Queue()

# --- FUNÇÃO DE GRAVAÇÃO ---
def record_audio():
    global recording
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=1024,
                        input_device_index=INPUT_DEVICE_INDEX)
    
    frames = []
    while recording:
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    audio_queue.put(b''.join(frames))

# --- CLASSE DA APLICAÇÃO GUI ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Assistente de Entrevista IA")
        self.geometry("500x350")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Widgets da interface
        self.status_label = ctk.CTkLabel(self, text="Status: Pronto para ouvir...")
        self.status_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # --- ALTERAÇÃO AQUI ---
        # Adicionado wrap="word" para quebrar linhas entre palavras.
        self.response_textbox = ctk.CTkTextbox(self, state="disabled", font=("Helvetica", 14), wrap="word")
        self.response_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.record_button = ctk.CTkButton(self.button_frame, text="Ouvir Pergunta", command=self.start_recording_thread)
        self.record_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.stop_button = ctk.CTkButton(self.button_frame, text="Parar", command=self.stop_recording_action, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        if INPUT_DEVICE_INDEX is None:
            self.update_status("ATENÇÃO: Nenhum dispositivo de áudio selecionado!", "orange")

    def update_status(self, text, color="white"):
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def update_response(self, text):
        self.response_textbox.configure(state="normal")
        self.response_textbox.delete("1.0", "end")
        self.response_textbox.insert("1.0", text)
        self.response_textbox.configure(state="disabled")

    def start_recording_thread(self):
        global recording
        recording = True
        self.update_status("Ouvindo...")
        self.update_response("")
        self.record_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        threading.Thread(target=record_audio, daemon=True).start()

    def stop_recording_action(self):
        global recording
        recording = False
        self.update_status("Processando com a IA...")
        self.stop_button.configure(state="disabled")
        self.after(100, self.process_audio_from_queue)

    def process_audio_from_queue(self):
        try:
            from queue import Empty
            raw_audio_data = audio_queue.get(block=False)
            threading.Thread(target=self.get_gemini_response, args=(raw_audio_data,), daemon=True).start()
        except Empty:
            self.after(100, self.process_audio_from_queue)

    def get_gemini_response(self, raw_audio_data):
        wav_in_memory = io.BytesIO()
        with wave.open(wav_in_memory, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(SAMPLE_WIDTH)
            wf.setframerate(RATE)
            wf.writeframes(raw_audio_data)
        wav_bytes = wav_in_memory.getvalue()

        prompt_parts = [
            "Esta é uma pergunta de uma entrevista de emprego enviada como um arquivo de áudio. Sua tarefa é ouvir a pergunta e gerar uma resposta de alta qualidade, profissional e concisa que o entrevistado possa usar.",
            {"mime_type": "audio/wav", "data": wav_bytes}
        ]

        try:
            response = model.generate_content(prompt_parts)
            self.update_response(response.text)
            self.update_status("Resposta gerada! Pronto para ouvir...")
        except Exception as e:
            print(f"Ocorreu um erro na API: {e}") 
            self.update_response(f"Erro na API: {e}")
            self.update_status("Erro. Tente novamente.", "red")
        
        self.record_button.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()