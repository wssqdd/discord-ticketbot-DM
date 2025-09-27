import discord
from discord.ext import commands
import os
import asyncio
import json


config_path = "./config.json"


async def load_config():
    with open(config_path, "r") as f:
        config = json.load(f)
        return config
with open(config_path, "r") as f:
    config = json.load(f)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config["prefix"], intents=intents, help_command=None)

@bot.event
async def on_ready():
    print("Bot démarer facile")


@bot.command()
async def lock_ticket(ctx):
    if not ctx.author.guild_permissions.administrator:
        return

    config = await load_config()

    if config["state_ticket"] == "off":
        embed = discord.Embed(
            title="`🚫` - Erreur",
            description="*Le système est déjà `off`*",
            color=0xFF0000
        )
        embed.set_footer(
            text=ctx.author.name,
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        embed.timestamp = discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)
        return
    else:
        config["state_ticket"] = "off"
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        embed = discord.Embed(
            title="`🪄` - Ticket",
            description="*Le système de ticket est désactivé*",
            color=int(config["color"], 16)
        )
        embed.set_footer(
            text=ctx.author.name,
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        embed.timestamp = discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)
        return


@bot.command()
async def unlock_ticket(ctx):
    if not ctx.author.guild_permissions.administrator:
        return

    config = await load_config()

    if config["state_ticket"] == "on":
        embed = discord.Embed(
            title="`🚫` - Erreur",
            description="*Le système est déjà `on`*",
            color=0xFF0000
        )
        embed.set_footer(
            text=ctx.author.name,
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        embed.timestamp = discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)
        return
    else:
        config["state_ticket"] = "on"
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        embed = discord.Embed(
            title="`🪄` - Ticket",
            description="*Le système de ticket est activé*",
            color=int(config["color"], 16)
        )
        embed.set_footer(
            text=ctx.author.name,
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        embed.timestamp = discord.utils.utcnow()
        await ctx.reply(embed=embed, mention_author=False)
        return

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    config = await load_config()

    if isinstance(message.channel, discord.DMChannel) and config["state_ticket"] == "off":
        return

    if isinstance(message.channel, discord.DMChannel):
        channel_id = int(config["channel_ticket_id"])
        log_channel = bot.get_channel(channel_id)
        transcript_channel_id= int(config["transcript_ticket_id"])
        transcript_channel = bot.get_channel(transcript_channel_id)

        if log_channel is None:
            print("[ERREUR] Salon introuvable")
            return

        embed = discord.Embed(
            title="`📩` - Nouveau message",
            description=f"*Message de {message.author.mention}*",
            color=int(config["color"], 16)
        )
        if message.content:
            embed.add_field(name="Contenu", value=f"```{message.content}```", inline=False)
        if message.attachments:
            embed.add_field(
                name="📎 Pièces jointes",
                value="\n".join([att.url for att in message.attachments]),
                inline=False
            )

        embed.set_footer(
            text=message.author.name,
            icon_url=message.author.avatar.url if message.author.avatar else None
        )
        embed.timestamp = discord.utils.utcnow()

        view = discord.ui.View(timeout=None)

        async def delete_ticket_callback(interaction: discord.Interaction):
            config = await load_config()

            await interaction.response.defer()

            try:
                # Récupérer le channel DM avec l'utilisateur original
                dm_channel = message.author.dm_channel
                if dm_channel is None:
                    dm_channel = await message.author.create_dm()

                messages = []
                async for dm_message in dm_channel.history(limit=None, oldest_first=True):
                    timestamp = dm_message.created_at.strftime("%d/%m/%Y %H:%M:%S")
                    author_name = "Bot" if dm_message.author == bot.user else dm_message.author.display_name

                    content = dm_message.content if dm_message.content else ""

                    if dm_message.embeds:
                        embed_content = []
                        for embed in dm_message.embeds:
                            if embed.title:
                                embed_content.append(f"Titre: {embed.title}")
                            if embed.description:
                                embed_content.append(f"Description: {embed.description}")
                            for field in embed.fields:
                                if field.name:
                                    embed_content.append(f"{field.name}: {field.value}")
                                else:
                                    embed_content.append(f"{field.value}")

                        if embed_content:
                            content += f" [Embed: {' | '.join(embed_content)}]"

                    if not content:
                        content = "[Aucun contenu]"

                    msg_info = f"[{timestamp}] {author_name}: {content}"

                    if dm_message.attachments:
                        attachments = ", ".join([att.url for att in dm_message.attachments])
                        msg_info += f" [Pièces jointes: {attachments}]"

                    messages.append(msg_info)

                transcript = "\n".join(messages)

                import io

                transcript_file = discord.File(
                    fp=io.StringIO(transcript),
                    filename=f"transcript-dm-{message.author.name}.txt"
                )
                embed_trans = discord.Embed(
                    title="",
                    description=f"**Transcript du ticket avec {message.author.mention}**",
                )
                await transcript_channel.send(embed = embed_trans)
                msg = await transcript_channel.send(file=transcript_file)
                transcript_embed = discord.Embed(
                    title="`📁` - Ticket supprimé",
                    description=f"*Ticket supprimé par {interaction.user.mention}*",
                    color=int(config["color"], 16)
                )
                transcript_embed.add_field(
                    name="", 
                    value=f"*transcription du ticket disponible ici: {msg.jump_url}*", 
                    inline=False
                )
                transcript_embed.set_footer(text=f"Utilisateur: {message.author.name}")
                transcript_embed.timestamp = discord.utils.utcnow()
                embed = discord.Embed(
                    title="`📩` - Ticket supprimé",
                    description=f"*Ticket supprimé par {interaction.user.mention}*",
                    color=0xFF0000
                )
                embed.add_field(name="", value="*Merci de contacter l'équipe de support si vous voulez avoir le transcript du ticket*")
                embed.set_footer(text=f"Utilisateur: {message.author.name}")
                embed.timestamp = discord.utils.utcnow()
                await message.author.send(embed=embed)
                if log_channel:
                    await log_channel.send(embed=transcript_embed)
                    await interaction.followup.send("✅ Ticket supprimé avec succès.", ephemeral=True)
                else:
                    await interaction.followup.send("❌ Erreur lors de la suppression.", ephemeral=True)

            except Exception as e:
                await interaction.followup.send(f"❌ Erreur: {str(e)}", ephemeral=True)

        async def reply_callback(interaction: discord.Interaction):
            modal = discord.ui.Modal(title="Répondre au message")

            msg_input = discord.ui.TextInput(
                label="Message",
                style=discord.TextStyle.long,
                placeholder="Tape ta réponse ici...",
                required=True,
                max_length=2000
            )
            modal.add_item(msg_input)

            async def modal_callback(modal_interaction: discord.Interaction):
                try:
                    response_text = modal_interaction.data['components'][0]['components'][0]['value']
                    reply_embed = discord.Embed(
                        title="`📩` - Nouveau message de l'équipe de support",
                        description=f"*Message de {modal_interaction.user.mention}*",
                        color=int(config["color"], 16)
                    )
                    reply_embed.add_field(name="", value=f"```{response_text}```", inline=False)
                    reply_embed.add_field(name="", value="*Pour répondre à ce message, envoyez un message dans ce salon.*", inline=False)
                    reply_embed.set_footer(
                        text=modal_interaction.user.name,
                        icon_url=modal_interaction.user.avatar.url if modal_interaction.user.avatar else None
                    )
                    reply_embed.timestamp = discord.utils.utcnow()
                    await message.author.send(embed=reply_embed)
                    await modal_interaction.response.send_message("✅ Message envoyé.", ephemeral=True)
                    await log_channel.send(
                        f"{message.author.mention} a reçu un message de {modal_interaction.user.mention}"
                    )
                except discord.Forbidden:
                    await modal_interaction.response.send_message("❌ Impossible d'envoyer le message.", ephemeral=True)

            modal.on_submit = modal_callback
            await interaction.response.send_modal(modal)

        button = discord.ui.Button(label="Répondre", style=discord.ButtonStyle.secondary)
        button2 = discord.ui.Button(label="Supprimer", style=discord.ButtonStyle.danger)
        button.callback = reply_callback
        button2.callback = delete_ticket_callback
        view.add_item(button2)
        view.add_item(button)

        await log_channel.send(embed=embed, view=view)


token = config["token"]
bot.run(token)
