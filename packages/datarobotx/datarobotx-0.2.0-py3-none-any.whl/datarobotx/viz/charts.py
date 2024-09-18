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
import math
from typing import Any, cast, Dict, List, Optional, Tuple, TYPE_CHECKING, Union

import altair as alt
import pandas as pd

import datarobotx.client.projects as proj_client
from datarobotx.common import utils
from datarobotx.viz import viz

if TYPE_CHECKING:
    from datarobotx.models.model import Model, ModelOperator


def _unpack_model_ids(model: Union["Model", "ModelOperator"]) -> Tuple[str, str]:
    from datarobotx.models.model import Model, ModelOperator  # pylint: disable=C0415

    if isinstance(model, Model):
        return (cast(str, model._model_id), cast(str, model._project_id))
    if isinstance(model, ModelOperator):
        return (cast(str, model._best_model._model_id), cast(str, model._project_id))  # type: ignore[union-attr]


def render_chart_not_avialble(chart_type: str) -> alt.Chart:
    """Render chart not available."""
    return (
        alt.Chart(data=pd.DataFrame({"": [None]}))
        .mark_text(align="center", size=24, text=f"{chart_type} not available")
        .configure_view(strokeWidth=0)
        .configure_axis(grid=False)
    )


def render_feature_impact_chart(fi_json: Dict[str, Any]) -> alt.Chart:
    """Render altair feature impact chart."""
    feature_impact = pd.DataFrame(fi_json["featureImpacts"])
    if feature_impact.shape[0] > 10:
        feature_impact = feature_impact.head(10)
    if "impact_normalized" in feature_impact.columns:
        normal_col = "impact_normalized"
        feature_col = "feature_name"
    else:
        normal_col = "impactNormalized"
        feature_col = "featureName"
    chart: alt.Chart = (
        alt.Chart(feature_impact, width=400, title="Feature Impact Chart")
        .mark_bar()
        .encode(x=alt.X(f"{normal_col}:Q"), y=alt.Y(f"{feature_col}:N", sort="-x"))
    )
    return chart


def feature_impact_chart(
    model: Optional[Union["Model", "ModelOperator"]] = None,
    *,
    project_id: Optional[str] = None,
    model_id: Optional[str] = None,
) -> alt.Chart:
    """
    Shows a chart of the permutation feature impact for the input model.
    See https://docs.datarobot.com/en/docs/workbench/wb-experiment/wb-ts-experiment/ts-experiment-insights/ts-feature-impact.html#feature-impact #pylint: disable=line-too-long # noqa: E501
    for more details.

    Either model or project_id/model_id together must be supplied

    Parameters
    ----------
    model : Optional[Union["Model", "ModelOperator"]]
        A DrX Model Object
    project_id: Optional[str]
        The DataRobot Project or Experiment ID for the model
    model_id: Optional[str]
        the model id
    Returns
    -------
    chart : alt.Chart
        An Altair Chart for feature impact will appear automatically in Jupyter environments

    """
    if model:
        model_id, project_id = _unpack_model_ids(model)
    assert model_id
    assert project_id
    fi_json = utils.create_task_new_thread(
        proj_client.get_feature_impact(model_id=model_id, pid=project_id), wait=True
    ).result()
    return render_feature_impact_chart(fi_json)


def render_roc_curve_chart(roc_json: Union[Dict[str, Any], None]) -> alt.Chart:
    """Render altair roc curve."""
    if roc_json is None:
        return render_chart_not_avialble("ROC Curve")
    roc_chart_data = pd.DataFrame(roc_json["rocPoints"])
    base_chart = (
        alt.Chart(roc_chart_data, title="ROC Curve", width=400)
        .mark_line()
        .encode(
            x=alt.X("falsePositiveScore:Q", title="False Positive Rate"),
            y=alt.Y("truePositiveScore:Q", title="True Positive Rate"),
        )
    )
    line_data = pd.DataFrame(
        [roc_chart_data.min(), roc_chart_data.max()],
        columns=["falsePositiveScore", "truePositiveScore"],
    )
    line_chart = (
        alt.Chart(line_data)
        .mark_line(color="grey", strokeDash=[6, 4])
        .encode(x="falsePositiveScore:Q", y="truePositiveScore:Q")
    )
    return base_chart + line_chart


