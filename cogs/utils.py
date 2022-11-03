import re, html2text


def cleanhtml(raw_html):
    CLEANR1 = re.compile(r'<.*?>', re.MULTILINE|re.DOTALL)
    CLEANR2 = re.compile(r'=[A-Za-z0-9]{2}')
    CLEANR3 = re.compile(r'=\s')
    cleantext = re.sub(CLEANR1, '', raw_html)
    cleantext = re.sub(CLEANR2, '', cleantext)
    cleantext = re.sub(CLEANR3, '', cleantext)
    return cleantext

def parse_pdf(text):
    part = "<" + "<".join(str(text).split("<")[1:])
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_tables = True
    h.ignore_images = True
    h.ignore_emphasis = True
    body = h.handle(part)
    body = cleanhtml(body).strip()
    return body