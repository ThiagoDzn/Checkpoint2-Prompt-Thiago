import json
from pathlib import Path
from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot

_PERSONAS_PATH = Path(__file__).parent.parent / "prompts" / "system_prompts.json"
with open(_PERSONAS_PATH, encoding="utf-8") as f:
    PERSONAS = json.load(f)

def zero_shot(tarefa, input_texto):
    return montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="Domínio: Análise Financeira",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )

def few_shot(tarefa, input_texto, exemplos):
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="Domínio: Análise Financeira",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    exs = (exemplos or tarefa.get("exemplos_fewshot", []))[:3]
    return adicionar_exemplos(prompt_base, exs)

def chain_of_thought(tarefa, input_texto):
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="Domínio: Análise Financeira",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    return adicionar_cot(prompt_base, tarefa.get("passos_cot", []))

def role_prompting(tarefa, input_texto):
    chave = tarefa.get("persona", "analista_financeiro")
    persona = PERSONAS.get(chave, PERSONAS[list(PERSONAS.keys())[0]])
    system_prompt = (
        f"Você é {persona['nome']}.\n"
        f"Experiência: {persona['experiencia']}\n"
        f"Especialidade: {persona['especialidade']}\n"
        f"Tom de voz: {persona['tom_de_voz']}\n"
        f"Limitações: {persona['limitacoes']}"
    )
    user_prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto="Use sua especialidade para analisar o dado abaixo.",
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    return system_prompt, user_prompt