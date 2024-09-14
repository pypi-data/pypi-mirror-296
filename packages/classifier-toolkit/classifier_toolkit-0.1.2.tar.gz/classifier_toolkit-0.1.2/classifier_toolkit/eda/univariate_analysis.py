import math
from datetime import date, datetime
from typing import List, Literal, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency


class UnivariateAnalysis:
    def __init__(
        self, df: pd.DataFrame, target_column: str, numerical_features: List[str]
    ) -> None:
        """
        Initialize the UnivariateAnalysis class with data and configuration.

        Parameters
        ----------
        df : pd.DataFrame
            The data to be analyzed.
        target_column : str
            The target column for analysis.
        numerical_features : List[str]
            List of numerical features.
        """
        self.data = df.copy()
        self.target_column = target_column
        self.numerical_features = numerical_features or []

    @staticmethod
    def _get_cramers_v(data: pd.DataFrame, var1: str, var2: str) -> float:
        """
        Calculate Cramer's V statistic for two variables.

        Parameters
        ----------
        data : pd.DataFrame
            The data containing the variables.
        var1 : str
            The first variable.
        var2 : str
            The second variable.

        Returns
        -------
        float
            Cramer's V statistic.
        """
        confusion_matrix = pd.crosstab(data[var1], data[var2])
        chi2 = chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum().sum()
        min_dim = min(confusion_matrix.shape) - 1

        return np.sqrt(chi2 / (n * min_dim))

    def _prepare_cramersV_features(
        self, numerical_features: List[str], n_bins: int = 5
    ) -> List[str]:
        """
        Prepare features for Cramer's V calculation by binning numerical features.

        Parameters
        ----------
        numerical_features : List[str]
            List of numerical feature names.
        n_bins : int, optional
            Number of bins for continuous variables, by default 5.

        Returns
        -------
        List[str]
            List of features prepared for Cramer's V calculation.
        """
        cramersV_var_list = self.data.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        # Exclude the target column
        cramersV_var_list = [
            var for var in cramersV_var_list if var != self.target_column
        ]

        for num in numerical_features:
            unique_values = self.data[num].nunique()

            if (
                unique_values > 1
            ):  # Ensure there are at least two unique values for binning
                try:
                    self.data[f"{num}_bin"] = pd.qcut(
                        self.data[num], q=n_bins, duplicates="drop"
                    )
                    # Check if the resulting bins are more than 1
                    if self.data[f"{num}_bin"].nunique() <= 1:
                        raise ValueError(
                            f"Only 1 bin created for {num} with q={n_bins}."
                        )

                except ValueError as e:
                    print(
                        f"Equal frequency binning not possible for {num}, attempting 2 bins: {e}"
                    )
                    if pd.api.types.is_integer_dtype(self.data[num]):
                        # For integer type, ensure bins are whole numbers
                        self.data[f"{num}_bin"] = pd.cut(
                            self.data[num], bins=2, include_lowest=True, right=False
                        )
                    else:
                        # For non-integer type, fallback to 2 equal frequency bins
                        self.data[f"{num}_bin"] = pd.qcut(
                            self.data[num], q=2, duplicates="drop"
                        )
                cramersV_var_list.append(f"{num}_bin")
            else:
                # Handle the case where there is only one unique value
                print(f"Skipping {num} as it has only {unique_values} unique value(s).")

        return cramersV_var_list

    def plot_cramers_v(
        self,
        numerical_features: List[str],
        excluded_vars: List[str],
        filter_threshold: float,
        n_bins: int = 5,
        fig_width: int = 800,
        fig_height: int = 800,
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        Calculate and plot Cramer's V for multiple features using Plotly Express.

        Parameters
        ----------
        numerical_features : List[str]
            List of numerical feature names.
        excluded_vars : List[str]
            List of variables to exclude from the analysis.
        n_bins : int, optional
            Number of bins for continuous variables, by default 5.
        fig_width : int, optional
            Width of the figure in pixels, by default 800.
        fig_height : int, optional
            Height of the figure in pixels, by default 800.

        Returns
        -------
        pd.DataFrame
            DataFrame containing Cramer's V values.
        """
        cramersV_var_list = self._prepare_cramersV_features(numerical_features, n_bins)

        # Exclude any specified variables
        cramersV_var_list = [
            var for var in cramersV_var_list if var not in excluded_vars
        ]

        rows = []
        for cat in cramersV_var_list:
            cramers = UnivariateAnalysis._get_cramers_v(
                self.data, cat, self.target_column
            )
            rows.append(round(cramers, 2))

        cramers_results = pd.DataFrame(
            rows, columns=[self.target_column], index=cramersV_var_list
        )

        # Create a Plotly heatmap
        fig = px.imshow(
            cramers_results,
            labels={"x": self.target_column, "y": "Features", "color": "Cramer's V"},
            color_continuous_scale="Plasma",
            text_auto=True,
            aspect="auto",
            width=fig_width,
            height=fig_height,
        )

        fig.update_layout(
            title="Cramer's V with Target Variable",
            xaxis_title=self.target_column,
            yaxis_title="Features",
        )

        fig.show()

        filtered_vars = cramers_results[
            cramers_results[self.target_column] > filter_threshold
        ].index.tolist()

        return cramers_results, filtered_vars

    def _calculate_information_value(
        self, feature_col: str, target_col: str, bins: int = 10, show_woe: bool = False
    ) -> Union[Tuple[float, pd.DataFrame], float]:
        """
        Calculate Information Value for a single feature.

        Parameters
        ----------
        feature_col : str
            Name of the feature column.
        target_col : str
            Name of the target column.
        bins : int, optional
            Number of bins for continuous variables, by default 10.
        show_woe : bool, optional
            Boolean to show WOE values, by default False.

        Returns
        -------
        Tuple[float, pd.DataFrame] or float
            Information Value and optionally the WOE DataFrame.
        """
        df = pd.DataFrame(
            {
                feature_col: self.data[feature_col],
                target_col: self.data[target_col].astype(float),
            }
        )

        if df[feature_col].dtype in ["int64", "float64"]:
            df["bins"] = pd.qcut(df[feature_col], q=bins, duplicates="drop")
        else:
            df["bins"] = df[feature_col]

        total_good = df[target_col].sum()
        total_bad = df[target_col].count() - total_good

        # Explicitly setting observed=False to retain current behavior
        grouped = df.groupby("bins", observed=False)[target_col].agg(["sum", "count"])
        grouped["good"] = grouped["sum"]
        grouped["bad"] = grouped["count"] - grouped["sum"]

        # Add a small value to prevent division by zero
        epsilon = 1e-10
        grouped["good_pct"] = (grouped["good"] + epsilon) / (total_good + epsilon)
        grouped["bad_pct"] = (grouped["bad"] + epsilon) / (total_bad + epsilon)

        grouped["woe"] = np.log(grouped["good_pct"] / grouped["bad_pct"])
        grouped["iv"] = (grouped["good_pct"] - grouped["bad_pct"]) * grouped["woe"]

        iv = grouped["iv"].sum()

        if show_woe:
            return iv, grouped[["good", "bad", "good_pct", "bad_pct", "woe", "iv"]]
        else:
            return iv

    def plot_information_value(
        self,
        numerical_features: List[str],
        filter_threshold: float,
        target_column: str,
        bins: int = 10,
        fig_width: int = 800,
        fig_height: int = 800,
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        Calculate and plot Information Value for multiple features using Plotly Express.

        Parameters
        ----------
        numerical_features : List[str]
            List of numerical feature names.
        target_column : str
            Name of the target column.
        bins : int, optional
            Number of bins for continuous variables, by default 10.
        fig_width : int, optional
            Width of the figure in pixels, by default 800.
        fig_height : int, optional
            Height of the figure in pixels, by default 800.

        Returns
        -------
        pd.DataFrame
            DataFrame containing Information Values.
        """
        iv_values = []
        for feature in numerical_features:
            iv = self._calculate_information_value(feature, target_column, bins)
            iv_values.append(iv)

        iv_df = pd.DataFrame(
            iv_values, columns=[target_column], index=numerical_features
        )

        # Create the heatmap using Plotly Express
        fig = px.imshow(
            iv_df,
            labels={"x": "Features", "y": target_column, "color": "Information Value"},
            color_continuous_scale="Plasma",
            text_auto=True,
            aspect="auto",
            width=fig_width,
            height=fig_height,
        )

        # Update layout
        fig.update_layout(
            title="Information Value with Target Variable",
            xaxis_title="Features",
            yaxis_title=target_column,
        )

        # Display the figure
        fig.show()

        filtered_vars = iv_df[filter_threshold < iv_df[target_column]].index.tolist()

        return iv_df, filtered_vars

    def plot_distributions(
        self,
        numerical_columns: Optional[List[str]] = None,
        grouped: bool = False,
        fig_width: int = 1100,
        fig_height: int = 600,
    ) -> None:
        """
        Plot the distribution of numerical columns using Plotly Express.

        Parameters
        ----------
        numerical_columns : Optional[List[str]], optional
            List of numerical columns to plot. If None, all numerical features will be available for selection.
        grouped : bool, optional
            If True, plot distributions grouped by the target variable, by default False.
        fig_width : int, optional
            Width of the figure in pixels, by default 800.
        fig_height : int, optional
            Height of the figure in pixels, by default 500.
        """
        if numerical_columns is None:
            numerical_columns = self.numerical_features

        # Create the initial figure
        fig = go.Figure()

        # Add traces for each numerical column (initially hidden)
        for col in numerical_columns:
            if grouped:
                for target_value in self.data[self.target_column].unique():
                    data = self.data[self.data[self.target_column] == target_value]
                    fig.add_trace(
                        go.Histogram(
                            x=data[col],
                            name=f"{col} ({self.target_column}={target_value})",
                            visible=False,
                        )
                    )
            else:
                fig.add_trace(go.Histogram(x=self.data[col], name=col, visible=False))

        # Create buttons for dropdown
        buttons = []
        for i, col in enumerate(numerical_columns):
            button = {
                "method": "update",
                "label": col,
                "args": [
                    {"visible": [False] * len(fig.data)},  # type: ignore
                    {"title": f"Distribution of {col}"},
                ],
            }
            if grouped:
                for j in range(len(self.data[self.target_column].unique())):
                    button["args"][0]["visible"][
                        i * len(self.data[self.target_column].unique()) + j
                    ] = True
            else:
                button["args"][0]["visible"][i] = True
            buttons.append(button)

        # Update layout
        fig.update_layout(
            updatemenus=[
                {
                    "active": 0,
                    "buttons": buttons,
                    "direction": "down",
                    "pad": {"r": 10, "t": 10},
                    "showactive": True,
                    "x": 0.1,
                    "xanchor": "left",
                    "y": 1.15,
                    "yanchor": "top",
                },
            ],
            annotations=[
                {
                    "text": "Select Feature:",
                    "showarrow": False,
                    "x": 0,
                    "y": 1.085,
                    "yref": "paper",
                    "align": "left",
                }
            ],
            barmode="overlay" if grouped else "stack",
            width=fig_width,
            height=fig_height,
        )

        # Make the first trace visible
        if len(fig.data) > 0:  # type: ignore
            fig.data[0].visible = True  # type: ignore

        fig.show()

    def _make_partitions(self, number_of_partitions) -> pd.DataFrame:
        """
        Partition the numerical features into 4 bins.

        Returns
        -------
        pd.DataFrame
            DataFrame with partitioned numerical features.
        """
        partitioned = self.data.copy()
        for num in self.numerical_features:
            partitioned[num + "_bin"] = pd.qcut(
                x=partitioned[num],
                q=number_of_partitions,
                labels=False,
                duplicates="drop",
            ).astype("category")
        return partitioned

    def get_num_feature_repartition(
        self, time_col: str, number_of_partitions: int = 4, freq: str = "1ME"
    ) -> Optional[pd.DataFrame]:
        """
        Plot the risk class repartition through time and return a table of the risk class repartition through time.

        Parameters
        ----------
        time_col : str
            Name of the column that contains the observation date.
        freq : str, optional
            The frequency at which the risk class is aggregated ('D', 'M', or 'Y'), by default '1ME'.

        Returns
        -------
        Optional[pd.DataFrame]
            DataFrame containing the risk class repartition through time.
        """
        partitioned = self._make_partitions(number_of_partitions)

        # Drop rows where the time column is NaT
        if partitioned[time_col].isnull().any():
            print(
                f"There are missing entries in the {time_col} column, dropping them for the functionality; however, try to mitigate the problem."
            )
            partitioned = partitioned.dropna(subset=[time_col])

        row_nb = math.ceil(len(self.numerical_features) / 2)
        fig, ax = plt.subplots(row_nb, 2, figsize=(20, number_of_partitions * row_nb))
        i, j = 0, 0

        for num in self.numerical_features:
            axes = ax[j] if row_nb == 1 else ax[i, j]

            # Group by and count
            draw = (
                partitioned.groupby(
                    [num + "_bin", pd.Grouper(key=time_col, freq=freq)], observed=False
                )[self.target_column]
                .count()
                .reset_index()
            )

            # Create 'freq' column with aligned indices
            draw["freq"] = draw.groupby([time_col])[self.target_column].transform(
                lambda x: x / x.sum()
            )

            # Ensure that the indices align
            draw_pivot = pd.pivot_table(
                draw,
                values="freq",
                index=time_col,
                columns=num + "_bin",
                observed=False,
            )

            draw_pivot.plot.bar(stacked=True, ax=axes)

            if j == 0:
                j += 1
            else:
                i += 1
                j = 0

        plt.show()
        return None

    def _prepare_data_for_psi(
        self,
        number_of_partitions: int,
        time_col: str,
        start_date: Union[str, datetime, date],
        end_date: Union[str, datetime, date],
    ):
        """
        Prepare data for PSI calculation by filtering based on the time column.

        Parameters
        ----------
        time_col : str
            Name of the column that contains the observation date.
        start_date : Union[str, datetime, date]
            Start date for the PSI calculation.
        end_date : Union[str, datetime, date]
            End date for the PSI calculation.
        """
        self.data = self._make_partitions(number_of_partitions)

        # Convert string dates to datetime if necessary
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)

        # Ensure time_col is in datetime format
        self.data[time_col] = pd.to_datetime(self.data[time_col])

        _filter_date = (self.data[time_col] >= start_date) & (
            self.data[time_col] < end_date
        )
        self.data = self.data.loc[_filter_date]
        self.data.reset_index(drop=True, inplace=True)

    def _calculate_psi_single(
        self,
        time_col: str,
        time_expected: Union[str, datetime, date],
        col: str,
        buckets: int,
        bucket_type: Literal["quantile", "fixed_width"] = "quantile",
    ):
        """
        Calculate the Population Stability Index (PSI) for a single feature.

        Parameters
        ----------
        time_col : str
            Name of the column that contains the observation date.
        time_expected : Union[str, datetime, date]
            The expected date for the PSI calculation.
        col : str
            Name of the column to calculate the PSI.
        buckets : int
            Number of buckets for binning.
        bucket_type : Literal["quantile", "fixed_width"]
            The type of binning to use.

        Returns
        -------
        float
            Population Stability Index for the feature.
        """
        if isinstance(time_expected, str):
            time_expected = pd.to_datetime(time_expected)

        _filter_expected = self.data[time_col] < time_expected
        expected = self.data.loc[_filter_expected, col]
        observed = self.data.loc[~_filter_expected, col]

        bins = self._create_bins(self.data[col], buckets, bucket_type)

        expected_counts, _ = np.histogram(expected, bins=bins)
        observed_counts, _ = np.histogram(observed, bins=bins)

        expected_percents = expected_counts / len(expected)
        observed_percents = observed_counts / len(observed)

        # Add a small value to prevent division by zero
        epsilon = 1e-10
        psi = np.sum(
            (observed_percents - expected_percents)
            * np.log((observed_percents + epsilon) / (expected_percents + epsilon))
        )

        return psi

    def _create_bins(
        self,
        series: pd.Series,
        buckets: int,
        bucket_type: Literal["quantile", "fixed_width"],
    ) -> np.ndarray:
        if bucket_type == "quantile":
            return pd.qcut(series, q=buckets, duplicates="drop", retbins=True)[1]
        else:  # fixed_width
            return pd.cut(series, bins=buckets, retbins=True)[1]

    def _create_buckets(self, series: pd.Series, bins: np.ndarray) -> pd.Series:
        return pd.cut(
            series,
            bins=bins,  # type: ignore
            labels=range(len(bins) - 1),
            include_lowest=True,
        )

    def _calculate_psi(
        self,
        expected: pd.Series,
        observed: pd.Series,
        bins: np.ndarray,
        epsilon: float = 1e-5,
    ) -> float:
        expected_bucket = self._create_buckets(expected, bins)
        observed_bucket = self._create_buckets(observed, bins)

        all_buckets = range(len(bins) - 1)
        expected_dist = expected_bucket.value_counts(normalize=True).reindex(
            all_buckets, fill_value=epsilon
        )
        observed_dist = observed_bucket.value_counts(normalize=True).reindex(
            all_buckets, fill_value=epsilon
        )

        # Avoid division by zero and log(0)
        psi_values = (observed_dist - expected_dist) * np.log(
            np.maximum(observed_dist, epsilon) / np.maximum(expected_dist, epsilon)
        )
        return psi_values.sum()

    def calculate_psi(
        self,
        train: pd.DataFrame,
        test: Optional[pd.DataFrame],
        time_col: str,
        time_expected: Union[str, datetime, date],
        buckets: int = 10,
        bucket_type: Literal["quantile", "fixed_width"] = "quantile",
        epsilon: float = 1e-5,
    ) -> pd.DataFrame:
        psi_values = {}
        for feature in self.numerical_features:
            if test is None:
                expected = train[train[time_col] < time_expected][feature]
                observed = train[train[time_col] >= time_expected][feature]
            else:
                expected = train[feature]
                observed = test[feature]

            combined = pd.concat([expected, observed])
            bins = self._create_bins(combined, buckets, bucket_type)
            psi = self._calculate_psi(expected, observed, bins, epsilon)
            psi_values[feature] = psi

        return pd.DataFrame.from_dict(psi_values, orient="index", columns=["PSI"])

    def plot_psi(
        self, psi_df: pd.DataFrame, fig_width: int = 800, fig_height: int = 600
    ) -> go.Figure:
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=psi_df.index,
                y=psi_df["PSI"],
                text=psi_df["PSI"].round(4),
                textposition="auto",
            )
        )

        fig.update_layout(
            title="Population Stability Index (PSI) for Numerical Features",
            xaxis_title="Features",
            yaxis_title="PSI Value",
            width=fig_width,
            height=fig_height,
        )

        fig.add_hline(
            y=0.1,
            line_dash="dash",
            line_color="orange",
            annotation_text="Warning",
            annotation_position="bottom right",
        )
        fig.add_hline(
            y=0.25,
            line_dash="dash",
            line_color="red",
            annotation_text="Critical",
            annotation_position="bottom right",
        )

        return fig

    def compute_psi(
        self,
        time_col: str,
        time_expected: Union[str, datetime, date],
        start_date: Union[str, datetime, date],
        end_date: Union[str, datetime, date],
        test_data: Optional[pd.DataFrame] = None,
        buckets: int = 10,
        bucket_type: Literal["quantile", "fixed_width"] = "quantile",
        test_mode: bool = False,
    ) -> pd.DataFrame:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        if isinstance(time_expected, str):
            time_expected = pd.to_datetime(time_expected)

        self.data[time_col] = pd.to_datetime(self.data[time_col])
        filtered_data = self.data[
            (self.data[time_col] >= start_date) & (self.data[time_col] < end_date)
        ]

        if test_data is not None:
            test_data[time_col] = pd.to_datetime(test_data[time_col])
            test_filtered = test_data[
                (test_data[time_col] >= start_date) & (test_data[time_col] < end_date)
            ]
        else:
            test_filtered = None

        psi_df = self.calculate_psi(
            filtered_data, test_filtered, time_col, time_expected, buckets, bucket_type
        )

        fig = self.plot_psi(psi_df)
        if not test_mode:
            fig.show()

        print("\nPopulation Stability Index (PSI) for Numerical Features:")
        print("-" * 80)
        print(f"{'Feature':<60} {'PSI':>15}")
        print("-" * 80)
        for feature, psi in psi_df.iterrows():
            print(f"{feature:<60} {psi['PSI']:>15.6f}")
        print("-" * 80)
        return psi_df

    def _calculate_psi_all(
        self,
        time_col: str,
        time_expected: Union[str, datetime, date],
        buckets: int,
        bucket_type: Literal["quantile", "fixed_width"],
    ) -> pd.Series:
        """
        Calculate the Population Stability Index (PSI) for all numerical features.

        Parameters
        ----------
        time_col : str
            Name of the column that contains the observation date.
        time_expected : Union[str, datetime, date]
            The expected date for the PSI calculation.
        buckets : int
            Number of buckets for binning.
        bucket_type : Literal["quantile", "fixed_width"]
            The type of binning to use.

        Returns
        -------
        pd.Series
            Series containing PSI values for all numerical features.
        """
        dict_psi = {}
        for num in self.numerical_features:
            dict_psi[num] = self._calculate_psi_single(
                time_col, time_expected, num, buckets, bucket_type
            )
        return pd.Series(dict_psi)
