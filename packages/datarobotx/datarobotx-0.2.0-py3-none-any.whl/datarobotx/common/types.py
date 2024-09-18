#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

import pandas as pd
from typing_extensions import TypedDict


class TimeSeriesPredictParams(TypedDict):
    """Typed dict for time series predict parameters."""

    forecastPoint: Optional[str]
    predictionsStartDate: Optional[str]
    predictionsEndDate: Optional[str]
    type: Optional[str]
    relaxKnownInAdvanceFeaturesCheck: Optional[bool]


class AutopilotModelType:
    """Type for type checking if an AutopilotModel."""

    def set_params(self, **kwargs: Any) -> AutopilotModelType:
        raise NotImplementedError()

    def get_params(self) -> Union[Dict[Any, Any], Any]:
        raise NotImplementedError()


@dataclass
class ModelKind:
    """Capabilities of a deployed DataRobot model.

    See https://app.datarobot.com/docs/api/reference/public-api/models.html#properties_103
    """

    isAnomalyDetectionModel: bool = False
    isCombinedModel: bool = False
    isDecisionFlow: bool = False
    isFeatureDiscovery: bool = False
    isMultiseries: bool = False
    isTimeSeries: bool = False
    isUnsupervisedLearning: bool = False
    isClustering: bool = False
    isMultilabel: bool = False
    isMultiClass: bool = False
    isRegression: bool = False
    isBinary: bool = False
    isTextGen: bool = False
    seriesId: Optional[str] = None
    timestampCol: Optional[str] = None
    targetName: Optional[str] = None
    projectId: Optional[str] = None

    @staticmethod
    def infer_model_kind(
        settings_json: Dict[str, Any], deployment_json: Dict[str, Any]
    ) -> ModelKind:
        """
        Infer DataRobot deployed model capabilities.

        Uses response from
          - GET /deployments/{did}/
          - GET /deployments/{did}/settings/

        Parameters
        ----------
        settings_json : dict
            HTTP response from GET /deployments/{did}/settings/
        deploymnet_json : dict
            HTTP response from GET /deployments/{did}/

        Returns
        -------
        ModelKind
            Data structure with deployment capabilities

        Notes
        -----
        Due to limitations of the API, returned predictions may also need to be
        inspected to correctly infer all capabilities. See
        `confirm_model_kind_from_results`

        """
        projectId = deployment_json["model"]["projectId"]
        isAnomalyDetectionModel = False
        isCombinedModel = False
        isDecisionFlow = False
        isFeatureDiscovery = False
        isMultiseries = False
        isTimeSeries = False
        isUnsupervisedLearning = deployment_json["model"]["unsupervisedMode"]
        isMultilabel = False
        isClustering = False
        isMultiClass = False
        isBinary = False
        timestampCol = None
        isRegression = False
        isTextGen: bool = False
        if deployment_json["model"]["targetType"] == "Multilabel":
            isMultilabel = True
        if deployment_json["model"]["targetType"] == "Regression":
            isRegression = True
        if deployment_json["model"]["targetType"] == "TextGeneration":
            isTextGen = True
        targetName = deployment_json["model"].get("targetName", None)
        # Are we anomalous? Due to Datarobot API error the unsupervisedType can't be relied on
        # we are leaving this code here so that you know we tried it and hope that one day
        # VIZAI-4050 can be properly fixed see slack https://datarobot.slack.com/archives/C019E6X2WMU/p1671724949085819
        # if isUnsupervisedLearning:
        #     if deployment_json['model']['unsupervisedType'] == 'anomaly': Unsupervised type not available
        #         isAnomalyDetectionModel = True
        #     else:
        #         isClustering = True

        # are we using decision flow?
        isDecisionFlow = deployment_json["model"].get("hasDecisionFlow", False)
        # are we using feature discovery?
        isFeatureDiscovery = deployment_json["capabilities"]["supportsSecondaryDatasets"]
        # are we a time series model
        if settings_json["predictionsByForecastDate"]["columnName"]:
            isTimeSeries = True
            timestampCol = settings_json["predictionsByForecastDate"]["columnName"]
            # there is no current way to find the seriesID
        # are we multilable?
        if deployment_json["model"]["targetType"] == "Multiclass":
            if deployment_json["model"]["targetName"] is not None:
                isMultiClass = True
            else:
                isClustering = True
        else:
            isMultiClass = False
        # are we binary?
        if deployment_json["model"]["targetType"] == "Binary":
            isBinary = True

        return ModelKind(
            projectId=projectId,
            isAnomalyDetectionModel=isAnomalyDetectionModel,
            isCombinedModel=isCombinedModel,
            isDecisionFlow=isDecisionFlow,
            isFeatureDiscovery=isFeatureDiscovery,
            isMultiseries=isMultiseries,
            isMultilabel=isMultilabel,
            isTimeSeries=isTimeSeries,
            isClustering=isClustering,
            isUnsupervisedLearning=isUnsupervisedLearning,
            isMultiClass=isMultiClass,
            isBinary=isBinary,
            timestampCol=timestampCol,
            targetName=targetName,
            isRegression=isRegression,
            isTextGen=isTextGen,
        )

    def confirm_model_kind_from_results(
        self,
        df_results: Optional[pd.DataFrame] = None,
        json_results: Optional[Dict[str, Any]] = None,
    ) -> ModelKind:
        """
        Update ModelKind based on returned predictions.

        ModelKind objects are generated from data received from the `deployment` and
        `deploymentSettings` routes. Unfortunately, the information in these responses
        is not sufficient to infer all capabilities. This function takes returned
        batch or real time predictions and updates a few capabilities, specifically:

            - Whether a deployment is anomaly detection
            - `seriesId` of time series models

        Parameters
        ----------
        df_results : pd.DataFrame, optional
            Predictions returned from a completed batch prediction job
            (as a DataFrame).
        json_results : dict, optional
            Predictions returned from requesting RT predictions
            (JSON response body).

        Returns
        -------
        self : ModelKind
            Updated model capabilities (mutated in place)
        """
        if df_results is not None:
            if "ANOMALY_SCORE" in df_results.columns:
                self.isAnomalyDetectionModel = True
        if json_results is not None:
            if (
                len(json_results["data"][0]["predictionValues"]) == 1
                and json_results["data"][0]["predictionValues"][0]["label"] == "Anomaly Score"
            ):
                self.isAnomalyDetectionModel = True
        if self.isTimeSeries:
            if df_results is not None:
                if self.timestampCol is not None:
                    if "(actual)" in self.timestampCol:
                        # DataRobot transforms the datetime column and creates a new
                        # column with the "(actual)" suffix. Therefore, to identify
                        # the timestamp used in time series predictions we will find
                        # the column based on position. DataRobot returns in the
                        # following format:
                        #
                        # SERIES_ID | FORECAST_POINT | TIMESTAMP_COL
                        # or for single series
                        # FORECAST_POINT | TIMESTAMP_COL
                        if df_results.columns[0] == "FORECAST_POINT":
                            self.timestampCol = str(df_results.columns[1])
                        else:
                            self.timestampCol = str(df_results.columns[2])
        return self
