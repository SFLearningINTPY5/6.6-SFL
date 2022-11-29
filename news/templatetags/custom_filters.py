from django import template
import re

register = template.Library()

@register.filter()
def censor(value: str):
    bad_word = ['drx', 'кибер']
    ln = len(bad_word)
    after_censor = ''
    string = ''
    model = "*"
    for i in value:
        string += i
        new_string = string.lower()
        word_ln = 0
        for j in bad_word:
            if new_string in j:
                word_ln += 1
        if new_string == j:
            after_censor += model + len(string)
            word_ln -= 1
            string = ''
        if word_ln == ln:
            after_censor += string
        if new_string != ' ' and new_string not in bad_word:
            after_censor += string
        elif new_string != ' ':
            after_censor += model + len(string)
    return f'{after_censor}'
