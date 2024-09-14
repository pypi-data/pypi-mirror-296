from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union

import pandas as pd

from examples.constants import PATH_DATA_PROCESSED

from .bivariate_analysis import BivariateAnalysis
from .feature_engineering import FeatureEngineering
from .first_glance import FirstGlance
from .univariate_analysis import UnivariateAnalysis
from .visualizations import Visualizations
from .warnings import EDAWarning, WarningSystem, get_default_warnings

# Define the type for the transformations list
TransformationType = List[Dict[str, Union[str, Dict[str, Any]]]]


class EDAToolkit:
    @staticmethod
    def save_intermediary(path: Path, interm: pd.DataFrame, fname: str):
        """
        Save an intermediary DataFrame to a CSV file.

        Parameters
        ----------
        path : Path
            The directory path where the CSV file will be saved.
        interm : pd.DataFrame
            The DataFrame to save.
        fname : str
            The file name for the CSV file (without extension).
        """
        if not path:
            raise ValueError(
                "Please make sure to specify the path in the constants file."
            )
        else:
            path_to_save = f"{path}/df_{fname}.csv"
            interm.to_csv(path_to_save, index=False)

    def __init__(
        self,
        dataframe: pd.DataFrame,
        can_be_negative: List[str],
        target_column: Optional[str] = None,
        exclusion: Optional[List[str]] = None,
        numerical_columns: Optional[List[str]] = None,
        categorical_columns: Optional[List[str]] = None,
        id_column: Optional[str] = None,
        to_be_enc: Optional[List[str]] = None,
        warning_system: Optional[WarningSystem] = None,
    ) -> None:
        """
        Initialize the EDAToolkit class with data and configuration settings.

        Parameters
        ----------
        dataframe : pd.DataFrame
            The dataset to be analyzed.
        can_be_negative : List[str]
            List of columns where negative values are permissible.
        target_column : Optional[str], optional
            The target column for analysis, by default None.
        exclusion : Optional[List[str]], optional
            List of columns to exclude from analysis, by default None.
        numerical_columns : Optional[List[str]], optional
            List of numerical columns in the data, by default None.
        categorical_columns : Optional[List[str]], optional
            List of categorical columns in the data, by default None.
        id_column : Optional[str], optional
            Column used as an identifier, by default None.
        to_be_enc : Optional[List[str]], optional
            List of columns to be encoded, by default None.
        warning_system : Optional[WarningSystem], optional
            The warning system to use, by default None.
        """
        self.dataframe = dataframe
        self.target_column = target_column or ""
        self.exclusion = exclusion or []
        self.can_be_negative = can_be_negative
        self.numerical_columns = numerical_columns or []
        self.categorical_columns = categorical_columns or []
        self.id_column = id_column or ""
        self.to_be_enc = to_be_enc or []

        # Initialize an empty list for transformations
        self.transformations: TransformationType = []

        # Initialize the warning system
        default_warning_system = get_default_warnings(
            df=self.dataframe,
            target_column=self.target_column,
            numerical_columns=self.numerical_columns,
            can_be_negative=self.can_be_negative,
            cardinality_exclusion=self.exclusion,
            id_column=self.id_column,
        )
        self.warning_system = warning_system or WarningSystem(default_warning_system)

        self.first_glance = FirstGlance(
            self.dataframe,
            self.numerical_columns,
            self.categorical_columns,
            exclusion,
            id_column,
        )

        self.visualizations = Visualizations(
            self.dataframe,
            self.target_column,
            self.numerical_columns,
            self.categorical_columns,
        )
        self.univariate_analysis = UnivariateAnalysis(
            self.dataframe, self.target_column, self.numerical_columns
        )
        self.bivariate_analysis = BivariateAnalysis(
            self.dataframe, self.numerical_columns
        )
        self.feature_engineering = FeatureEngineering(
            self.dataframe,
            self.target_column,
            self.numerical_columns,
            self.categorical_columns,
            self.to_be_enc,
            self.transformations,
        )

    def get_transformations(
        self, unwanted_features: Optional[List] = None
    ) -> TransformationType:
        """
        Get the list of transformations applied to the data.

        Parameters
        ----------
        unwanted_features : Optional[List], optional
            List of features to exclude from the transformations, by default None.

        Returns
        -------
        TransformationType
            A list of transformations.
        """
        if unwanted_features:
            for unwanted_feature in unwanted_features:
                self.transformations = [
                    transform
                    for transform in self.transformations
                    if transform["feature"] != unwanted_feature
                ]
        return self.transformations

    def register_custom_warning(self, name: str, warning_obj: EDAWarning):
        """
        Register a custom warning function.

        Parameters
        ----------
        name : str
            The name of the custom warning.
        func : WarningFunction
            The warning function to register.
        """
        self.warning_system.register_warning(name, warning_obj)

    def print_warnings(self):
        """
        Print all warnings for the dataset.
        """
        warnings = self.warning_system.run_warnings()

        for warning_name, warning_list in warnings.items():
            if warning_list:
                print(f"\n{warning_name.replace('_', ' ').title()} Warnings:")
                print("-" * 50)

                # Group warnings by type
                grouped_warnings = {}
                for warning in warning_list:
                    warning_type = warning["warning_type"]
                    if warning_type not in grouped_warnings:
                        grouped_warnings[warning_type] = []
                    grouped_warnings[warning_type].append(warning["message"])

                for warning_type, messages in grouped_warnings.items():
                    print(f"{warning_type}:")
                    if len(messages) == 1 and ":" in messages[0]:
                        # For warnings with a single message containing a colon (like missing values)
                        header, values = messages[0].split(":", 1)
                        print(header.strip() + ":")
                        for item in values.strip().split(","):
                            print(f"  {item.strip()}")
                    else:
                        # For other types of warnings
                        for message in messages:
                            print(f"  {message}")
                    print("-" * 50)

    def perform_checks(self):
        """
        Perform exploratory data analysis on the dataset.
        """
        self.first_glance.super_vision()
        self.first_glance.check_duplicates()

    def plot_target_evolution(self):
        """
        Plot the target balance and evolution over time.
        """
        self.visualizations.plot_target_balance()
        self.visualizations.plot_target_evolution("scheduled_at", "min_balance_3m")

    def plot_numerical_distributions(self, sub_plots: bool = False):
        """
        Plot distributions of numerical columns.

        Parameters
        ----------
        sub_plots : bool, optional
            If True, create subplots for each distribution, by default False.
        """
        self.univariate_analysis.plot_distributions(
            self.numerical_columns, grouped=sub_plots
        )

    def plot_categorical_cardinalities(self):
        """
        Plot cardinalities of categorical columns.
        """
        self.visualizations.plot_categorical_value_counts()
        self.visualizations.visualize_high_cardinality(
            excluded_vars=self.exclusion, id_column=self.id_column
        )
        self.visualizations.visualize_low_cardinality()

    def plot_bivariate_numnum(self, columns: Optional[List[str]] = None):
        """
        Plot bivariate analysis for numerical-numerical column pairs.

        Parameters
        ----------
        columns : List[str], optional
            List of columns to include in the analysis, by default all numerical columns.
        """
        if columns is None:
            columns = []
        self.bivariate_analysis.generate_correlation_heatmap(columns)

    def plot_vif(self):
        """
        Plot Variance Inflation Factor (VIF) for numerical columns.
        """
        self.visualizations.plot_vif_failsafe()

    def plot_numerical_repartitioning(
        self, number_of_partitions: int, time_column: str
    ):
        """
        Plot numerical feature repartitioning over time.

        Parameters
        ----------
        number_of_partitions : int
            Number of partitions to use for binning.
        time_column : str
            Name of the time column.
        """
        self.univariate_analysis.get_num_feature_repartition(
            time_column, number_of_partitions
        )

    def print_psi(
        self,
        buckets: int,
        bucket_type: Literal["quantile", "fixed_width"],
        time_column: str,
        time_expected: Union[str, datetime, date],
        end_date: Union[str, datetime, date],
        start_date: Union[str, datetime, date],
        test_data: Optional[pd.DataFrame] = None,
    ):
        """
        Print Population Stability Index (PSI) for numerical features.

        Parameters
        ----------
        buckets : int
            Number of buckets for binning.
        bucket_type : Literal["quantile", "fixed_width"]
            The type of binning to use.
        time_column : str
            Name of the time column.
        time_expected : Union[str, datetime, date]
            Expected time for PSI calculation.
        end_date : Union[str, datetime, date]
            End date for PSI calculation.
        start_date : Union[str, datetime, date]
            Start date for PSI calculation.
        test_data : Optional[pd.DataFrame], optional
            Test dataset for PSI calculation, by default None.
        """
        print("Calculating PSI with the following parameters:")
        print(f"Time column: {time_column}")
        print(f"Start date: {start_date}")
        print(f"End date: {end_date}")
        print(f"Expected time (split point): {time_expected}")
        print(f"Number of buckets: {buckets}")
        print(f"Bucket type: {bucket_type}")
        print(f"Using separate test data: {'Yes' if test_data is not None else 'No'}")
        print("=" * 60)

        # Print data info before PSI calculation
        print(f"Data shape before PSI calculation: {self.dataframe.shape}")
        print(
            f"Date range in data: {self.dataframe[time_column].min()} to {self.dataframe[time_column].max()}"
        )

        if test_data is not None:
            print(f"Test data shape: {test_data.shape}")
            print(
                f"Date range in test data: {test_data[time_column].min()} to {test_data[time_column].max()}"
            )

        self.univariate_analysis.compute_psi(
            time_column,
            time_expected,
            start_date,
            end_date,
            test_data,
            buckets,
            bucket_type,
        )

        # Print data info after PSI calculation
        print(
            f"Data shape after PSI calculation: {self.univariate_analysis.data.shape}"
        )
        print(
            f"Date range in filtered data: {self.univariate_analysis.data[time_column].min()} to {self.univariate_analysis.data[time_column].max()}"
        )

    def plot_num_cat_anova(self):
        """
        Plot ANOVA results for numerical-categorical column pairs.
        """
        fig, _ = self.bivariate_analysis.perform_anova_numeric_categorical(
            cat_cols=self.categorical_columns
        )
        fig.show()

    def plot_cat_cat_cramersv(self):
        """
        Plot Cramer's V for categorical-categorical column pairs.
        """
        self.bivariate_analysis.plot_pairwise_cramers_v(
            categorical_features=self.categorical_columns
        )

    def plot_num_univariate(self, threshold_c: float, threshold_iv: float):
        """
        Plot univariate analysis for numerical columns.

        Parameters
        ----------
        threshold_c : float
            Threshold for Cramer's V filtering.
        threshold_iv : float
            Threshold for Information Value filtering.

        Returns
        -------
        Tuple[List[str], List[str]]
            Filtered variables based on Cramer's V and Information Value.
        """
        _, filtered_cramers = self.univariate_analysis.plot_cramers_v(
            self.numerical_columns,
            excluded_vars=self.exclusion,
            filter_threshold=threshold_c,
        )

        _, filtered_iv = self.univariate_analysis.plot_information_value(
            numerical_features=self.numerical_columns,
            filter_threshold=threshold_iv,
            target_column=self.target_column,
        )
        return filtered_cramers, filtered_iv

    def impute_preview_normalization_numerics(
        self,
        imputation_method,
        eliminated: Optional[List[str]] = None,
    ):
        """
        Impute missing values and preview normalization for numerical columns.

        Parameters
        ----------
        imputation_method : Literal["knn", "mean", "median", "most_frequent", "quantile"]
            Method to use for imputation.
        eliminated : Optional[List[str]], optional
            List of columns to eliminate, by default None.
        """
        imputed = self.feature_engineering.handle_missing_values(imputation_method)
        transforms = self.get_transformations(unwanted_features=eliminated)

        EDAToolkit.save_intermediary(PATH_DATA_PROCESSED, imputed, "imputed")
        print("Imputed dataframe saved in the processed directory.")

        self.feature_engineering = FeatureEngineering(
            imputed,
            self.target_column,
            self.numerical_columns,
            self.to_be_enc,
            transformations=transforms,
        )

        self.feature_engineering.diagnose_normality_transform()

    def normalize_numericals(self, to_transformed):
        """
        Apply normality transformations to numerical columns.

        Parameters
        ----------
        to_transformed : List[str]
            List of columns to be transformed.
        """
        transformed = self.feature_engineering.apply_normality_transformations(
            to_transformed
        )
        transforms = self.get_transformations()
        EDAToolkit.save_intermediary(PATH_DATA_PROCESSED, transformed, "transformed")
        print("Transformed dataframe saved in the processed directory.")

        self.feature_engineering = FeatureEngineering(
            transformed,
            self.target_column,
            self.numerical_columns,
            self.to_be_enc,
            transformations=transforms,
        )

    def process_low_cardinality_cols(
        self,
        handling_method: Literal[
            "kmeans", "fixed_width", "exponential", "quantile", "equal_frequency"
        ],
    ):
        """
        Process low cardinality columns.

        Parameters
        ----------
        handling_method : Literal["kmeans", "fixed_width", "exponential", "quantile", "equal_frequency"]
            Method to use for handling low cardinality columns.
        """
        binned = self.feature_engineering.binnings(methods=handling_method)
        EDAToolkit.save_intermediary(PATH_DATA_PROCESSED, binned, "binned")
        print(
            "Variables with low cardinality are treated and saved in the processed directory."
        )

    def process_high_cardinality(
        self,
        selected_cols,
        handling_method: Literal["gathering", "woe", "perlich"],
    ):
        """
        Process high cardinality columns.

        Parameters
        ----------
        selected_cols : List[str]
            List of columns to process.
        handling_method : Literal["gathering", "woe", "perlich"]
            Method to use for handling high cardinality columns.
        """
        high_card = (
            self.feature_engineering.transform_and_plot_high_cardinality_histograms(
                selected_cols, method=handling_method
            )
        )
        if high_card is not None:
            EDAToolkit.save_intermediary(
                PATH_DATA_PROCESSED, high_card, "high_cardinality_treated"
            )
            print(
                "High cardinality variables are treated and dataframe saved in the processed directory."
            )
            transforms = self.get_transformations()

            self.feature_engineering = FeatureEngineering(
                high_card,
                self.target_column,
                self.numerical_columns,
                self.to_be_enc,
                transformations=transforms,
            )
        else:
            print("High cardinality treatment failed.")

    def plot_target_frequency_cols(self, scaling: bool):
        """
        Plot target frequency for numerical columns.

        Parameters
        ----------
        scaling : bool
            If True, apply scaling to the columns before plotting.
        """
        self.visualizations.plot_numerical_target_frequency_line(scale=scaling)

    def print_crosstab_freqs(self, num_rows):
        """
        Print cross-tabulation frequencies for categorical columns.

        Parameters
        ----------
        num_rows : int
            Number of rows to display in the output.
        """
        freqs = self.visualizations.calc_cat_target_freq()

        print(freqs.head(n=num_rows))

    def encode_categoricals(self, method):
        """
        Encode categorical columns.

        Parameters
        ----------
        method : Literal["one_hot", "distribution", "woe", "catboost"]
            Encoding method to use.
        """
        self.feature_engineering.encoding_categorical(method)

    def winsorize_numericals(self, columns_to_transformed):
        """
        Apply winsorization to numerical columns.

        Parameters
        ----------
        columns_to_transformed : List[str]
            List of columns to transform.
        """
        self.feature_engineering.apply_winsorization(columns_to_transformed)
