import os
import yaml
from typing import Dict, Any, Optional


class Config:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()

    def _get_default_config_path(self) -> str:
        """Get the default path for the configuration file."""
        return os.path.join(os.path.dirname(__file__), "config.yaml")

    def _load_config(self) -> Dict[str, Any]:
        """Load the configuration from a YAML file."""
        default_config = {
            "data": {"test_size": 0.2, "random_state": 42, "validation_size": 0.2},
            "models": {
                "random_forest": {"n_estimators": 100, "random_state": 42},
                "xgboost": {
                    "n_estimators": 100,
                    "random_state": 42,
                    "learning_rate": 0.1,
                },
            },
            "evaluation": {"cv_folds": 5, "scoring": ["neg_mean_squared_error", "r2"]},
        }
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                file_config = yaml.safe_load(f)
                default_config.update(file_config)

        return default_config

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
