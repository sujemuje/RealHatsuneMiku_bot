import discord


def init(tree):
    loop = False

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


    @tree.command(
        name='join',
        description='Łączy się z kanałem głosowym'
    )
    async def __command_join(
            interaction: discord.Interaction
    ) -> None:
        await __join(interaction)


    @tree.command(
        name='loop',
        description='Włącza/wyłącza zapętlenie utworów'
    )
    async def __command_loop(
            interaction: discord.Interaction
    ) -> None:
        global loop
        loop = not loop

        if loop:
            await interaction.response.send_message(f'Zapętlenie utworów włączone')
        else:
            await interaction.response.send_message(f'Zapętlenie utworów wyłączone')


    @tree.command(
        name='play',
        description='Odtwarza wybrane utwory'
    )
    async def __command_play(
            interaction: discord.Interaction
    ) -> None:
        await __join(interaction)

        vc = interaction.guild.voice_client
        global loop

        def play_in_loop(first=False):
            if loop or first:
                vc.play(discord.FFmpegPCMAudio("./audio/Plastic Memories ED.mp3"), after=play_in_loop)

        play_in_loop(first=True)