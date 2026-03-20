import requests
import re
import spacy
import time
from perfis import perf_para_auditoria 


nlp = spacy.load("pt_core_news_lg")


def coletar_tiktok_api(usuario):
    usuario_limpo = usuario.replace("@", "")
    url = "https://tiktok-scraper7.p.rapidapi.com/user/posts"
    querystring = {"unique_id": usuario_limpo, "count": "10"}

    headers = {
        "x-rapidapi-key": "4f8019696dmshdd0bf9bef1a0e88p19c92djsnc4e453cd785b",
        "x-rapidapi-host": "tiktok-scraper7.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)

        if response.status_code == 200:
            dados = response.json()
            videos = dados.get('data', {}).get('videos', [])
            
            posts_processados = []

            for v in videos:
                legenda = v.get('title', '') 

                if legenda:
                    posts_processados.append({"perfil": usuario_limpo, "texto": legenda})
            return posts_processados
        
        else:
            print(f"  ❌ Erro na API para @{usuario_limpo}: Status {response.status_code}")
            return []
        
    except Exception as e:
        print(f"  ❌ Erro de conexão ao coletar @{usuario_limpo}: {e}")
        return []

def realizar_auditoria(texto):

    padrao_sinalizacao = r'[#*]?(publi|ad|patrocinado|parceria)\b'
    padrao_mencao = r'@([\w.]+)'
    padrao_cupom = r'(?i)(?:cupom|codigo|código|voucher|🏷️)\s*:?\s*([A-Z0-9]+)'

    sinalizacoes = re.findall(padrao_sinalizacao, texto, flags=re.IGNORECASE)
    nomes_mencionados = re.findall(padrao_mencao, texto)
    cupons = re.findall(padrao_cupom, texto)
    
    doc = nlp(texto)
    marcas_nlp = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    
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

print(f"\n{'='*80}\nSISTEMA DE AUDITORIA: MAPA DE AUTENTICIDADE\n{'='*80}")
print(f"Carregados {len(perf_para_auditoria)} perfis da base de dados externa.\n")

for perfil in perf_para_auditoria:
    print(f"🔎 Analisando perfil: @{perfil}...")
    
    posts = coletar_tiktok_api(perfil)
    
    if not posts:
        print(f"  (Nenhum post processado para @{perfil})\n")
        continue

    for i, post in enumerate(posts):
        res = realizar_auditoria(post['texto'])
        
        print(f"  [POST {i+1}]")
        print(f"  Legenda: {post['texto'][:75]}...")
        print(f"  Entidades: {res['entidades']}")
        print(f"  Cupons: {res['cupons']}")
        print(f"  DIAGNÓSTICO: {res['diagnostico']}")
        print("-" * 40)
    
    time.sleep(2)

print(f"\n{'='*80}\nPROCESSO FINALIZADO\n{'='*80}")