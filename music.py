import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
  def __init__(self, client):
      self.client = client

  @commands.command(aliases=['p'])
  async def play(self,ctx,url):
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel!")
    else:
      voice_channel = ctx.author.voice.channel

      if ctx.voice_client is None:
        await voice_channel.connect()  
      else:
        await ctx.voice_client.move_to(voice_channel)

      ctx.voice_client.stop()

      FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
      YDL_OPTIONS = {'format':"bestaudio"}
      vc = ctx.voice_client

      with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2,
        **FFMPEG_OPTIONS)
        vc.play(source)

  @commands.command(aliases=['dc'])
  async def disconnect(self,ctx):
    if ctx.voice_client.is_playing() == True:
      await ctx.voice_client.disconnect()
    else:
      await ctx.send("Nothing currently connected.")

  @commands.command()
  async def pause(self,ctx):
    if ctx.voice_client.is_playing():
      await ctx.send("Paused :pause_button:")
      await ctx.voice_client.pause()
    else:
      await ctx.send("Nothing currently playing.")

  @commands.command()
  async def resume(self,ctx):
    if ctx.voice_client.is_playing() == False:
      await ctx.send("Resumed :arrow_forward:")
      await ctx.voice_client.resume()
    else:
      await ctx.send("Nothing currently paused.")

def setup(client):
  client.add_cog(music(client))