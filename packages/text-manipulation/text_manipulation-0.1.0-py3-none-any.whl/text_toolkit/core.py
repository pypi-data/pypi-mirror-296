def count_periods(text):
    """Retourne le nombre de points dans le texte."""
    return text.count('.')

def count_exclamations(text):
    """Retourne le nombre de points d'exclamation dans le texte."""
    return text.count('!')

def count_words(text):
    """Retourne le nombre de mots dans le texte."""
    return len(text.split())

def count_commas(text):
    """Retourne le nombre de virgules dans le texte."""
    return text.count(',')

def count_sentences(text):
    """Retourne le nombre de phrases dans le texte en comptant les points, points d'interrogation, et points d'exclamation."""
    return text.count('.') + text.count('!') + text.count('?')

def count_questions(text):
    """Retourne le nombre de points d'interrogation dans le texte."""
    return text.count('?')
