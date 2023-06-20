import configparser as cp
import sqlite3 as sql

import interactions as i
from interactions import BrandColors, Button, ButtonStyle, Embed

from Translator import Translator

scope_ids = []


class ApplicationCommand(i.Extension):
    def __init__(self, bot):
        self.config = cp.ConfigParser()
        self.config.read("config.ini")
        global scope_ids
        scope_ids = self.config["General"]["scope_ids"].split(",")
        self.cur = sql.connect("questions.db").cursor()

    async def complete_application(self, user_id: int, language: str):
        accept_button = Button(
            label="Annehmen",
            style=ButtonStyle.SUCCESS,
            custom_id="button_accept"
        )
        decline_button = Button(
            label="Ablehnen",
            style=ButtonStyle.DANGER,
            custom_id="button_decline"
        )
        self.cur.execute("SELECT * FROM answers WHERE user_id = ?",
                         (user_id,))
        answers = self.cur.fetchone()
        member = await self.bot.fetch_member(user_id, scope_ids[0])
        app_embed = Embed(
            title="♔FALLING SKY♔\nClan Application",
            description=f"{str(member.mention)} hat eine Bewerbung abgeschlossen!",
            color=BrandColors.FUCHSIA.value
        )
        translator = Translator("de")
        for i in range(1, 12):
            question = translator.translate(f"app.questions.{i}")
            app_embed.add_field(
                name=question, value=answers[i])
        app_send_channel = await self.bot.fetch_channel(self.config["IDs"]["app_send_channel_id"])
        send_message = await app_send_channel.send(embed=app_embed, components=[accept_button, decline_button])
        self.cur.execute("INSERT INTO applications VALUES (?, ?, ?)",
                         (int(send_message.id), language, user_id))
        self.cur.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
        self.cur.execute("DELETE FROM answers WHERE user_id = ?", (user_id,))

    @i.slash_command(
        name="application",
        description="Basis Command für die Bewerbung",
        scopes=scope_ids
    )
    async def application(self, ctx: i.SlashContext):
        pass

    @application.subcommand(
        sub_cmd_name="setup",
        sub_cmd_description="Setup für die Bewerbung",
        options=[
            i.SlashCommandOption(
                name="channel",
                description="Der Channel, in dem die Bewerbungen gestartet werden sollen",
                type=i.OptionType.CHANNEL,
                required=True,
                channel_types=[i.ChannelType.GUILD_TEXT]
            )
        ]
    )
    async def setup(self, ctx: i.SlashContext, channel: i.models.discord.channel.GuildText):
        setup_embed = i.Embed(
            title="♔FALLING SKY♔\nClan Application",
            description="""<a:6544_heartarrow_purple:956574404647739503> Bitte klicke auf den entsprechenden Button,\
                um eine Bewerbung zu starten und beantworte danach die Fragen.\n\n\
                <a:bluearrowheartright:921367937829466152> Please click on the corresponding button to start an\
                application and answer the questions afterwards.""",
            color=i.BrandColors.FUCHSIA.value,
            thumbnail=i.EmbedAttachment(
                url="https://cdn.discordapp.com/attachments/1088092124467183616/1120459818268901438/a_8c47aa36de8915783706e52c85b351db.gif"),
            images=[i.EmbedAttachment(
                url="https://cdn.discordapp.com/attachments/967765571582173214/1097873276396642344/GridArt_20230418_135243029.png")]
        )
        components = [
            i.Button(
                label="Deutsche Bewerbung",
                style=i.ButtonStyle.PRIMARY,
                custom_id="button_german",
                emoji="🇩🇪"
            ),
            i.Button(
                label="English Application",
                style=i.ButtonStyle.PRIMARY,
                custom_id="button_english",
                emoji="🇬🇧"
            )
        ]
        await channel.send(embed=setup_embed, components=components)
        await ctx.send("Setup erfolgreich!", ephemeral=True)

    @i.component_callback("button_german")
    async def german_application(self, ctx: i.ComponentContext):
        self.cur.execute("SELECT * FROM applications WHERE user_id = ?",
                         (int(ctx.author.id),))
        if self.cur.fetchone() is not None:
            await ctx.send("Du hast bereits eine Bewerbung!", ephemeral=True)
            return
        abort_button = i.Button(
            label="Abbrechen",
            style=i.ButtonStyle.DANGER,
            custom_id="button_abort"
        )
        dm_channel: i.models.discord.channel.DM = await ctx.author.fetch_dm()
        self.cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)",
                         (int(ctx.author.id), int(ctx.channel.id), 1, "de"))
        self.cur.execute("INSERT INTO answers (user_id) VALUES (?)",
                         (int(ctx.author.id),))
        await dm_channel.send(
            """Bitte beantworte die nachfolgenden Fragen in diesem Chat.""", components=[abort_button])
        await dm_channel.send("""*Frage 1/11*\nWie hei\N{Latin Small Letter Sharp S}t du? (Ingame **und** Reallife)""")
        await ctx.send("Bitte schaue in deine Privatnachrichten!", ephemeral=True)

    @i.component_callback("button_english")
    async def english_application(self, ctx: i.ComponentContext):
        self.cur.execute("SELECT * FROM applications WHERE user_id = ?",
                         (int(ctx.author.id),))
        if self.cur.fetchone() is not None:
            await ctx.send("You already have an application!", ephemeral=True)
            return
        abort_button = i.Button(
            label="Abort",
            style=i.ButtonStyle.DANGER,
            custom_id="button_abort"
        )
        dm_channel: i.models.discord.channel.DM = await ctx.author.fetch_dm()
        self.cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)",
                         (int(ctx.author.id), int(ctx.channel.id), 1, "en"))
        self.cur.execute("INSERT INTO answers (user_id) VALUES (?)",
                         (int(ctx.author.id),))
        await dm_channel.send(
            """Please answer the following questions in this chat.""", components=[abort_button])
        await dm_channel.send("""*Question 1/11*\nWhat's your name? (Ingame **and** real life)""")
        await ctx.send("Please check your private messages!", ephemeral=True)

    @i.component_callback("button_abort")
    async def abort(self, ctx: i.ComponentContext):
        self.cur.execute("DELETE FROM user WHERE user_id = ?", (int(ctx.author.id),))
        self.cur.execute("DELETE FROM answers WHERE user_id = ?", (int(ctx.author.id),))
        await ctx.send(":thumbsup:")

    @i.component_callback("button_accept")
    async def accept(self, ctx: i.ComponentContext):
        self.cur.execute("SELECT * FROM applications WHERE message_id = ?",
                         (int(ctx.message.id),))
        application = self.cur.fetchone()
        user = await self.bot.fetch_user(application[2])
        translator = Translator(application[1])
        await user.send(translator.translate("app.accepted"))
        accept_button: Button = ctx.component
        accept_button.disabled = True
        components = [accept_button]
        await ctx.edit_origin(embeds=ctx.message.embeds, components=components)
        self.cur.execute("DELETE FROM applications WHERE message_id = ?",
                         (int(ctx.message.id),))

    @i.component_callback("button_decline")
    async def decline(self, ctx: i.ComponentContext):
        self.cur.execute("SELECT * FROM applications WHERE message_id = ?",
                         (int(ctx.message.id),))
        application = self.cur.fetchone()
        user = await self.bot.fetch_user(application[2])
        translator = Translator(application[1])
        await user.send(translator.translate("app.declined"))
        decline_button: Button = ctx.component
        decline_button.disabled = True
        components = [decline_button]
        await ctx.edit_origin(embeds=ctx.message.embeds, components=components)
        self.cur.execute("DELETE FROM applications WHERE message_id = ?",
                         (int(ctx.message.id),))

    @i.listen()
    async def on_message_create(self, event: i.events.MessageCreate):
        if not isinstance(event.message.channel, i.DMChannel) or event.message.author == self.bot.user:
            return
        self.cur.execute("SELECT * FROM user WHERE user_id = ?",
                         (int(event.message.author.id),))
        user = self.cur.fetchone()
        if user is None:
            return
        translator = Translator(user[3])
        self.cur.execute(f"UPDATE answers SET answer_{user[2]} = ? WHERE user_id = ?",
                         (event.message.content, user[0]))
        if user[2] == 11:
            await self.complete_application(user[0], user[3])
            await event.message.channel.send(translator.translate("app.done"))
            return
        self.cur.execute(
            "UPDATE user SET current_question = ? WHERE user_id = ?", (user[2] + 1, user[0]))
        question = "*" + translator.translate("app.questions.question") + f" {str(user[2] + 1)}/11*\n" +\
            translator.translate(f"app.questions.{user[2] + 1}")
        await event.message.channel.send(question)


def setup(bot):
    ApplicationCommand(bot)
