## [4.1.9] - 2020-01-21
### Fixed
- Typo in BrowserType
- Prevent to download resources with urls that starts from `data:`
- Creating VGResource with Python 2
## [4.1.8] - 2020-01-20
### Updated
- Visual Grid: Added older versions support for Chrome, Firefox and Safari browsers. [Trello 1479](https://trello.com/c/kwsR1zql)
## [4.1.7] - 2020-01-17
### Fixed
- Dependencies warning at runtime [Trello 1476](https://trello.com/c/Rmqo8HPM)
- Infinite loop during render when opened without viewport size [#90](https://github.com/applitools/eyes.sdk.python/pull/90)
## [4.1.6] - 2020-01-08
### Fixed
- Multiple instances opening on Windows [Trello 1457](https://trello.com/c/noYzDV70)
## [4.1.5] - 2020-01-08
### Fixed
- Wrong screenshot location when using .fully() [Trello 1455](https://trello.com/c/veMyZsyg)
- Handling setoverflow [Trello 1448](https://trello.com/c/cIgjp0z6)
- Broken By.XPATH select in fluent interface [Trello 1452](https://trello.com/c/R0bFRpSc)
## [4.1.4] - 2019-12-30
### Added
- Support SVG resource fetching [Trello 193](https://trello.com/c/nZdODyjL)
## [4.1.3] - 2019-12-20
### Fixed
- Python SDK was abort_async [Trello 1090](https://trello.com/c/SCsMv6JN)
- (selenium) Not working switching to previous context after check [Trello 1262](https://trello.com/c/YoGEYS09)
- (visualgrid) Test should be aborted if rendering failed [Trello 46](https://trello.com/c/diOQDnzi)
## [4.1.2] - 2019-12-15
### Added
- Fluent interface for Configuration [Trello 1407](https://trello.com/c/KUCeFzik)
### Fixed
- Call of eyes.get_configuration() raises exception [Trello 1405](https://trello.com/c/QUiQG4RI)
## [4.1.1] - 2019-12-10
### Fixed
- eyes get/set_configuration() was returning configuration instance instead of clone [Trello 1378](https://trello.com/c/WtnHxRzD)
- Classic Runner get_all_test_results() Throws type error [Trello 1381](https://trello.com/c/kJJBEu4M)
## [4.1.0] - 2019-12-9
### Fixed
- app_urls and api_urls were always None in TestResults
- Validation error when passing RectangleSize as viewport_size in Configuration
- CSS scrolling in chrome 78. [Trello 1206](https://trello.com/c/euVqe1Sv)
- Rotation on mobile is broken [Trello 1354](https://trello.com/c/hS6Lv8PT)
- Capturing iframe's with VG [Trello 1356](https://trello.com/c/J5so3FDN)
- VG test don't run correctly with multiple Eyes [Trello 1329](https://trello.com/c/6KHE8FAO)
### Added
- Match region support in VG
- Check region support in VisualGrid client [Trello 1360](https://trello.com/c/rFOwfgwA)
- DomCapture 7.0.22, DomSnapshot 1.4.8 [Trello 1227](https://trello.com/c/d5hmB3gG)
- ClassicRunner [Trello 1093](https://trello.com/c/DxBia1UC)
- Type hints for Target class.
- Allow to get/set Configuration in Eyes with methods.
- This CHANGELOG file.
