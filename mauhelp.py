from dataclasses import dataclass, field
from html import escape
from typing import Literal, Type

from maubot import MessageEvent, Plugin
from maubot.handlers import command
from mautrix.types import EventType, Format, MessageType, TextMessageEventContent
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper

Lang = Literal["en", "ru"]
LANGS: tuple[Lang, ...] = ("en", "ru")
HelpStyle = Literal["classic", "compact", "outline"]
HELP_STYLES: tuple[HelpStyle, ...] = ("classic", "compact", "outline")

HELP_HELP: dict[Lang, str] = {
    "en": "Shows this help text",
    "ru": "Показывает этот текст справки",
}

LANG_SUBCOMMAND_HELP: dict[Lang, str] = {
    "en": "Set interface language: en or ru",
    "ru": "Установить язык: en или ru",
}

HELP_EN_TO_RU: dict[str, str] = {
    HELP_HELP["en"]: HELP_HELP["ru"],
    LANG_SUBCOMMAND_HELP["en"]: LANG_SUBCOMMAND_HELP["ru"],
}

MESSAGES: dict[str, dict[Lang, str]] = {
    "lang_set": {
        "en": "Language set to English.",
        "ru": "Язык установлен: русский.",
    },
    "lang_invalid": {
        "en": "Invalid language. Use: en or ru",
        "ru": "Неверный язык. Доступно: en или ru",
    },
    "plugin_header": {
        "en": "Plugin",
        "ru": "Плагин",
    },
    "unknown_plugin": {
        "en": "other",
        "ru": "прочее",
    },
}

HELP_PLUGIN_ID = "NEXT.helper"
SECTION_RULE = "────────────────────"


@dataclass
class SubcommandHelp:
    prefix: str
    usage_args: str
    help: str | None


@dataclass
class CommandHelp:
    prefix: str
    usage_args: str
    help: str | None
    require_subcommand: bool
    subcommands: list[SubcommandHelp] = field(default_factory=list)


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("language")
        helper.copy_dict("room_languages")
        helper.copy("help_style")


