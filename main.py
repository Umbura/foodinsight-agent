"""
FoodInsight Agent (Project Huginn)
==================================
Sistema de inteligência de mercado baseado em Agentes Autônomos.

Updates v2.2:
- FIX: Formatação da Descrição Longa (Layout unificado e sem rótulos meta).
- FIX: Problema de Repetição (Implementação de rotação aleatória de tópicos de busca).
- Feature: Busca Social integrada.
- Melhorias gerais de estabilidade e clareza do código.
Version: 2.2.0 (Stable Output)
"""

import os
import logging
import sys
import random # Importante para variar o resultado
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# --- 1. LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("FoodInsight")

# --- 2. CONFIG ---
@dataclass
class AppConfig:
    groq_api_key: str
    serper_api_key: Optional[str] = None
    model_name: str = "groq/llama-3.3-70b-versatile" 
    temperature: float = 0.85

    @classmethod
    def load(cls) -> 'AppConfig':
        load_dotenv()
        return cls(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            serper_api_key=os.getenv("SERPER_API_KEY")
        )

# --- 3. SYSTEM CORE ---
class FoodInsightCrew:
    def __init__(self, config: AppConfig):
        self.config = config
        self.llm = LLM(
            model=self.config.model_name,
            api_key=self.config.groq_api_key,
            temperature=self.config.temperature
        )
        self.search_tool = SerperDevTool() if self.config.serper_api_key else None

    def _create_agents(self) -> List[Agent]:
        
        # Agente 1: Pesquisador
        self.researcher = Agent(
            role='Huginn - Social Trend Scout',
            goal='Mapear oportunidades virais inexploradas (Fugir do óbvio)',
            backstory=(
                "Você é um caçador de tendências que odeia o 'mais do mesmo'. "
                "Se todo mundo está falando de 'Morango do Amor', você busca a próxima coisa. "
                "Você vasculha TikTok e Instagram buscando o que está começando a crescer."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.search_tool] if self.search_tool else []
        )

        # Agente 2: Arquiteto 
        self.architect = Agent(
            role='Menu Engineer',
            goal='Transformar tendência em produto de delivery viável',
            backstory="Engenheiro de alimentos focado em operação, custo e transportabilidade.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        # Agente 3: Marketing
        self.strategist = Agent(
            role='Delivery Copywriter',
            goal='Gerar descrições no formato Padrão Ouro do iFood',
            backstory=(
                "Copywriter sênior. Você não explica o que está fazendo, você apenas entrega o texto pronto. "
                "Você segue templates visuais rigorosamente. Você sabe embutir a segurança da embalagem "
                "dentro da narrativa sensorial, sem criar parágrafos separados chatos."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        return [self.researcher, self.architect, self.strategist]

    def _create_tasks(self) -> List[Task]:
        # LÓGICA ANTI-REPETIÇÃO:
        # Sorteamos um "ângulo" de pesquisa diferente a cada execução.
        search_angles = [
            "lanches salgados virais tiktok brasil 2025",
            "novos sabores de hamburguer artesanal tendencias",
            "comida de rua coreana popular no brasil",
            "sobremesas diferentes delivery 2025",
            "sanduiches gourmet tendencias instagram",
            "fusion food brasil tendencias rua"
        ]
        chosen_angle = random.choice(search_angles)
        logger.info(f"🎲 Ângulo de pesquisa sorteado: '{chosen_angle}'")

        task_scan = Task(
            description=f"""
            Use a ferramenta de busca para investigar este tópico: "{chosen_angle}".
            
            REGRAS DE PESQUISA:
            1. Ignore "Morango do Amor" ou "Copo da Felicidade" (estão saturados).
            2. Busque algo NOVO ou uma variação criativa.
            3. O foco é encontrar um produto que possa ser vendido no delivery HOJE.
            """,
            expected_output="Relatório com 3 oportunidades de produtos detectadas.",
            agent=self.researcher
        )

        task_design = Task(
            description=(
                "Escolha a melhor oportunidade da lista. "
                "Defina o produto tecnicamente: Nome, Ingredientes e Solução de Embalagem."
            ),
            expected_output="Ficha técnica do produto.",
            agent=self.architect,
            context=[task_scan]
        )

        task_marketing = Task(
            description="""
            Crie o cadastro do produto seguindo ESTRITAMENTE o modelo abaixo.
            Não adicione textos como "Aqui está a descrição". Apenas preencha o modelo.
            
            REGRAS DE CONTEÚDO:
            - Nome: Deve ser [Produto] + [Diferencial]. Ex: "Smash Burger Angus com Crosta".
            - Descrição Longa: Deve ser um texto fluido. Fale dos ingredientes, do sabor e, 
              no meio ou final do parágrafo, mencione que a embalagem garante que chegue perfeito.
              NÃO crie um subtítulo "Segurança da Embalagem". Integre isso no texto.
            
            --- MODELO DE SAÍDA (Copie este formato) ---
            ### NOME: [Insira Nome Aqui]

            ### DESCRIÇÃO CURTA: 
            [Insira Descrição de 140 chars]

            ### DESCRIÇÃO LONGA: 
            [Insira Texto Persuasivo de 1 parágrafo longo, incluindo sabor e embalagem]

            ### HASHTAGS: 
            - #[Tag1]
            - #[Tag2]
            - #[Tag3]
            - #[Tag4]
            - #[Tag5]
            --------------------------------------------
            """,
            expected_output="Texto formatado no layout solicitado.",
            agent=self.strategist,
            context=[task_design]
        )

        return [task_scan, task_design, task_marketing]

    def run(self) -> str:
        logger.info("Inicializando Squad...")
        
        # Force random seed refresh
        random.seed(datetime.now().timestamp())
        
        agents = self._create_agents()
        tasks = self._create_tasks()

        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential,
            cache=False, # cache desativado para evitar vieses
            memory=False
        )

        return crew.kickoff()

# --- 4. ENTRY POINT ---
if __name__ == "__main__":
    try:
        
        config = AppConfig.load()
        system = FoodInsightCrew(config)
        
        print("\n🦅 Huginn v2.2 (Social + Anti-Loop + Clean Layout)...\n")
        
        result = system.run()
        
        output_file = "insight_report.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(result))
            
        print(f"\n✅ Relatório gerado: {output_file}")

    except Exception as e:
        logger.critical(f"Erro: {e}", exc_info=True)