Here are some suggestions to improve and standardize your `README.md` file for clarity, structure, and consistency:

---

# `rosetta`

The `rosetta` module facilitates translations between source terms and canonical words and allows translations to revert to their original source terms. 

## Overview

The module uses a dictionary file (`dictionaries.toml`) to map one or more source words to a canonical term, organized into specific **dialects** such as event names or channel names for EDF files. This allows source terms to be translated into human-readable text or system-specific terms (e.g., channel names). When a canonical word is translated back to a source word, the original source word is correctly restored.

### Example Usage

```python
canonical = rosetta.get_canonical("Queixo", Dialect.DESCRIPTIONS)
# canonical is 'CHIN'

source = rosetta.get_source("CHIN", Dialect.DESCRIPTIONS)
# source is 'Queixo'
```

If Spanish source words are added to the dictionary:

```python
canonical = rosetta.get_canonical("Mentón", Dialect.DESCRIPTIONS)
# canonical is 'CHIN'

source = rosetta.get_source("CHIN", Dialect.DESCRIPTIONS)
# source is 'Mentón'
```

The correct source word is returned for the translated canonical term.

### Available Dialects

- **EVENTS** - Event names such as `SNORE`, `AROUSAL`, etc.
- **DESCRIPTIONS** - Human-readable descriptions
- **CHANNEL_NAMES_EDF** - Channel names specific to EDF files
- **CHANNEL_NAMES_XML** - Channel names specific to XML/RML files

### System-Specific Translations

Translations are system-specific to avoid conflicts, e.g., NEUROVIRTUAL channel names differ from RESPIRONICS channel names. The system type is specified during initialization.

### Case Handling

Lookups in the dictionaries are case-insensitive (e.g., `QUEIXO` and `Queixo` both translate to `CHIN`). However, when source words are returned, case is preserved.

## Quick Start

```python
from ml_shared.type_defs import SystemType
from rosetta.rosetta import rosetta, Dialect

# Load a dictionary for a specific system type
rosetta.load_from_file(SystemType.NEUROVIRTUAL)

# Translate a source term to a canonical term
canonical = rosetta.get_canonical("QUEIXO", Dialect.DESCRIPTIONS)

# Translate a canonical term back to its original source term
source = rosetta.get_source("CHIN", Dialect.DESCRIPTIONS)
```
