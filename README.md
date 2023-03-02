# SEML - Somewhat Easier YAML

This is a YAML variant created so that I wouldn't have to read the voluminous YAML spec.
Every SEML document should also be valid YAML, but not the reverse.

A SEML file corresponds to a JSON value. To avoid the
[Norway problem](https://hitchdev.com/strictyaml/why/implicit-typing-removed/) and similar issues,
all leaf values are parsed as strings.

This is version 1.0 of the SEML spec.

## Grammar

```
ALNUM   := Unicode alpha, Unicode digit, underscore, dash
CHAR    := Everything except '\n'
WHITE   := ' '*
KEY     := ALNUM+
VALUE   := CHAR+
INDENT  := WHITE*
OBJECT_ENTRY := KEY ':' VALUE?
ARRAY_ENTRY  := '-' VALUE?
EMPTY_LINE   :=
COMMENT      := '#' VALUE?
LINE    := INDENT (OBJECT_ENTRY | ARRAY_ENTRY | EMPTY_LINE | COMMENT) '\n'
SEML    := LINE*
```

## Parsing

Split the file into lines. Discard empty lines and comments.

Each line has an indentation, which is the number of spaces in front.
The first line must have an indentation of 0.

Array entries are considered indented by one greater than the number of spaces.
This is to allow array entries with the same indentation as the object key they are a part of.

The value of a SEML file is the parsing operation applied to the file. This operation will
exhaust the available lines.

### The parsing operation

The parsing operation may recurse. As such, it may be parameterized with a minimum indentation.
It consumes lines from the input text and returns a list of entries, with a length of at least one.
Either all entries are object entries, or all are array entries; else it is an error.

The first line's indentation is the expected indentation. It must be **greater** than the minimum indentation,
if one is passed.

Any line that has indentation greater than expected is an error.

Repeat while the current line's indentation is equal to the expected indentation:

- If the current element has a value, remove whitespace from the front and back of the value and
add the element to the list to be returned.

- If the current element is an array element without a value, recurse with the expected indentation.
Add an array of the returned elements to the returned list.

- If the current element is an object element without a value, recurse with the expected indentation.
Add an object element with the current element's key and an object of the returned elements to the returned list.

## Example:

```
foo:
  bar: baz
  whee:
  - 1
  # 1 was too small.
  - 2
  -
    key: value
```

This is parsed as the JSON object:

```
{
  "foo": {
    "bar": "baz",
    "whee": [
      "1",
      "2",
      {
        "key": "value"
      }
    ]
  }
}
```