# Mapa de Autenticidade: Auditoria de Publicidade

Este projeto utiliza Processamento de Linguagem Natural (NLP) e Expressões Regulares (RE) para identificar publicidades em redes sociais.

## Como funciona:
- **Regex (RE):** Captura padrões como `@menções`, `#hashtags` e `cupons`.
- **Spacy (NLP):** Identifica entidades organizacionais (marcas) no texto.
- **Auditoria:** Cruza os dados para verificar se o post é uma publicidade explícita ou omissa.

A Expressão Regular foi modelada especificamente para capturar os "truques" de alcance dos influenciadores, como o uso de símbolos como *publi.