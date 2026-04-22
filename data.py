import numpy as np
import pandas as pd
from N_Tools import as_col

COLS_TO_KEEP = 4 # If we set this to a different number it would minorly break things
df = pd.read_csv("breast_cancer_sklearn.csv")
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
colnames = list(df_shuffled.columns[0:COLS_TO_KEEP])
X = np.array(df_shuffled[colnames])
y = np.array(df_shuffled["target"])
yX = np.hstack([as_col(y.astype(X.dtype)), X])
