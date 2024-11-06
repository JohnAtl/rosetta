# rosetta
Translate from source to canonical words, then back to original source words.

This module uses a dictionary (dictionaries.toml), where it looks up a canonical word from one or more source words. These translations are further grouped into dialects, such as events or edf channel names, so that a source word may be translated to text that is human readable, such as a description, as well as to words specific to the system, such as channel names. The module further ensures that when a canonical word is translated back to a source word, the correct source word is used.

For example:
```
canonical = rosetta.get_canonical("Queixo", Dialect.DESCRIPTIONS)
# canonical is CHIN
source = rosetta.get_source("CHIN", Dialect.DESCRIPTIONS)
# source is Queixo
```
If Spanish source words are added to the dictionary:
```
canonical = rosetta.get_canonical("Mentón", Dialect.DESCRIPTIONS)
# canonical is CHIN
source = rosetta.get_source("CHIN", Dialect.DESCRIPTIONS)
# source is Mentón
```
Thus, the proper source word is returned for the translated canonical word.

Dialects currently available:
EVENTS - Event names, such as SNORE, AROUSAL, etc.
DESCRIPTIONS - Descriptions for humans to read
CHANNEL_NAMES_EDF - EDF channel names
CHANNEL_NAMES_XML - XML/RML channel names

Translations are also system-specific, so that NEUROVIRTUAL channel names do not clash with RESPIRONICS channel names, etc. The system is chosen when rosetta is initialized.

```
from ml_shared.type_defs import SystemType
from rosetta.rosetta import rosetta, Dialect

rosetta.load_from_file(SystemType.NEUROVIRTUAL)
...
canonical = rosetta.get_canonical("QUEIXO", Dialect.DESCRIPTIONS)
...
```

Case is preserved, and lookups in the dictionaries are case insensitive, so QUEIXO and Queixo will both return CHIN. Source words are returned with case preserved, so in the previous example, QUEIXO or Queixo will be returned.
