#
# Copyright 2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import datetime as dt
import logging
import typing as t
from typing import Any, cast, Dict, Tuple

import numpy as np
import pandas as pd

import datarobotx.client.datasets as datasets_client
import datarobotx.client.projects as proj_client
from datarobotx.common import utils
from datarobotx.common.types import TimeSeriesPredictParams

logger = logging.getLogger("drx")


async def prepare_prediction_data(
    project_id: str,
    X: t.Union[pd.DataFrame, str],
    as_of: t.Optional[t.Union[str, dt.datetime]] = None,
    for_dates: t.Optional[
        t.Union[str, dt.datetime, Tuple[str, str], Tuple[dt.datetime, dt.datetime]]
    ] = None,
) -> t.Tuple[pd.DataFrame, TimeSeriesPredictParams, Dict[str, Any]]:
    """
    Prepare a dataset for time series predictions.

    Parameters
    ----------
    project_id: str
        Project id
    X : pandas.DataFrame or str
        Dataset to compute predictions on; target column can be included
        or omitted. If str, can be AI catalog dataset id or name (if unambiguous)
    as_of : str or datetime, optional
        The date on which forecasting is performed, by default None
    for_dates : str or datetime or tuple of str or datetime, optional
        The dates being forecasted, by default None
        If str, returns a single row for the most recent forecast
        possible for this date.
        If tuple, returns a single row for the most recent forecast
        possible for each date in the range.

    Returns
    -------
    Tuple[pd.DataFrame, TimeSeriesPredictParams, Dict[str, Any]]
        Tuple of (X_predict, time_series_parameters, ts_project_settings)
        X_predict : pd.DataFrame
            Modified dataset to compute predictions on
        time_series_parameters : TimeSeriesPredictParams
            Time series specific parameters for prediction
        ts_project_settings : Dict[str, Any]
            Project settings for time series predictions. Important in post processing
    """
    # Download data (needed to make time format changes and append values for future predictions)
    if isinstance(X, str):
        X = await datasets_client.get_dataset_file(X)

    ts_project_settings = await _get_project_settings(project_id, X)

    _validate_time_series_predict_args(ts_project_settings, as_of, for_dates)

    X_predict = _make_prediction_dataset(
        X,
        ts_project_settings,
        as_of,
        for_dates,
    )

    time_series_parameters = _get_time_series_parameters(ts_project_settings, as_of, for_dates)

    return X_predict, time_series_parameters, ts_project_settings


async def _get_project_settings(project_id: str, X: pd.DataFrame) -> Dict[str, Any]:
    """
    Make a giant dictionary of everything we need to make time series predictions.

    Parameters
    ----------
    project_id : str
        Project id
    X : pd.DataFrame
        Dataset to compute predictions on. Note that X is chosen as the variable name
        for consistency with the sklearn API.
    """
    datetime_data = await proj_client.get_datetime_partitioning(project_id)
    project_data = await proj_client.get_project(project_id)

    datetime_data["unsupervisedMode"] = project_data["unsupervisedMode"]
    datetime_data["datetimePartitionColumn"] = datetime_data["datetimePartitionColumn"].replace(
        " (actual)", ""
    )
    if not datetime_data["unsupervisedMode"]:
        datetime_data["target"] = project_data["target"].replace(" (actual)", "")
        datetime_data["latestDatapoint"] = pd.to_datetime(
            X.loc[
                X[datetime_data["target"]].notnull(),
                datetime_data["datetimePartitionColumn"],
            ],
            utc=True,
        ).max()
    else:
        datetime_data["latestDatapoint"] = pd.to_datetime(
            X[datetime_data["datetimePartitionColumn"]], utc=True
        ).max()

    datetime_data["kiaFeatures"] = [
        i["featureName"] for i in datetime_data["featureSettings"] if i["knownInAdvance"]
    ]

    datetime_data["timeUnitToSecond"] = utils.TIME_UNIT_MAPPING["to_seconds"][
        datetime_data["windowsBasisUnit"]
    ]
    datetime_data["pandasFrequency"] = utils.TIME_UNIT_MAPPING["to_pandas_offset"][
        datetime_data["windowsBasisUnit"]
    ]

    datetime_data["minimumDate"] = pd.to_datetime(
        X[datetime_data["datetimePartitionColumn"]].min(), utc=True
    )
    datetime_data["minimumForecastPoint"] = datetime_data["minimumDate"] + pd.to_timedelta(
        datetime_data["timeUnitToSecond"] * -datetime_data["featureDerivationWindowStart"],
        unit="s",
    )
    datetime_data["maximumForecastDate"] = datetime_data["latestDatapoint"] + pd.to_timedelta(
        datetime_data["timeUnitToSecond"] * datetime_data["forecastWindowEnd"],
        unit="s",
    )

    return datetime_data


