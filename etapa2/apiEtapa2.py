import requests
import re
import spacy
import time
# Importando sua base de perfis externa
from perfis import perf_para_auditoria 

# 1. Configuração da Inteligência Artificial (spaCy)
# O modelo 'pt_core_news_lg' é o que você está usando para Processamento de Linguagem Natural
try:
    nlp = spacy.load("pt_core_news_lg")
except Exception:
    print("Erro: Certifique-se de que o modelo 'pt_core_news_lg' do spaCy está instalado.")

# 2. Função para Coleta de Dados via Web API (TikTok)
def coletar_tiktok_api(usuario):
    usuario_limpo = usuario.replace("@", "")
    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"
    querystring = {"unique_id": usuario_limpo, "count": "3"}

    headers = {
        # Sua chave validada no painel da RapidAPI
        "x-rapidapi-key": "4f8019696dmshdd0bf9bef1a0e88p19c92djsnc4e453cd785b",
        "x-rapidapi-host": "tiktok-scraper7.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        if response.status_code == 200:
            dados = response.json()
            # Estrutura JSON da API TIKWM: data -> videos
            videos = dados.get('data', {}).get('videos', [])
            
            posts_processados = []
            for v in videos:
                legenda = v.get('title', '') # No TikTok, o título do vídeo é a legenda
                if legenda:
                    posts_processados.append({"perfil": usuario_limpo, "texto": legenda})
            return posts_processados
        else:
            print(f"  ❌ Erro na API para @{usuario_limpo}: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"  ❌ Erro de conexão ao coletar @{usuario_limpo}: {e}")
        return []

# 3. Função de Auditoria (Lógica da Etapa 1)
def realizar_auditoria(texto):
    # Regex para identificar sinalizações e cupons
    padrao_sinalizacao = r'[#*]?(publi|ad|patrocinado|parceria)\b'
    padrao_mencao = r'@([\w.]+)'
    padrao_cupom = r'(?i)(?:cupom|codigo|código|voucher|🏷️)\s*:?\s*([A-Z0-9]+)'

    sinalizacoes = re.findall(padrao_sinalizacao, texto, flags=re.IGNORECASE)
    nomes_mencionados = re.findall(padrao_mencao, texto)
    cupons = re.findall(padrao_cupom, texto)
    
    # Processamento com spaCy para identificar Organizações (marcas)
    doc = nlp(texto)
    marcas_nlp = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    
    # Unifica as marcas detectadas pela IA e pelas menções com '@'
    todas_as_entidades = list(set(marcas_nlp + nomes_mencionados))
    
    tem_sinalizacao = len(sinalizacoes) > 0
    tem_vinculo_comercial = len(todas_as_entidades) > 0 or len(cupons) > 0

    if tem_vinculo_comercial:
        if tem_sinalizacao:
            diagnostico = "✅ PUBLICIDADE EXPLÍCITA (Sinalizada)"
        else:
            diagnostico = "⚠️ PUBLICIDADE OMISSA (Indícios detectados)"
    else:
        diagnostico = "📑 POST ANALISADO (Sem indícios comerciais óbvios)"

    return {
        "entidades": todas_as_entidades,
        "cupons": cupons,
        "diagnostico": diagnostico
    }

# --- 4. FLUXO DE EXECUÇÃO ---
print(f"\n{'='*80}\nSISTEMA DE AUDITORIA: MAPA DE AUTENTICIDADE\n{'='*80}")
print(f"Carregados {len(perf_para_auditoria)} perfis da base de dados externa.\n")

for perfil in perf_para_auditoria:
    print(f"🔎 Analisando perfil: @{perfil}...")
    
    # Coleta real via API
    posts = coletar_tiktok_api(perfil)
    
    if not posts:
        print(f"  (Nenhum post processado para @{perfil})\n")
        continue

    # Auditoria de cada post coletado
    for i, post in enumerate(posts):
        res = realizar_auditoria(post['texto'])
        
        print(f"  [POST {i+1}]")
        print(f"  Legenda: {post['texto'][:75]}...")
        print(f"  Entidades: {res['entidades']}")
        print(f"  Cupons: {res['cupons']}")
        print(f"  DIAGNÓSTICO: {res['diagnostico']}")
        print("-" * 40)
    
    # Pausa entre perfis (boas práticas de API)
    time.sleep(2)

print(f"\n{'='*80}\nPROCESSO FINALIZADO\n{'='*80}")