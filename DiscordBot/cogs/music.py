import discord
from discord.ext import commands
import yt_dlp

intents= discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format' : 'bestaudio', 'noplaylist' : True}

class Music(commands.Cog, name="Music"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music channel ready")

    @commands.command()
    async def play(self, ctx, * ,search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        
        if ctx.voice_client is None:
            try:
                await voice_channel.connect()
            except Exception as e:
                await ctx.send(f"Failed to connect to the voice channel: {e}")
                return
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch: {search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.append((url,title))
                await ctx.send(f'Added to queue: **{title}**')
                
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)
            
    @commands.command()
    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _:self.bot.loop.create_task(self.play_next(ctx)))
        elif not ctx.voice_client.is_playing():
            await ctx.send("queue is empty.")

    @commands.command()
    async def skip(self,ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Music is Skipped.")

    @commands.command()
    async def clear(self, ctx):
        try:
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                self.queue.clear()
                await ctx.send("Music is Cleared.")
        except Exception as e:
            print(f"Error: {e}")

    @commands.command()
    async def list_queue(self, ctx):
        try:
            if not self.queue:
                await ctx.send("Queue is currently empty.")
            else:
                queue_list = ""
                start = 0
                for i, (url, title) in enumerate(self.queue,start):
                    if start==0:
                        queue_list += f"Next up. **{title}**\n"
                        start+=1
                    else:
                        queue_list += f"{i} - **{title}**\n"
                    
                embed = discord.Embed(title="Music Queue", description=queue_list, color=discord.Color.blue())
                await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error: {e}")

    @commands.command()
    async def pause(self, ctx):
        try:
            if not ctx.voice_client.is_playing():
                await ctx.send("There are no music playing right now.")
            else:
                ctx.voice_client.pause()
                await ctx.send("Music is paused.")
        except Exception as e:
            print(f"Error: {e}")

    @commands.command()
    async def resume(self ,ctx):
        try:
            if not ctx.voice_client.is_playing():
                ctx.voice_client.resume()
                await ctx.send("Music is resumed.")
            else:
                await ctx.send("Music is already playing.")
        except Exception as e:
            await ctx.send(f"Error {e}")

    @commands.command()
    async def disconnect(self, ctx):
        try:
            if not ctx.voice_client:
                await ctx.send("Currently not in a voice channel.")
            else:
                await ctx.voice_client.disconnect()
                await ctx.send(f"Disconnected from the {ctx.author.voice.channel}.")
        except Exception as e:
            await ctx.send(f"Error {e}")

async def setup(bot):
    await bot.add_cog(Music(bot))
