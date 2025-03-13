def get_multiline_input(prompt):
    """Get multi-line input from the user until Ctrl+D is pressed."""
    print(prompt)
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        # User pressed Ctrl+D
        pass
    return "\n".join(lines)


# Get the first multi-line input
first_text = get_multiline_input("Enter the first text (press Ctrl+D when finished):")

# Get the second multi-line input
second_text = get_multiline_input("Enter the second text (press Ctrl+D when finished):")

# Split both inputs into lines
first_lines = first_text.splitlines()
second_lines = second_text.splitlines()

# Find common elements
common_lines = set(first_lines).intersection(set(second_lines))

# Print common elements in alphabetical order
if common_lines:
    print("\nCommon lines in alphabetical order:")
    for line in sorted(common_lines):
        print(line)
else:
    print("\nNo common lines found.")
