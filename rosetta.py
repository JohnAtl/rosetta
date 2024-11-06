"""
This module provides a `Rosetta` class that facilitates term translations across different
dialects in a system. It loads dictionary data from a TOML file based on a specified
system type and enables lookups to obtain canonical or source terms.

It handles dialect-specific translations for terms, making it possible to convert
between system-specific terminology and a standard set of terms.

Classes:
    Rosetta: Manages term translation between source terms and canonical forms within
             different dialects for a specified system type.
"""

from importlib import resources
from os.path import exists
from pathlib import Path

import toml

from src.hypnos.type_defs import Dialect, FilePath, SystemType


class NoTranslationError(Exception):
    """
    Exception thrown when there is a translation error.
    """


class Rosetta:
    """
    Manages translations between source terms and canonical forms for different dialects
    within a specified system. The `Rosetta` class loads a dictionary based on the
    specified `system_type`, allowing bidirectional translations for terms in various
    dialects.

    Attributes:
        PACKAGE_NAME (str): The default package name where dictionary files are located.
        system_type (SystemType): Specifies the system type for dictionary loading.
        _translated (dict[str, dict[str, str]]): Internal storage of mappings between
            canonical terms and source terms, facilitating fast reverse lookups.
        _dictionary (dict): The loaded dictionary data for the specified system type,
            containing translation mappings for each dialect.
    """

    _instance = None

    PACKAGE_NAME = "hypnos"

    _dictionary = {}
    _translated = {}
    system_type: SystemType = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def load_from_file(
        cls,
        system_type: SystemType,
        dictionary_filepath: FilePath = Path("dictionaries.toml"),
    ):
        """
        Load dictionary from a TOML file.
        """
        cls.system_type = system_type
        if not exists(dictionary_filepath):
            dictionary_filepath = (
                Path(str(resources.files(Rosetta.PACKAGE_NAME))) / dictionary_filepath
            )
        if not exists(dictionary_filepath):
            raise FileNotFoundError(f"Dictionary file {dictionary_filepath} not found.")

        cls._translated: dict[str, dict[str, str]] = {}
        all_dictionaries = toml.load(dictionary_filepath)
        cls._dictionary = all_dictionaries[system_type.short_name]

    @classmethod
    def get_canonical(cls, source: str, dialect: Dialect) -> str:
        """
        Retrieve the canonical term for a given source term within a specified dialect.

        Args:
            source (str): The source term to be translated.
            dialect (Dialect): The dialect in which the source term resides.

        Returns:
            str: The canonical term corresponding to the provided source term.

        Raises:
            ValueError: If no canonical term is found for the given source term
                within the specified dialect.

        Side Effects:
            Updates the internal `_translated` dictionary, storing the mapping
            between the canonical and source term for future reference.
        """

        if source is None:
            return None

        dialect_dict = cls._dictionary[dialect.dialect]
        for canonical, sources in dialect_dict.items():
            if source in sources:
                if dialect.dialect not in cls._translated:
                    cls._translated[dialect.dialect] = {}
                cls._translated[dialect.dialect][canonical] = source
                return canonical
        raise NoTranslationError(
            f"No translation for {source} in {cls.system_type}[{dialect}]"
        )

    @classmethod
    def get_source(cls, canonical: str, dialect: Dialect) -> str:
        """
        Retrieve the source term corresponding to a previously translated canonical term
        within a specified dialect.

        Args:
            canonical (str): The canonical term to be looked up.
            dialect (Dialect): The dialect in which the canonical term resides.

        Returns:
            str: The source term associated with the specified canonical term.

        Raises:
            ValueError: If the canonical term was not previously translated in the
                specified dialect and therefore cannot be found in the internal `_translated`
                dictionary.
        """
        if dialect.dialect not in cls._translated:
            cls._translated[dialect.dialect] = {}
        if canonical in cls._translated[dialect.dialect]:
            return cls._translated[dialect.dialect][canonical]
        # If not previously translated, default to the first source text availabl
        if canonical in cls._dictionary[dialect.dialect]:
            first_source = cls._dictionary[dialect.dialect][canonical][0]
            cls._translated[dialect.dialect][canonical] = first_source
            return cls._translated[dialect.dialect][canonical]
        raise NoTranslationError(
            f"No source text for {canonical} in {cls.system_type}[{dialect.dialect}]"
        )


rosetta = Rosetta.get_instance()
