# Model Analyzer

A comprehensive tool for analyzing machine learning models in Jupyter notebooks. This tool can parse `.ipynb` files and HTML exports to detect models, extract hyperparameters, identify datasets, and provide recommendations for improvement.

## Features

- **Model Detection**: Identifies models from popular ML frameworks (scikit-learn, XGBoost, LightGBM, TensorFlow, PyTorch)
- **Training/Evaluation Detection**: Finds cells containing model training (`.fit()`) and evaluation (`.predict()`, `.score()`) code
- **Hyperparameter Extraction**: Extracts visible hyperparameters from model instantiation
- **Dataset Analysis**: Detects dataset loading and identifies dataset names
- **Recommendations**: Provides suggestions for model improvement
- **Warnings**: Identifies potential issues with model choices
- **Multiple Output Formats**: Generates HTML reports and JSON summaries
- **Web Interface**: GitHub Pages-ready web interface for browser-based analysis

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Analyze a Jupyter notebook
python model_analyzer.py notebook.ipynb

# Analyze an HTML export
python model_analyzer.py notebook.html

# Generate HTML report
python model_analyzer.py notebook.ipynb --output report.html

# Generate JSON output
python model_analyzer.py notebook.ipynb --format json --output analysis.json
```

### Python API

```python
from model_analyzer import ModelAnalyzer

# Create analyzer instance
analyzer = ModelAnalyzer()

# Analyze notebook
result = analyzer.parse_notebook('notebook.ipynb')

# Generate HTML report
html_report = analyzer.generate_report(result, 'report.html')

# Access analysis results
print(f"Found {len(result.models)} models")
print(f"Training cells: {result.training_cells}")
print(f"Recommendations: {result.recommendations}")
```

### Jupyter Notebook Usage

```python
# In a Jupyter notebook cell
import sys
sys.path.append('.')

from model_analyzer import ModelAnalyzer

# Analyze the current notebook
analyzer = ModelAnalyzer()
result = analyzer.parse_notebook('current_notebook.ipynb')

# Display results
print(f"Models found: {len(result.models)}")
for model in result.models:
    print(f"- {model.model_type} (Cell {model.cell_index})")
    if model.hyperparameters:
        print(f"  Hyperparameters: {model.hyperparameters}")

# Show recommendations
print("\\nRecommendations:")
for rec in result.recommendations:
    print(f"- {rec}")
```

### Web Interface

The project includes a web interface (`index.html`) that can be hosted on GitHub Pages:

1. Upload your repository to GitHub
2. Enable GitHub Pages in repository settings
3. Visit your GitHub Pages URL to access the analyzer
4. Drag and drop `.ipynb` or `.html` files to analyze them in the browser

## Detected Patterns

### Model Types
- **Scikit-learn**: LinearRegression, RandomForestRegressor, SVC, etc.
- **XGBoost**: XGBRegressor, XGBClassifier, xgb.train
- **LightGBM**: LGBMRegressor, LGBMClassifier, lgb.train
- **TensorFlow**: tf.keras.models.Sequential, tf.keras.Model
- **PyTorch**: torch.nn.Module, nn.Linear

### Training Methods
- `.fit()`, `.train()`, `.compile()`, `.fit_generator()`

### Evaluation Methods
- `.predict()`, `.score()`, `.evaluate()`, `.predict_proba()`
- `cross_val_score()`, `accuracy_score()`, `mean_squared_error()`

### Dataset Loading
- `pd.read_csv()`, `pd.read_excel()`
- `load_iris()`, `load_boston()`, `load_diabetes()`
- `make_classification()`, `make_regression()`

## Example Output

### Console Output
```
Models found: 3
- RandomForestRegressor (Cell 5)
  Hyperparameters: {'n_estimators': 100, 'max_depth': 10}
- LinearRegression (Cell 7)
- XGBRegressor (Cell 9)
  Hyperparameters: {'learning_rate': 0.1, 'n_estimators': 200}

Recommendations:
- Consider hyperparameter tuning for better performance
- Implement cross-validation for robust model evaluation
- Consider feature engineering and data preprocessing

Warnings:
- No cross-validation detected. Model may not generalize well
```

### HTML Report
The HTML report includes:
- Summary statistics (model count, dataset count, training cells)
- Detailed model cards with hyperparameters and source code
- Dataset information
- Color-coded recommendations and warnings
- Interactive tabs for easy navigation

## GitHub Pages Deployment

1. Fork or clone this repository
2. Enable GitHub Pages in your repository settings
3. Choose "Deploy from branch" and select "main" branch
4. Your analyzer will be available at `https://yourusername.github.io/model-explainer/`

## Supported File Types

- **Jupyter Notebooks** (`.ipynb`): Full parsing support with cell metadata
- **HTML Exports**: Basic parsing of code cells from exported notebooks

## Limitations

- Hyperparameter extraction works best with simple, literal values
- Complex model instantiation patterns may not be detected
- Dynamic model creation may not be captured
- HTML parsing is less accurate than native notebook parsing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.