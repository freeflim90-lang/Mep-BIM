# Contributing

Thank you for considering a contribution to this project! This repository is designed to be easy to use, extend, and improve.

## How to contribute

1. Fork the repository.
2. Create a feature branch with a descriptive name, such as `feature/add-forecasting-docs`.
3. Make your changes locally.
4. Run the project to verify behavior and outputs.
5. Open a pull request with a clear description of your changes.

## Code guidelines

- Follow Python best practices.
- Keep code readable and well-organized.
- Add or update documentation for any feature or behavior change.
- Use descriptive commit messages.

## Testing changes

Before submitting, run:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python main.py --model random_forest --forecast-horizon 72 --test-fraction 0.2
```

## Issues and feature requests

If you find a bug or want to suggest an improvement, please open an issue with:

- a short title
- reproduction steps
- expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the project `LICENSE` file.
