import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT_DIR = Path("output")
GRAFICOS_DIR = OUTPUT_DIR / "graficos"
CSV_PATH = OUTPUT_DIR / "resultados.csv"

TECNICAS = ["zero_shot", "few_shot", "chain_of_thought", "role_prompting"]
CORES = {
    "zero_shot": "#4C72B0",
    "few_shot": "#DD8452",
    "chain_of_thought": "#55A868",
    "role_prompting": "#C44E52",
}

def gerar_tabela(resultados):
    df = pd.DataFrame(resultados)
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    print("\n" + "="*80)
    print("TABELA COMPARATIVA DE RESULTADOS")
    print("="*80)
    cols = ["tarefa", "tecnica", "acuracia_media", "tokens_medios", "tempo_medio_ms"]
    cols_ex = [c for c in cols if c in df.columns]
    print(df[cols_ex].to_string(index=False))
    print("="*80 + "\n")
    return df

def grafico_acuracia(df):
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    tarefas = df["tarefa"].unique()
    tecnicas = [t for t in TECNICAS if t in df["tecnica"].unique()]
    x = range(len(tarefas))
    width = 0.8 / len(tecnicas)
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, tec in enumerate(tecnicas):
        vals = [df[(df["tarefa"]==tar)&(df["tecnica"]==tec)]["acuracia_media"].mean() for tar in tarefas]
        offset = (i - len(tecnicas)/2 + 0.5) * width
        bars = ax.bar([xi+offset for xi in x], vals, width, label=tec, color=CORES[tec], alpha=0.85)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01, f"{val:.2f}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(list(x))
    ax.set_xticklabels(tarefas, rotation=15, ha="right")
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("Acurácia Média")
    ax.set_title("Acurácia por Técnica e Tarefa")
    ax.legend(loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(GRAFICOS_DIR / "acuracia.png", dpi=150)
    plt.close(fig)
    print("  [report] Gráfico salvo: output/graficos/acuracia.png")

def grafico_custo(df):
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    resumo = df.groupby("tecnica")["tokens_medios"].mean().reindex(TECNICAS).dropna()
    cores = [CORES[t] for t in resumo.index]
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(resumo.index, resumo.values, color=cores, alpha=0.85)
    for bar, val in zip(bars, resumo.values):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{val:.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Tokens Médios")
    ax.set_title("Custo de Tokens por Técnica")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(GRAFICOS_DIR / "custo_tokens.png", dpi=150)
    plt.close(fig)
    print("  [report] Gráfico salvo: output/graficos/custo_tokens.png")

def grafico_temperatura(resultados_temp):
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)
    temps = [r["temperatura"] for r in resultados_temp]
    consis = [r["consistencia"] for r in resultados_temp]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(temps, consis, marker="o", color="#4C72B0", linewidth=2, markersize=8)
    for t, c in zip(temps, consis):
        ax.annotate(f"{c:.0%}", (t, c), textcoords="offset points", xytext=(5, 5), fontsize=9)
    ax.set_xlabel("Temperatura")
    ax.set_ylabel("Consistência")
    ax.set_title("Consistência por Temperatura")
    ax.set_ylim(0, 1.1)
    ax.set_xticks(temps)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(GRAFICOS_DIR / "temperatura.png", dpi=150)
    plt.close(fig)
    print("  [report] Gráfico salvo: output/graficos/temperatura.png")

def recomendar(df):
    recomendacoes = {}
    print("\n" + "="*80)
    print("RECOMENDAÇÃO DE TÉCNICA POR TAREFA")
    print("="*80)
    for tarefa in df["tarefa"].unique():
        sub = df[df["tarefa"]==tarefa]
        melhor = sub.loc[sub["acuracia_media"].idxmax()]
        tec = melhor["tecnica"]
        acc = melhor["acuracia_media"]
        recomendacoes[tarefa] = tec
        print(f"\n  Tarefa : {tarefa}")
        print(f"  Melhor : {tec}  (acuracia={acc:.2f})")
    print("\n" + "="*80 + "\n")
    return recomendacoes