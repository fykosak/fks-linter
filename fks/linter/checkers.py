from fks.linter import Event

class LineLength:
    def __init__(self, linter, parser, max_len):
        self.linter = linter
        self.max_len = max_len

        parser.register(Event.LineEnd, self.line_end)

    def line_end(self, event):
        if event.context.colno > self.max_len:
            self.linter.l(event.context, \
              "Line exceeds {} characters limit.".format( \
              self.max_len))

class EqIndentation:
    def __init__(self, linter, parser, indent):
        self.linter = linter
        self.indent = indent

        self.expect = False
        self.depth = None
        self.equation = False

        parser.register(Event.Macro, self.macro)
        parser.register(Event.GroupBegin, self.group_begin)
        parser.register(Event.GroupEnd, self.group_end)
        parser.register(Event.TextBegin, self.text_begin)

    def macro(self, event):
        if event.args[0] == 'eq':
            self.expect = True

    def group_begin(self, event):
        if not self.expect:
            return
        self.expect = False

        self.depth = event.args[0]
        self.equation = True

    def group_end(self, event):
        if self.depth != event.args[0]:
            return

        self.depth = None
        self.equation = False

    def text_begin(self, event):
        if not self.equation:
            return

        if not event.args[0].startswith(self.indent):
            self.linter.l(event.context, "Wrong equation indentation.")
        
# XXX Such checker would be much easier written as regular expression
#     (However, this takes comment into account too.)
class TrailingWhitespace:
    def __init__(self, linter, parser):
        self.linter = linter

        parser.register(Event.TextEnd, self.text_end)

    def text_end(self, event):
        text = event.args[0]
        if len(text) == 0:
            return

        if text[-1].isspace():
            self.linter.l(event.context, "Trailing whitespace.")
        
class ForbiddenMacros:
    # accepts a list of pairs (forbidden macro, replacement)
    def __init__(self, linter, parser, macros):
        self.linter = linter
        self.macros = macros

        parser.register(Event.Macro, self.macro)

    def match(self, pattern, text):
        for p in range(3):
            if text[p] is None:
                return (pattern[p] is None)
            elif pattern[p] and pattern[p].fullmatch(text[p]) == None:
                return False
        return True

    def macro(self, event):
        for macro in self.macros:
            if self.match(macro[0], event.args):
                self.linter.l(event.context, \
                  "Forbidden macro {}, use {} instead.".format( \
                  event.to_string(macro[0]), macro[1]))


