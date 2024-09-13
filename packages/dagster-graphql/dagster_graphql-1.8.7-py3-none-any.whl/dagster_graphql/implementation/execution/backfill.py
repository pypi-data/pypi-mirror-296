from typing import TYPE_CHECKING, List, Sequence, Union, cast

import dagster._check as check
from dagster._core.definitions.selector import PartitionsByAssetSelector, RepositorySelector
from dagster._core.definitions.utils import is_valid_title_and_reason
from dagster._core.errors import (
    DagsterError,
    DagsterInvariantViolationError,
    DagsterUserCodeProcessError,
)
from dagster._core.events import AssetKey
from dagster._core.execution.asset_backfill import create_asset_backfill_data_from_asset_partitions
from dagster._core.execution.backfill import BulkActionStatus, PartitionBackfill
from dagster._core.execution.job_backfill import submit_backfill_runs
from dagster._core.remote_representation.external_data import ExternalPartitionExecutionErrorData
from dagster._core.utils import make_new_backfill_id
from dagster._core.workspace.permissions import Permissions
from dagster._time import datetime_from_timestamp, get_current_timestamp
from dagster._utils.caching_instance_queryer import CachingInstanceQueryer

from dagster_graphql.implementation.utils import (
    AssetBackfillPreviewParams,
    BackfillParams,
    assert_permission_for_asset_graph,
    assert_permission_for_location,
)

BACKFILL_CHUNK_SIZE = 25


if TYPE_CHECKING:
    from dagster_graphql.schema.backfill import (
        GrapheneAssetPartitions,
        GrapheneCancelBackfillSuccess,
        GrapheneLaunchBackfillSuccess,
        GrapheneResumeBackfillSuccess,
    )
    from dagster_graphql.schema.errors import GraphenePartitionSetNotFoundError
    from dagster_graphql.schema.util import ResolveInfo


def get_asset_backfill_preview(
    graphene_info: "ResolveInfo", backfill_preview_params: AssetBackfillPreviewParams
) -> Sequence["GrapheneAssetPartitions"]:
    from dagster_graphql.schema.backfill import GrapheneAssetPartitions

    asset_graph = graphene_info.context.asset_graph

    check.invariant(backfill_preview_params.get("assetSelection") is not None)
    check.invariant(backfill_preview_params.get("partitionNames") is not None)

    asset_selection = [
        cast(AssetKey, AssetKey.from_graphql_input(asset_key))
        for asset_key in backfill_preview_params["assetSelection"]
    ]
    partition_names: List[str] = backfill_preview_params["partitionNames"]

    asset_backfill_data = create_asset_backfill_data_from_asset_partitions(
        asset_graph, asset_selection, partition_names, graphene_info.context.instance
    )

    asset_partitions = []

    for asset_key in asset_backfill_data.get_targeted_asset_keys_topological_order(asset_graph):
        if asset_graph.get(asset_key).partitions_def:
            partitions_subset = asset_backfill_data.target_subset.partitions_subsets_by_asset_key[
                asset_key
            ]
            asset_partitions.append(
                GrapheneAssetPartitions(asset_key=asset_key, partitions_subset=partitions_subset)
            )
        else:
            asset_partitions.append(
                GrapheneAssetPartitions(asset_key=asset_key, partitions_subset=None)
            )

    return asset_partitions