def _validate_time_series_predict_args(
    ts_project_settings: Dict[str, Any],
    as_of: t.Optional[t.Union[str, dt.datetime]] = None,
    for_dates: t.Optional[
        t.Union[str, dt.datetime, Tuple[str, str], Tuple[dt.datetime, dt.datetime]]
    ] = None,
) -> None:
    """Validate that time series predictions can be made from request."""
    minimum_forecast_point = ts_project_settings["minimumForecastPoint"]
    maximum_forecast_date = ts_project_settings["maximumForecastDate"]

    if as_of is not None:
        assert (
            pd.to_datetime(as_of, utc=True) >= minimum_forecast_point
        ), f"Invalid as_of date: {as_of}. Must be after {minimum_forecast_point}"
        assert (
            pd.to_datetime(as_of, utc=True) <= maximum_forecast_date
        ), f"Invalid as_of date: {as_of}. Must be before {maximum_forecast_date}"

    elif for_dates is not None:
        for_dates = (for_dates, for_dates) if isinstance(for_dates, str) else for_dates
        assert (
            max(pd.to_datetime(for_dates, utc=True)) <= maximum_forecast_date
        ), f"Invalid for_dates: {for_dates} asks for predictions after latest possible date {maximum_forecast_date}"
        assert min(pd.to_datetime(for_dates, utc=True)) > minimum_forecast_point, (
            f"Invalid for_dates: {for_dates} for dates must all be after the minimum forecast point "
            + f"{minimum_forecast_point}"
        )

    assert (
        as_of is None or for_dates is None
    ), "Cannot specify both as_of and for_dates in a single request."


def _get_time_series_parameters(
    datetime_data: Dict[str, Any],
    as_of: t.Optional[t.Union[str, dt.datetime]] = None,
    for_dates: t.Optional[
        t.Union[str, dt.datetime, Tuple[str, str], Tuple[dt.datetime, dt.datetime]]
    ] = None,
) -> TimeSeriesPredictParams:
    """Return time-series specific parameters for prediction."""
    time_series_parameters = {}
    time_unit_to_second = datetime_data["timeUnitToSecond"]
    date_format = datetime_data["dateFormat"]

    if as_of is not None:
        time_series_parameters["forecastPoint"] = pd.to_datetime(as_of, utc=True).strftime(
            date_format
        )
    elif for_dates is not None:
        if isinstance(for_dates, str):
            for_dates = (for_dates, for_dates)
        elif isinstance(for_dates, dt.datetime):
            for_dates = (for_dates, for_dates)
        time_series_parameters["predictionsStartDate"] = pd.to_datetime(
            for_dates[0], utc=True
        ).strftime(date_format)
        time_series_parameters["predictionsEndDate"] = (
            pd.to_datetime(for_dates[1], utc=True) + pd.to_timedelta(time_unit_to_second, unit="s")
        ).strftime(date_format)

    return cast(TimeSeriesPredictParams, time_series_parameters)


def _make_prediction_dataset(
    X: pd.DataFrame,
    ts_project_settings: Dict[str, Any],
    as_of: t.Optional[t.Union[str, dt.datetime]] = None,
    for_dates: t.Optional[
        t.Union[str, dt.datetime, Tuple[str, str], Tuple[dt.datetime, dt.datetime]]
    ] = None,
) -> pd.DataFrame:
    """Create a dataset for predictions."""

    def build_future_dates(X: pd.DataFrame, end_date: dt.datetime) -> pd.DataFrame:
        """Append data to X if needed."""
        if end_date > latest_datapoint:
            future_dates = pd.date_range(
                start=latest_datapoint + pd.to_timedelta(time_unit_to_second, unit="s"),
                end=end_date,
                freq=pandas_frequency,
            )
            future_df = pd.DataFrame(
                {
                    datetime_partition_column: future_dates,
                    target_column: [0.0] * len(future_dates),
                }
            )

            if X[datetime_partition_column].max() < end_date:
                start_n = len(X)
                if multiseries_id_columns is not None:
                    multiseries_id = multiseries_id_columns[0].replace(" (actual)", "")

                    # Find series that need records appended
                    series_needing_future_data = (
                        X.groupby(multiseries_id)[datetime_partition_column]
                        .max()
                        .loc[lambda x: x < end_date]
                        .index.tolist()
                    )
                    future_df = pd.concat(
                        [
                            future_df.assign(**{multiseries_id: i})
                            for i in series_needing_future_data
                        ]
                    )
                    X = (
                        pd.concat((X, future_df))
                        .sort_values(by=[multiseries_id, datetime_partition_column])
                        .reset_index(drop=True)
                    )
                else:
                    X = (
                        pd.concat((X, future_df))
                        .sort_values(by=datetime_partition_column)
                        .reset_index(drop=True)
                    )
                logger.info("Appended %s rows to uploaded dataframe", len(X) - start_n)
            X = _handle_kia_features(X, ts_project_settings)
        return X

    datetime_partition_column = ts_project_settings["datetimePartitionColumn"]
    target_column = ts_project_settings.get("target")
    multiseries_id_columns = ts_project_settings["multiseriesIdColumns"]
    date_format = ts_project_settings["dateFormat"]
    time_unit_to_second = ts_project_settings["timeUnitToSecond"]
    pandas_frequency = ts_project_settings["pandasFrequency"]
    latest_datapoint = ts_project_settings["latestDatapoint"]

    X = X.copy()
    X[datetime_partition_column] = pd.to_datetime(X[datetime_partition_column], utc=True)
    if not ts_project_settings["unsupervisedMode"]:
        X[target_column] = X[target_column].fillna(0)
        if isinstance(as_of, (str, dt.datetime)):
            end_date = pd.to_datetime(as_of, utc=True) + pd.to_timedelta(
                time_unit_to_second * ts_project_settings["forecastWindowEnd"], unit="s"
            )
            X = build_future_dates(X, end_date)

        elif isinstance(for_dates, (str, dt.datetime)):
            end_date = pd.to_datetime(for_dates, utc=True)
            X = build_future_dates(X, end_date)

        elif isinstance(for_dates, tuple):
            _, end_date = pd.to_datetime(for_dates, utc=True)
            X = build_future_dates(X, end_date)

    X[datetime_partition_column] = X[datetime_partition_column].dt.strftime(date_format)
    return X


