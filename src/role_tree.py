import discord
import role_edit


group_role = discord.app_commands.Group(
    name='role',
    description='Role commands'
)
group_role.add_command(role_edit.group_role_edit)


@group_role.command(
    name='add',
    description='Dodaje rolę użytkownikowi'
)
async def __command_add(
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role
) -> None:
    await member.add_roles(role)
    await interaction.response.send_message('dodano')


@group_role.command(
    name='remove',
    description='Zabiera rolę użytkownikowi'
)
async def __command_remove(
        interaction: discord.Interaction,
        member: discord.Member,
        role: discord.Role
) -> None:
    await member.remove_roles(role)
    await interaction.response.send_message('zabrano')

