import re
import spacy
from base_dados import posts_para_auditoria 

nlp = spacy.load("pt_core_news_lg")

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
            diagnostico = "✅ PUBLICIDADE EXPLÍCITA (Sinalizada corretamente)"
        else:
            diagnostico = "⚠️ PUBLICIDADE OMISSA (Indícios detectados sem rótulo claro)"
    else:
        diagnostico = "📑 POST ANALISADO (Sem indícios comerciais óbvios)"

    return {
        "entidades": todas_as_entidades,
        "cupons": cupons,
        "sinalizado": "Sim" if tem_sinalizacao else "Não",
        "diagnostico": diagnostico
    }


print(f"\n{'='*80}\nSISTEMA DE AUDITORIA: MAPA DE AUTENTICIDADE\n{'='*80}")

for post in posts_para_auditoria:
    res = realizar_auditoria(post['texto'])
    
    print(f"POST {post['id']} | Perfil: {post['perfil']}")
    print(f"Entidades Identificadas (NLP + @): {res['entidades']}")
    print(f"Cupons/Códigos: {res['cupons']}")
    print(f"Sinalização Oficial Detectada: {res['sinalizado']}")
    print(f"DIAGNÓSTICO FINAL: {res['diagnostico']}")
    print("-" * 80)