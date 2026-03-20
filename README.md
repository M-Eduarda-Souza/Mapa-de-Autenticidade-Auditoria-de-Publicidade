# 🛡️ Sistema de Auditoria: Mapa de Autenticidade

Este projeto foi desenvolvido como parte da disciplina de Métodos Estatísticos Aplicados às Ciências Tecnológicas (ou sua matéria de Programação/Dados) na UFPB. O objetivo é realizar uma auditoria automatizada em legendas de redes sociais (TikTok) para identificar publicidades não sinalizadas.

## Etapa 1


Este projeto utiliza Processamento de Linguagem Natural (NLP) e Expressões Regulares (RE) para identificar publicidades em redes sociais, com base em dados estáticos.

### Como funciona:
- **Regex (RE):** Captura padrões como `@menções`, `#hashtags` e `cupons`.
- **Spacy (NLP):** Identifica entidades organizacionais (marcas) no texto.
- **Auditoria:** Cruza os dados para verificar se o post é uma publicidade explícita ou omissa.

A Expressão Regular foi modelada especificamente para capturar os "truques" de alcance dos influenciadores, como o uso de símbolos como *publi.

## Etapa 2
Diferente da primeira fase, que utilizava dados estáticos, esta versão:

Coleta de Dados Real: Utiliza a TikTok Scraper API (via RapidAPI) para buscar posts em tempo real.

Base de Dados Externa: Gerencia os perfis auditados através de um arquivo de configuração modular (perfis.py).

Processamento Multi-Perfil: Capacidade de auditar diversos influenciadores em um único ciclo de execução.

### 🛠️ Tecnologias Utilizadas
Python 3.13

spaCy: Processamento de Linguagem Natural com o modelo pt_core_news_lg para identificação de marcas (NER).

Regex (re): Expressões regulares para detecção de cupons e hashtags obrigatórias (#publi, #ad).

Requests: Comunicação com Web APIs REST.

RapidAPI: Gateway para acesso aos dados do TikTok sem bloqueios de segurança (Erro 403).

### 📋 Como Funciona
-**Importação:** O sistema lê a lista de usuários em perfis.py.

-**Coleta:** Para cada usuário, a API busca as 10 legendas mais recentes.

-**Análise de IA:**
O spaCy identifica se nomes de empresas (entidades ORG) aparecem no texto.

O Regex busca por padrões de cupons de desconto.

-**Diagnóstico:**

✅ PUBLICIDADE EXPLÍCITA: Vínculo comercial detectado e sinalizado.

⚠️ PUBLICIDADE OMISSA: Marcas ou cupons detectados sem sinalização clara.

📑 POST ANALISADO: Conteúdo orgânico sem indícios comerciais.

## 📁 Estrutura do Projeto

├── etapa1/           # Versão inicial com base estática

├── etapa2/           # Versão atual com Web API

│ -----  ├── apiEtapa2.py  # Código principal (Lógica e Coleta)

│ ----- ├── perfis.py     # Base de dados de influenciadores

│ ------└── base_dados.py # Suporte para dados locais

# Etapa 3

# 📊 Auditoria de Influenciadores: Transparência e Sentimento

Este projeto de **Ciência de Dados para Negócios** tem como objetivo auditar automaticamente postagens de influenciadores no Instagram, cruzando o nível de transparência das publicidades (Explicita vs. Omissa) com a reação real do público (Análise de Sentimento dos comentários).

## 🚀 Funcionalidades do Pipeline de Dados (ETL)

1. **Extração (Web Scraping / APIs):**
   * Coleta das últimas postagens do perfil via API RESTful (Método `GET`).
   * Extração granular de todos os comentários reais de cada post auditado (Método `POST`).

2. **Transformação e Análise (Inteligência Artificial & NLP):**
   * **Auditoria de Legenda:** Utilização da biblioteca `spaCy` (pt_core_news_lg) para Reconhecimento de Entidades Nomeadas (NER) e Expressões Regulares (Regex) para identificar marcas e cupons, classificando o post como *Publicidade Explícita*, *Publicidade Omissa* ou *Post Normal*.
   * **Análise de Sentimento (Público):** Utilização da biblioteca `Transformers` (Hugging Face) com o modelo *BERT Multilingual* para ler e interpretar o contexto de cada comentário individual, classificando-os como *Positivos/Alegres*, *Neutros* ou *Críticos/Insatisfeitos*.

3. **Carga e Visualização (Data Visualization):**
   * Geração automática de Dashboards individuais para cada perfil analisado utilizando `Pandas`, `Matplotlib` e `Seaborn`.
   * Visão granular do volume de publicidade vs. a reação específica do público em cada postagem.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Processamento de Linguagem Natural (NLP):** spaCy, Hugging Face Transformers (BERT)
* **Manipulação e Visualização de Dados:** Pandas, Matplotlib, Seaborn
* **Integração de Dados:** Biblioteca `requests` para consumo da RapidAPI (Instagram Looter 2 e instagram120)

## ⚙️ Como Executar

1. Instale as dependências do projeto:
   ```bash
   pip install requests spacy transformers pandas matplotlib seaborn torch
   python -m spacy download pt_core_news_lg
