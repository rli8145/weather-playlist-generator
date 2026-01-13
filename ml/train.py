from data import load_data
from models import naive_bayes, logistic_regression, random_forest, gradient_boosting

def train_models(X, y) -> dict[str, any]:
    models = {
        "Naive Bayes": naive_bayes(),
        "Logistic Regression": logistic_regression(),
        "Random Forest": random_forest(),
        "Gradient Boosting": gradient_boosting(),
    }
    trained_models = {}
    for name, model in models.items():
        model.fit(X, y)
        trained_models[name] = model
    return trained_models

def main() -> dict[str, any]:
    X, y = load_data()
    return train_models(X, y)

if __name__ == "__main__":
    main()
