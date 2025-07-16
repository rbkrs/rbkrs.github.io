#!/usr/bin/env python3
"""
Model Analyzer - Extract and analyze machine learning models from Jupyter notebooks

This script parses Jupyter notebook files (.ipynb) and optionally HTML exports
to detect model training, evaluation, and provide analysis recommendations.
"""

import json
import re
import ast
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from bs4 import BeautifulSoup
import nbformat


@dataclass
class ModelInfo:
    """Information about a detected model"""
    model_type: str
    hyperparameters: Dict[str, Any]
    cell_index: int
    source_code: str
    line_number: int = 0


@dataclass
class DatasetInfo:
    """Information about detected datasets"""
    name: str
    shape: Optional[Tuple[int, ...]]
    description: str
    cell_index: int


@dataclass
class AnalysisResult:
    """Complete analysis results"""
    models: List[ModelInfo]
    datasets: List[DatasetInfo]
    training_cells: List[int]
    evaluation_cells: List[int]
    recommendations: List[str]
    warnings: List[str]


class ModelAnalyzer:
    """Main analyzer class for extracting model information from notebooks"""
    
    def __init__(self):
        # Common model patterns to detect
        self.model_patterns = {
            'sklearn': [
                r'LinearRegression\s*\(',
                r'LogisticRegression\s*\(',
                r'RandomForestRegressor\s*\(',
                r'RandomForestClassifier\s*\(',
                r'SVC\s*\(',
                r'SVR\s*\(',
                r'GradientBoostingRegressor\s*\(',
                r'GradientBoostingClassifier\s*\(',
                r'DecisionTreeRegressor\s*\(',
                r'DecisionTreeClassifier\s*\(',
                r'KNeighborsRegressor\s*\(',
                r'KNeighborsClassifier\s*\(',
                r'MLPRegressor\s*\(',
                r'MLPClassifier\s*\(',
            ],
            'xgboost': [
                r'XGBRegressor\s*\(',
                r'XGBClassifier\s*\(',
                r'xgb\.train\s*\(',
            ],
            'lightgbm': [
                r'LGBMRegressor\s*\(',
                r'LGBMClassifier\s*\(',
                r'lgb\.train\s*\(',
            ],
            'tensorflow': [
                r'tf\.keras\.models\.Sequential\s*\(',
                r'keras\.models\.Sequential\s*\(',
                r'tf\.keras\.Model\s*\(',
                r'Model\s*\(',
            ],
            'pytorch': [
                r'torch\.nn\.Module',
                r'nn\.Module',
                r'torch\.nn\.Linear\s*\(',
                r'nn\.Linear\s*\(',
            ]
        }
        
        # Training method patterns
        self.training_patterns = [
            r'\.fit\s*\(',
            r'\.train\s*\(',
            r'model\.compile\s*\(',
            r'\.fit_generator\s*\(',
        ]
        
        # Evaluation method patterns
        self.evaluation_patterns = [
            r'\.predict\s*\(',
            r'\.score\s*\(',
            r'\.evaluate\s*\(',
            r'\.predict_proba\s*\(',
            r'cross_val_score\s*\(',
            r'train_test_split\s*\(',
            r'accuracy_score\s*\(',
            r'mean_squared_error\s*\(',
            r'classification_report\s*\(',
            r'confusion_matrix\s*\(',
        ]
        
        # Dataset patterns
        self.dataset_patterns = [
            r'pd\.read_csv\s*\(',
            r'pd\.read_excel\s*\(',
            r'load_iris\s*\(',
            r'load_boston\s*\(',
            r'load_diabetes\s*\(',
            r'load_wine\s*\(',
            r'load_breast_cancer\s*\(',
            r'make_classification\s*\(',
            r'make_regression\s*\(',
        ]

    def parse_notebook(self, notebook_path: str) -> AnalysisResult:
        """Parse a Jupyter notebook file and extract model information"""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = nbformat.read(f, as_version=4)
        except Exception as e:
            raise ValueError(f"Failed to parse notebook: {e}")
        
        models = []
        datasets = []
        training_cells = []
        evaluation_cells = []
        
        # Analyze each code cell
        for cell_idx, cell in enumerate(notebook.cells):
            if cell.cell_type == 'code':
                source = cell.source
                
                # Check for training patterns
                if self._contains_training_code(source):
                    training_cells.append(cell_idx)
                
                # Check for evaluation patterns
                if self._contains_evaluation_code(source):
                    evaluation_cells.append(cell_idx)
                
                # Extract model information
                cell_models = self._extract_models_from_cell(source, cell_idx)
                models.extend(cell_models)
                
                # Extract dataset information
                cell_datasets = self._extract_datasets_from_cell(source, cell_idx)
                datasets.extend(cell_datasets)
        
        # Generate recommendations and warnings
        recommendations = self._generate_recommendations(models, datasets)
        warnings = self._generate_warnings(models, datasets)
        
        return AnalysisResult(
            models=models,
            datasets=datasets,
            training_cells=training_cells,
            evaluation_cells=evaluation_cells,
            recommendations=recommendations,
            warnings=warnings
        )

    def parse_html(self, html_path: str) -> AnalysisResult:
        """Parse HTML export of Jupyter notebook"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
        except Exception as e:
            raise ValueError(f"Failed to parse HTML: {e}")
        
        models = []
        datasets = []
        training_cells = []
        evaluation_cells = []
        
        # Find code cells in HTML
        code_cells = soup.find_all('div', class_='highlight')
        
        for cell_idx, cell in enumerate(code_cells):
            source = cell.get_text()
            
            # Check for training patterns
            if self._contains_training_code(source):
                training_cells.append(cell_idx)
            
            # Check for evaluation patterns
            if self._contains_evaluation_code(source):
                evaluation_cells.append(cell_idx)
            
            # Extract model information
            cell_models = self._extract_models_from_cell(source, cell_idx)
            models.extend(cell_models)
            
            # Extract dataset information
            cell_datasets = self._extract_datasets_from_cell(source, cell_idx)
            datasets.extend(cell_datasets)
        
        # Generate recommendations and warnings
        recommendations = self._generate_recommendations(models, datasets)
        warnings = self._generate_warnings(models, datasets)
        
        return AnalysisResult(
            models=models,
            datasets=datasets,
            training_cells=training_cells,
            evaluation_cells=evaluation_cells,
            recommendations=recommendations,
            warnings=warnings
        )

    def _contains_training_code(self, source: str) -> bool:
        """Check if cell contains model training code"""
        return any(re.search(pattern, source, re.IGNORECASE) 
                  for pattern in self.training_patterns)

    def _contains_evaluation_code(self, source: str) -> bool:
        """Check if cell contains model evaluation code"""
        return any(re.search(pattern, source, re.IGNORECASE) 
                  for pattern in self.evaluation_patterns)

    def _extract_models_from_cell(self, source: str, cell_idx: int) -> List[ModelInfo]:
        """Extract model information from a code cell"""
        models = []
        
        for framework, patterns in self.model_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, source, re.IGNORECASE)
                for match in matches:
                    model_type = self._extract_model_type(match.group())
                    hyperparams = self._extract_hyperparameters(source, match.start())
                    
                    models.append(ModelInfo(
                        model_type=model_type,
                        hyperparameters=hyperparams,
                        cell_index=cell_idx,
                        source_code=source[max(0, match.start()-50):match.end()+50],
                        line_number=source[:match.start()].count('\n') + 1
                    ))
        
        return models

    def _extract_datasets_from_cell(self, source: str, cell_idx: int) -> List[DatasetInfo]:
        """Extract dataset information from a code cell"""
        datasets = []
        
        for pattern in self.dataset_patterns:
            matches = re.finditer(pattern, source, re.IGNORECASE)
            for match in matches:
                dataset_name = self._extract_dataset_name(source, match)
                shape = self._extract_dataset_shape(source, match.start())
                
                datasets.append(DatasetInfo(
                    name=dataset_name,
                    shape=shape,
                    description=f"Dataset loaded in cell {cell_idx}",
                    cell_index=cell_idx
                ))
        
        return datasets

    def _extract_model_type(self, match_text: str) -> str:
        """Extract clean model type name from match"""
        return re.sub(r'\s*\(.*', '', match_text.strip())

    def _extract_hyperparameters(self, source: str, start_pos: int) -> Dict[str, Any]:
        """Extract hyperparameters from model instantiation"""
        hyperparams = {}
        
        # Find the parentheses containing parameters
        paren_start = source.find('(', start_pos)
        if paren_start == -1:
            return hyperparams
        
        # Find matching closing parenthesis
        paren_count = 1
        paren_end = paren_start + 1
        while paren_end < len(source) and paren_count > 0:
            if source[paren_end] == '(':
                paren_count += 1
            elif source[paren_end] == ')':
                paren_count -= 1
            paren_end += 1
        
        if paren_count == 0:
            params_text = source[paren_start+1:paren_end-1]
            hyperparams = self._parse_parameters(params_text)
        
        return hyperparams

    def _parse_parameters(self, params_text: str) -> Dict[str, Any]:
        """Parse parameter string into dictionary"""
        hyperparams = {}
        
        # Simple parameter parsing (could be enhanced)
        param_pairs = re.findall(r'(\w+)\s*=\s*([^,]+)', params_text)
        for param_name, param_value in param_pairs:
            try:
                # Try to evaluate as Python literal
                hyperparams[param_name] = ast.literal_eval(param_value.strip())
            except:
                # Store as string if evaluation fails
                hyperparams[param_name] = param_value.strip()
        
        return hyperparams

    def _extract_dataset_name(self, source: str, match) -> str:
        """Extract dataset name from assignment"""
        lines = source[:match.start()].split('\n')
        current_line = lines[-1] if lines else ""
        
        # Look for variable assignment
        assignment_match = re.search(r'(\w+)\s*=', current_line)
        if assignment_match:
            return assignment_match.group(1)
        
        return f"dataset_{match.start()}"

    def _extract_dataset_shape(self, source: str, start_pos: int) -> Optional[Tuple[int, ...]]:
        """Extract dataset shape if mentioned"""
        # Look for shape information in surrounding context
        context = source[start_pos:start_pos+200]
        shape_match = re.search(r'shape[:\s]*\(([^)]+)\)', context)
        if shape_match:
            try:
                shape_str = shape_match.group(1)
                return tuple(int(x.strip()) for x in shape_str.split(','))
            except:
                pass
        
        return None

    def _generate_recommendations(self, models: List[ModelInfo], datasets: List[DatasetInfo]) -> List[str]:
        """Generate recommendations based on detected models and datasets"""
        recommendations = []
        
        if not models:
            recommendations.append("No models detected. Consider adding model training code.")
            return recommendations
        
        # Check for model diversity
        model_types = set(model.model_type for model in models)
        if len(model_types) == 1:
            recommendations.append("Consider trying multiple model types for comparison.")
        
        # Check for hyperparameter tuning
        tuned_models = [m for m in models if m.hyperparameters]
        if len(tuned_models) < len(models):
            recommendations.append("Consider hyperparameter tuning for better performance.")
        
        # Check for cross-validation
        recommendations.append("Implement cross-validation for robust model evaluation.")
        
        # Dataset recommendations
        if datasets:
            recommendations.append("Consider feature engineering and data preprocessing.")
        
        return recommendations

    def _generate_warnings(self, models: List[ModelInfo], datasets: List[DatasetInfo]) -> List[str]:
        """Generate warnings about potential issues"""
        warnings = []
        
        # Check for potentially problematic models
        problematic_models = ['DecisionTreeRegressor', 'DecisionTreeClassifier']
        for model in models:
            if any(prob in model.model_type for prob in problematic_models):
                if not model.hyperparameters.get('max_depth'):
                    warnings.append(f"Decision tree without max_depth may overfit (Cell {model.cell_index})")
        
        # Check for missing validation
        if models and not any('cross_val' in str(model.source_code) for model in models):
            warnings.append("No cross-validation detected. Model may not generalize well.")
        
        return warnings

    def generate_report(self, result: AnalysisResult, output_path: str = None) -> str:
        """Generate HTML report from analysis results"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Model Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .section {{ margin: 20px 0; }}
                .model-card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; }}
                .warning {{ color: #d32f2f; }}
                .recommendation {{ color: #1976d2; }}
                .hyperparams {{ background: #f5f5f5; padding: 10px; margin: 5px 0; }}
                pre {{ background: #f5f5f5; padding: 10px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <h1>Model Analysis Report</h1>
            
            <div class="section">
                <h2>Summary</h2>
                <p>Found {len(result.models)} models across {len(result.training_cells)} training cells</p>
                <p>Detected {len(result.datasets)} datasets</p>
            </div>
            
            <div class="section">
                <h2>Detected Models</h2>
                {self._generate_models_html(result.models)}
            </div>
            
            <div class="section">
                <h2>Datasets</h2>
                {self._generate_datasets_html(result.datasets)}
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                <ul>
                    {chr(10).join(f'<li class="recommendation">{rec}</li>' for rec in result.recommendations)}
                </ul>
            </div>
            
            <div class="section">
                <h2>Warnings</h2>
                <ul>
                    {chr(10).join(f'<li class="warning">{warning}</li>' for warning in result.warnings)}
                </ul>
            </div>
        </body>
        </html>
        """
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        return html_content

    def _generate_models_html(self, models: List[ModelInfo]) -> str:
        """Generate HTML for models section"""
        if not models:
            return "<p>No models detected</p>"
        
        html = ""
        for model in models:
            hyperparams_html = ""
            if model.hyperparameters:
                hyperparams_html = f"""
                <div class="hyperparams">
                    <strong>Hyperparameters:</strong><br>
                    {chr(10).join(f'{k}: {v}' for k, v in model.hyperparameters.items())}
                </div>
                """
            
            html += f"""
            <div class="model-card">
                <h3>{model.model_type}</h3>
                <p><strong>Cell:</strong> {model.cell_index} (Line {model.line_number})</p>
                {hyperparams_html}
                <pre>{model.source_code}</pre>
            </div>
            """
        
        return html

    def _generate_datasets_html(self, datasets: List[DatasetInfo]) -> str:
        """Generate HTML for datasets section"""
        if not datasets:
            return "<p>No datasets detected</p>"
        
        html = ""
        for dataset in datasets:
            shape_info = f" (Shape: {dataset.shape})" if dataset.shape else ""
            html += f"""
            <div class="model-card">
                <h3>{dataset.name}{shape_info}</h3>
                <p><strong>Cell:</strong> {dataset.cell_index}</p>
                <p>{dataset.description}</p>
            </div>
            """
        
        return html


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='Analyze machine learning models in Jupyter notebooks')
    parser.add_argument('input_file', help='Input notebook (.ipynb) or HTML file')
    parser.add_argument('--output', '-o', help='Output HTML report file')
    parser.add_argument('--format', choices=['json', 'html'], default='html', 
                       help='Output format (default: html)')
    
    args = parser.parse_args()
    
    analyzer = ModelAnalyzer()
    
    # Determine input file type and parse accordingly
    if args.input_file.endswith('.ipynb'):
        result = analyzer.parse_notebook(args.input_file)
    elif args.input_file.endswith('.html'):
        result = analyzer.parse_html(args.input_file)
    else:
        raise ValueError("Input file must be .ipynb or .html")
    
    # Generate output
    if args.format == 'json':
        # Convert to JSON (simplified representation)
        output = {
            'models': [
                {
                    'type': m.model_type,
                    'hyperparameters': m.hyperparameters,
                    'cell': m.cell_index
                } for m in result.models
            ],
            'datasets': [
                {
                    'name': d.name,
                    'shape': d.shape,
                    'cell': d.cell_index
                } for d in result.datasets
            ],
            'recommendations': result.recommendations,
            'warnings': result.warnings
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
        else:
            print(json.dumps(output, indent=2))
    
    else:  # HTML format
        report = analyzer.generate_report(result, args.output)
        if not args.output:
            print(report)


if __name__ == "__main__":
    main()