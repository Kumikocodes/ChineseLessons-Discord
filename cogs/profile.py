import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="perfil", description="Veja seu progresso.")
    async def perfil(self, interaction: discord.Interaction):
        async with aiosqlite.connect("database.db") as db:
            cursor = await db.execute("SELECT xp, level, correct_answers FROM users WHERE user_id = ?", (interaction.user.id,))
            data = await cursor.fetchone()
        
        if not data:
            await interaction.response.send_message("Você ainda não tem XP! Use `/quiz` ou `/estudar`.", ephemeral=True)
            return
            
        xp, level, answers = data
        prox_nivel = level * 100
        
        embed = discord.Embed(title=f"👤 Estudante {interaction.user.name}", color=0xFF69B4)
        embed.set_thumbnail(url=interaction.user.avatar.url if interaction.user.avatar else None)
        embed.add_field(name="Nível", value=f"🏅 {level}", inline=True)
        embed.add_field(name="XP Atual", value=f"✨ {xp} / {prox_nivel}", inline=True)
        embed.add_field(name="Respostas Corretas", value=f"✅ {answers}", inline=False)
        
        # Barra de progresso visual
        progresso = int((xp / prox_nivel) * 10)
        barra = "🟩" * progresso + "⬜" * (10 - progresso)
        embed.add_field(name="Progresso", value=barra, inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ranking", description="Quem são os melhores estudantes?")
    async def ranking(self, interaction: discord.Interaction):
        async with aiosqlite.connect("database.db") as db:
            cursor = await db.execute("SELECT user_id, level, xp FROM users ORDER BY level DESC, xp DESC LIMIT 5")
            rows = await cursor.fetchall()
        
        desc = ""
        for i, row in enumerate(rows):
            uid, lvl, xp = row
            # Tenta pegar o nome do usuário (pode ser None se ele saiu do server)
            user = self.bot.get_user(uid)
            nome = user.name if user else "Estudante Desconhecido"
            medalha = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
            desc += f"{medalha} **{nome}** - Nível {lvl} ({xp} XP)\n"
            
        embed = discord.Embed(title="🏆 Top 5 Estudantes", description=desc, color=0xFFD700)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))