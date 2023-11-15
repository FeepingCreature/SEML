# SEML - Somewhat Easier YAML

This is a YAML variant created so that I wouldn't have to read the voluminous YAML spec.
Every SEML document should also be valid YAML, but not the reverse.

A SEML file corresponds to a JSON value. To avoid the
[Norway problem](https://hitchdev.com/strictyaml/why/implicit-typing-removed/) and similar issues,
all leaf values are parsed as strings.

This is version 1.0 of the SEML spec.

## Why SEML

YAML is designed to be human readable and easy to edit, but the spec is very large.
My contention is that 10% of the implementation effort will give you 80% of the readability.

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

The value of a SEML file is the parse operation applied to the file. This operation will
exhaust the available lines.

### The parse operation

The parsing operation may recurse. As such, it may be parameterized with a minimum indentation.
It consumes lines from the input text and returns a value, which is formed by interpreting
a list of entries.

The first line's indentation is the expected indentation. It must be **greater** than the minimum indentation,
if one is passed.

Any line that has indentation greater than expected is an error.

Repeat while the current line's indentation is equal to the expected indentation:

- If the current entry has a value, remove whitespace from the front and back of the value and
add the entry to the list.

- If the current entry is an array entry without a value, recurse with the expected indentation.
Add an array entry of the returned value to the list.

- If the current entry is an object entry without a value, recurse with the expected indentation.
Add an object entry with the current entry's key and the returned value to the list.

- Interpret the list and return the result.

### The interpret operation

A list of entries may be interpreted as an object or an array value:

- if it consists of one or more object entries, it is an object value

- if it consists of one or more array entries, it is an array value

- else it is an error.

## Example

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

## How to do multiline strings

YAML Multiline strings are very useful, but they would complicate the parser somewhat. I'm trying to
ensure that every line can be parsed without requiring context.

So my recommendation is to just use an array:

```
text:
- This is a
- multiline string.
```
