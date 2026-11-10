import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================================================================
# CONFIGURAÇÃO PRINCIPAL: Altere apenas o caminho da pasta geral abaixo
# ==============================================================================
PASTA_RAIZ_XML = r"CAMINHO_PASTA"
# ==============================================================================

PASTA_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

# CONFIGURAÇÃO AVANÇADA DO CHROME (PERMISSÕES DE DOWNLOAD)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) 
prefs = {
    "download.default_directory": PASTA_DOWNLOADS,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def esperar_download_concluir(pasta):
    print("   -> Aguardando o download terminar no Chrome...")
    time.sleep(2) 
    while True:
        time.sleep(1)
        arquivos_baixando = [f for f in os.listdir(pasta) if f.endswith(".crdownload") or f.endswith(".part") or f.endswith(".tmp")]
        if not arquivos_baixando:
            break

def mover_ultimo_arquivo(origem, destino):
    time.sleep(1)
    arquivos = [os.path.join(origem, f) for f in os.listdir(origem) if f.endswith(".xml") or f.endswith(".zip")]
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)
        nome_arquivo = os.path.basename(ultimo_arquivo)
        shutil.move(ultimo_arquivo, os.path.join(destino, nome_arquivo))
        print(f"   ✓ Arquivo {nome_arquivo} movido e organizado!")

try:
    # Abre o site do TOTVS uma única vez
    driver.get("LINK_SITE") 
    
    print("\n[PASSO MANUAL] Faça o login e acesse a tela de exportação.")
    ano_desejado = input("Digite o ANO que deseja exportar (ex: 2025) e dê ENTER: ")

    # Configuração automática dos meses de faturamento
    bissexto = "29" if (int(ano_desejado) % 4 == 0 and int(ano_desejado) % 100 != 0) or (int(ano_desejado) % 400 == 0) else "28"
    dias_mes = ["31", bissexto, "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]
    nomes_mes = ["01_Janeiro", "02_Fevereiro", "03_Março", "04_Abril", "05_Maio", "06_Junho", "07_Julho", "08_Agosto", "09_Setembro", "10_Outubro", "11_Novembro", "12_Dezembro"]
    
    meses = []
    for i in range(12):
        num_m = str(i + 1).zfill(2)
        meses.append({
            "inicio": f"01/{num_m}/{ano_desejado}",
            "fim": f"{dias_mes[i]}/{num_m}/{ano_desejado}",
            "pasta": nomes_mes[i]
        })

    aba_principal = driver.current_window_handle

    # --- LOOP INFINITO PARA RODAR VÁRIAS LOJAS NA MESMA ABA ---
    while True:
        print("\n----------------------------------------------------------------")
        print("Mude a LOJA manualmente na tela do TOTVS antes de continuar.")
        num_loja = input("Digite o NÚMERO da loja selecionada (ou digite 'sair' para fechar): ")
        
        if num_loja.lower() == 'sair':
            print("\nEncerrando o programa de automação. Até mais!")
            break
            
        print(f"\n🚀 Iniciando a automação para a LOJA LG{num_loja} no ano {ano_desejado}...")

        for m in meses:
            print(f"\n📅 Período atual: {m['pasta']} ({m['inicio']} até {m['fim']})")
            
            # Estrutura com prefixo 'LG': Pasta_Geral \ LG[Número] \ [Ano] \ [Mês]
            nome_pasta_loja = f"LG{num_loja}"
            pasta_destino_final = os.path.join(PASTA_RAIZ_XML, nome_pasta_loja, ano_desejado, m['pasta'])
            os.makedirs(pasta_destino_final, exist_ok=True)
            
            # Preenche a Data Inicial
            campo_inicio = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="frmRetorno:calDataEmissaoInicialInputDate"]')))
            campo_inicio.clear()
            campo_inicio.send_keys(m['inicio'])
            
            # Preenche a Data Final
            campo_fim = driver.find_element(By.XPATH, '//*[@id="frmRetorno:calDataEmissaoFinalInputDate"]')
            campo_fim.clear()
            campo_fim.send_keys(m['fim'])
            
            time.sleep(0.5)
            
            # Clica em Gerar Retorno
            driver.find_element(By.XPATH, '//*[@id="frmRetorno:btnGerarRetorno"]').click()
            print("   -> Solicitação enviada. Aguardando processamento do TOTVS...")
            time.sleep(3)
            
                       # LOOP DE PESQUISA E CLIQUE ULTRA ROBUSTO (BUSCA POR ÍCONE E TEXTO)
            while True:
                try:
                    # 1. Clica em Pesquisar para atualizar a tabela de faturamento
                    driver.find_element(By.XPATH, '//*[@id="frmRetorno:btnPesquisar"]').click()
                    time.sleep(3)
                    
                    # 2. TENTATIVA A: Procura qualquer link que contenha "linkZIP" no ID
                    try:
                        botao_download = driver.find_element(By.XPATH, "//*[contains(@id, 'linkZIP')]")
                    except:
                        # TENTATIVA B: Procura o primeiro link dentro da tabela que tenha uma imagem/ícone dentro
                        try:
                            botao_download = driver.find_element(By.XPATH, "//table[contains(@id, 'gridConsultaRetorno')]//a[img or i]")
                        except:
                            # TENTATIVA C: Se falhar, busca de forma genérica por qualquer elemento com o id parcial do ZIP
                            botao_download = driver.find_element(By.XPATH, "//*[contains(@id, 'linkZIP')] | //a[contains(@href, 'download') or contains(@href, 'ZIP')]")

                    # 3. Força o clique via JavaScript (ignora se está oculto ou fora da tela)
                    driver.execute_script("arguments[0].click();", botao_download)
                    print("   -> Status: Botão clicado com sucesso via Sniper JS!")
                    time.sleep(4) # Tempo garantido para o Chrome registrar o início do download
                    break 
                    
                except Exception as e:
                    print("   -> Ícone de download ainda não apareceu ou mudou na tabela. Atualizando em 5 segundos...")
                    time.sleep(5)

            
            # Aguarda o download e move para a pasta final
            esperar_download_concluir(PASTA_DOWNLOADS)
            mover_ultimo_arquivo(PASTA_DOWNLOADS, pasta_destino_final)
            
        print(f"\n🎉 Concluído com sucesso os 12 meses da Loja LG{num_loja}!")

except Exception as e:
    print(f"\n❌ Ocorreu um erro inesperado: {e}")
