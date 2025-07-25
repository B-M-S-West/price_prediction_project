import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SingleImputer

from .config import Config
from .logging_cfg import get_logger

logger = get_logger(__name__)

class DataProcessor:
    """Data processing class for ML pipeline"""
    def __init__(self, config: Optional[config] = None):
        self.config = config or Config()
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        self.feature_names = {}

    def load_data(self, file_path: str, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load data from file
        
        Args:
            file_path: Path to data file
            target_column: Name of the target column

        Returns:
            Features and target data
        """
        logger.info(f"Loading data from {file_path}")

        # Determine file type and load accordingly
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format: {file_path}")
        
        def preprocess_features(self, X: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
            """
            Preprocess features including encoding and scaling.
            
            Args:
                X: Feature data
                fit: Whether to fit preprocessors
                
            Returns:
                Preprocessed features
            """
            X_processed = X.copy()

            # Handle missing values
            numeric_features = X_processed.select_dtypes(include=[np.number]).columns
            categorical_features = X_processed.select_dtypes(include=['object']).columns

            # Impute missing values
            if fit:
                # Numeric imputation
                if len(numeric_features) > 0:
                    self.imputers['numeric'] = SimpleImputer(strategy='median')
                    X_processed[numeric_features] = self.imputers['numeric'].fit_transform(
                        X_processed[numeric_features]
                    )
                
                # Categorical imputation
                if len(categorical_features) > 0:
                    self.imputers['categorical'] = SimpleImputer(strategy='most_frequent')
                    X_processed[categorical_features] = self.imputers['categorical'].fit_transform(
                        X_processed[categorical_features]
                    )
            else:
                # Transform using fitted imputers
                if 'numeric' in self.imputers and  len(numeric_features) > 0:
                    X_processed[numeric_features] = self.imputers['numeric'].transform(
                        X_processed[numeric_features]
                    )

                if 'categorical' in self.imputers and  len(categorical_features) > 0:
                    X_processed[categorical_features] = self.imputers['categorical'].transform(
                        X_processed[categorical_features]
                    )

            # Encode categorical features
            for col in categorical_features:
                if fit:
                    self.encoders[col] = LabelEncoder()
                    X_processed[col] = self.encoders[col].fit_transform(X_processed[col].astype(str))
                else:
                    if col in self.encoders:
                        # Handle unseen categories
                        unique_values = set(self.ecoders[col].classes_)
                        X_processed[col] = X_processed[col].astype(str).apply(
                            lambda x: x if x in unique_values else self.encoders[col].classes_[0]
                        )
                        X_processed[col] = self.encoders[col].transform(X_processed[col])
            
            # Scale numeric features
            if fit:
                self.scalers['features'] = StandardScaler()
                X_processed[numeric_features] = self.scalers['features'].fit_transform(
                    X_processed[numeric_features]
                )
                self.feature_names = X_processed.columns.tolist()
            else:
                if 'features' in self.scalers:
                    X_processed[numeric_features] = self.scalers['features'].transform(
                        X_processed[numeric_features]
                    )
            
            return X_processed