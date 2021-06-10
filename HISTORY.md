# Release History

## 1.2.0

### ⚠️Breaking Changes

- Add `load` and `loads` class methods to D2V class giving the ability to parse from a file or string.
- `D2V()` now expects a TextIO based object (e.g. `open(mode="rt")` or `StringIO`). You may wish to use the new
  `load` and `loads` commands instead if possible.

### Bug Fixes

- Cast flag file data as int, since it's an index to a file parsed into `D2V.videos`.

### Improvements

- Create this `HISTORY.md`, add in all previous missed releases with no history.
- Add the ability to select data from the D2V when reading from the cli `d2v` terminal command.
  E.g. `d2v vid.d2v settings.Aspect_Ratio`
- Add doc-string to cli `d2v` terminal command.
- Optimize the code that actually parses the D2V, making it more concise and readable.
- Update copyright years in the LICENSE file.

## 1.1.0

### New Features

- Once installed, `d2v` will be an available terminal command. This can be used to read or parse then read a D2V file.

### Improvements

- Replace setuptools/setup.py with Poetry for a much better dependency and package management environment.
- Delete now unnecessary bash scripts I used to use starting with v1.0.1 for setuptools usage (setuptools was annoying).
- D2V class moved from `__init__.py` to `d2v.py`. It's generally recommended for the init file to only have needed code
  on import only, it's also generally less readable at a glance where the class was. It's still imported and set in
  `__ALL__` so that `from pyd2v import D2V` is still possible.
- General improvements and to the README information and structure.

## 1.0.4

### Improvements

- Cast flag position, skip, vob, and cell data to integers.

## 1.0.3

### Bug fixes

- Add a check for the final flag, `ff` terminator. This verifies end-of-stream. It's not an actual flag, so it should
  not be parsed as one either (or even kept).

## 1.0.2

### Improvements

- Parse data info and flags at the bit-level.

## 1.0.1

### Bug fixes

- Remove int parsing on Location values; they are HEX, not int.

## 1.0.0

- Initial release.
