import discord
from discord.ext import commands
from discord import Interaction, Embed, app_commands
from discord.ui import View, Button
import asyncio
from typing import Union, List, Optional
from dataclasses import dataclass
from enum import Enum

TEXT1_ICON = "<:icons_text1:1352993725390782494>"
TEXT2_ICON = "<:icons_text2:1352993742294089840>"
TEXT3_ICON = "<:icons_text3:1352993758735761489>"
TEXT4_ICON = "<:icons_text4:1352993775202471990>"
TEXT5_ICON = "<:icons_text5:1352993792315097120>"
TEXT6_ICON = "<:icons_text6:1352993809033723925>"
GREEN_CHECK = "<:right1:1349089453762674718>"
DOWNLOAD_ICON = "<:icons_Download:1352990061398065202>"
ACTIVITIES_ICON = "<:icons_activities:1352990078095589486>"
ARCHIVE_ICON = "<:icons_archive:1352990094667288661>"
AWARD_ICON = "<:icons_award:1352990111603884042>"
EDIT_ICON = "<:icons_edit:1352990127865073745>"
EVENT_COLOUR_ICON = "<:icons_eventcolour:1352990144843616337>"
AUDIO_ENABLE_ICON = "<:icons_audioenable:1352990161247408139>"
DISCOVER_ICON = "<:icons_discover:1352990178935046255>"
NITRO_ICON = "<:icons_nitro:1352990196106530880>"
VERIFIED_ICON = "<:icons_verified:1352990211792961579>"
BOX_ICON = "<:icons_box:1352990245351850035>"
BRIGHT_ICON = "<:icons_bright:1352990262854680576>"
CONNECT_ICON = "<:icons_connect:1352990279535296522>"
RED_CROSS = "<:wrong1:1349089452001329304>"
BACK = "<:988409328698523708:1349064771743383563>"
NEXTF = "<:988409335791124551:1349064769453428776>"
STATS = "<:icon_Stats:1349070310132940881>"
MEMBER = "<:icon_member:1349070307993981109>"
OFFLINE = "<:icons_offline:1349070305733115944>"
ONLINE = "<:icons_online:1349070303602675814>"
DND = "<:icons_dred:1349845341368750102>"
SHUFFLE = "<:image:1349072926183264288>"
SETTINGS = "<:icons_settings:1349073236645773312>"
YELLOW = "<:icons_dyellow:1349766351497199687>"
SEARCH = "<:icons_search:1350127057681514549>"
PIN = "<:icons_pin:1350127648491438122>"
DOT = "<a:blue_dot:1345756118407970899>"
BUG = "<:icons_Bugs:859388130803974174>"

class HelpMenuType(Enum):
    DISABLED = 0
    BUTTONS = 1
    SELECT = 2

@dataclass
class HelpSettings:
    page_char_limit: int = 1000
    max_pages_in_guild: int = 2
    use_menus: HelpMenuType = HelpMenuType.BUTTONS
    show_hidden: bool = False
    show_aliases: bool = True
    delete_delay: int = 0
    react_timeout: int = 30
    use_embeds: bool = True

