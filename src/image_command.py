import discord
import aiohttp
import random


def init(tree):
    @tree.command(
        name='image',
        description='Searches for random image matching the given tag'
    )
    async def __command_poll(
            interaction: discord.Interaction,
            tag: str
    ) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.rule34.xxx/index.php?page=dapi&pid={random.randint(1, 20)}&s=post&q=index&tags={tag}&json=1') as resp:
                posts: list = await resp.json()
                posts.sort(key=lambda i: i['score'], reverse=True)
                message = f"Randomly searched for tag **{tag.capitalize()}**. Here are few best results: \n"
                i = 0
                for post in posts:
                    message += f'\timage link = {post["file_url"]}, score = {post["score"]}\n'
                    i += 1
                    if i == 7:
                        break
                await interaction.response.send_message(message)

