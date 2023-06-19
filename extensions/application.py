import interactions as i
import configparser as cp

scope_ids = []


class ApplicationCommand(i.Extension):
    def __init__(self, bot):
        config = cp.ConfigParser()
        config.read("config.ini")
        global scope_ids
        scope_ids = config["General"]["scope_ids"].split(",")

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
            title="♔FALLING SKY♔\nTeam Application",
            description="""<a:6544_heartarrow_purple:956574404647739503> Bitte klicke auf den entsprechenden Button,\
                um eine Bewerbung zu starten und beantworte danach die Fragen.\n\n\
                <:bluearrowheartright:921367937829466152> Please click on the corresponding button to start an\
                application and answer the questions afterwards.""",
            color=i.BrandColors.FUCHSIA.value,
            thumbnail=i.EmbedAttachment(
                url="https://cdn.discordapp.com/attachments/1088092124467183616/1120459818268901438/a_8c47aa36de8915783706e52c85b351db.gif"),
            images=[i.EmbedAttachment(
                url="https://cdn.discordapp.com/attachments/967765571582173214/1097871279652089947/GridArt_20230418_150124888.png")]
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


def setup(bot):
    ApplicationCommand(bot)