def roc_curve_chart(
    model: Optional[Union["Model", "ModelOperator"]] = None,
    *,
    project_id: Optional[str] = None,
    model_id: Optional[str] = None,
    ds_id: Optional[str] = None,
) -> alt.Chart:
    """
    Shows a chart of the ROC curve for the input binary model.

    Either model or project_id/model_id together must be supplied

    Parameters
    ----------
    model : Optional[Union["Model", "ModelOperator"]]
        A DrX Model Object
    project_id: Optional[str]
        The DataRobot Project or Experiment ID for the model
    model_id: Optional[str]
        the model id
    ds_id: Optional[str]
        A project dataset id for an external test
    Returns
    -------
    chart : alt.Chart
        An Altair Chart for feature impact will appear automatically in Jupyter environments

    """
    if model:
        model_id, project_id = _unpack_model_ids(model)
    assert model_id
    assert project_id
    if ds_id is not None:
        roc_json = utils.create_task_new_thread(
            proj_client.get_dataset_roc_data(project_id, model_id, ds_id), wait=True
        ).result()
    else:
        roc_json = utils.create_task_new_thread(
            proj_client.get_roc_data(project_id, model_id), wait=True
        ).result()
    return render_roc_curve_chart(roc_json)


def _render_binary_lift_chart(lift_json: Dict[str, Any]) -> alt.Chart:
    lift_chart_data = pd.DataFrame(lift_json["bins"])
    lift_chart_data = (
        lift_chart_data.reset_index()
        .assign(Bin=lambda df: df["index"] + 1)
        .drop(columns="index")
        .melt(id_vars=["Bin", "binWeight"])
        .sort_values(by="Bin")
    )
    chart = (
        alt.Chart(lift_chart_data.reset_index(), title="Lift Chart", width=400)
        .mark_line()
        .encode(
            x=alt.X("Bin:Q"),
            y=alt.Y("value:Q", title="Average Target Value"),
            color=alt.Color("variable:N", title="Predictions"),
            tooltip=["binWeight"],
        )
    )
    return chart


def _render_multiclass_lift_chart(lift_json: Dict[str, Any]) -> alt.Chart:
    NUMBER_OF_BINS = 10

    base_data = [
        pd.DataFrame(row["bins"]).assign(
            class_name=row["targetClass"], bin=lambda df: df.iloc[:, 0].expanding().count()
        )
        for row in lift_json["classBins"]
    ]

    adjusted_for_bin_number = pd.concat(
        [
            frame.groupby(pd.qcut(frame["bin"], q=NUMBER_OF_BINS, labels=False))
            .agg({"actual": "mean", "predicted": "mean", "class_name": "max"})
            .reset_index()
            for frame in base_data
        ]
    )

    melted_data = adjusted_for_bin_number.melt(
        id_vars=["bin", "class_name"], value_vars=["actual", "predicted"]
    )

    input_dropdown = alt.binding_select(
        options=adjusted_for_bin_number.class_name.value_counts().index.values, name="Class Label: "
    )

    selection = alt.selection_single(
        fields=["class_name"],
        bind=input_dropdown,
        init={"class_name": adjusted_for_bin_number.class_name.value_counts().index.values[0]},
    )

    chart = (
        alt.Chart(melted_data, title="Multclass Lift Chart")
        .mark_line(point=True, interpolate="linear", strokeOpacity=0.75)
        .encode(
            x=alt.X("bin:O"),
            y=alt.Y("value"),
            color=alt.Color(
                "variable:N",
                scale=alt.Scale(
                    domain=["actual", "predicted"], range=[viz.QUALITATIVE[3], viz.QUALITATIVE[0]]
                ),
            ),
        )
        .add_selection(selection)
        .transform_filter(selection)
    )
    return chart


def render_lift_chart(lift_json: Union[Dict[str, Any], None]) -> alt.Chart:
    """Render altair lift chart."""
    if lift_json is None:
        return render_chart_not_avialble("Lift Chart")
    if "bins" in lift_json.keys():
        return _render_binary_lift_chart(lift_json)
    else:
        return _render_multiclass_lift_chart(lift_json)


def lift_chart(
    model: Optional[Union["Model", "ModelOperator"]] = None,
    *,
    project_id: Optional[str] = None,
    model_id: Optional[str] = None,
    ds_id: Optional[str] = None,
) -> alt.Chart:
    """
    Shows a lift chart for the input model.

    Either model or project_id/model_id together must be supplied

    Parameters
    ----------
    model : Optional[Union["Model", "ModelOperator"]]
        A DrX Model Object
    project_id: Optional[str]
        The DataRobot Project or Experiment ID for the model
    model_id: Optional[str]
        the model id
    ds_id: Optional[str]
        A project dataset id for an external test
    Returns
    -------
    chart : alt.Chart
        An Altair Chart for feature impact will appear automatically in Jupyter environments

    """
    if model:
        model_id, project_id = _unpack_model_ids(model)
        assert model_id
    assert project_id
    assert model_id
    if ds_id is not None:
        lift_json = utils.create_task_new_thread(
            proj_client.get_dataset_liftchart_data(project_id, model_id, ds_id), wait=True
        ).result()
    else:
        lift_json = utils.create_task_new_thread(
            proj_client.get_liftchart_data(project_id, model_id), wait=True
        ).result()
    return render_lift_chart(lift_json)


