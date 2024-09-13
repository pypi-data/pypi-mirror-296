from collections.abc import Iterator
from functools import cache

from allotropy.allotrope.models.adm.pcr.benchling._2023._09.qpcr import ExperimentType
from allotropy.parsers.appbio_quantstudio.appbio_quantstudio_structure import (
    WellItem,
)
from allotropy.parsers.appbio_quantstudio.appbio_quantstudio_views import (
    SampleView,
    TargetRoleView,
    TargetView,
)
from allotropy.parsers.appbio_quantstudio.views import ViewData
from allotropy.parsers.utils.calculated_data_documents.definition import (
    CalculatedDocument,
    DataSource,
)
from allotropy.parsers.utils.uuids import random_uuid_str
from allotropy.parsers.utils.values import assert_not_none


@cache
def build_quantity(well_item: WellItem) -> CalculatedDocument | None:
    if (quantity := well_item.result.quantity) is None:
        return None

    data_sources = []
    if well_item.result.cycle_threshold_result is not None:
        data_sources.append(
            DataSource(feature="cycle threshold result", reference=well_item)
        )

    if well_item.result.y_intercept is not None:
        data_sources.append(DataSource(feature="y-intercept", reference=well_item))

    if well_item.result.slope is not None:
        data_sources.append(DataSource(feature="slope", reference=well_item))

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="quantity",
        value=quantity,
        data_sources=data_sources,
    )


@cache
def build_quantity_mean(
    view_data: ViewData[WellItem], sample: str, target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (quantity_mean := well_items[0].result.quantity_mean) is None:
        return None

    data_sources = []
    for well_item in well_items:
        quantity_ref = build_quantity(well_item)
        if quantity_ref is None:
            return None

        data_sources.append(
            DataSource(
                feature="quantity",
                reference=quantity_ref,
            )
        )

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="quantity mean",
        value=quantity_mean,
        data_sources=data_sources,
    )


@cache
def build_quantity_sd(
    view_data: ViewData[WellItem], sample: str, target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (quantity_sd := well_items[0].result.quantity_sd) is None:
        return None

    data_sources = []
    for well_item in well_items:
        quantity_ref = build_quantity(well_item)
        if quantity_ref is None:
            return None

        data_sources.append(
            DataSource(
                feature="quantity",
                reference=quantity_ref,
            )
        )

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="quantity sd",
        value=quantity_sd,
        data_sources=data_sources,
    )


@cache
def build_ct_mean(
    view_data: ViewData[WellItem], sample: str, target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (ct_mean := well_items[0].result.ct_mean) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="ct mean",
        value=ct_mean,
        data_sources=[
            DataSource(feature="cycle threshold result", reference=well_item)
            for well_item in well_items
        ],
    )


@cache
def build_ct_sd(
    view_data: ViewData[WellItem], sample: str, target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (ct_sd := well_items[0].result.ct_sd) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="ct sd",
        value=ct_sd,
        data_sources=[
            DataSource(feature="cycle threshold result", reference=well_item)
            for well_item in well_items
        ],
    )


@cache
def build_delta_ct_mean(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
    r_target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (delta_ct_mean := well_items[0].result.delta_ct_mean) is None:
        return None

    ct_mean_ref = build_ct_mean(view_data, sample, target)
    if ct_mean_ref is None:
        return None

    r_ct_mean_ref = build_ct_mean(view_data, sample, r_target)
    if r_ct_mean_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="delta ct mean",
        value=delta_ct_mean,
        data_sources=[
            DataSource(
                feature="ct mean",
                reference=ct_mean_ref,
            ),
            DataSource(
                feature="ct mean",
                reference=r_ct_mean_ref,
            ),
        ],
    )


@cache
def build_delta_ct_se(
    view_data: ViewData[WellItem], sample: str, target: str, r_target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (delta_ct_se := well_items[0].result.delta_ct_se) is None:
        return None

    ct_mean_ref = build_ct_mean(view_data, sample, target)
    if ct_mean_ref is None:
        return None

    r_ct_mean_ref = build_ct_mean(view_data, sample, r_target)
    if r_ct_mean_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="delta ct se",
        value=delta_ct_se,
        data_sources=[
            DataSource(feature="ct mean", reference=ct_mean_ref),
            DataSource(feature="ct mean", reference=r_ct_mean_ref),
        ],
    )