class HelpView(View):
    def __init__(self, pages: List[Union[str, Embed]], timeout: int = 30, original_message=None, author: Optional[discord.User] = None):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.current_page = 0
        self.max_page = len(pages) - 1
        self.original_message = original_message
        self.author = author
        self.update_buttons()

    def update_buttons(self):
        self.previous_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == self.max_page
        self.page_counter.label = f"{self.current_page + 1}/{self.max_page + 1}"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.author and interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "⚠️ Only the person who used the help command can use these buttons.",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(emoji=BACK, style=discord.ButtonStyle.secondary)
    async def previous_button(self, interaction: Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            page = self.pages[self.current_page]
            if isinstance(page, Embed):
                await interaction.response.edit_message(embed=page, view=self)
            else:
                await interaction.response.edit_message(content=page, embed=None, view=self)

    @discord.ui.button(label="1/1", style=discord.ButtonStyle.secondary, disabled=True)
    async def page_counter(self, interaction: Interaction, button: Button):
        await interaction.response.defer()

    @discord.ui.button(emoji=NEXTF, style=discord.ButtonStyle.secondary)
    async def next_button(self, interaction: Interaction, button: Button):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.update_buttons()
            page = self.pages[self.current_page]
            if isinstance(page, Embed):
                await interaction.response.edit_message(embed=page, view=self)
            else:
                await interaction.response.edit_message(content=page, embed=None, view=self)

    @discord.ui.button(emoji=RED_CROSS, style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: Interaction, button: Button):
        await interaction.response.defer()
        try:
            await interaction.delete_original_response()
        except:
            try:
                await interaction.message.delete()
            except:
                pass
        if self.original_message:
            try:
                await self.original_message.add_reaction(GREEN_CHECK)
            except:
                pass
        self.stop()

class HelpFormatter:
    def __init__(self, settings: HelpSettings = None):
        self.settings = settings or HelpSettings()
    async def send_help(self, ctx_or_interaction, help_for: str = None):
        if isinstance(ctx_or_interaction, discord.Interaction):
            ctx = await commands.Context.from_interaction(ctx_or_interaction)
            ctx._original_interaction = ctx_or_interaction
        else:
            ctx = ctx_or_interaction
            ctx._original_interaction = None
        if help_for is None:
            await self.send_bot_help(ctx)
        elif help_for.lower() in ['cogs', 'categories']:
            await self.send_cog_list(ctx)
        else:
            command = ctx.bot.get_command(help_for)
            if command:
                await self.send_command_help(ctx, command)
            else:
                cog = ctx.bot.get_cog(help_for)
                if cog:
                    await self.send_cog_help(ctx, cog)
                else:
                    await self.send_command_not_found(ctx, help_for)
    async def send_bot_help(self, ctx):
        bot = ctx.bot
        cog_commands = {}
        no_cog_commands = []
        for command in bot.commands:
            if not self.can_show_command(command):
                continue
            if command.cog:
                cog_name = command.cog.qualified_name
                if cog_name not in cog_commands:
                    cog_commands[cog_name] = []
                cog_commands[cog_name].append(command)
            else:
                no_cog_commands.append(command)
        pages = []
        current_embed = None
        current_length = 0
        def create_new_embed():
            embed = Embed(
                title="Help Categories",
                color=0xff7800
            )
            return embed
        def add_category_to_embed(embed, cog_name, commands_list):
            if not commands_list:
                return 0
            category_text = f"**__{cog_name}:__**\n"
            command_lines = []
            for command in sorted(commands_list, key=lambda x: x.name):
                description = command.short_doc or "No description available."
                command_lines.append(f"**{command.name}** {description}")
            category_content = category_text + "\n".join(command_lines)
            if len(category_content) > 1000:
                return -1
            embed.add_field(
                name="",
                value=category_content,
                inline=False
            )
            return len(category_content)
        current_embed = create_new_embed()
        current_length = 0
        for cog_name, commands_list in sorted(cog_commands.items()):
            if not commands_list:
                continue
            category_length = len(f"**__{cog_name}:__**\n") + sum(
                len(f"**{cmd.name}** {cmd.short_doc or 'No description available.'}\n") 
                for cmd in commands_list
            )
            if current_length + category_length > self.settings.page_char_limit and current_embed.fields:
                pages.append(current_embed)
                current_embed = create_new_embed()
                current_length = 0
            added_length = add_category_to_embed(current_embed, cog_name, commands_list)
            if added_length == -1:
                if current_embed.fields:
                    pages.append(current_embed)
                category_embed = create_new_embed()
                add_category_to_embed(category_embed, cog_name, commands_list)
                pages.append(category_embed)
                current_embed = create_new_embed()
                current_length = 0
            else:
                current_length += added_length
        if no_cog_commands:
            category_length = len("**__Other Commands:__**\n") + sum(
                len(f"**{cmd.name}** {cmd.short_doc or 'No description available.'}\n") 
                for cmd in no_cog_commands
            )
            if current_length + category_length > self.settings.page_char_limit and current_embed.fields:
                pages.append(current_embed)
                current_embed = create_new_embed()
            add_category_to_embed(current_embed, "Other Commands", no_cog_commands)
        if current_embed.fields:
            pages.append(current_embed)
        total_pages = len(pages)
        for i, page in enumerate(pages, 1):
            if total_pages > 1:
                page.description = f"Page {i} of {total_pages}"
            page.add_field(
                name="",
                value=f"Type `{ctx.prefix}help <command>` for more info on a command. You can also type `{ctx.prefix}help <category>` for more info on a category.",
                inline=False
            )
        if not pages:
            embed = create_new_embed()
            embed.add_field(
                name="No Commands Available",
                value="No commands are currently available.",
                inline=False
            )
            pages = [embed]
        await self.send_pages(ctx, pages)
    async def send_cog_help(self, ctx, cog):
        cog_commands = [cmd for cmd in cog.get_commands() if self.can_show_command(cmd)]
        if not cog_commands:
            embed = Embed(
                title="No Commands Found",
                description=f"No commands found in {cog.qualified_name}",
                color=0xff7800
            )
            await ctx.send(embed=embed)
            return
        embed = Embed(
            title=f"{cog.qualified_name} Commands",
            color=0xff7800
        )
        if cog.description:
            embed.description = cog.description
        command_list = []
        for command in sorted(cog_commands, key=lambda x: x.name):
            description = command.short_doc or "No description available"
            command_list.append(f"`{ctx.prefix}{command.name}` - {description}")
        pages = self.paginate_text(command_list, embed)
        await self.send_pages(ctx, pages)
    async def send_command_help(self, ctx, command):
        embed = Embed(
            title="",
            color=0xff7800
        )
        signature = f"{ctx.prefix}{command.qualified_name}"
        if command.signature:
            signature += f" {command.signature}"
        embed.add_field(
            name="Syntax:",
            value=f"```\n{signature}\n```",
            inline=False
        )
        description = command.help or command.short_doc or "No description available."
        embed.description = description
        if isinstance(command, commands.Group):
            subcommands = [cmd for cmd in command.commands if self.can_show_command(cmd)]
            if subcommands:
                subcmd_text = []
                for subcmd in sorted(subcommands, key=lambda x: x.name):
                    subcmd_desc = subcmd.short_doc or "No description available."
                    subcmd_text.append(f"**{subcmd.name}** {subcmd_desc}")
                embed.add_field(
                    name="Subcommands:",
                    value="\n".join(subcmd_text),
                    inline=False
                )
        embed.add_field(
            name="",
            value=f"Type `{ctx.prefix}help <command>` for more info on a command. You can also type `{ctx.prefix}help <category>` for more info on a category.",
            inline=False
        )
        await self.send_pages(ctx, [embed])
    async def send_cog_list(self, ctx):
        embed = Embed(
            title="Command Categories",
            description=f"Use `{ctx.prefix}help [category]` to see commands in that category.",
            color=0xff7800
        )
        cog_info = []
        for cog_name, cog in ctx.bot.cogs.items():
            commands_count = len([cmd for cmd in cog.get_commands() if self.can_show_command(cmd)])
            if commands_count > 0:
                description = cog.description or "No description available"
                cog_info.append(f"**{cog_name}** ({commands_count} commands)\n{description[:100]}...")
        if cog_info:
            embed.description += "\n\n" + "\n\n".join(cog_info)
        await self.send_pages(ctx, [embed])
    async def send_command_not_found(self, ctx, command_name: str):
        embed = Embed(
            title="Command Not Found",
            description=f"No command or category named `{command_name}` was found.",
            color=0xff7800
        )
        all_commands = [cmd.name for cmd in ctx.bot.commands if self.can_show_command(cmd)]
        all_commands.extend(ctx.bot.cogs.keys())
        suggestions = [cmd for cmd in all_commands if command_name.lower() in cmd.lower()][:5]
        if suggestions:
            embed.add_field(
                name="Did you mean?",
                value=", ".join([f"`{suggestion}`" for suggestion in suggestions]),
                inline=False
            )
        embed.set_footer(text=f"Use {ctx.prefix}help to see all available commands.")
        await ctx.send(embed=embed)
    def can_show_command(self, command) -> bool:
        if command.hidden and not self.settings.show_hidden:
            return False
        return True
    def paginate_text(self, text_list: List[str], base_embed: Embed) -> List[Embed]:
        pages = []
        current_embed = base_embed.copy()
        current_text = []
        current_length = len(base_embed.description or "")
        for text in text_list:
            if current_length + len(text) > self.settings.page_char_limit and current_text:
                current_embed.add_field(
                    name="Commands", 
                    value="\n".join(current_text), 
                    inline=False
                )
                pages.append(current_embed)
                current_embed = base_embed.copy()
                current_text = [text]
                current_length = len(base_embed.description or "") + len(text)
            else:
                current_text.append(text)
                current_length += len(text)
        if current_text:
            current_embed.add_field(
                name="Commands", 
                value="\n".join(current_text), 
                inline=False
            )
            pages.append(current_embed)
        return pages or [base_embed]
    async def send_pages(self, ctx, pages: List[Embed]):
        if not pages:
            return
        if len(pages) == 1:
            await ctx.send(embed=pages[0])
            return
        if self.settings.use_menus == HelpMenuType.BUTTONS:
            original_message = None
            if hasattr(ctx, '_original_interaction') and ctx._original_interaction is None:
                original_message = ctx.message
            view = HelpView(pages, timeout=self.settings.react_timeout, original_message=original_message, author=ctx.author)
            message = await ctx.send(embed=pages[0], view=view)
            if self.settings.delete_delay > 0:
                await asyncio.sleep(self.settings.delete_delay)
                try:
                    await message.delete()
                except:
                    pass
        else:
            for page in pages[:self.settings.max_pages_in_guild]:
                await ctx.send(embed=page)

class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
        self.formatter = HelpFormatter()
        bot.remove_command('help')
    @commands.command(name="help", aliases=["h", "commands"])
    async def help_command(self, ctx, *, command: str = None):
        """
        Shows help information for commands and categories.
        
        Usage:
        - `help` - Show all commands grouped by category
        - `help [command]` - Show detailed help for a specific command
        - `help [category]` - Show all commands in a category
        """
        await self.formatter.send_help(ctx, command)

    @app_commands.command(name="help", description="Get help information")
    async def help_slash(self, interaction: Interaction, command: Optional[str] = None):
        """
        Slash version of the help command.
        """
        await self.formatter.send_help(interaction, command)
    @commands.command(name="categories", aliases=["cogs"])
    async def categories_command(self, ctx):
        """
        Shows all command categories.
        """
        await self.formatter.send_cog_list(ctx)
    
async def setup(bot):
    await bot.add_cog(HelpCog(bot)) 