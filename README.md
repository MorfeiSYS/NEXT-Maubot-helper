# NEXT-Maubot-helper

Плагин [maubot](https://github.com/maubot/maubot), который выводит справку по командам загруженных ботов (команда help, как у отдельных плагинов).

Репозиторий: [github.com/MorfeiSYS/NEXT-Maubot-helper](https://github.com/MorfeiSYS/NEXT-Maubot-helper)

Лицензия: [GPL-3.0](LICENSE)

История изменений: [CHANGELOG.md](CHANGELOG.md)

## Использование

В комнате Matrix с настроенным ботом: `<prefix>help` (например `!help`). Плагин перечисляет команды всех загруженных обработчиков с тем же префиксом.

## Язык (en / ru)

Поддерживается только явное переключение (без автоопределения):

- `<prefix>help lang en` — язык комнаты: английский
- `<prefix>help lang ru` — язык комнаты: русский
- `<prefix>help` — список команд; **тексты справки только у этого плагина** (`help`, `help lang`) выводятся на выбранном языке; остальные плагины — в оригинале

В конфиге инстанса (maubot → Instances → Config):

- `language` — язык по умолчанию (`en` или `ru`)
- `room_languages` — переопределение по room id (заполняется автоматически при `help lang`)
- `help_style` — оформление справки:
  - `classic` — линии `────`, маркеры `•` / `↳` / `·`
  - `compact` — заголовок `[plugin_id]`, списки через `-`
  - `outline` — заголовок `=== plugin_id ===`, строки `>` / `>>`

## Сборка на ПК (Windows)

Нужен Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
.\build.ps1
```

Или двойной клик по `build.bat`.

Готовый пакет: `build/NEXT-Maubot-helper-v<версия>.mbp` (версия из файла [VERSION](VERSION) на момент запуска сборки). Загрузите `.mbp` в веб-интерфейс maubot (Plugins → upload).

После успешной сборки `build.ps1` увеличивает patch в `VERSION` и `maubot.yaml` на 1 (например `1.0.1` → `1.0.2` для следующего релиза). Major/minor меняйте в `VERSION` вручную перед сборкой.

Вручную:

```powershell
python -m maubot.cli build -o build/NEXT-Maubot-helper-v1.0.0.mbp
```

Перед релизом обновите [CHANGELOG.md](CHANGELOG.md). Номер patch в [VERSION](VERSION) задайте для текущего релиза; `version` в `maubot.yaml` подтянется при сборке.
