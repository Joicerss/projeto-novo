import pandas as pd
from playwright.sync_api import sync_playwright
import time
import random

def coletar_dados_tjsp(processos):
    print("--- 🤖 INICIANDO ROBÔ DO TJSP ---")
    dados_coletados = []

    with sync_playwright() as p:
        # headless=False faz o navegador abrir na sua tela para você ver!
        # slow_mo=1000 deixa o robô mais lento (1 seg entre ações) para não parecer ataque
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        for processo in processos:
            print(f"🔍 Consultando: {processo}")
            
            try:
                # URL oficial de consulta do TJSP
                url = f"https://esaj.tjsp.jus.br/cpopg/show.do?processo.numero={processo}"
                
                # Vai para a página
                page.goto(url, timeout=20000)

                # Verifica se o processo existe ou se deu erro
                conteudo_pagina = page.content()
                
                if "Não foi possível" in conteudo_pagina or "processo não encontrado" in conteudo_pagina:
                    print("   ❌ Não encontrado.")
                    status = "Nao Encontrado"
                    classe = "N/A"
                    assunto = "N/A"
                else:
                    # --- RASPAGEM DE DADOS (WEB SCRAPING) ---
                    # Tenta pegar a Classe
                    try:
                        classe = page.locator("#classeProcesso").inner_text().strip()
                    except:
                        classe = "Não identificado"

                    # Tenta pegar o Assunto
                    try:
                        assunto = page.locator("#assuntoProcesso").inner_text().strip()
                    except:
                        assunto = "Não identificado"
                    
                    status = "Sucesso"
                    print(f"   ✅ Encontrado! Classe: {classe} | Assunto: {assunto}")

                # Guarda os dados na memória
                dados_coletados.append({
                    "numero_cnj": processo,
                    "status": status,
                    "classe": classe,
                    "assunto": assunto,
                    "url": url
                })
                
                # Pausa aleatória entre 2 e 4 segundos (para parecer humano)
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"   ⚠️ Erro técnico ao acessar: {e}")
                dados_coletados.append({
                    "numero_cnj": processo,
                    "status": f"Erro: {e}", 
                    "classe": "", 
                    "assunto": "", 
                    "url": ""
                })

        browser.close()

    return pd.DataFrame(dados_coletados)

# ---BLOCO PRINCIPAL DE EXECUÇÃO ---
print("📂 Lendo arquivo 'base_mestra_limpa.csv'...")

try:
    # 1. Lê a base limpa que criamos no passo anterior
    # O separador é ponto-e-vírgula (;) porque definimos assim na aula 01
    df = pd.read_csv('base_mestra_limpa.csv', sep=';')
    
    # 2. Filtra apenas processos de SP (Código 8.26)
    df_sp = df[df['Tribunal'] == 'TJSP']
    
    if len(df_sp) > 0:
        print(f"🎯 Encontrados {len(df_sp)} processos do TJSP para coletar.")
        
        # Converte a coluna de processos para uma lista
        lista_processos = df_sp['processo_formatado'].tolist()
        
        # 3. Roda a função do Robô
        df_resultado = coletar_dados_tjsp(lista_processos)
        
        # 4. Salva o resultado final
        nome_arquivo_saida = 'dados_tjsp_coletados.csv'
        df_resultado.to_csv(nome_arquivo_saida, index=False, sep=';')
        
        print(f"\n💾 Coleta finalizada! Abra o arquivo '{nome_arquivo_saida}' para ver os resultados.")
        print("-" * 50)
        print(df_resultado)
        print("-" * 50)
        
    else:
        print("⚠️ Nenhum processo do TJSP (8.26) encontrado na base limpa. Verifique se há processos de SP na sua lista.")

except FileNotFoundError:
    print("❌ Erro: O arquivo 'base_mestra_limpa.csv' não foi encontrado.")
    print("👉 Dica: Rode o script 'aula01_saneamento_base.py' antes deste!")
