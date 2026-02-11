def make_full_name(given_name, family_name):
    # Fíjate bien: hay un ESPACIO después del punto y coma
    full_name = f"{family_name}; {given_name}" 
    return full_name


def extract_family_name(full_name):
    """Extract and return the family name from the full name string."""
    # Find the index where "; " appears
    semicolon_index = full_name.index("; ")

    # Extract the family name (everything before the semicolon)
    family_name = full_name[0 : semicolon_index]
    return family_name


def extract_given_name(full_name):
    """Extract and return the given name from the full name string."""
    # Find the index where "; " appears
    semicolon_index = full_name.index("; ")

    # FIX: Start extracting 2 characters after the semicolon 
    # to skip both the ';' and the ' '
    given_name = full_name[semicolon_index + 2 : ]
    return given_name