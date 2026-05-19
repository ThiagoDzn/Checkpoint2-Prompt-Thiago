def montar_prompt(instrucao, contexto="", input_dados="", formato_output=""):
    if not instrucao.strip():
        raise ValueError("'instrucao' não pode estar vazia.")
    if not input_dados.strip():
        raise ValueError("'input_dados' não pode estar vazio.")
    partes = []
    partes.append(f"## Instrução\n{instrucao.strip()}")
    if contexto.strip():
        partes.append(f"## Contexto\n{contexto.strip()}")
    partes.append(f"## Dados\n{input_dados.strip()}")
    if formato_output.strip():
        partes.append(f"## Formato de Saída\n{formato_output.strip()}")
    return "\n\n".join(partes)

def adicionar_exemplos(prompt, exemplos):
    if not exemplos:
        return prompt
    linhas = ["## Exemplos"]
    for ex in exemplos:
        linhas.append(f'Input: "{ex["input"]}"')
        linhas.append(f'Output: "{ex["output"]}"')
        linhas.append("")
    bloco = "\n".join(linhas).rstrip()
    return bloco + "\n\n" + prompt

def adicionar_cot(prompt, passos):
    if not passos:
        return prompt
    linhas = ["## Raciocínio — Pense passo a passo:"]
    for i, passo in enumerate(passos, 1):
        linhas.append(f"{i}. {passo}")
    return prompt + "\n\n" + "\n".join(linhas)