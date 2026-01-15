import joblib
from pathlib import Path

from data import load_data
from models import gradient_boosting


def main() -> None:
    X, y = load_data()
    model = gradient_boosting()
    model.fit(X, y)

    models_dir = Path("backend/models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "model.pkl"
    joblib.dump(model, model_path)
    print(f"Saved model to {model_path}")


if __name__ == "__main__":
    main()
