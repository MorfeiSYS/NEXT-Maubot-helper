# Changelog

Все заметные изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версии — [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/MorfeiSYS/NEXT-Maubot-helper/releases/tag/v1.0.0
