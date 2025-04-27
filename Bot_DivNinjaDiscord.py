#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot de Divulgação Automática no Discord (Bot_DivNinjaDiscord) By JF
O Bot DivNinja Discord foi desenvolvido com o objetivo de criar uma automação altamente eficiente, segura e discreta para divulgação via mensagens diretas (DMs) no Discord.
"""

import requests
import random
import time
import os
import json
import logging
from datetime import datetime

# Configuração de logs com codificação UTF-8 para evitar erros com emojis
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("Bot_DivNinjaDiscord.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Bot_DivNinjaDiscord")

# Solicita o token ao iniciar o programa
TOKEN = input("Cole o token da sua conta Discord: ")

# Configurações do bot
DELAYS = [25, 30, 35, 45]  # Delays variados em segundos
PAUSA_A_CADA = 10  # Pausa a cada X mensagens enviadas
TEMPO_PAUSA = (180, 300)  # Tempo de pausa em segundos (min, max)

# Caminhos dos arquivos de registro
ARQUIVO_ENVIADOS = "enviados.txt"
ARQUIVO_FALHOU = "falhou_dm.txt"

# Mensagens rotativas para envio
MENSAGENS = [ Sua mensagem aqui ]  # Adicione suas mensagens aqui

# Headers para as requisições
headers = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def carregar_arquivo(nome_arquivo):
    """Carrega IDs de usuários de um arquivo."""
    if not os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            pass
        return set()
    
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        return set(linha.strip() for linha in f if linha.strip())

def salvar_usuario(user_id, arquivo):
    """Salva o ID do usuário no arquivo especificado."""
    with open(arquivo, 'a', encoding='utf-8') as f:
        f.write(f"{user_id}\n")

def obter_servidores():
    """Obtém a lista de servidores (guilds) que o usuário está."""
    url = "https://discord.com/api/v9/users/@me/guilds"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Erro ao obter servidores: {response.status_code} - {response.text}")
        return []

def obter_canais_texto(guild_id):
    """Obtém a lista de canais de texto de um servidor."""
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Filtra apenas canais de texto (type 0)
        return [canal for canal in response.json() if canal['type'] == 0]
    else:
        logger.error(f"Erro ao obter canais do servidor {guild_id}: {response.status_code} - {response.text}")
        return []

def obter_mensagens_canal(channel_id, limit=100):
    """Obtém mensagens de um canal para extrair usuários ativos."""
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Erro ao obter mensagens do canal {channel_id}: {response.status_code} - {response.text}")
        return []

def criar_dm(user_id):
    """Cria um canal de DM com um usuário."""
    url = "https://discord.com/api/v9/users/@me/channels"
    data = {
        "recipient_id": user_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["id"]
    else:
        logger.error(f"Erro ao criar DM com usuário {user_id}: {response.status_code} - {response.text}")
        return None

def enviar_mensagem(channel_id, mensagem):
    """Envia uma mensagem para um canal."""
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    data = {
        "content": mensagem
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return True
    else:
        logger.error(f"Erro ao enviar mensagem para o canal {channel_id}: {response.status_code} - {response.text}")
        return False

def main():
    # Carrega os IDs de usuários que já receberam mensagens
    usuarios_enviados = carregar_arquivo(ARQUIVO_ENVIADOS)
    usuarios_falhou = carregar_arquivo(ARQUIVO_FALHOU)
    
    logger.info("Bot iniciado!")
    logger.info(f"{len(usuarios_enviados)} usuários já receberam mensagens anteriormente.")
    logger.info(f"{len(usuarios_falhou)} usuários com DMs bloqueadas registrados.")
    
    # Obtém a lista de servidores
    servidores = obter_servidores()
    logger.info(f"Conectado em {len(servidores)} servidores.")
    
    # Lista para armazenar todos os usuários ativos
    todos_usuarios = set()
    
    # Coleta usuários ativos de todos os servidores
    for servidor in servidores:
        guild_id = servidor["id"]
        guild_name = servidor["name"]
        
        try:
            logger.info(f"Coletando usuários ativos do servidor: {guild_name} (ID: {guild_id})")
            
            # Obtém canais de texto do servidor
            canais = obter_canais_texto(guild_id)
            logger.info(f"Encontrados {len(canais)} canais de texto no servidor {guild_name}")
            
            # Limita a 5 canais por servidor para evitar rate limits
            canais_para_verificar = canais[:5] if len(canais) > 5 else canais
            
            # Coleta usuários de mensagens recentes em cada canal
            for canal in canais_para_verificar:
                canal_id = canal["id"]
                canal_nome = canal["name"]
                
                logger.info(f"Verificando mensagens no canal #{canal_nome}")
                
                # Obtém mensagens recentes
                mensagens = obter_mensagens_canal(canal_id, 50)
                
                # Extrai IDs de usuários das mensagens
                for msg in mensagens:
                    user_id = msg["author"]["id"]
                    username = msg["author"]["username"]
                    
                    # Ignora bots e a própria conta
                    if msg["author"].get("bot", False) or user_id == TOKEN.split(".")[0]:
                        continue
                    
                    # Verifica se o usuário já recebeu mensagem ou falhou anteriormente
                    if user_id not in usuarios_enviados and user_id not in usuarios_falhou:
                        todos_usuarios.add((user_id, username, msg["author"].get("discriminator", "0000")))
                
                # Pausa entre canais para evitar rate limits
                time.sleep(1)
        
        except Exception as e:
            logger.error(f"Erro ao processar servidor {guild_name}: {e}")
    
    # Converte para lista e embaralha
    usuarios_lista = list(todos_usuarios)
    random.shuffle(usuarios_lista)
    
    logger.info(f"Total de {len(usuarios_lista)} usuários únicos para enviar mensagens.")
    
    # Contadores para estatísticas
    total_enviados = 0
    total_falhou = 0
    
    # Contador para controlar as pausas
    contador_mensagens = 0
    
    # Envia mensagens para cada usuário
    for user_id, username, discriminator in usuarios_lista:
        # Verifica novamente se o usuário já recebeu mensagem
        if user_id in usuarios_enviados or user_id in usuarios_falhou:
            continue
        
        # Seleciona uma mensagem aleatória
        mensagem = random.choice(MENSAGENS)
        
        try:
            # Cria um canal de DM com o usuário
            dm_channel_id = criar_dm(user_id)
            
            if dm_channel_id:
                # Tenta enviar a mensagem
                if enviar_mensagem(dm_channel_id, mensagem):
                    # Registra o envio bem-sucedido
                    salvar_usuario(user_id, ARQUIVO_ENVIADOS)
                    usuarios_enviados.add(user_id)
                    total_enviados += 1
                    
                    logger.info(f"Mensagem enviada para: {username}#{discriminator} (ID: {user_id}) ✅")
                    
                    # Incrementa o contador de mensagens
                    contador_mensagens += 1
                    
                    # Verifica se é hora de fazer uma pausa
                    if contador_mensagens >= PAUSA_A_CADA:
                        tempo_pausa = random.randint(TEMPO_PAUSA[0], TEMPO_PAUSA[1])
                        logger.info(f"Pausa de {tempo_pausa//60} minutos para evitar detecção...")
                        time.sleep(tempo_pausa)
                        contador_mensagens = 0  # Reinicia o contador
                    else:
                        # Delay variado entre mensagens para simular comportamento humano
                        tempo_espera = random.choice(DELAYS)
                        logger.info(f"Aguardando {tempo_espera} segundos antes da próxima mensagem...")
                        time.sleep(tempo_espera)
                else:
                    # Falha ao enviar mensagem
                    logger.warning(f"Falha ao enviar mensagem para {username}#{discriminator} (ID: {user_id}).")
                    salvar_usuario(user_id, ARQUIVO_FALHOU)
                    usuarios_falhou.add(user_id)
                    total_falhou += 1
            else:
                # Falha ao criar canal de DM
                logger.warning(f"Usuário {username}#{discriminator} (ID: {user_id}) não aceita DMs.")
                salvar_usuario(user_id, ARQUIVO_FALHOU)
                usuarios_falhou.add(user_id)
                total_falhou += 1
        
        except Exception as e:
            # Outros erros
            logger.error(f"Erro ao processar usuário {username}#{discriminator} (ID: {user_id}): {e}")
            salvar_usuario(user_id, ARQUIVO_FALHOU)
            usuarios_falhou.add(user_id)
            total_falhou += 1
    
    # Finaliza o processo
    logger.info("✅ Envio finalizado!")
    logger.info(f"Total enviados: {total_enviados}")
    logger.info(f"Total recusados: {total_falhou}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Processo interrompido pelo usuário.")
    except Exception as e:
        logger.critical(f"Erro crítico: {e}")