def _handle_kia_features(
    X: pd.DataFrame,
    ts_project_settings: Dict[str, Any],
) -> pd.DataFrame:
    """Handle known in advance features."""
    datetime_partition_column = ts_project_settings["datetimePartitionColumn"]
    latest_datapoint = ts_project_settings["latestDatapoint"]
    kia_features = ts_project_settings["kiaFeatures"]

    if len(kia_features) > 0:
        kia_futures = X[X[datetime_partition_column] > latest_datapoint][kia_features]
        if kia_futures.isna().all().all() and len(kia_futures) > 0:
            logger.warning(
                "You requested forward looking predictions without "
                "supplying known in advance values. This is "
                "usually a bad idea and may result in poor "
                "predictions. Drx will do its best by using the "
                "most frequent known in advance values in scoring data."
            )
            kia_mapping = X[kia_features].mode().to_dict(orient="records")[0]
            X = X.copy()
            for i in kia_features:
                X[i] = np.where(
                    (X[datetime_partition_column] > latest_datapoint),
                    kia_mapping[i],
                    X[i],
                )
    return X


def post_process_predictions(
    X: pd.DataFrame,
    ts_project_settings: Dict[str, Any],
    for_dates: t.Optional[
        t.Union[str, dt.datetime, Tuple[str, str], Tuple[dt.datetime, dt.datetime]]
    ] = None,
) -> pd.DataFrame:
    """Filtering exercise to exclude unwanted values from results."""
    if for_dates is not None:
        forecast_window_start = ts_project_settings["forecastWindowStart"]
        latest_data_point = ts_project_settings["latestDatapoint"]
        X = X.copy().assign(
            forecast_point=lambda x: pd.to_datetime(x["forecastPoint"], utc=True),
            timestamp=lambda x: pd.to_datetime(x["timestamp"], utc=True),
        )
        X_from_past = X.loc[
            (X["forecastDistance"] == forecast_window_start)
            & (pd.to_datetime(X["forecastPoint"], utc=True) <= latest_data_point)
        ]
        X_from_future = X.loc[
            (X["forecastDistance"] > forecast_window_start)
            & (pd.to_datetime(X["forecastPoint"], utc=True) == latest_data_point)
        ]
        return cast(
            pd.DataFrame,
            pd.concat((X_from_past, X_from_future))
            .sort_values(by=["seriesId", "timestamp"])
            .reset_index(drop=True)
            .assign(
                timestamp=lambda x: x["timestamp"].dt.strftime(ts_project_settings["dateFormat"])
            ),
        )
    return X


def _has_ts_helper_args(
    as_of: t.Optional[t.Union[str, dt.datetime]] = None,
    for_dates: t.Optional[
        t.Union[str, dt.datetime, Tuple[str, str], Tuple[dt.datetime, dt.datetime]]
    ] = None,
    **kwargs: Any,
) -> bool:
    """Check if any of the arguments are passed."""
    if as_of is not None or for_dates is not None:
        ts_api_arguments = ["predictionsStartDate", "predictionsEndDate", "forecastPoint"]
        for argument in kwargs:
            assert (
                argument not in ts_api_arguments
            ), f"Argument {argument} is not supported when 'as_of' or 'for_dates' are passed"
        return True
    return False
