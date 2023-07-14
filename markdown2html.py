#!/usr/bin/python3
import sys
import os
import hashlib

if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.exists(input_file):
    print(f"Missing {input_file}", file=sys.stderr)
    sys.exit(1)

# Read the input file
with open(input_file, "r") as f:
    markdown_content = f.readlines()

# Convert Markdown headings to HTML
html_content = ""
is_list = False
is_paragraph = False
for line in markdown_content:
    if line.startswith("- "):
        if not is_list:
            if is_paragraph:
                html_content += "</p>\n"
                is_paragraph = False
            html_content += "<ul>\n"
            is_list = True
        list_item = line.strip("- \n")
        html_content += f"    <li>{list_item}</li>\n"
    elif line.strip() == "":
        if is_list:
            html_content += "</ul>\n"
            is_list = False
        if not is_paragraph:
            html_content += "<p>\n"
            is_paragraph = True
        html_content += "</p>\n"
        is_paragraph = False
        html_content += line
    else:
        if is_list:
            html_content += "</ul>\n"
            is_list = False
        if not is_paragraph:
            html_content += "<p>\n"
            is_paragraph = True
        if "[[" in line and "]]" in line:
            start_index = line.index("[[") + 2
            end_index = line.index("]]")
            content = line[start_index:end_index]
            hashed_content = hashlib.md5(content.encode("utf-8")).hexdigest()
            line = line.replace(f"[[{content}]]", hashed_content)
        if "((" in line and "))" in line:
            start_index = line.index("((") + 2
            end_index = line.index("))")
            content = line[start_index:end_index]
            modified_content = content.replace("c", "").replace("C", "")
            line = line.replace(f"(({content}))", modified_content)
        html_content += f"    {line.strip()}"
        if line.strip() != "":
            html_content += "<br />\n"

# Check if the list or paragraph is still open at the end of the file
if is_list:
    html_content += "</ul>\n"
if is_paragraph:
    html_content += "</p>\n"

# Write the HTML content to the output file
with open(output_file, "w") as f:
    f.write(html_content)

sys.exit(0)
