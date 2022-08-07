import discord


group_role_edit = discord.app_commands.Group(
    name='edit',
    description='Role editing commands'
)


@group_role_edit.command(
    name='name',
    description='Edytuje nazwę danej roli'
)
async def __command_name(
        interaction: discord.Interaction,
        role: discord.Role,
        new_name: str
) -> None:
    await role.edit(name=new_name)
    await interaction.response.send_message('Role edited successfully')


colors = {
    'red': 0xff0000,
    'green': 0x00ff00,
    'blue': 0x0000ff
}


@group_role_edit.command(
    name='color',
    description='Edytuje kolor danej roli'
)
async def __command_color(
        interaction: discord.Interaction,
        role: discord.Role,
        new_color: str
) -> None:
    try:
        color = colors[new_color]
        await role.edit(color=color)
        await interaction.response.send_message('Role edited successfully')
    except KeyError:
        if len(new_color) == 6:
            try:
                color = discord.Color(int(new_color, 16))
                await role.edit(color=color)
                await interaction.response.send_message('Role edited successfully')
            except ValueError:
                await interaction.response.send_message('Color field is invalid')
        else:
            await interaction.response.send_message('Color field is invalid')

