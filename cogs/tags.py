import discord
from discord.ext import commands
from discord import app_commands
import json
import os

TAG_FILE = "tags.json"

class TagSystem(commands.Cog):
    """Manage reusable server tags with text or embed content."""

    def __init__(self, bot):
        self.bot = bot
        self.tags = self.load_tags()

    def load_tags(self):
        if os.path.exists(TAG_FILE):
            with open(TAG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_tags(self):
        with open(TAG_FILE, "w") as f:
            json.dump(self.tags, f, indent=4)

    def get_guild_tags(self, guild_id):
        return self.tags.setdefault(str(guild_id), {})

    # ---------- Prefix Commands (Admin Only) ----------

    @commands.group(name="tag", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def tag(self, ctx, name: str = None):
        """Show a tag by name or list all available tags."""
        tags = self.get_guild_tags(ctx.guild.id)

        if not name:
            if not tags:
                return await ctx.send("<:ap_crossmark:1382760353904988230> No tags created yet.")
            return await ctx.send("📌 Available Tags: " + ", ".join(tags.keys()))

        tag = tags.get(name.lower())
        if not tag:
            return await ctx.send("<:ap_crossmark:1382760353904988230> Tag not found.")

        if tag["type"] == "text":
            await ctx.send(tag["content"])
        elif tag["type"] == "embed":
            embed = discord.Embed(title=tag.get("title"), description=tag.get("content"), color=discord.Color.blurple())
            await ctx.send(embed=embed)

    @tag.command(name="create")
    @commands.has_permissions(administrator=True)
    async def create_tag(self, ctx, name: str, type: str, *, content: str):
        """Create a new tag (text or embed)."""
        tags = self.get_guild_tags(ctx.guild.id)
        name = name.lower()
        if name in tags:
            return await ctx.send("<:ap_crossmark:1382760353904988230> Tag already exists.")

        if type == "text":
            tags[name] = {"type": "text", "content": content}
        elif type == "embed":
            if "|" not in content:
                return await ctx.send("<:ap_crossmark:1382760353904988230> For embed tags, use format: `Title | Description`")
            title, desc = map(str.strip, content.split("|", 1))
            tags[name] = {"type": "embed", "title": title, "content": desc}
        else:
            return await ctx.send("<:ap_crossmark:1382760353904988230> Type must be `text` or `embed`.")

        self.save_tags()
        await ctx.send(f"<:ap_checkmark:1382760062728273920> Tag `{name}` created.")

    @tag.command(name="edit")
    @commands.has_permissions(administrator=True)
    async def edit_tag(self, ctx, name: str, *, new_content: str):
        """Edit an existing tag's content."""
        tags = self.get_guild_tags(ctx.guild.id)
        name = name.lower()
        tag = tags.get(name)
        if not tag:
            return await ctx.send("<:ap_crossmark:1382760353904988230> Tag not found.")

        if tag["type"] == "text":
            tag["content"] = new_content
        elif tag["type"] == "embed":
            if "|" not in new_content:
                return await ctx.send("<:ap_crossmark:1382760353904988230> For embed tags, use format: `Title | Description`")
            title, desc = map(str.strip, new_content.split("|", 1))
            tag["title"] = title
            tag["content"] = desc

        self.save_tags()
        await ctx.send(f"<:ap_checkmark:1382760062728273920> Tag `{name}` updated.")

    @tag.command(name="delete")
    @commands.has_permissions(administrator=True)
    async def delete_tag(self, ctx, name: str):
        """Delete a saved tag."""
        tags = self.get_guild_tags(ctx.guild.id)
        name = name.lower()
        if name not in tags:
            return await ctx.send("<:ap_crossmark:1382760353904988230> Tag not found.")
        del tags[name]
        self.save_tags()
        await ctx.send(f"<:ap_checkmark:1382760062728273920> Tag `{name}` deleted.")

    @tag.command(name="list")
    @commands.has_permissions(administrator=True)
    async def list_tags(self, ctx):
        """List all available tags."""
        tags = self.get_guild_tags(ctx.guild.id)
        if not tags:
            return await ctx.send("<:ap_crossmark:1382760353904988230> No tags created yet.")
        await ctx.send("📌 Tags: " + ", ".join(tags.keys()))

    # ---------- Slash Commands (Admin Only) ----------

    @app_commands.command(name="tag_show", description="Show a saved tag")
    async def slash_tag(self, interaction: discord.Interaction, name: str):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> You need administrator permission.", ephemeral=True)

        tag = self.get_guild_tags(interaction.guild.id).get(name.lower())
        if not tag:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> Tag not found.", ephemeral=True)

        if tag["type"] == "text":
            await interaction.response.send_message(tag["content"])
        elif tag["type"] == "embed":
            embed = discord.Embed(title=tag.get("title"), description=tag.get("content"), color=discord.Color.blurple())
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="tag_create", description="Create a new tag")
    @app_commands.describe(name="Name of the tag", type="text or embed", content="Text, or for embed: Title | Description")
    async def slash_create(self, interaction: discord.Interaction, name: str, type: str, content: str):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> You need administrator permission.", ephemeral=True)

        tags = self.get_guild_tags(interaction.guild.id)
        name = name.lower()
        if name in tags:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> Tag already exists.", ephemeral=True)

        if type == "text":
            tags[name] = {"type": "text", "content": content}
        elif type == "embed":
            if "|" not in content:
                return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> Use format: `Title | Description`", ephemeral=True)
            title, desc = map(str.strip, content.split("|", 1))
            tags[name] = {"type": "embed", "title": title, "content": desc}
        else:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> Type must be `text` or `embed`.", ephemeral=True)

        self.save_tags()
        await interaction.response.send_message(f"<:ap_checkmark:1382760062728273920> Tag `{name}` created.")

    @app_commands.command(name="tag_edit", description="Edit an existing tag")
    async def slash_edit(self, interaction: discord.Interaction, name: str, new_content: str):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> You need administrator permission.", ephemeral=True)

        tags = self.get_guild_tags(interaction.guild.id)
        name = name.lower()
        tag = tags.get(name)
        if not tag:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> Tag not found.", ephemeral=True)

        if tag["type"] == "text":
            tag["content"] = new_content
        elif tag["type"] == "embed":
            if "|" not in new_content:
                return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> Use format: `Title | Description`", ephemeral=True)
            title, desc = map(str.strip, new_content.split("|", 1))
            tag["title"] = title
            tag["content"] = desc

        self.save_tags()
        await interaction.response.send_message(f"<:ap_checkmark:1382760062728273920> Tag `{name}` updated.")

    @app_commands.command(name="tag_delete", description="Delete a tag")
    async def slash_delete(self, interaction: discord.Interaction, name: str):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> You need administrator permission.", ephemeral=True)

        tags = self.get_guild_tags(interaction.guild.id)
        name = name.lower()
        if name not in tags:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> Tag not found.", ephemeral=True)
        del tags[name]
        self.save_tags()
        await interaction.response.send_message(f"<:ap_checkmark:1382760062728273920> Tag `{name}` deleted.")

    @app_commands.command(name="tag_list", description="List all tags")
    async def slash_list(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> You need administrator permission.", ephemeral=True)

        tags = self.get_guild_tags(interaction.guild.id)
        if not tags:
            return await interaction.response.send_message("<:ap_crossmark:1382760353904988230> No tags created.", ephemeral=True)
        await interaction.response.send_message("📌 Tags: " + ", ".join(tags.keys()), ephemeral=True)

async def setup(bot):
    await bot.add_cog(TagSystem(bot))
