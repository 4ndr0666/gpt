# Split the content into sections
sections = content.split(',\n')

# Replace the color values in the sections
for i, section in enumerate(sections):
    for key, value in new_color_scheme.items():
        if f'"{key}"' in section:
            sections[i] = re.sub(r':\s*".+?"', f': "{value}"', section)

# Join the sections back together
modified_content = ',\n'.join(sections)

# Write the modified content back to the file
with open(file_path, 'w') as file:
    file.write(modified_content)

modified_content[:500]  # Displaying the first 500 characters
