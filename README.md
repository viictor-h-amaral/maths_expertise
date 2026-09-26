# Ritmo Mental

Aplicação web básica para treinar aritmética mental com uma sessão de 3 minutos.

## Executar localmente

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000` no navegador.

A aplicação permite treinos de 1, 3, 5 ou 10 minutos nos domínios naturais, inteiros, racionais, irracionais e reais. Ao fim de cada treino, exibe um resumo comparado às tentativas anteriores do mesmo domínio e duração, com opções para voltar ao início, abrir o histórico ou repetir a configuração. Em celulares, cada domínio oferece um teclado próprio, incluindo sinais, vírgula, π, e e operadores quando necessário. As tentativas ficam salvas no navegador e podem ser exportadas ou importadas em JSON ou CSV compatível com Excel. O histórico inclui um dashboard com filtros por domínio e duração, evolução de precisão e ritmo, e distribuição de partidas.
