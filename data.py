import numpy as np
import pandas as pd
from N_Tools import as_col

COLS_TO_KEEP = 4 # If we set this to a different number it would minorly break things
df = pd.read_csv("breast_cancer_sklearn.csv")
colnames = list(df.columns[0:COLS_TO_KEEP])
X = np.array(df[colnames])
y = np.array(df["target"])
yX = np.hstack([as_col(y.astype(X.dtype)), X])
