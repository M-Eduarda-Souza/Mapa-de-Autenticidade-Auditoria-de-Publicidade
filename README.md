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

<<<<<<< HEAD
│ ------└── base_dados.py # Suporte para dados locais
=======
│ ------└── base_dados.py # Suporte para dados locais
>>>>>>> 72fbbca (3 fase do projeto, auditoria + análise de sentimetos e dashboards individuais)
