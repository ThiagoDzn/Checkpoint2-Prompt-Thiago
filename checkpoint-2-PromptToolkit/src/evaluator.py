import json

def contar_tokens(texto):
    return max(1, round(len(texto.split()) * 1.35))

def medir_acuracia(resposta, esperado):
    if isinstance(esperado, dict):
        return _acuracia_dict(resposta, esperado)
    return _acuracia_texto(resposta, str(esperado))

def _acuracia_texto(resposta, esperado):
    r = resposta.strip().upper()
    e = esperado.strip().upper()
    if r == e:
        return 1.0
    if e in r:
        return 0.7
    return 0.0

def _acuracia_dict(resposta, esperado):
    try:
        inicio = resposta.find("{")
        fim = resposta.rfind("}") + 1
        if inicio == -1 or fim == 0:
            return 0.0
        obtido = json.loads(resposta[inicio:fim])
    except:
        return 0.0
    if not esperado:
        return 0.0
    acertos = 0
    for chave, valor_esp in esperado.items():
        valor_obt = obtido.get(chave)
        if valor_esp is None and valor_obt is None:
            acertos += 1
        elif valor_esp is not None and valor_obt is not None:
            if str(valor_esp).strip().upper() == str(valor_obt).strip().upper():
                acertos += 1
            else:
                acertos += 0.5
    return round(acertos / len(esperado), 4)

def medir_consistencia(respostas):
    if not respostas:
        return 0.0
    normalizadas = [r.strip().upper() for r in respostas]
    mais_freq = max(set(normalizadas), key=normalizadas.count)
    return round(normalizadas.count(mais_freq) / len(normalizadas), 4)

def testar_temperatura(cliente, prompt, system="", temps=None, n_repeticoes=3):
    if temps is None:
        temps = [0.1, 0.5, 1.0]
    resultados = []
    for temp in temps:
        respostas = []
        tokens_tot = 0
        tempo_tot = 0.0
        for _ in range(n_repeticoes):
            r = cliente.chat(prompt, system=system, temp=temp)
            respostas.append(r["resposta"])
            tokens_tot += r["tokens_prompt"] + r["tokens_resposta"]
            tempo_tot += r["tempo_ms"]
        resultados.append({
            "temperatura": temp,
            "consistencia": medir_consistencia(respostas),
            "tokens_medios": round(tokens_tot / n_repeticoes, 1),
            "tempo_medio_ms": round(tempo_tot / n_repeticoes, 1),
            "respostas": respostas,
        })
    return resultados