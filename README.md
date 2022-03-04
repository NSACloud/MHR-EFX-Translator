# Monster Hunter Rise EFX Translator
This tool translates internal EFX names from Japanese to English so that the function of each EFX entry is easier to understand when editing the file.

## Japanese EFX Names
![Japanese EFX Names](https://github.com/mhvuze/MonsterHunterRiseModding/blob/main/img/guides/efx/efxTranslator/efxNamesJapanese.png)
## Translated English EFX Names
![Translated English EFX Names](https://github.com/mhvuze/MonsterHunterRiseModding/blob/main/img/guides/efx/efxTranslator/efxNamesEnglish.png)

The translations are done automatically through Google Translate. As a result, translations aren't perfect, but they should be mostly good enough to determine the function of the EFX entry. The translation results can be edited manually inside translationCache.tsv using Notepad++ or Excel.

To translate to another language, delete translationCache.tsv. Then open EFXLangTranslator.py and change TO_LANGAUGE to whatever language you want to translate to. Note that building the translation cache from nothing will take a long time.

## Usage
**Download from Code > Download ZIP**

Requires **[Python](https://www.python.org/downloads/)**

Also requires the ```translators``` package.

To install translators, open the command prompt and enter ```pip install translators```

To use the tool, drag the ```vfx``` folder from the extracted pak file onto ```EFXLangTranslator.py```

## Output
![Tool Output](https://github.com/mhvuze/MonsterHunterRiseModding/blob/main/img/guides/efx/efxTranslator/toolOutput.png)
