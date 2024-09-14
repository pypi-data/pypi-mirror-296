# anansi
`anansi` (`ANother ANSI`) is yet antoher python library for ANSI escape characters. The name "anansi" was inspired by the Akan folktale character Anansi.

# Install
```bash
python3 -m pip install py-anansi --upgrade
```

# Usage

## Colors
```python
from anansi.font.colors import background as bg
from anansi.font.colors import foreground as fg

print(fg.red+bg.blue + "Hello" + bg.off + " World!" + fg.off)
```

## Effects
```python
from anansi.font import effects as eff

print(eff.underline + "Hello" + eff.underline_off+eff.blink + " World!" + eff.blink_off)
```

# License
MIT
