import discord
from discord.ext import commands

class Greeting(commands.Cog, name="Greeting"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Greeting ready")

#Commands
    @commands.command()
    async def hello(self,ctx):
        await ctx.send(f"hello{ctx.author.mention}")

    @commands.command()
    async def hi(self,ctx):
        await ctx.send(f"hi{ctx.author.mention}")


#End Commands
async def setup(bot):
    await bot.add_cog(Greeting(bot))



    