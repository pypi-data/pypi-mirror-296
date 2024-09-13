# TextLoop

A Reflex custom component for looping text based on [easy-react-text-loop](https://www.npmjs.com/package/easy-react-text-loop) React component.

## Installation

### PIP

```bash
pip install reflex-text-loop
```

### Poetry

```bash
poetry add reflex-text-loop
```

## Usage

### Props

| Name | Type | Default | Description |
|--|--|--|--|
| `animation` | `string` | `tween` | One of `tween`, `spring`, `inertia`, `keyframes`, `just` |
| `timeout` | `number` | `2500` | Animation timout in `ms` |
| `text` | `string` | None | Comma separated words which will be used in animation |

## Sample

```python
from reflex_text_loop import TextLoop

def index():
    rx.text(
        TextLoop(
            "Un", "Dros", "Tres"
        )
    )
```