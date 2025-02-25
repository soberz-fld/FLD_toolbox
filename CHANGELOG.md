# Change Log
In this document, most significant changes are noted.
## [0.0.6] - 2025.02.21
### Changed
* Logging: Writing to file runs now in only one thread.
### Fixed
* Logging: Can be used in multi thread environments.
## [0.0.5 b4] - 2024.02.20
### Added
* Dynamic list to table string
* MariaDB connector can return header names
## [0.0.5 b3] - 2023.07.22
### Added
* ping / latency check
### Fixed
* HomeAssistant DB entity_id in states_meta instead of states
* HomeAssistant time tracking in timestamp instead of datetime
## [0.0.5 b2] - 2023.07.18
### Changed
* dict.py -> dicts.py
* list.py -> lists.py
* string.py -> strings.py
## [0.0.5 b1] - 2023.07.18
### Added
* calcs/geo
## [0.0.5] - 2023.07.17
### Added
* Package files
* files.idx3
## [0.0.4 b1] - 2023.05.29
### Changed
* Allow more than one sqlite_connector to be used
## [0.0.4] - 2023.05.29
### Added
* Colored_StdInOut
## [0.0.3] - 2023.05.27
### Added
* Email Connector
## [0.0.2] - 2023.04.18
### Added
* SQLite Connector
## [0.0.1 b2] - 2022.11.29
### Added
* media package
* media.pictures
* calcs.numbers
## [0.0.1 b1] - 2022.11.24
### Added
* ModbusTCP functionalities
* ModbusTCP-HomeAssistant-Gateway
* fldsvsmanager as a manager for scheduled services
* Logging: Log type 'alert'
### Fixed
* MariaDB connector error to log
## [0.0.1] - 2022.11.21
### Added
* Homeassistant_DB min/max and avg
### Changed
* Log changed from kwarg based to positional parameter based
### Fixed
* Home_assistant_connector time parameters
## [0.0.0 b3] - 2022.11.01
### Added
* List calculations
## [0.0.0 b2] - 2022.10.21
### Added
* Networking
* Connectors
    * Homeassistant
    * MariaDB
    * ModbusTCP
### Changed
* Restructured repository
## [0.0.0 b1] - 2022.07.28
### Added
* logging module
## [0.0.0] - 2022.07.27
### Comments
* Started project. Let's go.
<!--
## [0.0.0] - 2022.00.00
### Added
* abc
### Changed
* abc
### Fixed
* abc
### Comments
* abc
-->