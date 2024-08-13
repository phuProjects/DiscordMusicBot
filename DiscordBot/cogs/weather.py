import discord
import requests
from discord.ext import commands

api_key = "33db18d1d98d9193161ba439a78eb77f"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

class Weather(commands.Cog, name="Weather"):
    def __init__(self,bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather channel ready")

    @commands.command()
    async def weather(self, ctx, *, city: str):
        try:
            city_name = city
            if not api_key or not base_url:
                await ctx.send("API key or base URL is not set.")
                return

            city_name = city
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            channel = ctx.message.channel
            
            if x["cod"] != "404":
                if "main" in x and "weather" in x:
                    async with channel.typing():
                        y = x["main"]
                        current_temperature = y["temp"]
                        current_temperature_fahrenheit = round((current_temperature - 273.15) * (9/5) + 32) 
                        current_pressure = y["pressure"]
                        current_humidity = y["humidity"]
                        z = x["weather"]
                        weather_description = z[0]["description"]
                        weather_description = z[0]["description"]
                        embed = discord.Embed(title=f"Weather in {city_name}",
                                        color=discord.Color.blue(),
                                        timestamp=ctx.message.created_at,)
                        embed.add_field(name="Descripition", value=f"**{weather_description}**", inline=False)
                        embed.add_field(name="Temperature(F)", value=f"**{current_temperature_fahrenheit}°F**", inline=False)
                        embed.add_field(name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
                        embed.add_field(name="Atmospheric Pressure(hPa)", value=f"**{current_pressure}hPa**", inline=False)
                        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                        embed.set_footer(text=f"Requested")
                        await channel.send(embed=embed)
                else:
                    await channel.send(f"Weather data for '{city_name}' is currently unavailable. Please try again later.")
            else:
                await channel.send("City not found.")
        except Exception as e:
            print(f"Weather Error: {e}")

async def setup(bot):
    await bot.add_cog(Weather(bot))


        