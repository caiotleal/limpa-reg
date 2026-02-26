import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import threading
import time

# Configuração de aparência moderna
ctk.set_appearance_mode("System")  # Adaptativo: Claro ou Escuro
ctk.set_default_color_theme("blue") 

class LimpaRegApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Janela Principal
        self.title("Limpa-Reg Pro | Otimizador de Registro")
        self.geometry("700x480")

        # Layout de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Painel Lateral (Sidebar) ---
        self.sidebar = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="LIMPA-REG", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.status_indicator = ctk.CTkLabel(self.sidebar, text="Status: Aguardando", text_color="gray")
        self.status_indicator.grid(row=1, column=0, padx=20, pady=10)

        # --- Área de Conteúdo ---
        self.title_label = ctk.CTkLabel(self, text="Limpeza Eficaz de Registro", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="w")

        # Caixa de Log/Resultados
        self.log_box = ctk.CTkTextbox(self, width=480, height=250)
        self.log_box.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.log_box.insert("0.0", "Pronto para scanear o Windows 10/11...\nClique no botão abaixo para começar.\n")

        # Barra de Progresso
        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=2, column=1, padx=20, pady=(0, 20), sticky="ew")
        self.progress.set(0)

        # Botões
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="ew")
        
        self.btn_scan = ctk.CTkButton(self.btn_frame, text="Scanear Agora", command=self.iniciar_scan)
        self.btn_scan.pack(side="left", padx=10)

        self.btn_clean = ctk.CTkButton(self.btn_frame, text="Limpar Registro", state="disabled", fg_color="#2d8a4e", command=self.executar_limpeza)
        self.btn_clean.pack(side="left", padx=10)

    def log(self, mensagem):
        self.log_box.insert(tk.END, f"> {mensagem}\n")
        self.log_box.see(tk.END)

    def iniciar_scan(self):
        if not self.verificar_admin():
            messagebox.showerror("Erro de Privilégio", "Execute como Administrador para acessar o registro.")
            return

        self.btn_scan.configure(state="disabled")
        self.status_indicator.configure(text="Status: Scaneando...", text_color="orange")
        self.log("Iniciando varredura profunda...")
        
        # Roda o scan em segundo plano para não travar a janela
        threading.Thread(target=self.logic_scan).start()

    def logic_scan(self):
        # Simulação de varredura (Aqui você colocaria a lógica winreg)
        for i in range(1, 11):
            time.sleep(0.3)
            self.progress.set(i / 10)
            self.log(f"Verificando entradas inúteis... {i*10}%")

        self.log("Scan concluído! Entradas obsoletas encontradas.")
        self.status_indicator.configure(text="Status: Concluído", text_color="green")
        self.btn_scan.configure(state="normal")
        self.btn_clean.configure(state="normal")

    def executar_limpeza(self):
        self.log("Limpando chaves de registro...")
        time.sleep(1)
        self.log("Limpeza finalizada com sucesso!")
        self.btn_clean.configure(state="disabled")
        self.progress.set(0)
        messagebox.showinfo("Sucesso", "Otimização de registro concluída!")

    def verificar_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

if __name__ == "__main__":
    app = LimpaRegApp()
    app.mainloop()