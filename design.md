# SAX parsing principle

  - implicit args
    - character no
    - line no
    - character no on line
    - current line

  -  high-level arg
    - in math mode

# events #

  - macro-begin(name)
  - macro-end(name)
  - line-begin
  - line-end
  - comment-begin
  - comment-end

# checkers #
  - line length
  - eq is indented
  - whitespace at end of line
  - sentence begins on new line?
  - eq is part of sentence
