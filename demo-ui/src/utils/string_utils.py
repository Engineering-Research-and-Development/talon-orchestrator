
def convert_to_title_case(snake_str):
    # Split the string by underscores
    words = snake_str.split('_')
    # Capitalize each word
    capitalized_words = [word.capitalize() for word in words]
    # Join the words with spaces
    title_case_str = ' '.join(capitalized_words)
    return title_case_str