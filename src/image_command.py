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
                i, l = 0, 10 if len(posts) > 10 else len(posts)
                while i < l:
                    if posts[i]['file_url'][-3:] == 'mp4':
                        posts.pop(i)
                    else:
                        i += 1

                link = posts[random.randint(0, l - 1)]['file_url']

                embed = discord.Embed.from_dict(
                    {
                        "title": tag,
                        "type": "image",
                        "image": {
                            "url": link
                        },
                        "color": 0xff6666
                    }
                )
                await interaction.response.send_message(embed=embed)

                """message = f"Randomly searched for tag **{tag.capitalize()}**. Here are few best results: \n"
                i = 0
                for post in posts:
                    message += f'\timage link = {post["file_url"]}, score = {post["score"]}\n'
                    i += 1
                    if i == 7:
                        break
                await interaction.response.send_message(message)"""
