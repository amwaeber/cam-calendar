import re

def safe_linkify(text: str) -> str:

    # 1. Extract and protect <a>...</a> blocks
    a_tag_pattern = re.compile(r'<a\s+[^>]*?>.*?</a>', re.DOTALL | re.IGNORECASE)
    protected = []

    def protect(match):
        protected.append(match.group(0))
        return f"[[PROTECTED_LINK_{len(protected) - 1}]]"

    text = a_tag_pattern.sub(protect, text)

    # 2. Replace https:// and www. (but not http://)
    def url_repl(match):
        url = match.group(0)
        href = url if url.startswith("https://") else f"https://{url}"
        return f'<a href="{href}">{url}</a>'

    url_pattern = re.compile(r'\b(?:https://[^\s<>"\']+|www\.[^\s<>"\']+)', re.IGNORECASE)
    text = url_pattern.sub(url_repl, text)

    # 3. Replace email addresses not already inside links
    def email_repl(match):
        email = match.group(0)
        return f'<a href="mailto:{email}">{email}</a>'

    email_pattern = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b')
    text = email_pattern.sub(email_repl, text)

    # 4. Restore protected <a> tags
    for i, original in enumerate(protected):
        text = text.replace(f"[[PROTECTED_LINK_{i}]]", original)

    return text