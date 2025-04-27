# 🤖 Bot DivNinja Discord

Automação ultra-stealth para envio de mensagens diretas no Discord, focada em divulgação segura, inteligente e de alta performance.

---

## 📋 Sobre o Projeto

O **Bot DivNinja Discord** coleta usuários ativos em servidores, envia mensagens diretas com comportamento humano realista e alterna automaticamente entre múltiplos tokens para reduzir riscos de detecção e banimento.

O objetivo principal é maximizar a entrega de mensagens e minimizar a exposição da conta no ambiente do Discord.


---

## 🚀 Funcionalidades

- 🎯 **Coleta de usuários ativos** através das mensagens em canais de texto.
- 🧠 **Envio humanizado** (nonce realista, headers dinâmicos, delays variáveis).
- 🔄 **Rotação automática de tokens** após X mensagens enviadas.
- ⏳ **Delays naturais entre envios** (60 a 120 segundos).
- 💤 **Pausas longas aleatórias** a cada 5 mensagens (10 a 20 minutos).
- 📑 **Registros automáticos** de quem já recebeu ou recusou mensagens.
- 📜 **Logs completos** em tempo real.


---

## 📂 Estrutura de Arquivos

```plaintext
bot_divninjaDiscord.py    # Código principal do bot
tokens.txt                # Lista de tokens de contas fake (um por linha)
enviados.txt              # IDs que já receberam mensagem
falhou_dm.txt             # IDs que não aceitam DMs
bot_divninjaDiscord.log   # Log de atividades do bot
```


---

## ⚙️ Tecnologias Utilizadas

- Python 3.11+
- requests
- json
- base64
- logging


---

## 🔥 Como usar

1. Crie o arquivo `tokens.txt` com **um token válido por linha**.
2. (`enviados.txt` e `falhou_dm.txt` serão criados automaticamente apos iniciar o bot).
3. Execute o bot:

```bash
python bot_divninjaDiscord.py
```

4. O bot vai:
    - Conectar com o primeiro token
    - Coletar usuários ativos
    - Enviar até 10 mensagens por conta
    - Trocar automaticamente para o próximo token


---

## ⚡ Resultados Esperados

- Alta taxa de entrega para usuários reais.
- Redução significativa no risco de bloqueios e banimentos.
- Comportamento indistinguível de um humano no Discord.


---

## 📜 Aviso

> Este projeto foi desenvolvido totalmente por mim, JF! **apenas para fins educacionais e de testes**.
>
> O uso de automações em contas pessoais no Discord pode violar os Termos de Serviço da plataforma.


---

## 🧠 Desenvolvido por **JF CREATIVE LAB**

Codigo Aberto, totalmente gratis para testes e novas versões

Com foco em alta performance, stealth e automação profissional no ambiente Discord!

---

**Obrigado por conferir o projeto!** 🚀
