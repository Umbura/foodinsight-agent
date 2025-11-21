# 🦅 FoodInsight Agent (Project Huginn)

> **Sistema Autônomo de Inteligência de Mercado para Food Delivery**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/Orchestration-CrewAI-orange)](https://crewai.com)
[![Groq](https://img.shields.io/badge/Inference-Llama%203.3-purple)](https://groq.com)

O **FoodInsight** é uma arquitetura de agentes de IA projetada para acelerar o ciclo de inovação em *Dark Kitchens*. O sistema simula uma esteira de P&D (Pesquisa e Desenvolvimento), varrendo redes sociais em busca de tendências virais e transformando dados não estruturados em produtos validados para plataformas como iFood.

---

## 🏗️ Arquitetura (Agentic Workflow)

O projeto implementa o padrão de orquestração **CrewAI**, coordenando três agentes especializados que atuam sequencialmente:

1.  **🦅 Huginn (Trend Scout):** 
    *   *Função:* Agente explorador que utiliza *Google Search Operators* para minerar micro-tendências no TikTok e Instagram.
    *   *Tecnologia:* Integração com SerperDev API e lógica estocástica para variação de busca.
2.  **👨‍🍳 Menu Engineer:** 
    *   *Função:* Analisa a viabilidade técnica, custos e logística de transporte (embalagem) dos produtos sugeridos.
3.  **📱 Delivery Copywriter:** 
    *   *Função:* Gera metadados otimizados para conversão (SEO, Descrições Sensoriais) seguindo templates rígidos de UX Writing.

---

## 🚧 Jornada de Desenvolvimento & Desafios (Engineering Log)

Este projeto foi desenvolvido em ciclos rápidos de iteração. Abaixo, documentamos os principais desafios técnicos enfrentados e as soluções de engenharia aplicadas:

### 1. O Problema da Repetição (Loop de Alucinação)
*   **Desafio:** Inicialmente, o agente entrava em um viés de confirmação, sugerindo repetidamente o mesmo produto ("Morango do Amor") devido ao cache agressivo do framework e prompts estáticos.
*   **Solução:** Implementamos uma rotação aleatória de tópicos de busca (`search_angles`) combinada com a desativação programática do cache (`cache=False`) e seed baseada em timestamp. Isso forçou a entropia do sistema, garantindo resultados inéditos a cada execução.

### 2. Rate Limiting e Depreciação de Modelos
*   **Desafio:** Durante testes de estresse, atingimos o *Rate Limit* (TPD) da API da Groq e enfrentamos a depreciação súbita do modelo `llama-3-70b`.
*   **Solução:** 
    *   Migração imediata para o modelo `llama-3.3-70b-versatile`.
    *   Criação de uma classe de configuração (`AppConfig`) robusta para facilitar a troca rápida de modelos (Fallback para 8B) e validação de variáveis de ambiente.

### 3. Alinhamento de Expectativa (Prompt Engineering)
*   **Desafio:** O agente de marketing gerava nomes abstratos ("GlobeBite") que não performam bem em apps de delivery, onde a clareza é rei.
*   **Solução:** Refinamento das *System Instructions*. Definimos regras rígidas de formatação e um conceito "Híbrido" (Nome Descritivo + Diferencial Premium), além de proibir a criação de seções de texto isoladas para a embalagem, forçando uma narrativa fluida.

---

## 🛠️ Tech Stack

*   **Linguagem:** Python 3.10+
*   **Framework:** CrewAI (Multi-Agent Systems)
*   **LLM Engine:** Llama 3.3 70B via Groq (Selecionado pela latência <1s e alta capacidade de raciocínio).
*   **Tools:** SerperDev (Web Search & Social Listening).
*   **Safety:** Gerenciamento de segredos via `.env` e validação de tipos.

---

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/umbura/foodinsight-agent.git
   cd foodinsight-agent
