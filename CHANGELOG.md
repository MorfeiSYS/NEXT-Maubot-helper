# Changelog

Все заметные изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версии — [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.5] - 2026-11-09

### Added

- Конфиг `help_style`: `classic` (по умолчанию), `compact`, `outline` — три варианта оформления вывода `help`.
- Артефакт релиза `NEXT-Maubot-helper-v1.0.5.mbp`.

## [1.0.4] - 2026-11-09

### Fixed

- Справка `help`: каждая строка через `\n\n` и HTML `<div>`; ответ без reply-thread (`respond`), чтобы клиент не склеивал строки.

### Added

- Артефакт релиза `NEXT-Maubot-helper-v1.0.4.mbp`.

## [1.0.3] - 2026-11-09

### Fixed

- Справка `help`: переносы строк в Matrix (HTML `<br/>`, без схлопывания markdown).

### Added

- Артефакт релиза `NEXT-Maubot-helper-v1.0.3.mbp`.

## [1.0.2] - 2026-11-09

### Changed

- Вывод `help`: группировка по плагину (`meta.id`), разделители и компактные блоки команд вместо слепленного текста Usage.
- Подкоманда смены языка: `help lang` (вместо `help-lang`).

### Added

- Артефакт релиза `NEXT-Maubot-helper-v1.0.2.mbp`.

## [1.0.1] - 2026-11-09

### Added

- Локализация en/ru для строк самого плагина; команды `<prefix>help lang en` и `<prefix>help lang ru` с сохранением выбора в `room_languages`.
- Конфиг инстанса (`base-config.yaml`): `language`, `room_languages`; в `maubot.yaml` включён `config: true`.
- Артефакт релиза `NEXT-Maubot-helper-v1.0.1.mbp`.
- `build.ps1`: после сборки patch-версия в `VERSION` и `maubot.yaml` увеличивается на 1 (следующая сборка — следующий patch).

### Changed

- `maubot.yaml`: id плагина `NEXT.helper` (вместо `ru.morfeisys.next_maubot_helper`).

## [1.0.0] - 2026-03-24

### Added

- Локальная сборка плагина в каталог `build/` (`build.ps1`, `build.bat`, `VERSION`, `requirements-dev.txt`); на Windows `build.ps1` использует `.venv` и задаёт `HOME` для `mbc`.
- Артефакт релиза `NEXT-Maubot-helper-v1.0.0.mbp`.

### Changed

- Ребрендинг под репозиторий [MorfeiSYS/NEXT-Maubot-helper](https://github.com/MorfeiSYS/NEXT-Maubot-helper).
- `maubot.yaml`: id `ru.morfeisys.next_maubot_helper`, version `1.0.0`, license `GPL-3.0`.
- Обновлён `README.md` под проект NEXT-Maubot-helper.

[Unreleased]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/compare/v1.0.5...HEAD
[1.0.5]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/releases/tag/v1.0.5
[1.0.4]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/releases/tag/v1.0.4
[1.0.3]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/releases/tag/v1.0.3
[1.0.2]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/releases/tag/v1.0.2
[1.0.1]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/releases/tag/v1.0.1
[1.0.0]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/releases/tag/v1.0.0
