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

A aplicação gera somas, subtrações, multiplicações e divisões exatas. Ao fim da sessão, mostra acertos, erros, precisão e cálculos por minuto.
