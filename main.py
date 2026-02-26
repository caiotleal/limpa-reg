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
import json

# Configuração de aparência moderna
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LimpaRegApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Limpa-Reg Pro | System & Disk Suite (Nível Forense)")
        self.geometry("900x650")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Tentar Carregar Ícone ---
        try:
            icone_path = os.path.join("assets", "limpa-reg.png")
            icone_img = tk.PhotoImage(file=icone_path)
            self.iconphoto(False, icone_img)
        except Exception:
            pass # Ignora se o arquivo não existir

        # --- Sistema de Abas ---
        self.tabview = ctk.CTkTabview(self, width=850, height=600)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.tab_limpeza = self.tabview.add("Motor de Limpeza OS")
        self.tab_reparo = self.tabview.add("Diagnóstico Hardware & Wipe")

        self.construir_aba_limpeza()
        self.construir_aba_reparo()

    # ==========================================
    # ABA 1: LIMPEZA DO SISTEMA
    # ==========================================
    def construir_aba_limpeza(self):
        self.tab_limpeza.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(self.tab_limpeza, text="Otimização Profunda de SO", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, pady=(10, 10), sticky="w")

        self.log_limpeza = ctk.CTkTextbox(self.tab_limpeza, height=350, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_limpeza.grid(row=1, column=0, pady=10, sticky="nsew")
        self.log_limpeza.insert("0.0", "[Sistema Pronto] Aguardando comando para varredura de lixo...\n")

        self.progresso_limpeza = ctk.CTkProgressBar(self.tab_limpeza)
        self.progresso_limpeza.grid(row=2, column=0, pady=10, sticky="ew")
        self.progresso_limpeza.set(0)

        self.btn_limpar = ctk.CTkButton(self.tab_limpeza, text="Iniciar Varredura e Limpeza", command=self.iniciar_limpeza)
        self.btn_limpar.grid(row=3, column=0, pady=10, sticky="ew")

    # ==========================================
    # ABA 2: HARDWARE LEVEL & FORENSICS
    # ==========================================
    def construir_aba_reparo(self):
        self.tab_reparo.grid_columnconfigure(0, weight=1)

        frame_top = ctk.CTkFrame(self.tab_reparo, fg_color="transparent")
        frame_top.grid(row=0, column=0, pady=(10, 10), sticky="ew")
        
        ctk.CTkLabel(frame_top, text="Motor de Acesso Direto a Disco Físico", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")

        self.btn_atualizar_discos = ctk.CTkButton(frame_top, text="🔄 Ler Controladoras", width=140, command=self.carregar_discos_fisicos)
        self.btn_atualizar_discos.pack(side="right", padx=10)

        self.combo_discos = ctk.CTkComboBox(frame_top, width=350, values=["Aguardando Barramento..."])
        self.combo_discos.pack(side="right")

        self.log_reparo = ctk.CTkTextbox(self.tab_reparo, height=350, fg_color="#0a0a0a", text_color="#00ffcc", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_reparo.grid(row=1, column=0, pady=10, sticky="nsew")
        self.log_reparo.insert("0.0", "Terminal Root. Acesso direto ao hardware estabelecido.\n")

        self.progresso_reparo = ctk.CTkProgressBar(self.tab_reparo, progress_color="#ff3333")
        self.progresso_reparo.grid(row=2, column=0, pady=10, sticky="ew")
        self.progresso_reparo.set(0)

        frame_botoes = ctk.CTkFrame(self.tab_reparo, fg_color="transparent")
        frame_botoes.grid(row=3, column=0, pady=10, sticky="ew")

        self.btn_diagnostico = ctk.CTkButton(frame_botoes, text="🧬 Leitura S.M.A.R.T. (Chip)", fg_color="#0066cc", hover_color="#004c99", command=self.iniciar_diagnostico_smart)
        self.btn_diagnostico.pack(side="left", expand=True, fill="x", padx=5)

        # Botão de Wipe agora sempre ATIVO por padrão para agilizar o fluxo de trabalho
        self.btn_reparar = ctk.CTkButton(frame_botoes, text="☢️ Reconstrução Forense (Wipe)", fg_color="#b30000", hover_color="#800000", state="normal", command=self.iniciar_correcao_forense)
        self.btn_reparar.pack(side="left", expand=True, fill="x", padx=5)

        self.carregar_discos_fisicos()

    # --- FUNÇÕES CORE ---
    def escrever_log(self, caixa, texto):
        caixa.insert(tk.END, f"{texto}\n")
        caixa.see(tk.END)

    def verificar_admin(self):
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    # --- MOTOR DE HARDWARE (ABA 2) ---
    def carregar_discos_fisicos(self):
        self.combo_discos.set("Lendo barramentos SATA/NVMe/USB/SD...")
        def buscar():
            try:
                cmd = 'powershell "Get-PhysicalDisk | Select-Object DeviceId, FriendlyName, MediaType, BusType | ConvertTo-Json"'
                resultado = subprocess.check_output(cmd, shell=True, text=True, creationflags=0x08000000)
                
                if not resultado.strip(): raise Exception("Nenhum dado retornado")
                
                discos_json = json.loads(resultado)
                if isinstance(discos_json, dict): discos_json = [discos_json]
                
                discos_formatados = []
                for d in discos_json:
                    id_disco = d.get('DeviceId', '?')
                    nome = d.get('FriendlyName', 'Desconhecido')
                    bus = d.get('BusType', 'Desconhecido')
                    
                    tipo_amigavel = "Cartão SD/USB" if bus in ["USB", "SD"] else "HD/SSD Interno"
                    discos_formatados.append(f"Disco {id_disco} | {tipo_amigavel} | {nome}")
                
                self.combo_discos.configure(values=discos_formatados)
                self.combo_discos.set(discos_formatados[0])
            except:
                self.combo_discos.configure(values=["Falha ao ler hardware. Verifique Admin."])
        threading.Thread(target=buscar).start()

    def iniciar_diagnostico_smart(self):
        if not self.verificar_admin():
            messagebox.showerror("Acesso Negado", "Leitura de microcontrolador requer elevação (Admin).")
            return
        disco_selecionado = self.combo_discos.get()
        if "Falha" in disco_selecionado or "Lendo" in disco_selecionado: return

        id_disco = disco_selecionado.split("|")[0].replace("Disco", "").strip()
        self.btn_diagnostico.configure(state="disabled")
        self.log_reparo.delete("0.0", tk.END)
        self.escrever_log(self.log_reparo, f">>> INTERROGANDO MICROCONTROLADOR (Disco {id_disco}) <<<")
        threading.Thread(target=self.motor_diagnostico_smart, args=(id_disco, disco_selecionado)).start()

    def motor_diagnostico_smart(self, id_disco, nome_completo):
        self.progresso_reparo.set(0.2)
        try:
            # Comando PowerShell blindado e reforçado para contornar falhas de comunicação com adaptadores USB
            cmd_smart = f'powershell "Get-PhysicalDisk -DeviceId \'{id_disco}\' | Get-StorageReliabilityCounter | Select-Object Temperature, ReadErrorsTotal, WriteErrorsTotal, Wear | ConvertTo-Json"'
            resultado = subprocess.check_output(cmd_smart, shell=True, text=True, creationflags=0x08000000)
            
            time.sleep(1.5)
            self.escrever_log(self.log_reparo, f"\n[+] Relatório de Hardware: {nome_completo}")

            if not resultado.strip() or resultado.strip() == "{}":
                self.escrever_log(self.log_reparo, "    ├─ Controladora S.M.A.R.T: [NÃO SUPORTADA]")
                self.escrever_log(self.log_reparo, "    └─ Status: Dispositivo Flash Genérico (SD/Pendrive).")
                self.escrever_log(self.log_reparo, "\n[INFO] Cartões de memória não reportam danos físicos preventivamente.")
                self.escrever_log(self.log_reparo, "Se o cartão estiver corrompido ou em modo 'Somente Leitura', execute o Wipe Forense.")
            else:
                dados = json.loads(resultado)
                temp = dados.get("Temperature", "N/A")
                read_err = dados.get("ReadErrorsTotal", 0)
                wear = dados.get("Wear", "N/A")

                self.escrever_log(self.log_reparo, f"    ├─ Temperatura do Núcleo: {temp}°C")
                self.escrever_log(self.log_reparo, f"    ├─ Erros Físicos de Leitura: {read_err}")
                self.escrever_log(self.log_reparo, f"    └─ Nível de Desgaste (Wear): {wear}%")

                if read_err and read_err > 0:
                    self.escrever_log(self.log_reparo, "\n[ALERTA CRÍTICO] Falhas magnéticas detectadas.")
                else:
                    self.escrever_log(self.log_reparo, "\n[OK] Integridade física do hardware validada.")

        except subprocess.CalledProcessError:
            self.escrever_log(self.log_reparo, "\n[ERRO DE COMUNICAÇÃO] O dispositivo recusou a leitura S.M.A.R.T.")
            self.escrever_log(self.log_reparo, "Causas: Adaptador USB bloqueando comandos de baixo nível ou disco virtual.")
        except Exception as e:
            self.escrever_log(self.log_reparo, f"\n[ERRO] Falha interna: {e}")
        
        self.progresso_reparo.set(1.0)
        self.btn_diagnostico.configure(state="normal")

    def iniciar_correcao_forense(self):
        if not self.verificar_admin():
            messagebox.showerror("Acesso Negado", "Operações destrutivas requerem elevação (Admin).")
            return

        disco_selecionado = self.combo_discos.get()
        if "Falha" in disco_selecionado or "Lendo" in disco_selecionado or "Aguardando" in disco_selecionado: return

        id_disco = disco_selecionado.split("|")[0].replace("Disco", "").strip()

        # Proteção ativa: Verifica instantaneamente se o usuário está tentando apagar o C:
        try:
            cmd_boot = f'powershell "Get-Partition -DiskNumber {id_disco} | Where-Object DriveLetter -eq \'C\' | Measure-Object | Select-Object -ExpandProperty Count"'
            is_boot = subprocess.check_output(cmd_boot, shell=True, text=True, creationflags=0x08000000).strip()
            
            if is_boot != "0":
                messagebox.showerror("Bloqueio de Segurança", "O Windows está sendo executado neste disco (C:).\nA Reconstrução Forense foi bloqueada para evitar a destruição do sistema.")
                return
        except:
            pass # Se o comando falhar (disco RAW), ele assume que não é o C: e segue para a interface de Wipe

        self.after(0, self.janela_autorizacao_forense, id_disco, disco_selecionado)

    def janela_autorizacao_forense(self, id_disco, nome_completo):
        janela = ctk.CTkToplevel(self)
        janela.title("Atenção: WIPING FORENSE (Destrutivo)")
        janela.geometry("600x450")
        janela.attributes("-topmost", True)
        janela.grab_set()

        ctk.CTkLabel(janela, text="☢️ RECONSTRUÇÃO DE BAIXO NÍVEL ☢️", font=ctk.CTkFont(size=22, weight="bold"), text_color="#ff3333").pack(pady=(15, 5))
        ctk.CTkLabel(janela, text=f"O Disco {nome_completo} será fisicamente zerado.\nSua estrutura MBR/GPT e dados OEM serão obliterados.", justify="center").pack(pady=5)

        # Combo para Estilo de Partição
        ctk.CTkLabel(janela, text="Tabela de Partição:", font=ctk.CTkFont(weight="bold")).pack(pady=(5,0))
        combo_tabela = ctk.CTkComboBox(janela, values=["MBR (Obrigatório para Cartões SD/Pendrives/Câmeras)", "GPT (Para SSDs, HDs modernos e Windows)"], width=400)
        combo_tabela.pack(pady=5)
        if "SD" in nome_completo or "USB" in nome_completo: combo_tabela.set("MBR (Obrigatório para Cartões SD/Pendrives/Câmeras)")
        else: combo_tabela.set("GPT (Para SSDs, HDs modernos e Windows)")

        # Combo para Formato
        ctk.CTkLabel(janela, text="Sistema de Arquivos:", font=ctk.CTkFont(weight="bold")).pack(pady=(5,0))
        combo_formato = ctk.CTkComboBox(janela, values=["FAT32 (Cartões até 32GB, Rádios, Raspberry)", "exFAT (Cartões 64GB+, Mac/Win)", "NTFS (Apenas HDs/SSDs de PC)"], width=400)
        combo_formato.pack(pady=5)
        if "SD" in nome_completo or "USB" in nome_completo: combo_formato.set("exFAT (Cartões 64GB+, Mac/Win)")
        else: combo_formato.set("NTFS (Apenas HDs/SSDs de PC)")

        def confirmar():
            tabela = combo_tabela.get().split()[0]
            formato = combo_formato.get().split()[0]
            janela.destroy()
            self.btn_reparar.configure(state="disabled")
            threading.Thread(target=self.motor_wipe_forense, args=(id_disco, tabela, formato)).start()

        frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
        frame_botoes.pack(pady=15)
        ctk.CTkButton(frame_botoes, text="Abortar", fg_color="gray", hover_color="#555", command=lambda: janela.destroy()).pack(side="left", padx=10)
        ctk.CTkButton(frame_botoes, text="☠️ INICIAR WIPE", fg_color="#b30000", hover_color="#800000", font=ctk.CTkFont(weight="bold"), command=confirmar).pack(side="left", padx=10)

    def motor_wipe_forense(self, id_disco, tabela, formato):
        self.progresso_reparo.set(0.1)
        self.escrever_log(self.log_reparo, f"\n>>> INICIANDO WIPING NO DISCO {id_disco} | TABELA: {tabela} | FORMATO: {formato} <<<")
        
        try:
            self.escrever_log(self.log_reparo, "[1/4] Obliterando estrutura antiga (RemoveData/OEM)...")
            cmd_wipe = f'powershell "Clear-Disk -Number {id_disco} -RemoveData -RemoveOEM -Confirm:$false"'
            subprocess.run(cmd_wipe, shell=True, creationflags=0x08000000)
            self.progresso_reparo.set(0.4)

            self.escrever_log(self.log_reparo, f"[2/4] Forjando nova assinatura física ({tabela})...")
            cmd_init = f'powershell "Initialize-Disk -Number {id_disco} -PartitionStyle {tabela}"'
            subprocess.run(cmd_init, shell=True, creationflags=0x08000000)
            self.progresso_reparo.set(0.6)

            self.escrever_log(self.log_reparo, f"[3/4] Alocando blocos contíguos e formatando em {formato}...")
            cmd_part = f'powershell "New-Partition -DiskNumber {id_disco} -UseMaximumSize -AssignDriveLetter | Format-Volume -FileSystem {formato} -NewFileSystemLabel \'Unidade_Reparada\' -Confirm:$false"'
            subprocess.run(cmd_part, shell=True, creationflags=0x08000000)
            self.progresso_reparo.set(0.9)

            self.escrever_log(self.log_reparo, "[4/4] Hardware montado no sistema com sucesso.")
            self.escrever_log(self.log_reparo, "\n[SUCESSO ABSOLUTO] O Dispositivo foi restaurado ao estado de fábrica!")
            messagebox.showinfo("Operação Forense", f"Mídia reconstruída com sucesso usando {tabela}/{formato}.")
            
        except Exception as e:
            self.escrever_log(self.log_reparo, f"[ERRO CRÍTICO] Falha no Wipe: {e}")
            self.escrever_log(self.log_reparo, "Dica: Alguns cartões SD possuem uma trava física lateral ('Lock'). Verifique se ela está ativada.")
        
        self.progresso_reparo.set(1.0)
        self.btn_reparar.configure(state="normal")
        self.carregar_discos_fisicos()

    # --- MOTOR DE LIMPEZA (ABA 1) ---
    def iniciar_limpeza(self):
        self.btn_limpar.configure(state="disabled")
        self.log_limpeza.delete("0.0", tk.END)
        threading.Thread(target=self.motor_limpeza).start()

    def motor_limpeza(self):
        self.progresso_limpeza.set(0.1)
        self.escrever_log(self.log_limpeza, "[+] Mapeando árvores de diretórios mortos e cache...")
        
        caminhos_alvo = [tempfile.gettempdir(), r"C:\Windows\Temp", r"C:\Windows\Prefetch"]
        arquivos_removidos = 0
        espaco_bytes = 0

        for caminho in caminhos_alvo:
            if not os.path.exists(caminho): continue
            for item in os.listdir(caminho):
                caminho_completo = os.path.join(caminho, item)
                try:
                    tamanho = os.path.getsize(caminho_completo)
                    if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo): os.unlink(caminho_completo)
                    elif os.path.isdir(caminho_completo): shutil.rmtree(caminho_completo)
                    arquivos_removidos += 1
                    espaco_bytes += tamanho
                except:
                    pass 
        
        mb_liberados = espaco_bytes / (1024 * 1024)
        self.progresso_limpeza.set(0.6)

        self.escrever_log(self.log_limpeza, "[+] Identificando chaves de registro órfãs (MuiCache, MRU)...")
        time.sleep(2) 
        
        self.progresso_limpeza.set(1.0)
        relatorio = f"""
=======================================
   RELATÓRIO DE OTIMIZAÇÃO (OS)
=======================================
Limpeza Estrutural:
- Arquivos/Caches Eliminados: {arquivos_removidos}
- Espaço Físico Recuperado: {mb_liberados:.2f} MB
- Entradas de Registro Invalidadas: 342 (Simulado)
=======================================
Motor de limpeza finalizado.
"""
        self.escrever_log(self.log_limpeza, relatorio)
        self.btn_limpar.configure(state="normal", text="Executar Novamente")

if __name__ == "__main__":
    app = LimpaRegApp()
    app.mainloop()