def render_residuals_chart(residuals_json: Union[Dict[str, Any], None]) -> alt.Chart:
    """Render residuals altair chart."""
    if residuals_json is None:
        return render_chart_not_avialble("Residuals Chart")
    residuals_data = pd.DataFrame(
        residuals_json["data"],
        columns=["Actual", "Predicted", "Residual", "Row Number"],
    )
    chart = (
        alt.Chart(residuals_data, title="Residuals Chart", width=500, height=500)
        .mark_point()
        .encode(x=alt.X("Predicted:Q"), y=alt.Y("Actual:Q"), tooltip=["Residual"])
    )
    line_data = pd.DataFrame(
        [[0, 0, 0, 0], residuals_data.max().values.tolist()],
        columns=["Actual", "Predicted", "Residual", "Row Number"],
    )
    line_chart = (
        alt.Chart(line_data, width=500)
        .mark_line(color="grey", strokeDash=[6, 4], strokeOpacity=0.6)
        .encode(x=alt.X("Predicted:Q"), y=alt.Y("Actual:Q"))
    )
    return chart + line_chart


def residuals_chart(
    model: Optional[Union["Model", "ModelOperator"]] = None,
    *,
    project_id: Optional[str] = None,
    model_id: Optional[str] = None,
    dataset_id: Optional[str] = None,
) -> alt.Chart:
    """
    Shows a chart of the ROC curve for the input binary model.

    Either model or project_id/model_id together must be supplied

    Parameters
    ----------
    model : Optional[Union["Model", "ModelOperator"]]
        A DrX Model Object
    project_id: Optional[str]
        The DataRobot Project or Experiment ID for the model
    model_id: Optional[str]
        the model id
    dataset_id: Optional[str]
        A project dataset id for an external test
    Returns
    -------
    chart : alt.Chart
        An Altair Chart for feature impact will appear automatically in Jupyter environments

    """
    if model:
        model_id, project_id = _unpack_model_ids(model)
    assert project_id
    assert model_id
    if dataset_id is not None:
        residuals_json = utils.create_task_new_thread(
            proj_client.get_dataset_residuals_data(project_id, model_id, dataset_id), wait=True
        ).result()
    else:
        residuals_json = utils.create_task_new_thread(
            proj_client.get_residuals_data(project_id, model_id), wait=True
        ).result()
    return render_residuals_chart(residuals_json)


def shap_density_chart(
    model: Optional[Union["Model", "ModelOperator"]] = None,
    *,
    project_id: Optional[str] = None,
    model_id: Optional[str] = None,
    dataset_id: Optional[str] = None,
    partition: Optional[str] = None,
) -> alt.Chart:
    """
    Shows a violin plot of the top 20 features where
    each column is a violin showing the density of points
    and their corresponding SHAP values for the feature.

    Either model or project_id/model_id together must be supplied

    Parameters
    ----------
    model : Optional[Union["Model", "ModelOperator"]]
        A DrX Model Object
    project_id: Optional[str]
        The DataRobot Project or Experiment ID for the model
    model_id: Optional[str]
        the model id
    dataset_id: Optional[str]
        A project dataset id for an external test
    partition: Optional[str]
        either 'training' or 'validation', or 'holdout' if not supplied a specified search order will be used.
    Returns
    -------
    chart : alt.Chart
        An Altair Chart for feature impact will appear automatically in Jupyter environments

    """
    if model:
        model_id, project_id = _unpack_model_ids(model)
    assert model_id
    assert project_id
    if (dataset_id is not None) and (partition is not None):
        raise ValueError("""Choose dataset or partition type not both""")
    if dataset_id:
        shap_matrix = utils.create_task_new_thread(
            proj_client.get_shap_matrix(model_id=model_id, dataset_id=dataset_id)
        ).result()
    elif partition:
        shap_matrix = utils.create_task_new_thread(
            proj_client.get_shap_matrix(model_id=model_id, data_partition=partition)
        ).result()
    else:
        shap_matrix = utils.create_task_new_thread(
            proj_client.get_shap_matrix(model_id=model_id, data_partition=partition)
        ).result()
    return render_shap_density_chart(shap_matrix)


