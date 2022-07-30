import discord
import time


def init(tree, client):
    @tree.command(
        name='typing_speedrun',
        description='Gra w jak najszybsze przepisanie wylosowanego ciągu znaków'
    )
    async def __command_typing_speedrun(
            interaction: discord.Interaction
    ) -> None:
        string = 'abcde'   # str = randomstring
        await interaction.response.send_message(f'Przepisz tekst: `{string}`!')

        def check(m):
            return m.channel == interaction.channel

        time_limit = 15.0

        TIME_S = time.time()
        msg = await client.wait_for('message', check=check, timeout=time_limit)
        TIME_E = time.time()

        while msg.content.lower() != string:
            time_delta = TIME_E - TIME_S
            time_limit -= time_delta

            TIME_S = time.time()
            msg = await client.wait_for('message', check=check, timeout=time_limit)
            TIME_E = time.time()

        time_delta = TIME_E - TIME_S
        time_limit -= time_delta
        await interaction.edit_original_message(content=f'Gratulacje, przepisałeś: `{string}` w {15.0 - time_limit} sekund!')
