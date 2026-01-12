import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split

from data import load_data
import train

def main() -> None:
    trained_models = train.main()
    model_order = ["Naive Bayes", "Logistic Regression", "Random Forest"]
    models = {name: trained_models[name] for name in model_order if name in trained_models}

    X, y = load_data()
    labels = sorted(y.unique())
    _, X_test, _, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=train.stratify_target(y),
    )

    fig, axes = plt.subplots(1, len(models), figsize=(5 * len(models), 4))
    if len(models) == 1:
        axes = [axes]

    for ax, (name, model) in zip(axes, models.items()):
        predictions = model.predict(X_test)
        matrix = confusion_matrix(y_test, predictions, labels=labels)
        print(f"{name} confusion matrix:")
        print(matrix)
        display = ConfusionMatrixDisplay(matrix, display_labels=labels)
        display.plot(ax=ax, cmap="Blues", colorbar=False)
        ax.set_title(name.replace("_", " ").title())

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
