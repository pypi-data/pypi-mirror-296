class LoremIpsumGenerator:
    def __init__(self):
        self.full_text = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi "
            "ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit "
            "in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint "
            "occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        )

    def get_text(self, char_count):
        """Returns Lorem Ipsum text with the requested number of characters.
        If the requested length exceeds the original text, the text will repeat."""
        if char_count > 0:
            repeated_text = (self.full_text * ((char_count // len(self.full_text)) + 1))[:char_count]
            return repeated_text
        else:
            return "bruh"

def generate_lorem(char_count):
    generator = LoremIpsumGenerator()
    return generator.get_text(char_count)
