"""
DoE Statistical Analysis Logic
Extracted from doe_analysis_gui.pyw
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from typing import Dict, List, Optional


class DoEAnalyzer:
    """Statistical analysis via regression"""

    MODEL_TYPES = {
        'linear': 'Linear (main effects only)',
        'interactions': 'Linear with 2-way interactions',
        'quadratic': 'Quadratic (interactions + squared terms)',
        'purequadratic': 'Pure quadratic (squared terms only)'
    }

    def __init__(self):
        self.data = None
        self.model = None
        self.model_type = 'linear'
        self.factor_columns = []
        self.categorical_factors = []
        self.numeric_factors = []
        self.response_column = None
        self.results = None

    def set_data(self, data: pd.DataFrame, factor_columns: List[str],
                 categorical_factors: List[str], numeric_factors: List[str],
                 response_column: str):
        """Set data and factor information"""
        self.data = data.copy()
        self.factor_columns = factor_columns
        self.categorical_factors = categorical_factors
        self.numeric_factors = numeric_factors
        self.response_column = response_column

    def _build_interaction_terms(self, factor_terms: List[str]) -> List[str]:
        """Build interaction terms for all factor combinations"""
        interactions = []
        for i in range(len(factor_terms)):
            for j in range(i + 1, len(factor_terms)):
                interactions.append(f"{factor_terms[i]}:{factor_terms[j]}")
        return interactions

    def build_formula(self, model_type: str = 'linear') -> str:
        """
        Build regression formula based on model type

        Args:
            model_type: One of 'linear', 'interactions', 'quadratic', 'purequadratic'

        Returns:
            Regression formula string for statsmodels
        """
        self.model_type = model_type

        # Prepare factor terms
        factor_terms = []
        for factor in self.factor_columns:
            if factor in self.categorical_factors:
                # C() treats as categorical, Q() quotes column names with spaces
                factor_terms.append(f"C(Q('{factor}'))")
            else:
                factor_terms.append(f"Q('{factor}')")

        # Build formula based on model type
        if model_type == 'linear':
            formula = f"Q('{self.response_column}') ~ " + " + ".join(factor_terms)

        elif model_type == 'interactions':
            main_effects = " + ".join(factor_terms)
            interactions = self._build_interaction_terms(factor_terms)
            formula = f"Q('{self.response_column}') ~ {main_effects}"
            if interactions:
                formula += " + " + " + ".join(interactions)

        elif model_type == 'quadratic':
            main_effects = " + ".join(factor_terms)
            interactions = self._build_interaction_terms(factor_terms)
            squared_terms = []
            for factor in self.numeric_factors:
                squared_terms.append(f"I(Q('{factor}')**2)")
            formula = f"Q('{self.response_column}') ~ {main_effects}"
            if interactions:
                formula += " + " + " + ".join(interactions)
            if squared_terms:
                formula += " + " + " + ".join(squared_terms)

        elif model_type == 'purequadratic':
            main_effects = " + ".join(factor_terms)
            squared_terms = []
            for factor in self.numeric_factors:
                squared_terms.append(f"I(Q('{factor}')**2)")
            formula = f"Q('{self.response_column}') ~ {main_effects}"
            if squared_terms:
                formula += " + " + " + ".join(squared_terms)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        return formula

    def fit_model(self, model_type: str = 'linear') -> Dict:
        """
        Fit regression model

        Args:
            model_type: One of 'linear', 'interactions', 'quadratic', 'purequadratic'

        Returns:
            Dict with model results
        """
        if self.data is None:
            raise ValueError("No data set")

        formula = self.build_formula(model_type)
        self.model = smf.ols(formula=formula, data=self.data).fit()
        self.results = self._extract_results()
        return self.results

    def _extract_results(self) -> Dict:
        """Extract and organize model results"""
        summary_df = pd.DataFrame({
            'Coefficient': self.model.params,
            'Std Error': self.model.bse,
            't-statistic': self.model.tvalues,
            'p-value': self.model.pvalues,
            'Significant': self.model.pvalues < 0.05
        })

        model_stats = {
            'R-squared': self.model.rsquared,
            'Adjusted R-squared': self.model.rsquared_adj,
            'RMSE': np.sqrt(self.model.mse_resid),
            'F-statistic': self.model.fvalue,
            'F p-value': self.model.f_pvalue,
            'AIC': self.model.aic,
            'BIC': self.model.bic,
            'Observations': int(self.model.nobs),
            'DF Residuals': int(self.model.df_resid),
            'DF Model': int(self.model.df_model)
        }

        return {
            'coefficients': summary_df,
            'model_stats': model_stats,
            'model_type': self.model_type,
            'formula': self.model.model.formula,
            'predictions': self.model.fittedvalues,
            'residuals': self.model.resid
        }

    def get_significant_factors(self, alpha: float = 0.05) -> List[str]:
        """Get list of significant factors"""
        if self.results is None:
            raise ValueError("No results available")

        coef_df = self.results['coefficients']
        significant = coef_df[coef_df['p-value'] < alpha]
        return [idx for idx in significant.index if idx != 'Intercept']

    def calculate_main_effects(self) -> Dict[str, pd.DataFrame]:
        """
        Calculate main effects for each factor

        Returns:
            Dict mapping factor_name → DataFrame with mean/std/count per level
        """
        if self.data is None:
            raise ValueError("No data available")

        main_effects = {}
        for factor in self.factor_columns:
            # Group by factor levels and calculate statistics
            effects = self.data.groupby(factor)[self.response_column].agg(['mean', 'std', 'count'])
            effects.columns = ['Mean Response', 'Std Dev', 'Count']
            main_effects[factor] = effects

        return main_effects

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict response for new data

        Args:
            X: DataFrame with factor columns

        Returns:
            Array of predicted response values
        """
        if self.model is None:
            raise ValueError("No model fitted")

        return self.model.predict(X)