def create_and_launch_partition_backfill(
    graphene_info: "ResolveInfo",
    backfill_params: BackfillParams,
) -> Union["GrapheneLaunchBackfillSuccess", "GraphenePartitionSetNotFoundError"]:
    from dagster_graphql.schema.backfill import GrapheneLaunchBackfillSuccess
    from dagster_graphql.schema.errors import GraphenePartitionSetNotFoundError

    backfill_id = make_new_backfill_id()

    asset_selection = (
        [
            cast(AssetKey, AssetKey.from_graphql_input(asset_key))
            for asset_key in backfill_params["assetSelection"]
        ]
        if backfill_params.get("assetSelection")
        else None
    )

    partitions_by_assets = backfill_params.get("partitionsByAssets")

    if (
        asset_selection or backfill_params.get("selector") or backfill_params.get("partitionNames")
    ) and partitions_by_assets:
        raise DagsterInvariantViolationError(
            "partitions_by_assets cannot be used together with asset_selection, selector, or"
            " partitionNames"
        )

    tags = {t["key"]: t["value"] for t in backfill_params.get("tags", [])}

    tags = {**tags, **graphene_info.context.get_viewer_tags()}

    backfill_timestamp = get_current_timestamp()

    if backfill_params.get("selector") is not None:  # job backfill
        partition_set_selector = backfill_params["selector"]
        partition_set_name = partition_set_selector.get("partitionSetName")
        repository_selector = RepositorySelector.from_graphql_input(
            partition_set_selector.get("repositorySelector")
        )
        assert_permission_for_location(
            graphene_info, Permissions.LAUNCH_PARTITION_BACKFILL, repository_selector.location_name
        )
        location = graphene_info.context.get_code_location(repository_selector.location_name)

        repository = location.get_repository(repository_selector.repository_name)
        matches = [
            partition_set
            for partition_set in repository.get_external_partition_sets()
            if partition_set.name == partition_set_selector.get("partitionSetName")
        ]
        if not matches:
            return GraphenePartitionSetNotFoundError(partition_set_name)

        if len(matches) != 1:
            raise DagsterInvariantViolationError(
                f"Partition set names must be unique: found {len(matches)} matches for {partition_set_name}"
            )
        external_partition_set = next(iter(matches))

        if backfill_params.get("allPartitions"):
            result = graphene_info.context.get_external_partition_names(
                repository_handle=repository.handle,
                job_name=external_partition_set.job_name,
                instance=graphene_info.context.instance,
                selected_asset_keys=None,
            )
            if isinstance(result, ExternalPartitionExecutionErrorData):
                raise DagsterUserCodeProcessError.from_error_info(result.error)
            partition_names = result.partition_names
        elif backfill_params.get("partitionNames"):
            partition_names = backfill_params["partitionNames"]
        else:
            raise DagsterError(
                'Backfill requested without specifying either "allPartitions" or "partitionNames" '
                "arguments"
            )

        is_valid_title, reason = is_valid_title_and_reason(backfill_params.get("title"))
        if not is_valid_title:
            raise DagsterInvariantViolationError(reason)

        backfill = PartitionBackfill(
            backfill_id=backfill_id,
            partition_set_origin=external_partition_set.get_external_origin(),
            status=BulkActionStatus.REQUESTED,
            partition_names=partition_names,
            from_failure=bool(backfill_params.get("fromFailure")),
            reexecution_steps=backfill_params.get("reexecutionSteps"),
            tags=tags,
            backfill_timestamp=backfill_timestamp,
            asset_selection=asset_selection,
            title=backfill_params.get("title"),
            description=backfill_params.get("description"),
        )

        if backfill_params.get("forceSynchronousSubmission"):
            # should only be used in a test situation
            to_submit = [name for name in partition_names]
            submitted_run_ids: List[str] = []

            while to_submit:
                chunk = to_submit[:BACKFILL_CHUNK_SIZE]
                to_submit = to_submit[BACKFILL_CHUNK_SIZE:]
                submitted_run_ids.extend(
                    run_id
                    for run_id in submit_backfill_runs(
                        graphene_info.context.instance,
                        create_workspace=lambda: graphene_info.context,
                        backfill_job=backfill,
                        partition_names_or_ranges=chunk,
                    )
                    if run_id is not None
                )
            return GrapheneLaunchBackfillSuccess(
                backfill_id=backfill_id, launched_run_ids=submitted_run_ids
            )
    elif asset_selection is not None:  # pure asset backfill
        if backfill_params.get("forceSynchronousSubmission"):
            raise DagsterError(
                "forceSynchronousSubmission is not supported for pure asset backfills"
            )

        if backfill_params.get("fromFailure"):
            raise DagsterError("fromFailure is not supported for pure asset backfills")

        asset_graph = graphene_info.context.asset_graph

        assert_permission_for_asset_graph(
            graphene_info, asset_graph, asset_selection, Permissions.LAUNCH_PARTITION_BACKFILL
        )

        backfill = PartitionBackfill.from_asset_partitions(
            asset_graph=asset_graph,
            backfill_id=backfill_id,
            tags=tags,
            backfill_timestamp=backfill_timestamp,
            asset_selection=asset_selection,
            partition_names=backfill_params.get("partitionNames"),
            dynamic_partitions_store=CachingInstanceQueryer(
                graphene_info.context.instance,
                asset_graph,
                datetime_from_timestamp(backfill_timestamp),
            ),
            all_partitions=backfill_params.get("allPartitions", False),
            title=backfill_params.get("title"),
            description=backfill_params.get("description"),
        )
    elif partitions_by_assets is not None:
        if backfill_params.get("forceSynchronousSubmission"):
            raise DagsterError(
                "forceSynchronousSubmission is not supported for pure asset backfills"
            )

        if backfill_params.get("fromFailure"):
            raise DagsterError("fromFailure is not supported for pure asset backfills")

        asset_graph = graphene_info.context.asset_graph

        partitions_by_assets = [
            PartitionsByAssetSelector.from_graphql_input(partitions_by_asset_selector)
            for partitions_by_asset_selector in partitions_by_assets
        ]

        selected_assets = list({selector.asset_key for selector in partitions_by_assets})

        assert_permission_for_asset_graph(
            graphene_info, asset_graph, selected_assets, Permissions.LAUNCH_PARTITION_BACKFILL
        )
        backfill = PartitionBackfill.from_partitions_by_assets(
            backfill_id=backfill_id,
            asset_graph=asset_graph,
            backfill_timestamp=backfill_timestamp,
            tags=tags,
            dynamic_partitions_store=CachingInstanceQueryer(
                graphene_info.context.instance,
                asset_graph,
                datetime_from_timestamp(backfill_timestamp),
            ),
            partitions_by_assets=partitions_by_assets,
            title=backfill_params.get("title"),
            description=backfill_params.get("description"),
        )
    else:
        raise DagsterError(
            "Backfill requested without specifying partition set selector or asset selection"
        )

    graphene_info.context.instance.add_backfill(backfill)
    return GrapheneLaunchBackfillSuccess(backfill_id=backfill_id)


