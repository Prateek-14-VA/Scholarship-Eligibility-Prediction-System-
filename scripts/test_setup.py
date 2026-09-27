"""
Week 1 - Day 1: Environment Setup Test
Verifies all required libraries are installed correctly.
"""

import sys
import pandas as pd
import numpy as np
import sklearn
import flask
import matplotlib
import plotly
import mysql.connector
import joblib
import openpyxl

print("=" * 55)
print("  SCHOLARSHIP ELIGIBILITY SYSTEM - SETUP VERIFICATION")
print("=" * 55)
print(f"  Python:        {sys.version.split()[0]}")
print(f"  Pandas:        {pd.__version__}")
print(f"  NumPy:         {np.__version__}")
print(f"  Scikit-learn:  {sklearn.__version__}")
print(f"  Flask:         {flask.__version__}")
print(f"  Matplotlib:    {matplotlib.__version__}")
print(f"  Plotly:        {plotly.__version__}")
print(f"  Joblib:        {joblib.__version__}")
print(f"  Openpyxl:      {openpyxl.__version__}")
print("=" * 55)
print("  ALL LIBRARIES INSTALLED SUCCESSFULLY!")
print("=" * 55)