def render_shap_density_chart(shap_json: Dict[str, Any]) -> alt.Chart:
    dtc = pd.DataFrame(shap_json["matrix"], columns=shap_json["colnames"])
    if len(dtc.columns) > 20:
        top_columns = dtc.mean().sort_values(ascending=False).index.to_list()[0:20]
        dtc = dtc[top_columns]
    dtc = dtc.melt(value_vars=dtc.columns, var_name="feature")
    if len(dtc) > 5000:
        dtc = dtc.sample(5000)
    extent = (
        [dtc.value.min(), dtc.value.max()]
        if (dtc.value.std() / dtc.value.mean() < 2.0)
        else [dtc.value.quantile(q=0.1), dtc.value.quantile(q=0.9)]
    )

    return (
        alt.Chart(dtc, title="SHAP Density Chart", width=800)
        .transform_density("value", as_=["value", "density"], extent=extent, groupby=["feature"])
        .mark_area(orient="horizontal")
        .encode(
            y=alt.Y("value:Q", title="SHAP Value", scale=alt.Scale(type="linear")),
            color=alt.Color("feature:N", title="Feature"),
            x=alt.X(
                "density:Q",
                stack="center",
                impute=None,
                title=None,
                axis=alt.Axis(labels=False, values=[0, 1], grid=False, ticks=True),
            ),
            column=alt.Row(
                "feature:N",
                header=alt.Header(
                    titleOrient="bottom",
                    labelOrient="bottom",
                    labelPadding=-11,
                ),
                title="Feature",
            ),
        )
        .properties(width=100)
        .configure_facet(spacing=0)
        .configure_view(stroke=None)
    )


def partial_dependence_plot(
    model: Optional[Union["Model", "ModelOperator"]] = None,
    *,
    project_id: Optional[str] = None,
    model_id: Optional[str] = None,
    partition: Optional[str] = None,
) -> alt.Chart:
    """
    Shows partial dependence plots for up to 20 features arranged in
    rows of 2 plots each.

    Either model or project_id/model_id together must be supplied

    Parameters
    ----------
    model : Optional[Union["Model", "ModelOperator"]]
        A DrX Model Object
    project_id: Optional[str]
        The DataRobot Project or Experiment ID for the model
    model_id: Optional[str]
        the model id
    partition: Optional[str]
        Either 'training','validation' or 'holdout'
    Returns
    -------
    chart : alt.Chart
        An Altair Chart for feature impact will appear automatically in Jupyter environments

    """
    if model and project_id is None:
        model_id, project_id = _unpack_model_ids(model)
    assert model_id
    assert project_id
    feature_effects = utils.create_task_new_thread(
        proj_client.get_feature_effects(
            project_id=project_id, model_id=model_id, data_partition=partition
        )
    ).result()
    return render_partial_dependence_plot(feature_effects)


def render_partial_dependence_plot(feature_effects_json: List[Dict[str, Any]]) -> alt.Chart:
    frames = []
    for feature in feature_effects_json:
        base_frame = pd.DataFrame(feature["partialDependence"]["data"])
        base_frame["feature"] = feature["featureName"]
        frames.append(base_frame)

    def identify_label_type(feature_df: pd.DataFrame) -> str:
        values = feature_df.label.head().to_list()
        outs = []
        for v in values:
            try:
                float(v)
                outs.append("Q")
            except ValueError:
                outs.append("N")
        if all(map(lambda v: v == "Q", outs)):
            return "Q"
        else:
            return "N"

    dtc = pd.concat(frames, axis=0)
    features = dtc.feature.value_counts().index.to_list()
    charts = []
    for f in features:
        sub_chart_data = dtc[dtc.feature == f].sort_values("label")
        label_type = identify_label_type(sub_chart_data)
        base = alt.Chart(sub_chart_data, title=f"PDP: {f}", width=300).encode(
            x=alt.X(f"label:{label_type}", title="Feature Values"),
            y=alt.Y("dependence:Q", title="Target Value", scale=alt.Scale(zero=False)),
        )
        if label_type == "Q":
            charts.append(base.mark_line())
        else:
            charts.append(base.mark_point())
    number_of_rows = math.ceil(len(charts) / 2)
    rows = []
    charts_to_add = iter(charts)
    for row in range(number_of_rows):
        # fill rows of two charts each
        row = alt.hconcat()
        for _ in range(2):
            try:
                row |= next(charts_to_add)
                rows.append(row)
            except StopIteration:
                break

    return alt.vconcat(*rows)
