from datetime import datetime

from discord.ext import commands
from strawpoll import Poll, ExistingPoll, HTTPException, StrawpollException

import bot.strawpoll_api.api


class Web(commands.Cog):
    """
    This contains various commands for interacting wit web-based services.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx: commands.Context, *args):
        """
        Creates a strawpoll from the arguments.
        :param args: Arguments from which the poll is created.
                     Note: Multi-word arguments have to be quoted.
                     Example: !poll "Is this command great?" Yes No
        :return: URL of the poll
        """
        if args.__len__() < 3 or args[0].__len__() == 0 or args[1].__len__() == 0 or args[2].__len__() == 0:
            #  check if there are enough arguments
            await ctx.send("Please specify at least a title and two options.")
            return
        if args.__len__() > 30:
            # check if there are too many arguments
            await ctx.send("Too many options. Only 30 are allowed.")
            return
        api: bot.strawpoll_api.api.API = bot.strawpoll_api.api.API()  # use the fixed version provided by this
        # project
        poll: Poll = Poll(args[0], args[1:])
        try:
            poll = await api.submit_poll(poll=poll)
        except StrawpollException as se:
            if isinstance(se, ExistingPoll):
                await ctx.send("Error: This poll already exists.")
            elif isinstance(se, HTTPException):
                name: str = "strawpoll_http_error.txt"
                with open(file=name, mode="w+", encoding='utf-8') as error_dump:
                    info: str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                    error_dump.writelines(info)
                    error_dump.writelines(se.args)
                    error_dump.close()
                await ctx.send("A HTTP Error occurred. Please try again later.")
            else:
                name: str = "strawpoll_error.txt"
                with open(file=name, mode="w+", encoding='utf-8') as error_dump:
                    info: str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n"
                    error_dump.writelines(info)
                    error_dump.writelines(se.__str__())
                    error_dump.close()
                await ctx.send("An error occurred. Please try again later.")
            return
        await ctx.send("Here is your poll:\n" + poll.url)

    @commands.command()
    async def github(self, ctx: commands.Context):
        """
        Sends a link to the bots github page.
        """
        await ctx.send("You can read and contribute to my source code on Github:\n"
                       "https://github.com/PatrickSchmitt98/Bot_Anders")


def setup(bot):  # Adds the web commands to the bot
    bot.add_cog(Web(bot))
