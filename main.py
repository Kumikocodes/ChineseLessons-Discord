import discord
from discord.ext import commands
import os
import aiosqlite
from dotenv import load_dotenv
import asyncio

# Carrega Token
load_dotenv()

# Configurações
DB_NAME = "database.db"

class ElysiaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="e!", intents=intents, help_command=None)

    async def setup_hook(self):
        # 1. Criação do Banco de Dados (Garante que a tabela existe)
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    correct_answers INTEGER DEFAULT 0
                )
            ''')
            await db.commit()
        
        # 2. Carregar Extensões (Cogs)
        # Certifique-se de que a pasta 'cogs' existe e tem os arquivos
        initial_extensions = ['cogs.study', 'cogs.games', 'cogs.profile']
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"✅ Módulo carregado: {extension}")
            except Exception as e:
                print(f"❌ Falha ao carregar {extension}: {e}")

        # 3. Sincronizar Comandos
        await self.tree.sync()
        print(f"🌸 {self.user} está pronta para ensinar!")

    async def add_xp(self, user_id, amount):
        """Função global segura para adicionar XP"""
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT xp, level FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()

            if not row:
                # Novo usuário
                await db.execute("INSERT INTO users (user_id, xp, level, correct_answers) VALUES (?, ?, 1, 1)", (user_id, amount))
                return 1, False # Nível 1, Sem Level Up
            
            xp, level = row
            xp += amount
            
            # Cálculo de Nível (Ex: Nível 1 precisa de 100xp, Nível 2 de 200xp...)
            xp_needed = level * 100
            leveled_up = False
            
            if xp >= xp_needed:
                level += 1
                xp = xp - xp_needed
                leveled_up = True
            
            await db.execute("UPDATE users SET xp = ?, level = ?, correct_answers = correct_answers + 1 WHERE user_id = ?", (xp, level, user_id))
            await db.commit()
            return level, leveled_up

bot = ElysiaBot()

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ ERRO: Token não encontrado no .env")
    else:
        # Cria pastas necessárias se não existirem
        if not os.path.exists('./audios'): os.makedirs('./audios')
        if not os.path.exists('./cogs'): os.makedirs('./cogs')
        
        bot.run(token)