import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

# Check files
print(os.listdir(r"C:\Users\Sandh\OneDrive\Desktop\Snack Recommender"))

# Load dataset with comments
data = pd.read_csv(r"C:\Users\Sandh\OneDrive\Desktop\Snack Recommender\snacks.csv")
data.columns = data.columns.str.strip()
data["mood"] = data["mood"].str.strip().str.lower()
data["time"] = data["time"].str.strip().str.lower()
data["snack"] = data["snack"].str.strip()
data["comment"] = data["comment"].str.strip()

# Encode categorical columns
le_mood = LabelEncoder()
le_time = LabelEncoder()
le_snack = LabelEncoder()

data["mood_enc"] = le_mood.fit_transform(data["mood"])
data["time_enc"] = le_time.fit_transform(data["time"])
data["snack_enc"] = le_snack.fit_transform(data["snack"])

# Features and target
X = data[["mood_enc", "time_enc"]]
y = data["snack_enc"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save everything
joblib.dump(model, "snack_model.pkl")
joblib.dump(le_mood, "le_mood.pkl")
joblib.dump(le_time, "le_time.pkl")
joblib.dump(le_snack, "le_snack.pkl")

# Save a dictionary for comments
snack_comment_dict = dict(zip(data["snack"], data["comment"]))
joblib.dump(snack_comment_dict, "snack_comment.pkl")

print("Model, encoders, and comments saved!")