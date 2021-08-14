from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

blue = "#1ca3ff"
lightBlue = "#7fc5ff"
darkMagenta = "#f50f6f"
greenYellow = "#b1da00"
fireRed = "#ff5e4a"
gray = "#9a9a9a"
lightPurple = "#8845ca"

def format(color, style=''):
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'black' in style:
        _format.setFont(QFont("Tajawal Black"))
    if 'bold' in style:
        _format.setFontWeight(QFont.Weight.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format

STYLES = {
    'library': format(lightPurple, 'black'),
    'keyword': format(blue, 'bold'),
    'operator': format(lightBlue),
    'brace': format(gray),
    'string': format(greenYellow),
    'comment': format(gray),
    'numbers': format(fireRed),
    'injlang': format(darkMagenta, 'italic')
}


class PythonHighlighter(QSyntaxHighlighter):
    library = [
        'ألف', 'مكتبة', 'نص'
    ]

    keywords = [
        'صنف', 'كائن', 'دالة', 'إذا', 'أو', 'وإلا', 'و', 'عدد', 'نص', 'اطبع',
        'نافذة', 'كلما', 'نهاية', 'رئيسية', 'إرجاع'
    ]

    operators = [
        '=',

        '==', '!=', '<', '<=', '>', '>=',

        '\+', '-', '\*', '/', '//', '\%', '\*\*',

        '\+=', '-=', '\*=', '/=', '\%=',

        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    injlang = [
        '_ج_', '_ب_', '_س_'
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        rules += [
            (r' [^ء-ي ]*[+-]?[0-9]+|^[+-]?[0-9]+', 0, STYLES['numbers']),
            (r' [^ء-ي ]*[+-]?[٠-٩]+|^[+-]?[٠-٩]+', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+\b', 0, STYLES['numbers']),
        ]

        rules += [('#%s($|[^\u0621-\u064A[^0-9]]*)' % l, 0, STYLES['library'])
                  for l in PythonHighlighter.library]
        rules += [('(^%(0)s|[\t| ]+%(0)s)($|[^\u0621-\u064A[^0-9]]*)' % {'0': w}, 0, STYLES['keyword'])
                  for w in PythonHighlighter.keywords]
        rules += [('%s' % o, 0, STYLES['operator'])
                  for o in PythonHighlighter.operators]
        rules += [('%s' % b, 0, STYLES['brace'])
                  for b in PythonHighlighter.braces]
        rules += [('%s' % i, 0, STYLES['injlang'])
                  for i in PythonHighlighter.injlang]

        rules += [
            (r'--[^\n]*', 0, STYLES['comment']),
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
        ]

        self.rules = [(QRegularExpression(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        for expression, nth, format in self.rules:
            matched = expression.match(text, 0)

            while matched.hasMatch():
                index = matched.capturedStart(nth)
                length = len(matched.captured(nth))
                self.setFormat(index, length, format)
                matched = expression.match(text, index + length)
