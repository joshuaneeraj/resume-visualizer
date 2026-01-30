"""Parse a LaTeX resume (sb2nov/resume template) into structured Python data."""

import re
from pathlib import Path


def _clean(text):
    """Strip LaTeX commands and escapes, returning plain text."""
    s = text.strip()
    # \href{url}{display} → display
    s = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', s)
    # Unwrap formatting commands (repeat for nesting)
    for _ in range(3):
        s = re.sub(
            r'\\(?:textbf|textit|small|scshape|Large|large)\s*\{([^}]*)\}',
            r'\1', s,
        )
    # Remove bare formatting commands without braces (\small, \scshape, etc.)
    s = re.sub(r'\\(?:small|scshape|Large|large)\b\s*', '', s)
    # Remove spacing commands
    s = re.sub(r'\\(?:vspace|hspace)\{[^}]*\}', '', s)
    # LaTeX character escapes
    s = s.replace('\\&', '&')
    s = s.replace('\\$', '$')
    s = s.replace('\\%', '%')
    s = s.replace('\\#', '#')
    # Typographic cleanup
    s = s.replace(' -- ', ' \u2014 ')   # en-dash → em-dash
    s = s.replace('$|$', '|')
    s = s.replace('\\\\', '')
    # Normalise whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def _extract_braced(text, n):
    """Extract the next *n* consecutive ``{…}`` arguments, respecting nesting."""
    args = []
    pos = 0
    for _ in range(n):
        start = text.find('{', pos)
        if start == -1:
            break
        depth = 0
        for i in range(start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    args.append(text[start + 1:i])
                    pos = i + 1
                    break
    return args


def _extract_items(text):
    r"""Return a list of plain-text strings from ``\resumeItem{…}`` calls."""
    items = []
    for m in re.finditer(r'\\resumeItem\{', text):
        pos = m.end()
        depth = 1
        for i in range(pos, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    items.append(_clean(text[pos:i]))
                    break
    return items


def _split_sections(body):
    r"""Split a document body into a header string and ``{name: text}`` dict."""
    pattern = re.compile(r'\\section\{([^}]+)\}')
    matches = [(m.start(), m.group(1)) for m in pattern.finditer(body)]

    header = body[:matches[0][0]] if matches else body
    sections = {}
    for i, (start, name) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(body)
        sections[name] = body[start:end]
    return header, sections


# ── Section parsers ────────────────────────────────────────────────────────

def _parse_header(text):
    info = {'name': '', 'phone': '', 'location': '', 'email': '', 'linkedin': ''}

    center = re.search(
        r'\\begin\{center\}(.*?)\\end\{center\}', text, re.DOTALL,
    )
    if not center:
        return info
    content = center.group(1)

    # Name
    name_m = re.search(r'\\scshape\s+(.*?)\}', content)
    if name_m:
        info['name'] = name_m.group(1).strip()

    # Contact parts (separated by $|$)
    contact_part = content.split('\\\\', 1)[-1] if '\\\\' in content else content
    for part in contact_part.split('$|$'):
        raw = part.strip()
        cleaned = _clean(raw)

        if re.search(r'[+]?\d[\d\s\-]{6,}', cleaned):
            info['phone'] = cleaned
        elif 'linkedin' in raw.lower():
            m = re.search(r'\\href\{[^}]*\}\{([^}]*)\}', raw)
            info['linkedin'] = m.group(1).strip() if m else cleaned
        elif 'mailto' in raw or '@' in cleaned:
            m = re.search(r'\\href\{mailto:([^}]*)\}', raw)
            info['email'] = m.group(1).strip() if m else cleaned
        elif cleaned and not cleaned.startswith('\\'):
            info['location'] = cleaned

    return info


def _parse_summary(text):
    text = re.sub(r'\\section\{Summary\}', '', text)
    # Strip LaTeX comments
    text = re.sub(r'%[^\n]*', '', text).strip()
    # The summary is wrapped in {braces}; extract the content properly
    if text.startswith('{'):
        args = _extract_braced(text, 1)
        if args:
            return _clean(args[0])
    return _clean(text)


def _parse_experience(text):
    entries = []
    for i, part in enumerate(
        re.split(r'\\resumeSubheading\s*\n?', text)[1:], 1,
    ):
        args = _extract_braced(part, 4)
        if len(args) < 4:
            continue
        # Experience args: {title}{period}{company}{location}
        entries.append({
            'title': _clean(args[0]),
            'period': _clean(args[1]),
            'company': _clean(args[2]),
            'location': _clean(args[3]),
            'image_index': i,
            'responsibilities': _extract_items(part),
        })
    return entries


def _parse_education(text):
    entries = []
    for i, part in enumerate(
        re.split(r'\\resumeSubheading\s*\n?', text)[1:], 1,
    ):
        args = _extract_braced(part, 4)
        if len(args) < 4:
            continue
        # Education args: {institution}{location}{degree}{period}
        entries.append({
            'institution': _clean(args[0]),
            'location': _clean(args[1]),
            'degree': _clean(args[2]),
            'period': _clean(args[3]),
            'image_index': i,
            'details': _extract_items(part),
        })
    return entries


def _parse_portfolios(text):
    portfolios = {}
    for m in re.finditer(
        r'\\textbf\{([^}]+?):\}\s*\\href\{([^}]*)\}\{([^}]*)\}', text,
    ):
        label = _clean(m.group(1))
        display = m.group(3).strip()
        portfolios[label] = display
    return portfolios


# ── Public API ─────────────────────────────────────────────────────────────

def parse_resume(filepath):
    """Parse a LaTeX resume and return structured data.

    Returns a dict with keys:
        personal_info  – dict (name, phone, location, email, linkedin, summary)
        experience     – list of dicts
        education      – list of dicts
        portfolios     – dict {label: display_url}
    """
    raw = Path(filepath).read_text()

    body_m = re.search(
        r'\\begin\{document\}(.*?)\\end\{document\}', raw, re.DOTALL,
    )
    if not body_m:
        raise ValueError(f'No \\begin{{document}} found in {filepath}')
    body = body_m.group(1)

    header, sections = _split_sections(body)

    personal_info = _parse_header(header)
    personal_info['summary'] = (
        _parse_summary(sections['Summary']) if 'Summary' in sections else ''
    )

    return {
        'personal_info': personal_info,
        'experience': _parse_experience(sections.get('Experience', '')),
        'education': _parse_education(sections.get('Education', '')),
        'portfolios': _parse_portfolios(sections.get('Portfolios', '')),
    }
