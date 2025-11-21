# FoodInsight Agent (Project Huginn)

> **Agente Inteligente de Mercado para Food Delivery**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/Orchestration-CrewAI-orange)](https://crewai.com)
[![Groq](https://img.shields.io/badge/Inference-Llama%203.3-purple)](https://groq.com)

O **FoodInsight** é uma arquitetura de agentes de IA projetada para acelerar o ciclo de inovação em *delivery*. O sistema simula uma esteira de P&D (Pesquisa e Desenvolvimento), varrendo redes sociais em busca de tendências virais de comidas, estruturando os dados e transformando em possiveis produtos.

Enfrentei alguns desafios na sua produção que, apesar da dor de cabeça, me rendeu uma boa experiencia por resolve-los. Esta foi minha primeira produção de um agente e me abriu os olhos para usar essa ferramenta em outros projetos.

A ideia de nomea-lo de Huginn ocorreu-me quando pensei no agente como um mensageiro. Odin, tudo sabia pois seus corvos assim lhe diziam. Huginn representa o pensamento e por meio dele Odin coletava dados sobre todas as coisas.

---

## Arquitetura

O projeto implementa o padrão de orquestração **CrewAI**, coordenando três agentes especializados que atuam sequencialmente:

1.  **Huginn (Trend Scout):** 
    *   *Função:* Agente explorador que utiliza *Google Search Operators* para minerar micro-tendências no TikTok e Instagram.
    *   *Tecnologia:* Integração com SerperDev API e lógica estocástica para variação de busca.
2.  **Menu Engineer:** 
    *   *Função:* Analisa a viabilidade técnica, custos e logística de transporte (embalagem) dos produtos sugeridos.
3.  **Delivery Copywriter:** 
    *   *Função:* Gera metadados otimizados para conversão (SEO, Descrições Sensoriais) seguindo templates rígidos de UX Writing.

---

## Desenvolvimento

Abaixo, documento os principais desafios técnicos enfrentados e as soluções aplicadas:

### 1. Conflito grave de dependências (urllib3)
   *   **Desafio:** Durante a instalação de algumas bibliotecas, principalmente a Selenium e Kubernetes, geraram conflitos ao **urllib3**. Cada biblioteca exigia uma faixa de versão incompatível entre si:
   *   Selenium requeria urllib3 >= 2.5.0 e Kubernetes requeria urllib3 < 2.4.0
   *   Como não existia versão única capaz de satisfazer ambas simultaneamente, o ambiente se tornava instável e o pip reportava erros constantes do dependency resolver.
   *   **Solução:** A saída foi isolar ambientes de execução, criando virtual environments independentes para cada conjunto de dependências. Isso permitiu instalar cada biblioteca com sua própria versão compatível do urllib3, eliminando completamente o conflito.

### 2. Contexto insufiente.
   *   **Desafio:** Como todo mundo sabe, os modelos de inteligencia artificial não possuem conhecimento em tempo real. O que inviabilizaria o projeto, pois o objetivo é saber o que está em alta nas redes.
   *   **Solução:** Inserir um mecanismo de pesquisa no modelo para a IA conseguir buscar informações na internet. No caso, optei pela API do **Serper**, que faria uma ponte entre a IA com o google.
### 3. O Problema da Repetição (Loop de Alucinação)
*   **Desafio:** Inicialmente, o agente entrava em um viés de confirmação, sugerindo repetidamente o mesmo produto ("Morango do Amor") devido ao cache agressivo do framework e prompts estáticos.
*   **Solução:** Implementamos uma rotação aleatória de tópicos de busca (`search_angles`) combinada com a desativação programática do cache (`cache=False`) e seed baseada em timestamp. Isso forçou a entropia do sistema, garantindo resultados inéditos a cada execução.

### 4. Rate Limiting e Depreciação de Modelos
*   **Desafio:** Durante testes de estresse, atingimos o *Rate Limit* (TPD) da API da Groq e enfrentamos a depreciação súbita do modelo `llama-3-70b`.
*   **Solução:** 
    *   Migração imediata para o modelo `llama-3.3-70b-versatile`.
    *   Criação de uma classe de configuração (`AppConfig`) robusta para facilitar a troca rápida de modelos (Fallback para 8B) e validação de variáveis de ambiente.

### 5. Alinhamento de Expectativa (Prompt Engineering)
*   **Desafio:** O agente de marketing gerava nomes abstratos ("GlobeBite") que não performam bem em apps de delivery, onde a clareza é rei.
*   **Solução:** Refinamento das *System Instructions*. Definimos regras rígidas de formatação e um conceito "Híbrido" (Nome Descritivo + Diferencial Premium), além de proibir a criação de seções de texto isoladas para a embalagem, forçando uma narrativa fluida.
*   
> *Nota do Autor: Solucionar estas problematicas ocasionou que o custo do token se tornou mais caro. Numa aplicação real é de se pensar os custos de token do agente e seu retorno, podendo ser necessários mais ajustes para baratear a operação.*

---

## Resultados

O sistema gera automaticamente relatórios detalhados.
📂 **[Clique aqui para ver um Relatório de Tendência Real gerado pelo Huginn](sample/insight_report_v2.2.md)**


---

## Como Executar

**1. Clone o repositório:**
```bash
git clone https://github.com/umbura/foodinsight-agent.git
   cd foodinsight-agent
````
   
**2. Configure o ambiente:**
```bash
python -m venv .venv
```
   Com o ambiente configurado, você deve certificar-se de estar dentro dele no terminal para instalar os requirements.
   
   *obs: Caso você não consiga executar o script é necessario desativar a politica de execução de script temporariamente.*
```bash
pip install -r requirements.txt
```
**3. Configuração de API:**
   Crie um arquivo .env na raiz do projeto, lá você deve inserir a API Key da IA que pretende utilizar. Ex: Grok, OpenAI, VertexAI:
```bash
GROQ_API_KEY=gsk_...
SERPER_API_KEY=...
```
**4. Execute com python.**

---
## Tech Stack

*   **Linguagem:** Python 3.10+
*   **Framework:** CrewAI (Multi-Agent Systems)
*   **LLM Engine:** Llama 3.3 70B via Groq (Selecionado pela latência <1s e alta capacidade de raciocínio).
*   **Tools:** SerperDev (Web Search & Social Listening).
*   **Safety:** Gerenciamento de segredos via `.env` e validação de tipos.













