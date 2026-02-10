"""This script checks for required dependencies.

If they are met, it generates a plot of random data.
"""
import sys

try:
    print("\nLOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")
    import pandas as pd
    print(f"[OK] pandas ({pd.__version__}) - Data manipulation ready")
    import matplotlib.pyplot as plt
    print(f"[OK] matplotlib "
          f"({plt.matplotlib.__version__}) - Visualization ready")
    import requests as rq
    print(f"[OK] requests ({rq.__version__}) - Network access ready")
    import numpy as np
    print(f"[OK] numpy ({np.__version__}) "
          f"- Numeric data manipulation ready\n")

except ImportError as e:
    print(f"Error module not imported: {e}")
    print("To ensure requirements with pip"
          "install requirements: pip install -r requirements.txt")
    print("More easy is use Poetry:\n pip install poetry")
    print("After just use <poetry install> "
          "it will install the dependencies in a venv")
    sys.exit(1)


if __name__ == "__main__":
    print("Analyzing Matrix Data...")
    data = np.random.randn(1000)
    print("Processing 1000 data points...")
    array_data = pd.DataFrame(data, columns=["Signal"])
    plt.plot(array_data)
    plt.savefig("matrix_analysis.png")
    print("Generating visualization...\n")

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")
