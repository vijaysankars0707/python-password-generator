# Task 3 - Secure Random Password Generator

## Run
```bash
python -m pip install -r requirements.txt
python password_generator.py
```

## Features
- Minimum length of 8
- Uppercase/lowercase/numbers/symbols
- At least two character types required
- Secure `secrets` generation
- Guaranteed character from every selected type
- Strength indicator
- Automatic clipboard copy
- Optional ambiguous-character exclusion
- Last five generated passwords retained only in session memory

The Python `secrets` module is used instead of `random` because it is intended for cryptographically strong random values suitable for passwords and other secrets.

**Security note:** The history is intentionally not saved to a file. Treat generated passwords as sensitive information.