@cache
def build_delta_delta_ct(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
    r_sample: str,
    r_target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (delta_delta_ct := well_items[0].result.delta_delta_ct) is None:
        return None

    delta_ct_mean_ref = build_delta_ct_mean(view_data, sample, target, r_target)
    if delta_ct_mean_ref is None:
        return None

    r_delta_ct_mean_ref = build_delta_ct_mean(view_data, r_sample, target, r_target)
    if r_delta_ct_mean_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="delta delta ct",
        value=delta_delta_ct,
        data_sources=[
            DataSource(
                feature="delta ct mean",
                reference=delta_ct_mean_ref,
            ),
            DataSource(
                feature="delta ct mean",
                reference=r_delta_ct_mean_ref,
            ),
        ],
    )


@cache
def build_rq(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
    r_sample: str,
    r_target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rq := well_items[0].result.rq) is None:
        return None

    delta_delta_ct_ref = build_delta_delta_ct(
        view_data, sample, target, r_sample, r_target
    )
    if delta_delta_ct_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rq",
        value=rq,
        data_sources=[
            DataSource(
                feature="delta delta ct",
                reference=delta_delta_ct_ref,
            )
        ],
    )


@cache
def build_rq_min(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
    r_sample: str,
    r_target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rq_min := well_items[0].result.rq_min) is None:
        return None

    rq_ref = build_rq(view_data, sample, target, r_sample, r_target)
    if rq_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rq min",
        value=rq_min,
        data_sources=[
            DataSource(
                feature="rq",
                reference=rq_ref,
            )
        ],
    )


@cache
def build_rq_max(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
    r_sample: str,
    r_target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rq_max := well_items[0].result.rq_max) is None:
        return None

    rq_ref = build_rq(view_data, sample, target, r_sample, r_target)
    if rq_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rq max",
        value=rq_max,
        data_sources=[
            DataSource(
                feature="rq",
                reference=rq_ref,
            ),
        ],
    )


@cache
def build_relative_rq(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rq := well_items[0].result.rq) is None:
        return None

    quantity_mean_ref = build_quantity_mean(view_data, sample, target)
    if quantity_mean_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rq",
        value=rq,
        data_sources=[
            DataSource(
                feature="quantity mean",
                reference=quantity_mean_ref,
            )
        ],
    )


@cache
def build_relative_rq_min(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rq_min := well_items[0].result.rq_min) is None:
        return None

    relative_rq_ref = build_relative_rq(view_data, sample, target)
    if relative_rq_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rq min",
        value=rq_min,
        data_sources=[
            DataSource(
                feature="rq",
                reference=relative_rq_ref,
            )
        ],
    )


@cache
def build_relative_rq_max(
    view_data: ViewData[WellItem],
    sample: str,
    target: str,
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rq_max := well_items[0].result.rq_max) is None:
        return None

    relative_rq_ref = build_relative_rq(view_data, sample, target)
    if relative_rq_ref is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rq max",
        value=rq_max,
        data_sources=[
            DataSource(
                feature="rq",
                reference=relative_rq_ref,
            ),
        ],
    )


@cache
def build_rn_mean(
    view_data: ViewData[WellItem], sample: str, target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rn_mean := well_items[0].result.rn_mean) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rn mean",
        value=rn_mean,
        data_sources=[
            DataSource(feature="normalized reporter result", reference=well_item)
            for well_item in well_items
        ],
    )


@cache
def build_rn_sd(
    view_data: ViewData[WellItem], sample: str, target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(sample, target)
    if (rn_sd := well_items[0].result.rn_sd) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="rn sd",
        value=rn_sd,
        data_sources=[
            DataSource(feature="normalized reporter result", reference=well_item)
            for well_item in well_items
        ],
    )


@cache
def build_y_intercept(
    view_data: ViewData[WellItem], target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(target)
    if (y_intercept := well_items[0].result.y_intercept) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="y intercept",
        value=y_intercept,
        data_sources=[
            DataSource(feature="cycle threshold result", reference=well_item)
            for well_item in well_items
        ],
    )


@cache
def build_r_squared(
    view_data: ViewData[WellItem], target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(target)
    if (r_squared := well_items[0].result.r_squared) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="r^2",
        value=r_squared,
        data_sources=[
            DataSource(feature="cycle threshold result", reference=well_item)
            for well_item in well_items
        ],
    )


@cache
def build_slope(
    view_data: ViewData[WellItem], target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(target)
    if (slope := well_items[0].result.slope) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="slope",
        value=slope,
        data_sources=[
            DataSource(feature="cycle threshold result", reference=well_item)
            for well_item in well_items
        ],
    )