class MauHelp(Plugin):
    async def start(self) -> None:
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    def get_room_lang(self, room_id: str) -> Lang:
        room_langs = self.config["room_languages"]
        if room_id in room_langs:
            lang = room_langs[room_id]
            if lang in LANGS:
                return lang
        default = self.config["language"]
        return default if default in LANGS else "en"

    def get_help_style(self) -> HelpStyle:
        style = self.config.get("help_style", "classic")
        return style if style in HELP_STYLES else "classic"

    def is_own_command_handler(self, handler_func) -> bool:
        return getattr(handler_func, "__bound_instance__", None) is self

    @staticmethod
    def localize_help_text(text: str | None, lang: Lang) -> str | None:
        if text is None or lang == "en":
            return text
        return HELP_EN_TO_RU.get(text, text)

    @staticmethod
    def handler_plugin_id(handler_func) -> str:
        inst = getattr(handler_func, "__bound_instance__", None)
        loader = getattr(inst, "loader", None) if inst is not None else None
        meta = getattr(loader, "meta", None) if loader is not None else None
        if meta is not None:
            return meta.id
        return ""

    @staticmethod
    def _usage_tail(args: str) -> str:
        args = (args or "").strip()
        return f" {args}" if args else ""

    def parse_command_help(self, handler_func, lang: Lang) -> CommandHelp:
        own = self.is_own_command_handler(handler_func)
        mb_help = handler_func.__mb_help__
        mb_help_out = self.localize_help_text(mb_help, lang) if own else mb_help
        subs: list[SubcommandHelp] = []
        for sub in handler_func.__mb_subcommands__:
            sub_help = sub.__mb_help__
            sub_help_out = (
                self.localize_help_text(sub_help, lang) if own else sub_help
            )
            subs.append(
                SubcommandHelp(
                    prefix=sub.__mb_prefix__,
                    usage_args=(sub.__mb_usage_args__ or "").strip(),
                    help=sub_help_out,
                )
            )
        return CommandHelp(
            prefix=handler_func.__mb_prefix__,
            usage_args=(handler_func.__mb_usage_args__ or "").strip(),
            help=mb_help_out,
            require_subcommand=handler_func.__mb_require_subcommand__,
            subcommands=subs,
        )

    def render_command(self, cmd: CommandHelp, style: HelpStyle) -> list[str]:
        lines: list[str] = []
        tail = self._usage_tail(cmd.usage_args)
        desc = f" — {cmd.help}" if cmd.help else ""

        if style == "classic":
            lines.append(f"• {cmd.prefix}{desc}" if desc else f"• {cmd.prefix}")
            if not cmd.require_subcommand and tail:
                lines.append(f"  ↳ {cmd.prefix}{tail}")
            for sub in cmd.subcommands:
                sub_desc = f" — {sub.help}" if sub.help else ""
                lines.append(
                    f"  · {sub.prefix}{self._usage_tail(sub.usage_args)}{sub_desc}"
                )
        elif style == "compact":
            lines.append(f"- {cmd.prefix}{desc}" if desc else f"- {cmd.prefix}")
            if not cmd.require_subcommand and tail:
                lines.append(f"    {cmd.prefix}{tail}")
            for sub in cmd.subcommands:
                sub_desc = f" — {sub.help}" if sub.help else ""
                lines.append(
                    f"  - {sub.prefix}{self._usage_tail(sub.usage_args)}{sub_desc}"
                )
        else:  # outline
            lines.append(f"> {cmd.prefix}{desc}" if desc else f"> {cmd.prefix}")
            if not cmd.require_subcommand and tail:
                lines.append(f">> {cmd.prefix}{tail}")
            for sub in cmd.subcommands:
                sub_desc = f" — {sub.help}" if sub.help else ""
                lines.append(
                    f">> {sub.prefix}{self._usage_tail(sub.usage_args)}{sub_desc}"
                )
        return lines

    def render_plugin_header(
        self, plugin_id: str, lang: Lang, style: HelpStyle
    ) -> list[str]:
        if style == "classic":
            word = MESSAGES["plugin_header"][lang]
            return [SECTION_RULE, f"{word}: {plugin_id}", SECTION_RULE]
        if style == "compact":
            return [f"[{plugin_id}]"]
        return [f"=== {plugin_id} ==="]

    def collect_by_plugin(self, lang: Lang) -> dict[str, list[tuple[str, CommandHelp]]]:
        by_plugin: dict[str, list[tuple[str, CommandHelp]]] = {}
        for handler_func in self.client.event_handlers[EventType.ROOM_MESSAGE]:
            if not (
                hasattr(handler_func, "__mb_name__")
                and hasattr(handler_func, "__mb_usage_inline__")
            ):
                continue

            plugin_id = self.handler_plugin_id(handler_func) or MESSAGES["unknown_plugin"][lang]
            cmd_name = handler_func.__mb_name__
            cmd = self.parse_command_help(handler_func, lang)
            by_plugin.setdefault(plugin_id, []).append((cmd_name, cmd))
        return by_plugin

    @staticmethod
    def sort_plugin_ids(by_plugin: dict[str, list], lang: Lang) -> list[str]:
        def sort_key(pid: str) -> tuple[int, str]:
            if pid == HELP_PLUGIN_ID:
                return (1, pid)
            if pid == MESSAGES["unknown_plugin"][lang]:
                return (2, pid)
            return (0, pid)

        return sorted(by_plugin.keys(), key=sort_key)

    def build_help_lines(self, lang: Lang, style: HelpStyle) -> list[str]:
        by_plugin = self.collect_by_plugin(lang)
        lines: list[str] = []
        first_plugin = True
        for plugin_id in self.sort_plugin_ids(by_plugin, lang):
            if not first_plugin:
                lines.append("")
            first_plugin = False

            lines.extend(self.render_plugin_header(plugin_id, lang, style))

            entries = sorted(by_plugin[plugin_id], key=lambda e: e[0])
            for i, (_, cmd) in enumerate(entries):
                if i > 0:
                    lines.append("")
                lines.extend(self.render_command(cmd, style))
        return lines

    @staticmethod
    def help_as_message(lines: list[str]) -> TextMessageEventContent:
        text = "\n\n".join(lines)
        html_parts = [
            f"<div>{escape(line)}</div>" if line else "<br/>" for line in lines
        ]
        return TextMessageEventContent(
            msgtype=MessageType.TEXT,
            body=text,
            format=Format.HTML,
            formatted_body="".join(html_parts),
        )

    @command.new(name="help", help=HELP_HELP["en"], require_subcommand=False)
    async def help(self, evt: MessageEvent) -> None:
        lang = self.get_room_lang(evt.room_id)
        style = self.get_help_style()
        await evt.respond(
            self.help_as_message(self.build_help_lines(lang, style)), reply=False
        )

    @help.subcommand("lang", help=LANG_SUBCOMMAND_HELP["en"])
    @command.argument("language", matches="en|ru")
    async def help_lang(self, evt: MessageEvent, language: str) -> None:
        language = language.lower()
        room_lang = self.get_room_lang(evt.room_id)
        if language not in LANGS:
            await evt.reply(MESSAGES["lang_invalid"][room_lang])
            return
        self.config["room_languages"][evt.room_id] = language
        self.config.save()
        await evt.reply(MESSAGES["lang_set"][language])
