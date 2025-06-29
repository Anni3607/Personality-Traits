import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import random

characters = [
    "Phil Dunphy", "Cameron Tucker", "Sheldon Cooper", "Ron Swanson", "Johan Liebert",
    "Nezuko", "Moira Rose", "Walter White", "Sherlock Holmes", "Batman",
    "Peter Griffin", "Daenerys", "Andy Dwyer", "Jethalal Gada", "Chandler Bing", "Michael Scott"
]

rows = []
for character in characters:
    for _ in range(10):
        answers = [random.randint(1, 3) for _ in range(15)]
        answers.append(character)
        rows.append(answers)

columns = [f"Q{i+1}" for i in range(15)] + ["Character"]
df = pd.DataFrame(rows, columns=columns)

X = df.drop("Character", axis=1)
y = df["Character"]

le = LabelEncoder()
y_encoded = le.fit_transform(y)

model = RandomForestClassifier()
model.fit(X, y_encoded)

joblib.dump(model, "character_predictor.pkl")
joblib.dump(le, "label_encoder.pkl")

print("✅ Model and encoder saved!")