@cache
def build_efficiency(
    view_data: ViewData[WellItem], target: str
) -> CalculatedDocument | None:
    well_items = view_data.get_leaf_item(target)
    if (efficiency := well_items[0].result.efficiency) is None:
        return None

    return CalculatedDocument(
        uuid=random_uuid_str(),
        name="efficiency",
        value=efficiency,
        data_sources=[
            DataSource(feature="cycle threshold result", reference=well_item)
            for well_item in well_items
        ],
    )


def iter_comparative_ct_calc_docs(
    view_data: ViewData[WellItem],
    r_sample: str,
    r_target: str,
) -> Iterator[CalculatedDocument]:
    # Quantity, Quantity Mean, Quantity SD, Ct Mean, Ct SD, Delta Ct Mean,
    # Delta Ct SE, Delta Delta Ct, RQ, RQ min, RQ max
    for sample, target in view_data.iter_keys():
        if calc_doc := build_quantity_mean(view_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_quantity_sd(view_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_ct_sd(view_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_delta_ct_se(view_data, sample, target, r_target):
            yield from calc_doc.iter_struct()

        if target != r_target:
            if calc_doc := build_rq_min(view_data, sample, target, r_sample, r_target):
                yield from calc_doc.iter_struct()

            if calc_doc := build_rq_max(view_data, sample, target, r_sample, r_target):
                yield from calc_doc.iter_struct()


def iter_standard_curve_calc_docs(
    view_st_data: ViewData[WellItem],
    view_tr_data: ViewData[WellItem],
) -> Iterator[CalculatedDocument]:
    # Quantity, Quantity Mean, Quantity SD, Ct Mean, Ct SD, Y-Intercept,
    # R(superscript 2), Slope, Efficiency
    for sample, target in view_st_data.iter_keys():
        if calc_doc := build_quantity_mean(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_quantity_sd(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_ct_mean(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_ct_sd(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

    for target in view_tr_data.data:
        if calc_doc := build_y_intercept(view_tr_data, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_r_squared(view_tr_data, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_slope(view_tr_data, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_efficiency(view_tr_data, target):
            yield from calc_doc.iter_struct()


def iter_relative_standard_curve_calc_docs(
    view_st_data: ViewData[WellItem],
    view_tr_data: ViewData[WellItem],
) -> Iterator[CalculatedDocument]:
    # Quantity, Quantity Mean, Quantity SD, Ct Mean, Ct SD, RQ, RQ min,
    # RQ max, Y-Intercept, R(superscript 2), Slope, Efficiency
    for sample, target in view_st_data.iter_keys():
        if calc_doc := build_quantity_mean(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_quantity_sd(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_ct_mean(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_ct_sd(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_relative_rq_min(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_relative_rq_max(view_st_data, sample, target):
            yield from calc_doc.iter_struct()

    for target in view_tr_data.data:
        if calc_doc := build_y_intercept(view_tr_data, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_r_squared(view_tr_data, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_slope(view_tr_data, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_efficiency(view_tr_data, target):
            yield from calc_doc.iter_struct()


def iter_presence_absence_calc_docs(
    view_data: ViewData[WellItem],
) -> Iterator[CalculatedDocument]:
    # Rn Mean, Rn SD
    for sample, target in view_data.iter_keys():
        if calc_doc := build_rn_mean(view_data, sample, target):
            yield from calc_doc.iter_struct()

        if calc_doc := build_rn_sd(view_data, sample, target):
            yield from calc_doc.iter_struct()


def iter_calculated_data_documents(
    well_items: list[WellItem],
    experiment_type: ExperimentType,
    r_sample: str | None,
    r_target: str | None,
) -> Iterator[CalculatedDocument]:
    view_st = SampleView(sub_view=TargetView())
    view_st_data = view_st.apply(well_items)

    view_tr = TargetRoleView()
    view_tr_data = view_tr.apply(well_items)

    if experiment_type == ExperimentType.relative_standard_curve_qPCR_experiment:
        yield from iter_relative_standard_curve_calc_docs(
            view_st_data,
            view_tr_data,
        )
    elif experiment_type == ExperimentType.comparative_CT_qPCR_experiment:
        yield from iter_comparative_ct_calc_docs(
            view_st_data,
            assert_not_none(r_sample),
            assert_not_none(r_target),
        )
    elif experiment_type == ExperimentType.standard_curve_qPCR_experiment:
        yield from iter_standard_curve_calc_docs(
            view_st_data,
            view_tr_data,
        )
    elif experiment_type == ExperimentType.presence_absence_qPCR_experiment:
        yield from iter_presence_absence_calc_docs(
            view_st_data,
        )