def cancel_partition_backfill(
    graphene_info: "ResolveInfo", backfill_id: str
) -> "GrapheneCancelBackfillSuccess":
    from dagster_graphql.schema.backfill import GrapheneCancelBackfillSuccess

    backfill = graphene_info.context.instance.get_backfill(backfill_id)
    if not backfill:
        check.failed(f"No backfill found for id: {backfill_id}")

    if backfill.is_asset_backfill:
        asset_graph = graphene_info.context.asset_graph
        assert_permission_for_asset_graph(
            graphene_info,
            asset_graph,
            backfill.asset_selection,
            Permissions.CANCEL_PARTITION_BACKFILL,
        )
        graphene_info.context.instance.update_backfill(
            backfill.with_status(BulkActionStatus.CANCELING)
        )

    else:
        partition_set_origin = check.not_none(backfill.partition_set_origin)
        location_name = partition_set_origin.selector.location_name
        assert_permission_for_location(
            graphene_info, Permissions.CANCEL_PARTITION_BACKFILL, location_name
        )
        graphene_info.context.instance.update_backfill(
            backfill.with_status(BulkActionStatus.CANCELED)
        )

    return GrapheneCancelBackfillSuccess(backfill_id=backfill_id)


def resume_partition_backfill(
    graphene_info: "ResolveInfo", backfill_id: str
) -> "GrapheneResumeBackfillSuccess":
    from dagster_graphql.schema.backfill import GrapheneResumeBackfillSuccess

    backfill = graphene_info.context.instance.get_backfill(backfill_id)
    if not backfill:
        check.failed(f"No backfill found for id: {backfill_id}")

    partition_set_origin = check.not_none(backfill.partition_set_origin)
    location_name = partition_set_origin.selector.location_name
    assert_permission_for_location(
        graphene_info, Permissions.LAUNCH_PARTITION_BACKFILL, location_name
    )

    graphene_info.context.instance.update_backfill(backfill.with_status(BulkActionStatus.REQUESTED))
    return GrapheneResumeBackfillSuccess(backfill_id=backfill_id)
