import soundcard as sc
import google.generativeai as genai
import customtkinter as ctk
import os
import threading
from dotenv import load_dotenv
import wave
import io
from queue import Queue
import numpy as np

# --- CONFIGURAÇÕES INICIAIS ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- OTIMIZAÇÃO DE ÁUDIO PARA VELOCIDADE ---
# Usamos configurações padrão para voz para minimizar o tamanho dos dados.
SAMPLE_RATE = 16000 # Reduzido de 48000
CHANNELS = 1        # Mono em vez de Estéreo

model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

recording = False
audio_queue = Queue()

# --- FUNÇÃO DE GRAVAÇÃO ---
def record_audio(window):
    global recording
    
    try:
        loopback_mic = None
        all_mics = sc.all_microphones(include_loopback=True)
        for mic in all_mics:
            if mic.isloopback:
                loopback_mic = mic
                print(f"Dispositivo de loopback encontrado: {mic.name}")
                break

        if loopback_mic is None:
            raise RuntimeError("Nenhum dispositivo de loopback de áudio foi encontrado.")

        window.update_status("Pronto para ouvir...")
        
        with loopback_mic.recorder(samplerate=SAMPLE_RATE, channels=CHANNELS) as mic:
            while True:
                if recording:
                    window.update_status("Ouvindo...")
                    frames = []
                    while recording:
                        data = mic.record(numframes=1024)
                        frames.append(data)
                    
                    if frames:
                        full_recording = np.concatenate(frames, axis=0)
                        audio_queue.put(full_recording)
    
    except Exception as e:
        error_message = f"Erro ao capturar áudio: {e}"
        print(error_message)
        window.update_status(error_message, "red")
        
# --- CLASSE DA APLICAÇÃO GUI ---
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Assistente de Entrevista IA")
        self.geometry("500x350")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(self, text="Status: Inicializando áudio...")
        self.status_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.response_textbox = ctk.CTkTextbox(self, state="disabled", font=("Helvetica", 14), wrap="word")
        self.response_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        self.record_button = ctk.CTkButton(self.button_frame, text="Ouvir Pergunta", command=self.start_recording_action)
        self.record_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.stop_button = ctk.CTkButton(self.button_frame, text="Parar", command=self.stop_recording_action, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        threading.Thread(target=record_audio, args=(self,), daemon=True).start()

    def update_status(self, text, color="white"):
        self.status_label.configure(text=f"Status: {text}", text_color=color)

    def update_response(self, text):
        self.response_textbox.configure(state="normal")
        self.response_textbox.delete("1.0", "end")
        self.response_textbox.insert("1.0", text)
        self.response_textbox.configure(state="disabled")

    def start_recording_action(self):
        global recording
        recording = True
        self.update_response("")
        self.record_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

    def stop_recording_action(self):
        global recording
        recording = False
        self.update_status("Processando com a IA...")
        self.stop_button.configure(state="disabled")
        self.after(100, self.process_audio_from_queue)

    def process_audio_from_queue(self):
        try:
            from queue import Empty
            numpy_audio_data = audio_queue.get(block=False)
            threading.Thread(target=self.get_gemini_response, args=(numpy_audio_data,), daemon=True).start()
        except Empty:
            self.after(100, self.process_audio_from_queue)

    def get_gemini_response(self, numpy_audio_data):
        int_data = (numpy_audio_data * 32767).astype(np.int16)
        
        wav_in_memory = io.BytesIO()
        with wave.open(wav_in_memory, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(int_data.tobytes())
        wav_bytes = wav_in_memory.getvalue()

        # --- PROMPT MELHORADO E MAIS DIRETO ---
        prompt_parts = [
            "Esta é uma pergunta de uma entrevista de emprego enviada como um arquivo de áudio. Sua tarefa é ouvir a pergunta e gerar uma resposta de alta qualidade, profissional e concisa que o entrevistado possa usar. Comece a resposta imediatamente, sem qualquer introdução como 'Claro,' ou 'Aqui está a resposta:'.",
            {"mime_type": "audio/wav", "data": wav_bytes}
        ]

        try:
            # --- ALTERAÇÃO PARA STREAMING ---
            # Usamos stream=True para receber a resposta em pedaços.
            response_stream = model.generate_content(prompt_parts, stream=True)
            
            full_response = ""
            # Loop que atualiza a GUI a cada novo pedaço de texto recebido.
            for chunk in response_stream:
                full_response += chunk.text
                self.update_response(full_response)
            
            self.update_status("Resposta gerada! Pronto para ouvir...")
        except Exception as e:
            print(f"Ocorreu um erro na API: {e}") 
            self.update_response(f"Erro na API: {e}")
            self.update_status("Erro. Tente novamente.", "red")
        
        self.record_button.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()