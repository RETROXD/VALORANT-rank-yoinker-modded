<p align="center">
    <a href="https://github.com/isaacKenyon/valorant-rank-yoinker/">
        <img src="assets/Logo.png" alt="Logo" width="160" height="160">
    </a>
<h5 align="center"> VALORANT rank yoinker</h5>

[![Discord][discord-shield]][discord-url]
[![Downloads][downloads-shield]][downloads-url]
[![Language][language-shield]][language-url]
[![License][license-shield]][license-url]
     
 
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
  </ol>

    
## About The Project

 ![Screenshot](assets/Example.png)
 ![Skin Showcase Image](assets/SkinShowcase.png)

|Their Queue|Current Skin|Current Rank|Rank Rating|Peak Rank|Account Level|
|:---:|:---:|:---:|:---:|:---:|:---:|
|![Parties](assets/Party.png)|![Skin](assets/Skin.png)|![Rank](assets/Rank.png)|![Rating](assets/Rating.png)|![Peak](assets/PeakRank.png)|![Level](assets/Level.png)|
    

## Usage
 **VALORANT must be open**.

### Bundled Release:

1) Download the [release](https://github.com/isaacKenyon/valorant-rank-yoinker/releases/latest).
2) Extract **all** files.
3) Run vRY.exe.

### Running from source:

1) Download [Python 3.10](https://www.python.org/downloads/release/python-3100/), make sure it is added to the PATH. (This is an option on installation.)
   1) Any Python version post 3.8 should work.
2) Download the [source](https://github.com/isaacKenyon/VALORANT-rank-yoinker/archive/refs/heads/main.zip).
3) Open a terminal within the source folder.
4) `pip install -r requirements.txt`
5) `main.py`

### Compiling from source:

1) `pip install cx_Freeze`
2) `python setup.py build`
3)  Open the new Build folder and find vRY.exe.

> `-` You can change the desired weapon by editing the gun in `config.json`, or by deleting the file for vRY re-prompt you.

> `-` View all skins: <https://vry.netlify.app/matchLoadouts>.

## What about that Tweet?

 The [Tweet](https://twitter.com/PlayVALORANT/status/1539728676815642624), which details Riot's API policies outlines how
 applications are not allowed to expose data hidden by the game client. As of Version 1.262, vRY respects streamer mode.

## Contributing

 Any contributions you make are **greatly appreciated**.
 
## Contact 

 Join the community discord:         
 
[![Discord Banner 2][discord-banner]][discord-url]

## Acknowledgements

 - [Valorant-API.com](https://valorant-api.com/)
 - [Hamper](https://hamper.codes/)
 - [D3CRYPT](https://d3crypt360.pages.dev/)
 
## Disclaimer

 THIS PROJECT IS NOT ASSOCIATED OR ENDORSED BY RIOT GAMES. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
    
 Whilst effort has been made to abide by Riot's API rules; you acknowledge that use of this software is done so at your own risk.


[discord-shield]: https://img.shields.io/discord/872101595037446144?color=7289da&label=Support&logo=discord&logoColor=7289da&style=for-the-badge
[discord-url]: https://discord.gg/HeTKed64Ka
[discord-banner]: https://discordapp.com/api/guilds/872101595037446144/widget.png?style=banner2

[downloads-shield]: https://img.shields.io/github/downloads/isaacKenyon/VALORANT-rank-yoinker/total?style=for-the-badge&logo=github
[downloads-url]: https://github.com/isaacKenyon/VALORANT-rank-yoinker/releases/latest

[language-shield]: https://img.shields.io/github/languages/top/isaacKenyon/Valorant-rank-yoinker?logo=python&logoColor=yellow&style=for-the-badge
[language-url]: https://www.python.org/

[license-shield]: https://img.shields.io/github/license/isaacKenyon/valorant-rank-yoinker?style=for-the-badge
[license-url]: https://github.com/isaacKenyon/valorant-rank-yoinker/blob/main/LICENSE
