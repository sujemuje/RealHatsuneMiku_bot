import discord


async def __join(interaction: discord.Interaction) -> None:

    if isinstance(interaction.user, discord.User):
        await interaction.response.send_message('Do użycia tylko na serwerach')
        return

    if interaction.user.voice is None:
        await interaction.response.send_message('Nie jesteś połączony z kanałem głosowym')
        return

    if interaction.guild.voice_client is None:
        await interaction.response.send_message(
            f'Połączono z kanałem {interaction.user.voice.channel.mention} na prośbę użytkownika {interaction.user.mention}'
        )
        await interaction.user.voice.channel.connect()
        return

    if interaction.guild.voice_client.channel is not interaction.user.voice.channel:
        await interaction.response.send_message(
            f'Przełączono na kanał {interaction.user.voice.channel.mention} na prośbę użytkownika {interaction.user.mention}'
        )
        await interaction.guild.voice_client.move_to(interaction.user.voice.channel)
    else:
        await interaction.response.send_message(
            'Bot jest już na kanale'
        )


@discord.app_commands.command(
    name='join',
    description='Łączy się z kanałem głosowym'
)
async def __command_join(
        interaction: discord.Interaction
) -> None:
    await __join(interaction)
