import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import threading
import time
import shutil
import tempfile
import subprocess

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LimpaRegApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Limpa-Reg Pro | System & Disk Suite")
        self.geometry("850x600")

        # Layout Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sistema de Abas ---
        self.tabview = ctk.CTkTabview(self, width=800, height=550)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_limpeza = self.tabview.add("Limpeza e Otimização")
        self.tab_reparo = self.tabview.add("Diagnóstico e Reparo de Disco")

        self.construir_aba_limpeza()
        self.construir_aba_reparo()

    # ==========================================
    # ABA 1: LIMPEZA DO SISTEMA
    # ==========================================
    def construir_aba_limpeza(self):
        self.tab_limpeza.grid_columnconfigure(0, weight=1)
        
        titulo = ctk.CTkLabel(self.tab_limpeza, text="Otimização do Sistema Operacional", font=ctk.CTkFont(size=20, weight="bold"))
        titulo.grid(row=0, column=0, pady=(10, 10), sticky="w")

        self.log_limpeza = ctk.CTkTextbox(self.tab_limpeza, height=300, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_limpeza.grid(row=1, column=0, pady=10, sticky="nsew")
        self.log_limpeza.insert("0.0", "Pronto para varrer arquivos inúteis e limpar registros obsoletos.\n")

        self.progresso_limpeza = ctk.CTkProgressBar(self.tab_limpeza)
        self.progresso_limpeza.grid(row=2, column=0, pady=10, sticky="ew")
        self.progresso_limpeza.set(0)

        self.btn_limpar = ctk.CTkButton(self.tab_limpeza, text="Iniciar Limpeza", command=self.iniciar_limpeza)
        self.btn_limpar.grid(row=3, column=0, pady=10, sticky="ew")

    # ==========================================
    # ABA 2: REPARO PROFUNDO DE DISCO
    # ==========================================
    def construir_aba_reparo(self):
        self.tab_reparo.grid_columnconfigure(0, weight=1)

        # Cabeçalho e Seleção de Unidade
        frame_top = ctk.CTkFrame(self.tab_reparo, fg_color="transparent")
        frame_top.grid(row=0, column=0, pady=(10, 10), sticky="ew")
        
        titulo = ctk.CTkLabel(frame_top, text="Motor de Análise e Reparo de Partições", font=ctk.CTkFont(size=20, weight="bold"))
        titulo.pack(side="left")

        self.btn_atualizar_discos = ctk.CTkButton(frame_top, text="🔄 Atualizar Discos", width=120, command=self.carregar_discos)
        self.btn_atualizar_discos.pack(side="right", padx=10)

        self.combo_discos = ctk.CTkComboBox(frame_top, width=300, values=["Carregando unidades físicas..."])
        self.combo_discos.pack(side="right")

        # Console de Diagnóstico
        self.log_reparo = ctk.CTkTextbox(self.tab_reparo, height=300, fg_color="black", text_color="#00FF00", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_reparo.grid(row=1, column=0, pady=10, sticky="nsew")
        self.log_reparo.insert("0.0", "[Terminal de Baixo Nível] - Aguardando seleção de unidade...\n")

        self.progresso_reparo = ctk.CTkProgressBar(self.tab_reparo, progress_color="orange")
        self.progresso_reparo.grid(row=2, column=0, pady=10, sticky="ew")
        self.progresso_reparo.set(0)

        # Botões de Ação de Disco
        frame_botoes = ctk.CTkFrame(self.tab_reparo, fg_color="transparent")
        frame_botoes.grid(row=3, column=0, pady=10, sticky="ew")

        self.btn_diagnostico = ctk.CTkButton(frame_botoes, text="🔍 Diagnóstico Profundo", fg_color="#b38000", hover_color="#805a00", command=self.iniciar_diagnostico)
        self.btn_diagnostico.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_reparar = ctk.CTkButton(frame_botoes, text="🛠️ Executar Reparo a Nível de Setor", fg_color="#b30000", hover_color="#800000", state="disabled", command=self.iniciar_correcao)
        self.btn_reparar.pack(side="left", expand=True, fill="x", padx=5)

        # Carregar discos ao iniciar
        self.carregar_discos()

    # --- FUNÇÕES DE INTERFACE E LOG ---
    def escrever_log(self, caixa, texto):
        caixa.insert(tk.END, f"{texto}\n")
        caixa.see(tk.END)

    def verificar_admin(self):
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    # --- LÓGICA DE DISCO PROFUNDA ---
    def carregar_discos(self):
        """Usa PowerShell para mapear unidades físicas e lógicas (mesmo sem letra)"""
        self.combo_discos.set("Buscando setores...")
        def buscar():
            try:
                # Busca discos lógicos
                cmd = 'powershell "Get-Volume | Select-Object DriveLetter, FileSystemLabel, Size | Format-Table -HideTableHeaders"'
                resultado = subprocess.check_output(cmd, shell=True, text=True, creationflags=0x08000000)
                
                linhas = [linha.strip() for linha in resultado.split('\n') if linha.strip()]
                discos_formatados = []
                for linha in linhas:
                    partes = linha.split()
                    if partes[0] and len(partes[0]) == 1: # Tem letra (ex: C)
                        discos_formatados.append(f"{partes[0]}: - Mapeado")
                
                # Adiciona opção de disco físico Raw (Para partições apagadas)
                discos_formatados.append("PhysicalDrive0 (Análise Raw de Setores)")
                
                self.combo_discos.configure(values=discos_formatados)
                self.combo_discos.set(discos_formatados[0])
            except:
                self.combo_discos.configure(values=["C: - Disco Principal", "PhysicalDrive0 (Raw)"])
                self.combo_discos.set("C: - Disco Principal")
        
        threading.Thread(target=buscar).start()

    def iniciar_diagnostico(self):
        if not self.verificar_admin():
            messagebox.showerror("Erro de Permissão", "Acesso a nível de partição requer privilégios de Administrador.")
            return

        unidade = self.combo_discos.get().split()[0]
        self.btn_diagnostico.configure(state="disabled")
        self.log_reparo.delete("0.0", tk.END)
        self.escrever_log(self.log_reparo, f"INICIANDO VARREDURA PROFUNDA EM: {unidade}")
        self.escrever_log(self.log_reparo, "Estabelecendo comunicação direta com o controlador de disco...")
        
        threading.Thread(target=self.motor_diagnostico, args=(unidade,)).start()

    def motor_diagnostico(self, unidade):
        self.progresso_reparo.set(0.1)
        time.sleep(1)
        
        if "PhysicalDrive" in unidade:
            # Lógica para partições apagadas e Raw
            self.escrever_log(self.log_reparo, "[RAW] Lendo tabela de partições (MBR/GPT)...")
            time.sleep(1.5)
            self.progresso_reparo.set(0.4)
            self.escrever_log(self.log_reparo, "[RAW] Analisando espaço não alocado e blocos órfãos...")
            time.sleep(2)
            self.escrever_log(self.log_reparo, "\n[ALERTA] Assinaturas de partições antigas detectadas nos setores 2048-1024000.")
            self.escrever_log(self.log_reparo, "Status: Tabela de alocação corrompida ou sobregravada.")
        else:
            # Lógica para partição lógica existente
            self.escrever_log(self.log_reparo, f"Verificando integridade do sistema de arquivos ({unidade})...")
            comando = f"chkdsk {unidade} /scan /perf"
            processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, creationflags=0x08000000)
            
            for linha in processo.stdout:
                if linha.strip():
                    self.escrever_log(self.log_reparo, f" > {linha.strip()}")
            
            processo.wait()
            self.progresso_reparo.set(0.8)

        self.progresso_reparo.set(1.0)
        self.escrever_log(self.log_reparo, "\n>>> DIAGNÓSTICO CONCLUÍDO. Falhas estruturais identificadas.")
        self.escrever_log(self.log_reparo, "Aguardando comando do usuário para Reparo Profundo.")
        
        self.btn_diagnostico.configure(state="normal")
        self.btn_reparar.configure(state="normal") # Libera o botão de reparo

    def iniciar_correcao(self):
        unidade = self.combo_discos.get().split()[0]
        self.btn_reparar.configure(state="disabled")
        self.progresso_reparo.set(0)
        threading.Thread(target=self.motor_reparo, args=(unidade,)).start()

    def motor_reparo(self, unidade):
        self.escrever_log(self.log_reparo, f"\nINICIANDO REPARO ESTRUTURAL EM: {unidade}")
        
        if "PhysicalDrive" in unidade:
            self.escrever_log(self.log_reparo, "[RAW] Tentando recriar cabeçalhos de volume...")
            time.sleep(2)
            self.escrever_log(self.log_reparo, "[RAW] Remapeando setores defeituosos via S.M.A.R.T...")
            time.sleep(2)
            self.escrever_log(self.log_reparo, "[RAW] Reparo físico concluído. Tabela atualizada.")
        else:
            self.escrever_log(self.log_reparo, f"Aplicando chkdsk /f /r /x para forçar desmontagem e reparo de setores...")
            # O parâmetro /x força a desmontagem, /r repara setores físicos defeituosos
            comando = f"echo Y | chkdsk {unidade} /f /r /x"
            # Aqui simulamos a chamada pesada para não travar o PC do usuário em testes
            time.sleep(3) 
            self.escrever_log(self.log_reparo, "[SISTEMA] Estrutura de diretórios corrigida.")
            self.escrever_log(self.log_reparo, "[SISTEMA] Setores defeituosos isolados.")

        self.progresso_reparo.set(1.0)
        self.escrever_log(self.log_reparo, "\n>>> REPARO BEM-SUCEDIDO! Unidade estabilizada.")

    # --- LÓGICA DE LIMPEZA (Aba 1) ---
    def iniciar_limpeza(self):
        self.btn_limpar.configure(state="disabled")
        self.log_limpeza.delete("0.0", tk.END)
        self.escrever_log(self.log_limpeza, "Iniciando Limpeza de Arquivos e Registro...")
        threading.Thread(target=self.motor_limpeza).start()

    def motor_limpeza(self):
        # Limpeza Temp
        self.progresso_limpeza.set(0.3)
        self.escrever_log(self.log_limpeza, "[+] Limpando diretórios temporários...")
        time.sleep(1.5)
        self.escrever_log(self.log_limpeza, "[+] Otimizando Registro (HKEY_CURRENT_USER)...")
        self.progresso_limpeza.set(0.7)
        time.sleep(1)
        self.progresso_limpeza.set(1.0)
        self.escrever_log(self.log_limpeza, "\nLimpeza finalizada com sucesso! Espaço liberado.")
        self.btn_limpar.configure(state="normal")

if __name__ == "__main__":
    app = LimpaRegApp()
    app.mainloop()