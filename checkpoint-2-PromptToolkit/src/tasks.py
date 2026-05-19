TAREFAS = {
    "classificacao_risco": {
        "nome": "classificacao_risco",
        "tipo": "classificacao",
        "instrucao": "Classifique o nível de risco financeiro do texto como: BAIXO, MEDIO, ALTO ou CRITICO.",
        "formato_output": "Responda APENAS com uma das palavras: BAIXO, MEDIO, ALTO ou CRITICO. Sem explicações adicionais.",
        "exemplos_fewshot": [
            {"input": "Empresa com dívida/EBITDA de 1,2x e caixa robusto.", "output": "BAIXO"},
            {"input": "Companhia com alavancagem de 4x e vencimento de dívida em 6 meses.", "output": "ALTO"},
            {"input": "Startup com burn rate acelerado e sem receita recorrente.", "output": "CRITICO"},
        ],
        "passos_cot": [
            "Identifique indicadores de endividamento mencionados no texto.",
            "Avalie a liquidez: há menção de caixa, reservas ou acesso a crédito?",
            "Verifique se há prazos de vencimento próximos ou inadimplência.",
            "Considere o setor e o contexto macroeconômico implícito.",
            "Com base nos pontos acima, classifique o risco: BAIXO, MEDIO, ALTO ou CRITICO.",
        ],
        "persona": "analista_financeiro",
    },
    "extracao_indicadores": {
        "nome": "extracao_indicadores",
        "tipo": "extracao",
        "instrucao": "Extraia os indicadores financeiros presentes no texto e retorne um JSON com as chaves: receita, lucro_liquido, margem, divida, ebitda. Use null para campos não mencionados.",
        "formato_output": 'Responda APENAS com um JSON válido, sem texto adicional. Exemplo: {"receita": "R$500M", "lucro_liquido": "R$80M", "margem": "16%", "divida": null, "ebitda": "R$120M"}',
        "exemplos_fewshot": [
            {"input": "A empresa registrou receita de R$1,2 bilhão e EBITDA de R$300 milhões.", "output": '{"receita": "R$1,2B", "lucro_liquido": null, "margem": null, "divida": null, "ebitda": "R$300M"}'},
            {"input": "Lucro líquido de R$45M com margem de 12% sobre receita de R$375M.", "output": '{"receita": "R$375M", "lucro_liquido": "R$45M", "margem": "12%", "divida": null, "ebitda": null}'},
            {"input": "Dívida bruta de R$2B e caixa de R$800M, resultando em dívida líquida de R$1,2B.", "output": '{"receita": null, "lucro_liquido": null, "margem": null, "divida": "R$1,2B", "ebitda": null}'},
        ],
        "passos_cot": [
            "Leia o texto e identifique todos os valores numéricos mencionados.",
            "Associe cada valor ao indicador correto: receita, lucro, margem, dívida ou EBITDA.",
            "Normalize as unidades (M = milhões, B = bilhões).",
            "Para campos não mencionados, use null.",
            "Monte o JSON final com as 5 chaves obrigatórias.",
        ],
        "persona": "analista_contabil",
    },
    "sumarizacao_relatorio": {
        "nome": "sumarizacao_relatorio",
        "tipo": "sumarizacao",
        "instrucao": "Resuma o trecho do relatório financeiro em até 3 bullet points destacando os pontos mais relevantes para um investidor.",
        "formato_output": "Responda com exatamente 3 bullet points iniciados por '•'. Cada bullet deve ter no máximo 20 palavras.",
        "exemplos_fewshot": [
            {"input": "No 3T24, a companhia apresentou crescimento de 18% na receita líquida, atingindo R$2,3 bilhões. O EBITDA ajustado cresceu 22%, com margem de 21,5%.", "output": "• Receita cresceu 18% no 3T24, atingindo R$2,3B.\n• EBITDA ajustado subiu 22% com margem de 21,5%.\n• Resultado impulsionado por crescimento orgânico."},
            {"input": "A empresa anunciou recompra de até 5% das ações e pagamento de dividendos de R$1,20 por ação, totalizando R$480M.", "output": "• Programa de recompra de até 5% das ações aprovado.\n• Dividendos de R$1,20/ação, totalizando R$480M.\n• Sinaliza confiança da gestão na geração de caixa."},
        ],
        "passos_cot": [
            "Identifique o tema central do trecho.",
            "Selecione os 3 fatos mais relevantes para um investidor.",
            "Formule cada fato de forma concisa, com no máximo 20 palavras.",
            "Inicie cada linha com '•'.",
        ],
        "persona": "analista_financeiro",
    },
}