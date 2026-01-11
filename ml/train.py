import pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

from data import load_data
from models import naive_bayes, logistic_regression, random_forest

def _stratify_target(y: pd.Series) -> pd.Series | None:
    class_counts = y.value_counts()
    if (class_counts < 2).any():
        return None
    return y

def _evaluate_model(name: str, model, X_train, X_test, y_train, y_test) -> float:
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    score = f1_score(y_test, predictions, average="weighted")
    print(f"{name} F1 Score: {score}")
    return score

def main() -> None:
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=_stratify_target(y),
    )
    models = {
        "Naive Bayes": naive_bayes(),
        "Logistic Regression": logistic_regression(),
        "Random Forest": random_forest(),
    }
    for name, model in models.items():
        _evaluate_model(name, model, X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main()

# Naive Bayes F1 Score: 0.7342055198289412
# Logistic Regression F1 Score: 0.7173927345064577
# Random Forest F1 Score: 0.7525009070941633