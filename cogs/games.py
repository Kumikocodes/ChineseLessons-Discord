import discord
from discord import app_commands
from discord.ext import commands
import json
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open('data/vocabulario.json', 'r', encoding='utf-8') as f:
                self.vocab = json.load(f)
        except:
            self.vocab = []

    @app_commands.command(name="quiz", description="Inicia um quiz valendo XP!")
    async def quiz(self, interaction: discord.Interaction):
        if len(self.vocab) < 4:
            return await interaction.response.send_message("Preciso de mais palavras no vocabulario.json!", ephemeral=True)
        
        target = random.choice(self.vocab)
        
        # Gera opções erradas
        opcoes = [target]
        while len(opcoes) < 4:
            x = random.choice(self.vocab)
            if x['hanzi'] != target['hanzi'] and x not in opcoes:
                opcoes.append(x)
        random.shuffle(opcoes)
        
        embed = discord.Embed(title="🎮 Quiz de Chinês", description=f"Qual é a tradução de **{target['hanzi']}**?", color=0xFFA500)
        view = QuizView(target, opcoes)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="tons", description="Desafio: Adivinhe o Pinyin correto!")
    async def tons(self, interaction: discord.Interaction):
        target = random.choice(self.vocab)
        # Esse jogo é simples: Mostra o Hanzi e Português, pede o Pinyin
        embed = discord.Embed(title="🎵 Desafio dos Tons", description=f"Qual é o Pinyin de: **{target['hanzi']}** ({target['traducao']})?", color=0x00BFFF)
        # Cria opções falsas de pinyin (simulação simples)
        opcoes_pinyin = [target['pinyin']]
        
        # Pega pinyin de outras palavras aleatórias
        while len(opcoes_pinyin) < 4:
            x = random.choice(self.vocab)
            if x['pinyin'] not in opcoes_pinyin:
                opcoes_pinyin.append(x['pinyin'])
        random.shuffle(opcoes_pinyin)

        view = ToneView(target['pinyin'], opcoes_pinyin)
        await interaction.response.send_message(embed=embed, view=view)

# --- VIEWS DOS JOGOS ---

class QuizView(discord.ui.View):
    def __init__(self, target, options):
        super().__init__(timeout=30)
        self.target = target
        for opt in options:
            btn = discord.ui.Button(label=opt['traducao'], style=discord.ButtonStyle.secondary)
            btn.callback = self.create_callback(opt, btn)
            self.add_item(btn)

    def create_callback(self, opt, btn):
        async def callback(interaction: discord.Interaction):
            # Desativa tudo
            for child in self.children: child.disabled = True
            
            if opt['hanzi'] == self.target['hanzi']:
                btn.style = discord.ButtonStyle.green
                xp = 25
                lvl, up = await interaction.client.add_xp(interaction.user.id, xp)
                msg = f"✅ **Correto!** Ganhou +{xp} XP."
                if up: msg += f"\n🆙 **LEVEL UP!** Você agora é nível {lvl}!"
            else:
                btn.style = discord.ButtonStyle.red
                msg = f"❌ Errado! A resposta era **{self.target['traducao']}**."
            
            await interaction.response.edit_message(content=msg, view=self)
        return callback

class ToneView(discord.ui.View):
    def __init__(self, correct_pinyin, options):
        super().__init__(timeout=30)
        self.correct = correct_pinyin
        for opt in options:
            btn = discord.ui.Button(label=opt, style=discord.ButtonStyle.primary)
            btn.callback = self.create_callback(opt, btn)
            self.add_item(btn)

    def create_callback(self, opt, btn):
        async def callback(interaction: discord.Interaction):
            for child in self.children: child.disabled = True
            
            if opt == self.correct:
                btn.style = discord.ButtonStyle.green
                await interaction.client.add_xp(interaction.user.id, 15)
                await interaction.response.edit_message(content="✅ **Acertou o tom!** +15 XP", view=self)
            else:
                btn.style = discord.ButtonStyle.red
                await interaction.response.edit_message(content=f"❌ **Errou...** Era {self.correct}", view=self)
        return callback

async def setup(bot):
    await bot.add_cog(Games(bot))