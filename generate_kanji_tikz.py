import json
import re

def parse_memo(memo_text):
    """
    Converts markdown formatting in memo string into LaTeX syntax.
    *word* or **word** -> \textbf{word}
    Converts literal newlines to LaTeX line breaks (\\).
    """
    # Replace *word* or **word** with \textbf{word}
    memo_tex = re.sub(r'\*\*(.*?)\*\*|\*(.*?)\*', lambda m: f"\\textbf{{{m.group(1) or m.group(2)}}}", memo_text)
    # Replace newlines with \\ for TikZ multiline nodes
    memo_tex = memo_tex.replace('\r\n', ' \\\\\n').replace('\n', ' \\\\\n')
    return memo_tex

def generate_tikz_code(data, width="0.48\\textwidth"):
    """
    Generates a scaled TikZ picture block from a dictionary item.
    """
    kanji = data.get("kanji", "")
    pronounce = data.get("pronounce", "")
    radicals = data.get("radicals", {})
    examples = data.get("examples", {})
    memo = data.get("memo", "")

    # Format memo text with bold tags and line breaks
    memo_formatted = parse_memo(memo)

    # Radical placement coordinates matching your original template layout
    radical_positions = [
        {"circle": (-0.31, 3.8), "char_pos": (-0.21, 3.75), "label_pos": (-0.41, 4.25)},
        {"circle": (0.79, 3.75), "char_pos": (0.79, 3.75), "label_pos": (0.89, 4.25)}
    ]

    radicals_code = []
    for idx, (rad_char, rad_label) in enumerate(radicals.items()):
        if idx < len(radical_positions):
            pos = radical_positions[idx]
        else:
            # Automatic horizontal offset fallback if there are more than 2 radicals
            offset = idx * 1.1
            pos = {
                "circle": (-0.31 + offset, 3.8),
                "char_pos": (-0.21 + offset, 3.75),
                "label_pos": (-0.41 + offset, 4.25)
            }
        
        rad_str = (
            f"  \\path ({pos['circle'][0]},{pos['circle'][1]}) circle (0.26cm);\n"
            f"  \\node[draw=none, node font=\\LARGE] at ({pos['char_pos'][0]},{pos['char_pos'][1]}) {{{rad_char}}};\n"
            f"  \\node[draw=none, node font=\\itshape] at ({pos['label_pos'][0]},{pos['label_pos'][1]}) {{{rad_label}}};"
        )
        radicals_code.append(rad_str)
    
    radicals_block = "\n".join(radicals_code)

    # Examples Matrix generation
    matrix_rows = []
    for ex_kanji, ex_info in examples.items():
        furigana = ex_info.get("furigana", "")
        meaning = ex_info.get("meaning", "")
        row = f"  |[node font=\\bfseries]| {{\\overset{{\\text{{\\tiny {furigana}}}}}{{\\text{{\\normalsize {ex_kanji}}}}}}}   \\textmd{{\\textit{{{meaning}}}}} \\\\"
        matrix_rows.append(row)
    
    matrix_block = "\n".join(matrix_rows)

    tikz_template = f"""\\resizebox{{{width}}}{{!}}{{%
\t\\begin{{tikzpicture}}
\t  \\path (0.28,3.2) circle (0.5cm);
\t  \\node[draw=none, node font=\\Huge\\bfseries, minimum height=0, minimum width=38] (node1) at (0.2,3.05) {{{kanji}}};
\t  \\node[draw=none, node font=\\large, minimum width=16] at (0.27,2.32) {{{pronounce}}};
{radicals_block}
\t  \\node[align=center, draw=none, node font=\\small\\itshape, minimum width=76] at (1.48,1.1) {{{memo_formatted}}};
\t  \\node[align=left, draw=none, node font=\\small\\itshape, minimum height=78, minimum width=63.6] at (2.67,3.16) {{}};
\t  \\matrix [matrix of nodes, ampersand replacement=\\\\&] at (3,3.33) {{
{matrix_block}
\t  }};
\t\\end{{tikzpicture}}%
}}"""
    return tikz_template

def process_json_file(json_file_path, output_md_path=None):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Accept either a single JSON object or a list of JSON objects
    if isinstance(data, dict):
        data = [data]
    
    tikz_blocks = [generate_tikz_code(item) for item in data]
    
    # If processing multiple cards, output them side-by-side in pairs
    formatted_output = []
    for i in range(0, len(tikz_blocks), 2):
        if i + 1 < len(tikz_blocks):
            pair = f"\\noindent\n{tikz_blocks[i]}\\hfill%\n{tikz_blocks[i+1]}\n\n"
        else:
            pair = f"\\noindent\n{tikz_blocks[i]}\n\n"
        formatted_output.append(pair)
    
    result = "".join(formatted_output)

    if output_md_path:
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(result)
            
    return result

if __name__ == "__main__":
    # Example usage:
    tikz_output = process_json_file("kanji_data.json", output_md_path="output_tikz.md")
    print(tikz_output)