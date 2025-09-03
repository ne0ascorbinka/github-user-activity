def plural(base: str, number: int) -> str:
    """Return the plural form of a word based on the given number."""
    if number == 1:
        return base
    if base.endswith('y') and base[-2] not in 'aeiou':
        return base[:-1] + 'ies'
    if base.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return base + 'es'
    return base + 's'