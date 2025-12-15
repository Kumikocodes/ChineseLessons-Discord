import discord
from discord import app_commands
from discord.ext import commands
import json
import random
import os
from gtts import gTTS
import uuid

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vocab = self.load_data()

    def load_data(self):
        try:
            with open('data/vocabulario.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao ler vocabulario.json: {e}")
            return []

    async def generate_audio(self, text):
        """Gera áudio em uma thread separada para não travar o bot"""
        filename = f"audios/{uuid.uuid4()}.mp3"
        def _save():
            tts = gTTS(text, lang='zh-cn')
            tts.save(filename)
        
        # Roda o gTTS num executor para não bloquear o bot
        await self.bot.loop.run_in_executor(None, _save)
        return filename

    # --- COMANDO DE ESTUDAR POR CATEGORIA ---
    @app_commands.command(name="estudar", description="Abra o menu de categorias para estudar.")
    async def estudar(self, interaction: discord.Interaction):
        # Pega categorias únicas
        categorias = list(set([item.get('categoria', 'Geral') for item in self.vocab]))
        view = CategorySelectView(categorias, self.vocab, self)
        embed = discord.Embed(title="📚 Central de Estudos", description="Selecione uma categoria abaixo para começar!", color=0xFFC0CB)
        await interaction.response.send_message(embed=embed, view=view)

    # --- COMANDO DICIONARIO ---
    @app_commands.command(name="dicionario", description="Busca uma palavra.")
    async def dicionario(self, interaction: discord.Interaction, palavra: str):
        await interaction.response.defer() # Dá mais tempo para gerar o áudio
        palavra = palavra.lower()
        found = next((i for i in self.vocab if palavra in i['hanzi'] or palavra in i['traducao'].lower()), None)
        
        if found:
            audio_path = await self.generate_audio(found['hanzi'])
            file = discord.File(audio_path, filename="pronuncia.mp3")
            
            embed = discord.Embed(title=f"🇨🇳 {found['hanzi']} ({found['pinyin']})", color=0x00FF00)
            embed.add_field(name="Tradução", value=found['traducao'])
            embed.add_field(name="Categoria", value=found.get('categoria', 'Geral'))
            
            # Se tiver imagem no JSON, adiciona
            if found.get('imagem'):
                embed.set_thumbnail(url=found['imagem'])

            await interaction.followup.send(embed=embed, file=file)
            os.remove(audio_path)
        else:
            await interaction.followup.send(f"Não encontrei '{palavra}'.", ephemeral=True)

# --- VIEWS (MENUS E BOTÕES) ---
class CategorySelectView(discord.ui.View):
    def __init__(self, categories, vocab, cog):
        super().__init__()
        self.vocab = vocab
        self.cog = cog
        
        # Cria o menu dropdown
        select = discord.ui.Select(placeholder="Escolha uma categoria...", min_values=1, max_values=1)
        for cat in categories:
            select.add_option(label=cat, description=f"Vocabulário de {cat}")
        
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        categoria_escolhida = interaction.data['values'][0]
        # Filtra palavras dessa categoria
        palavras_cat = [w for w in self.vocab if w.get('categoria') == categoria_escolhida]
        
        if not palavras_cat:
            await interaction.response.send_message("Categoria vazia!", ephemeral=True)
            return

        palavra = random.choice(palavras_cat)
        
        # Gera Flashcard
        audio_path = await self.cog.generate_audio(palavra['hanzi'])
        file = discord.File(audio_path, filename="pronuncia.mp3")
        
        embed = discord.Embed(title=f"🗂️ Categoria: {categoria_escolhida}", color=0xFFC0CB)
        embed.add_field(name="Hanzi", value=f"# {palavra['hanzi']}", inline=False)
        embed.add_field(name="Pinyin", value=f"||{palavra['pinyin']}||", inline=False)
        embed.add_field(name="Tradução", value=f"||{palavra['traducao']}||", inline=False)
        
        await interaction.response.send_message(embed=embed, file=file)
        os.remove(audio_path)

async def setup(bot):
    await bot.add_cog(Study(bot))