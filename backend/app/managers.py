"""
Custom managers for the gender analysis web app.
"""
from django.db import models


class DocumentManager(models.Manager):
    def create_document(self, **attributes):
        doc = self.create(**attributes)
        doc.get_tokenized_text_wc_and_pos()
        doc.get_tokenized_sentences()
        doc.get_aliases(get_corefs=True)
        doc.get_disambiguated_characters(cutoff_num=25)
        return doc


class CharacterManager(models.Manager):
    def create_character(self, alias):
        # operations that would have occurred within the init function occur here instead.
        character = self.create()
        character.aliases.add(alias)
        character.common_name = alias.get_name()
        character.count = alias.get_count()
        character.full_name = character.guess_full_name()
        character.gender = character.guess_gender()
        character.save()
        return character


class AliasManager(models.Manager):
    def create_alias(self, **attributes):
        alias = self.create(**attributes)
        all_pronouns = alias.calculate_pronouns()
        alias.raw_pronouns = all_pronouns[0]
        alias.pronoun_rates = all_pronouns[1]
        alias.sanitized_pronoun_rates = all_pronouns[2]
        alias.save()
        return alias
