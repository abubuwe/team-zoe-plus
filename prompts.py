def build_heading_prompt(snippet: str):
    return f"""You are an expert web accessibility consultant and web developer. In order to improve accessibility of a webpage, add a heading to the following code snippet where it is missing. The snippet is denoted with <snippet></snippet> XML tags.

Rules: 
- Output the code snippet with the additional heading.
- Keep **ALL** original content. Do not modify **ANY** content except to add the header.
- Output valid HTML, CSS and JavaScript, in the same order as the original snippet.
- Add any additional HTML tags as necessary, including <h1></h1>, <h2></h2>, <h3></h3> etc.
- Add a heading between any empty heading tags.
- If an HTML tag is styled to look like another HTML tag, replace it with the correct HTML tag.
- Make sure your output is correct and accessible. It is very important for people with disabilities to be able to read the original webpage.

Snippet:
<snippet>
{snippet}
</snippet>
"""