Um simples app para visualizar notebooks no browser e ir clicando em "next" para ir passando - Converte .ipynb em .htmls e depois mostra eles num UI simples do dash.

## Usando

- Instalar com `python3 -m pip install -r requirements.txt`;
- Baixar o .zip do seu grupo e dezipar ele - no final deve ter várias pastas, cada uma representando um aluno diferente.
- Rodar `python3 app.py`

## Limitações

- Se algum aluno não tiver submetido um .ipynb, será necessário corrigir manualmente.
- O programa roda duas vezes devido a como o dash funciona e demora ~2mins pra converter ~30 alunos


