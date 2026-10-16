
import pickle
from pathlib import Path

# Absolute path to the project root
project_root = Path(__file__).resolve().parent.parent

# Path to the machine learning model
model_path = project_root / 'assets' / 'model.pkl'

def load_model():

    with model_path.open('rb') as file:
        model = pickle.load(file)

    return model
