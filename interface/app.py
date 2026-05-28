import sys
import tkinter as tk
import customtkinter as cctk
from threading import Thread
import queue
import builtins
import time
import os

# Ajustar o path para poder importar o TCC
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TCC.pipeline import rodar_pipeline

import re

import ctypes

class GUI_Terminal(cctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DB Reader")
        self.geometry("450x500") # Aumentado para a direita
        self.resizable(False, False) # Bloqueado mexer no tamanho
        cctk.set_appearance_mode("dark")

        # Regex para remover códigos ANSI
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

        # Configuração de layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Widget de Texto para o Terminal
        self.textbox = cctk.CTkTextbox(
            self, 
            font=("Consolas", 13), 
            text_color="#cccccc", 
            fg_color="#1e1e1e"
        )
        self.textbox.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.textbox.tag_config("red", foreground="#ff4d4d") # Definir tag vermelha
        self.textbox.configure(state="disabled")

        # Frame para entrada com prompt e botões
        self.input_frame = cctk.CTkFrame(self, fg_color="#1e1e1e")
        self.input_frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.prompt_label = cctk.CTkLabel(self.input_frame, text=">", font=("Consolas", 14, "bold"), text_color="#007acc")
        self.prompt_label.grid(row=0, column=0, padx=(5, 5))

        self.entry = cctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Digite aqui...", 
            font=("Consolas", 13),
            fg_color="#3c3c3c",
            border_color="#3c3c3c",
            text_color="#ffffff"
        )
        self.entry.grid(row=0, column=1, sticky="ew", padx=(0, 5), pady=5)
        self.entry.bind("<Return>", lambda e: self.processar_entrada())

        # Botão Buscar
        self.btn_buscar = cctk.CTkButton(
            self.input_frame, 
            text="Buscar", 
            width=60, 
            command=self.processar_entrada,
            fg_color="#4a4a4a", # Cinza
            hover_color="#5a5a5a"
        )
        self.btn_buscar.grid(row=0, column=2, padx=2, pady=5)

        # Botão Cancelar
        self.btn_cancelar = cctk.CTkButton(
            self.input_frame, 
            text="Cancelar", 
            width=60, 
            command=self.cancelar_comando,
            fg_color="#a1260d",
            hover_color="#801e0a"
        )
        self.btn_cancelar.grid(row=0, column=3, padx=(2, 5), pady=5)

        # Filas para comunicação entre threads
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()

        # Redirecionar stdout e stderr
        sys.stdout = self.StdoutRedirector(self.output_queue, self)
        sys.stderr = self.StdoutRedirector(self.output_queue, self)

        # Substituir o input original
        builtins.input = self.custom_input

        # Iniciar loop de atualização da UI
        self.after(100, self.update_textbox)
        
        # Variáveis para animação de "pensando"
        self.is_thinking = False
        self.thinking_start_time = 0
        self.thinking_dots = 0
        self.thinking_line_index = None

        # Iniciar a lógica do pipeline
        self.iniciar_worker()

    def iniciar_worker(self):
        self.worker_thread = Thread(target=self.run_pipeline_loop, daemon=True)
        self.worker_thread.start()
        self.after(500, self.animate_thinking)

    def animate_thinking(self):
        if self.is_thinking:
            elapsed = time.time() - self.thinking_start_time
            
            if elapsed >= 3.0: # Apenas após 3 segundos
                self.thinking_dots = (self.thinking_dots % 3) + 1
                dots_str = "." * self.thinking_dots
                
                self.textbox.configure(state="normal")
                if self.thinking_line_index:
                    self.textbox.delete(f"{self.thinking_line_index} linestart", f"{self.thinking_line_index} lineend")
                    self.textbox.insert(self.thinking_line_index, dots_str)
                else:
                    self.textbox.insert(tk.END, "\n" + dots_str)
                    self.thinking_line_index = self.textbox.index("end-1c linestart")
                
                self.textbox.see(tk.END)
                self.textbox.configure(state="disabled")
        else:
            if self.thinking_line_index:
                self.textbox.configure(state="normal")
                self.textbox.delete(f"{self.thinking_line_index} linestart", f"{self.thinking_line_index} lineend+1c")
                self.thinking_line_index = None
                self.textbox.configure(state="disabled")

        self.after(500, self.animate_thinking)

    class StdoutRedirector:
        def __init__(self, q, parent):
            self.q = q
            self.parent = parent
        def write(self, str):
            if str.strip():
                self.parent.is_thinking = False
            self.q.put(str)
        def flush(self):
            pass

    def strip_ansi(self, text):
        return self.ansi_escape.sub('', text)

    def custom_input(self, prompt=""):
        self.is_thinking = False
        if prompt:
            clean_prompt = self.strip_ansi(prompt)
            self.output_queue.put(clean_prompt)
        
        self.after(0, lambda: self.entry.configure(state="normal"))
        self.after(0, lambda: self.btn_buscar.configure(state="normal"))
        self.after(0, lambda: self.entry.focus_set())
        
        while True:
            try:
                val = self.input_queue.get(timeout=0.1)
                self.thinking_start_time = time.time() # Reset do tempo
                self.is_thinking = True
                return val
            except queue.Empty:
                continue

    def processar_entrada(self):
        texto = self.entry.get()
        if not texto.strip(): return
        
        # Comando para limpar o terminal
        if texto.strip().lower() == "clear":
            self.textbox.configure(state="normal")
            
            # Pegar a última linha para ver se é um prompt
            linhas = self.textbox.get("1.0", tk.END).splitlines()
            ultimo_prompt = ""
            for linha in reversed(linhas):
                if "Você:" in linha or "Gerar gráfico?" in linha or "Exportar CSV?" in linha:
                    ultimo_prompt = linha
                    break
            
            self.textbox.delete("1.0", tk.END)
            if ultimo_prompt:
                self.textbox.insert(tk.END, ultimo_prompt)
            
            self.textbox.configure(state="disabled")
            self.entry.delete(0, tk.END)
            return

        self.entry.delete(0, tk.END)
        self.entry.configure(state="disabled")
        self.btn_buscar.configure(state="disabled")
        
        self.output_queue.put(texto + "\n")
        self.input_queue.put(texto)
        self.thinking_start_time = time.time() # Início da contagem
        self.is_thinking = True

    def cancelar_comando(self):
        self.is_thinking = False
        self.output_queue.put("\nBusca interrompida pelo usuário!\n")
        # Forçar uma exceção na thread worker para simular Ctrl+C
        if self.worker_thread.is_alive():
            thread_id = self.worker_thread.ident
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(KeyboardInterrupt))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        
        # Limpar filas
        while not self.input_queue.empty():
            self.input_queue.get()
        
        # Reabilitar campos após cancelamento
        self.after(0, lambda: self.entry.configure(state="normal"))
        self.after(0, lambda: self.btn_buscar.configure(state="normal"))
        
    def update_textbox(self):
        while not self.output_queue.empty():
            msg = self.output_queue.get()
            clean_msg = self.strip_ansi(msg)
            
            self.textbox.configure(state="normal")
            
            # Checar se a mensagem deve ser vermelha
            if "INVALID" in clean_msg or "Resultado inválido ou não encontrado!" in clean_msg or "Erro técnico:" in clean_msg or "Busca interrompida pelo usuário!" in clean_msg:
                self.textbox.insert(tk.END, clean_msg, "red")
            else:
                self.textbox.insert(tk.END, clean_msg)
                
            self.textbox.see(tk.END)
            self.textbox.configure(state="disabled")
        self.after(100, self.update_textbox)

    def run_pipeline_loop(self):
        while True:
            try:
                # O input() agora chama custom_input que habilita os campos
                pergunta = input("\nVocê: ")
                
                resposta = rodar_pipeline(pergunta)
                print(resposta)
            except KeyboardInterrupt:
                time.sleep(0.5)
            except Exception as e:
                print(f"\nErro no loop: {e}")
                time.sleep(1)

if __name__ == "__main__":
    app = GUI_Terminal()
    app.mainloop()
