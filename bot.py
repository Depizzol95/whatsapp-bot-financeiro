from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Dicionário para armazenar os gastos por categoria
gastos = {
    "mercado": 0,
    "combustível": 0,
    "oficina": 0,
    "farmácia": 0,
    "cerveja": 0
}

@app.route("/webhook", methods=["POST"])
def webhook():
    """Recebe mensagens do WhatsApp e processa os gastos"""
    msg = request.form.get("Body").lower().strip()  # Captura a mensagem e coloca em minúsculas
    print(f"Mensagem recebida: {msg}")  # Log para depuração

    response = MessagingResponse()
    
    palavras = msg.split()  # Divide a mensagem em palavras
    if len(palavras) == 2 and palavras[0] in gastos and palavras[1].isdigit():
        categoria = palavras[0]
        valor = float(palavras[1])
        
        gastos[categoria] += valor  # Atualiza o gasto da categoria
        response.message(f"Lançamento adicionado: {categoria} - R$ {valor:.2f}")
    
    elif msg == "balanço":
        # Resumo dos gastos
        resumo = "\n".join([f"{categoria}: R$ {valor:.2f}" for categoria, valor in gastos.items()])
        response.message(f"📊 *Balanço Geral:*\n{resumo}")

    else:
        response.message("Formato inválido! Envie algo como: 'mercado 10' ou 'balanco' para ver o total.")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
