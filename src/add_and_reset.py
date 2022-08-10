import discord
#import custom_client


def init(tree):  # , client: custom_client.Client):

    @tree.command(
        name='add',
        description='adds'
    )
    async def __command_add(interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("spierdalaj")
            return
        try:
            interaction.client.guild_counters[interaction.guild_id] += 1
        except KeyError:
            interaction.client.guild_counters[interaction.guild_id] = 1
        await interaction.response.send_message(interaction.client.guild_counters[interaction.guild_id])

    @tree.command(
        name='reset',
        description='resets'
    )
    async def __command_reset(interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("spierdalaj")
            return
        interaction.client.guild_counters[interaction.guild_id] = 0
        await interaction.response.send_message("Zresetowano licznik")
