import requests
import re
import spacy
from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import time

try:
    from perfis_insta import perfis_para_auditoria
except ImportError:
    print("❌ Erro: Crie o arquivo 'perfis_insta.py' com a lista 'perfis_para_auditoria'.")
    exit()

# ==============================================================================
# 1. CREDENCIAIS DA API
# ==============================================================================
API_KEY = "4f8019696dmshdd0bf9bef1a0e88p19c92djsnc4e453cd785b"

# ==============================================================================
# 2. CONFIGURAÇÃO DAS INTELIGÊNCIAS ARTIFICIAIS
# ==============================================================================
print("⏳ Carregando Modelos de Inteligência Artificial (Aguarde)...")
try:
    nlp = spacy.load("pt_core_news_lg")
except OSError:
    print("❌ Erro: Modelo 'pt_core_news_lg' não encontrado. Instale-o no terminal.")
    exit()

classificador_sentimento = pipeline(
    "sentiment-analysis", 
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# ==============================================================================
# 3. EXTRAÇÃO DE DADOS VIA WEB APIs
# ==============================================================================
def buscar_posts_do_perfil(usuario):
    usuario_limpo = usuario.replace("@", "")
    url = "https://instagram-looter2.p.rapidapi.com/profile"
    querystring = {"username": usuario_limpo}

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "instagram-looter2.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        if response.status_code == 200:
            dados = response.json()
            edges = dados.get('edge_owner_to_timeline_media', {}).get('edges', [])
            
            posts_processados = []
            for p in edges[:10]: 
                node = p.get('node', {})
                post_id = node.get('shortcode', '')
                
                legenda = ""
                edges_caption = node.get('edge_media_to_caption', {}).get('edges', [])
                if edges_caption:
                    legenda = edges_caption[0].get('node', {}).get('text', '')
                
                if post_id and legenda:
                    posts_processados.append({"id": post_id, "legenda": legenda})
            return posts_processados
    except Exception as e:
        print(f"  ❌ Erro ao buscar posts de @{usuario_limpo}: {e}")
    return []

def buscar_comentarios_do_post(post_id):
    url = "https://instagram120.p.rapidapi.com/api/instagram/mediaByShortcode"
    payload = {"shortcode": post_id}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "instagram120.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    comentarios = []
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            dados = response.json()
            if isinstance(dados, list) and len(dados) > 0:
                lista_comentarios = dados[0].get('meta', {}).get('comments', [])
                for c in lista_comentarios:
                    texto = c.get('text', '')
                    if texto:
                        comentarios.append(texto)
        return comentarios
    except Exception:
        return []

# ==============================================================================
# 4. FUNÇÃO DE AUDITORIA (Lendo cada comentário individualmente)
# ==============================================================================
def auditar_post_e_reacao(legenda, comentarios):
    #(Gráfico 1)
    doc = nlp(legenda)
    marcas = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    
    padrao_sinal = r'[#*]?(publi|ad|patrocinado|parceria)\b'
    padrao_cupom = r'(?i)(?:cupom|codigo|código)\s*:?\s*([A-Z0-9]+)'

    tem_sinalizacao = len(re.findall(padrao_sinal, legenda, flags=re.IGNORECASE)) > 0
    tem_vinculo = len(marcas) > 0 or len(re.findall(padrao_cupom, legenda)) > 0

    if tem_vinculo and tem_sinalizacao:
        diagnostico_publi = "Publicidade Explícita"
    elif tem_vinculo and not tem_sinalizacao:
        diagnostico_publi = "Publicidade Omissa"
    else:
        diagnostico_publi = "Post Normal"

    # Analisando comentário para o Gráfico 2
    lista_sentimentos_individuais = []
    for com in comentarios:
        resultado_ia = classificador_sentimento(com[:512])[0]
        estrelas = int(resultado_ia['label'].split()[0])
        
        if estrelas >= 4:
            lista_sentimentos_individuais.append("Alegre/Positivo")
        elif estrelas == 3:
            lista_sentimentos_individuais.append("Neutro")
        else:
            lista_sentimentos_individuais.append("Insatisfeito/Crítico")

    return diagnostico_publi, lista_sentimentos_individuais

# ==============================================================================
# 5. EXECUÇÃO DO PIPELINE DE DADOS
# ==============================================================================
print(f"\n{'='*80}\nSISTEMA DE AUDITORIA (VISÃO GRANULAR DE COMENTÁRIOS)\n{'='*80}")

dados_posts = [] 
dados_comentarios = []

for perfil in perfis_para_auditoria:
    print(f"\n📡 Analisando Perfil: @{perfil}")
    posts = buscar_posts_do_perfil(perfil)
    
    if not posts:
        print(f"   ↳ Pulando @{perfil} (Sem posts encontrados).")
        continue

    for i, post in enumerate(posts):
        ordem_post = f"{i+1}º Post"
        print(f"   ↳ Auditando {ordem_post} e classificando comentários...")
        
        comentarios_publico = buscar_comentarios_do_post(post['id'])
        diagnostico, sentimentos_individuais = auditar_post_e_reacao(post['legenda'], comentarios_publico)
        
        # Salva o Post para o Gráfico 1
        dados_posts.append({
            "Perfil": perfil,
            "Post_ID": ordem_post,
            "Diagnóstico": diagnostico
        })
        
        # Salva o comentário individualmente
        for sent in sentimentos_individuais:
            dados_comentarios.append({
                "Perfil": perfil,
                "Post": ordem_post,
                "Sentimento": sent
            })
            
        time.sleep(1)

# ==============================================================================
# 6. DASHBOARD ANALÍTICO (Gráficos Individuais)
# ==============================================================================
if dados_posts:
    print(f"\n{'='*80}\nGERANDO DASHBOARDS INDIVIDUAIS...\n{'='*80}")
    df_posts = pd.DataFrame(dados_posts)
    df_com = pd.DataFrame(dados_comentarios)

    sns.set_theme(style="whitegrid")
    perfis_auditados = df_posts["Perfil"].unique()

    for perfil in perfis_auditados:
        print(f"📊 Desenhando gráficos para o perfil: @{perfil}")
        
        df_p = df_posts[df_posts["Perfil"] == perfil]
        df_c = df_com[df_com["Perfil"] == perfil]
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        fig.suptitle(f"Auditoria de Influenciador: @{perfil}", fontsize=18, fontweight='black', color='#2c3e50')

        # GRÁFICO 1 
        sns.countplot(
            data=df_p, 
            x="Diagnóstico", 
            hue="Diagnóstico",
            order=["Post Normal", "Publicidade Omissa", "Publicidade Explícita"],
            palette={"Post Normal": "#075af3", "Publicidade Omissa": "#a00303", "Publicidade Explícita": "#fffb0b"},
            legend=False,
            ax=axes[0]
        )
        axes[0].set_title("Nível de Transparência nas Publicações", fontsize=13, fontweight='bold')
        axes[0].set_xlabel("Classificação Auditada pela IA")
        axes[0].set_ylabel("Quantidade de Posts Analisados")
        axes[0].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        # GRÁFICO 2:
        if len(df_c) > 0:
            sns.countplot(
                data=df_c, 
                y="Post", 
                hue="Sentimento", 
                hue_order=["Alegre/Positivo", "Neutro", "Insatisfeito/Crítico"],
                palette={"Alegre/Positivo": "#2ecc71", "Neutro": "#95a5a6", "Insatisfeito/Crítico": "#e74c3c"},
                ax=axes[1]
            )
            
            axes[1].set_title("Reação do Público (Comentários) X Publicação", fontsize=13, fontweight='bold')
            axes[1].set_ylabel("Publicações Analisadas")
            axes[1].set_xlabel("Quantidade de Comentários Individuais")
            axes[1].legend(title="Classificação da IA")
            axes[1].xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        else:
            axes[1].set_axis_off() 
            axes[1].text(0.5, 0.5, "Nenhum comentário encontrado neste perfil.", 
                         ha='center', va='center', fontsize=12, color='gray')

        plt.tight_layout()
        plt.show() 
else:
    print("\nNenhum dado processado para gerar os gráficos.")