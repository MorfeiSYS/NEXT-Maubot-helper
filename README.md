# NEXT-Maubot-helper

Плагин [maubot](https://github.com/maubot/maubot), который выводит справку по командам загруженных ботов (команда help, как у отдельных плагинов).

Репозиторий: [github.com/MorfeiSYS/NEXT-Maubot-helper](https://github.com/MorfeiSYS/NEXT-Maubot-helper)

Лицензия: [GPL-3.0](LICENSE)

История изменений: [CHANGELOG.md](CHANGELOG.md)

## Использование

В комнате Matrix с настроенным ботом: `<prefix>help` (например `!help`). Плагин перечисляет команды всех загруженных обработчиков с тем же префиксом.

## Сборка на ПК (Windows)

Нужен Python 3.10+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
.\build.ps1
```

Или двойной клик по `build.bat`.

Готовый пакет: `build/NEXT-Maubot-helper-v<версия>.mbp` (версия из файла [VERSION](VERSION)). Загрузите `.mbp` в веб-интерфейс maubot (Plugins → upload).

Вручную:

```powershell
python -m maubot.cli build -o build/NEXT-Maubot-helper-v1.0.0.mbp
```

Следующий релиз: обновите `VERSION`, поле `version` в `maubot.yaml` и [CHANGELOG.md](CHANGELOG.md), затем снова запустите `build.ps1`.
