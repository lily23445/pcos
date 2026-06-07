import pandas as pd

# Load your cleaned dataset
df = pd.read_csv("cleaned_pcos_data.csv")  
#BMI based labelling
def label_health_category(row):
    if row["bmi"] < 18.5:
        return "underweight"
    elif row["bmi"] < 25:
        return "normal"
    else:
        return "overweight"

df["health_category"] = df.apply(label_health_category, axis=1)
df["amhng/ml"] = pd.to_numeric(df["amhng/ml"], errors="coerce")
df["amhng/ml"] = df["amhng/ml"].fillna(df["amhng/ml"].mean())


#select features (X)
selected_features = [
    "age_yrs", "weight_kg", "heightcm", "bmi",
    "tsh_miu/l", "fsh/lh", "amhng/ml", "prlng/ml",
    "waistinch", "cycle_lengthdays",
     "hair_lossy/n", "skin_darkening_y/n"
]

X = df[selected_features]
y = df["health_category"]

#Train-test split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Train the model
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)

#Evaluate performance
from sklearn.metrics import classification_report

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

#save and load the model
import joblib
joblib.dump(model, "pcos_model.pkl")
loaded_model = joblib.load("pcos_model.pkl")