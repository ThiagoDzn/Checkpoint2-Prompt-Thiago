import json
import pandas as pd
from pathlib import Path

from src.llm_client import LLMClient
from src.tasks import TAREFAS
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.evaluator import medir_acuracia, contar_tokens, testar_temperatura
from src.report import gerar_tabela, grafico_acuracia, grafico_custo, grafico_temperatura, recomendar

DATA_DIR = Path("data")
INPUTS   = json.loads((DATA_DIR / "inputs.json").read_text(encoding="utf-8"))
EXEMPLOS = json.loads((DATA_DIR / "examples.json").read_text(encoding="utf-8"))

def executar_tecnica(nome_tec, tarefa, input_item, cliente, exemplos):
    input_texto = input_item["input"]
    esperado    = input_item["esperado"]
    system = ""

    if nome_tec == "zero_shot":
        prompt = zero_shot(tarefa, input_texto)
    elif nome_tec == "few_shot":
        prompt = few_shot(tarefa, input_texto, exemplos)
    elif nome_tec == "chain_of_thought":
        prompt = chain_of_thought(tarefa, input_texto)
    elif nome_tec == "role_prompting":
        system, prompt = role_prompting(tarefa, input_texto)

    resultado_llm   = cliente.chat(prompt, system=system, temp=0.3)
    resposta        = resultado_llm["resposta"]
    tokens_prompt   = resultado_llm["tokens_prompt"]   or contar_tokens(prompt + system)
    tokens_resposta = resultado_llm["tokens_resposta"] or contar_tokens(resposta)
    tempo_ms        = resultado_llm["tempo_ms"]
    acuracia        = medir_acuracia(resposta, esperado)

    return {
        "tarefa":          tarefa["nome"],
        "tecnica":         nome_tec,
        "acuracia":        acuracia,
        "tokens_prompt":   tokens_prompt,
        "tokens_resposta": tokens_resposta,
        "tokens_total":    tokens_prompt + tokens_resposta,
        "tempo_ms":        tempo_ms,
    }

def main():
    print("\n" + "="*70)
    print("  PROMPT TOOLKIT — DOMINIO FINANCEIRO")
    print("  FIAP · Prompt Engineering & AI · Checkpoint 02")
    print("="*70 + "\n")

    cliente  = LLMClient()
    todos    = []
    TECNICAS = ["zero_shot", "few_shot", "chain_of_thought", "role_prompting"]

    for nome_tarefa, tarefa in TAREFAS.items():
        inputs   = INPUTS.get(nome_tarefa, [])
        exemplos = EXEMPLOS.get(nome_tarefa, [])

        print(f"\n{'='*70}")
        print(f"  TAREFA: {nome_tarefa.upper()}")
        print(f"{'='*70}")

        for nome_tec in TECNICAS:
            print(f"\n  [{nome_tec}]")
            for i, item in enumerate(inputs):
                try:
                    r = executar_tecnica(nome_tec, tarefa, item, cliente, exemplos)
                    todos.append(r)
                    status = "OK" if r["acuracia"] >= 0.7 else "XX"
                    print(f"    [{status}] input[{i+1}] acuracia={r['acuracia']:.2f}  tokens={r['tokens_total']}  {r['tempo_ms']}ms")
                except Exception as e:
                    print(f"    [ERRO] input[{i+1}]: {e}")

    df_raw = pd.DataFrame(todos)
    df_agg = (
        df_raw
        .groupby(["tarefa", "tecnica"])
        .agg(
            acuracia_media =("acuracia",     "mean"),
            tokens_medios  =("tokens_total", "mean"),
            tempo_medio_ms =("tempo_ms",     "mean"),
        )
        .reset_index()
        .round(4)
    )

    print("\nGerando relatorio...")
    df = gerar_tabela(df_agg.to_dict("records"))

    print("Gerando graficos...")
    grafico_acuracia(df_agg)
    grafico_custo(df_agg)

    print("\nTestando temperaturas...")
    melhor_linha = df_agg.loc[df_agg["acuracia_media"].idxmax()]
    melhor_tec   = melhor_linha["tecnica"]
    melhor_tar   = melhor_linha["tarefa"]
    tarefa_obj   = TAREFAS[melhor_tar]
    input_ref    = INPUTS[melhor_tar][0]

    if melhor_tec == "role_prompting":
        system_ref, prompt_ref = role_prompting(tarefa_obj, input_ref["input"])
    elif melhor_tec == "few_shot":
        prompt_ref = few_shot(tarefa_obj, input_ref["input"], EXEMPLOS.get(melhor_tar, []))
        system_ref = ""
    elif melhor_tec == "chain_of_thought":
        prompt_ref = chain_of_thought(tarefa_obj, input_ref["input"])
        system_ref = ""
    else:
        prompt_ref = zero_shot(tarefa_obj, input_ref["input"])
        system_ref = ""

    res_temp = testar_temperatura(cliente, prompt_ref, system=system_ref, n_repeticoes=3)
    grafico_temperatura(res_temp)

    recomendar(df_agg)

    print("\nExecucao concluida!")
    print("  Resultados : output/resultados.csv")
    print("  Graficos   : output/graficos/")

if __name__ == "__main__":
    main()