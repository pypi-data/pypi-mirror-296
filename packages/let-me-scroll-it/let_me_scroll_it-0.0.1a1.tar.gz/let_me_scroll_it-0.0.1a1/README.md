Let Me Scroll It (lmsi)
=======================

`lmsi` is a command-line utility that produces a html web-page.
This web-page contains the images you provide the command-line
utility.

You can configure sections, titles for plots, and captions,
using the JSON configuration file of the form:

```json
{
  "Section Name": {
    "[0-9]*_.*png": {
      "caption": "A figure selected using regex.",
      "title": "Regex Selection",
      "regex": true
    },
    "no_regex_required.png": {
      "caption": "No regex requried for this, just searched on the filename",
      "title": "Fixed Name Selection"
    }
  }
}
```

You can use regex here or just a plain string. If you want the string to be
interpreted as a regular expression, you must use the
`"regex": true` option.

There is an example in the `example` directory.

You can use the utility as follows:

```
lmsi --files *.png --output index.html --config /path/to/config.json
```

Using `lmsi` without a config leads to all figures being
placed in the 'uncategorised' section.