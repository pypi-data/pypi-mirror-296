from typing import TYPE_CHECKING, Iterable, NamedTuple, Optional, Sequence, Union

import dagster._check as check
from dagster._annotations import PublicAttr
from dagster._core.definitions.asset_check_spec import AssetCheckKey
from dagster._core.definitions.asset_spec import AssetSpec
from dagster._core.definitions.events import AssetKey, CoercibleToAssetKey
from dagster._core.definitions.partition_mapping import (
    PartitionMapping,
    warn_if_partition_mapping_not_builtin,
)
from dagster._core.definitions.source_asset import SourceAsset
from dagster._core.errors import DagsterInvalidDefinitionError, DagsterInvariantViolationError

if TYPE_CHECKING:
    from dagster._core.definitions.assets import AssetsDefinition


CoercibleToAssetDep = Union[
    CoercibleToAssetKey, AssetSpec, "AssetsDefinition", SourceAsset, "AssetDep"
]


class AssetDep(
    NamedTuple(
        "_AssetDep",
        [
            ("asset_key", PublicAttr[AssetKey]),
            ("partition_mapping", PublicAttr[Optional[PartitionMapping]]),
        ],
    )
):
    """Specifies a dependency on an upstream asset.

    Attributes:
        asset (Union[AssetKey, str, AssetSpec, AssetsDefinition, SourceAsset]): The upstream asset to depend on.
        partition_mapping (Optional[PartitionMapping]): Defines what partitions to depend on in
            the upstream asset. If not provided and the upstream asset is partitioned, defaults to
            the default partition mapping for the partitions definition, which is typically maps
            partition keys to the same partition keys in upstream assets.

    Examples:
        .. code-block:: python

            upstream_asset = AssetSpec("upstream_asset")
            downstream_asset = AssetSpec(
                "downstream_asset",
                deps=[
                    AssetDep(
                        upstream_asset,
                        partition_mapping=TimeWindowPartitionMapping(start_offset=-1, end_offset=-1)
                    )
                ]
            )
    """

    def __new__(
        cls,
        asset: Union[CoercibleToAssetKey, AssetSpec, "AssetsDefinition", SourceAsset],
        *,
        partition_mapping: Optional[PartitionMapping] = None,
    ):
        from dagster._core.definitions.assets import AssetsDefinition

        if isinstance(asset, list):
            check.list_param(asset, "asset", of_type=str)
        else:
            check.inst_param(
                asset, "asset", (AssetKey, str, AssetSpec, AssetsDefinition, SourceAsset)
            )
        if isinstance(asset, AssetsDefinition) and len(asset.keys) > 1:
            # Only AssetsDefinition with a single asset can be passed
            raise DagsterInvalidDefinitionError(
                "Cannot create an AssetDep from a multi_asset AssetsDefinition."
                " Instead, specify dependencies on the assets created by the multi_asset"
                f" via AssetKeys or strings. For the multi_asset {asset.node_def.name}, the"
                f" available keys are: {asset.keys}."
            )

        asset_key = _get_asset_key(asset)

        if partition_mapping:
            warn_if_partition_mapping_not_builtin(partition_mapping)

        return super().__new__(
            cls,
            asset_key=asset_key,
            partition_mapping=check.opt_inst_param(
                partition_mapping,
                "partition_mapping",
                PartitionMapping,
            ),
        )

    @staticmethod
    def from_coercible(arg: "CoercibleToAssetDep") -> "AssetDep":
        # if arg is AssetDep, return the original object to retain partition_mapping
        return arg if isinstance(arg, AssetDep) else AssetDep(asset=arg)


def _get_asset_key(arg: "CoercibleToAssetDep") -> AssetKey:
    from dagster._core.definitions.assets import AssetsDefinition

    if isinstance(arg, (AssetsDefinition, SourceAsset, AssetSpec)):
        return arg.key
    elif isinstance(arg, AssetDep):
        return arg.asset_key
    else:
        return AssetKey.from_coercible(arg)


def coerce_to_deps_and_check_duplicates(
    coercible_to_asset_deps: Optional[Iterable["CoercibleToAssetDep"]],
    key: Union[AssetKey, AssetCheckKey],
) -> Sequence[AssetDep]:
    dep_set = {}
    if coercible_to_asset_deps:
        for dep in coercible_to_asset_deps:
            asset_dep = AssetDep.from_coercible(dep)

            # we cannot do deduplication via a set because MultiPartitionMappings have an internal
            # dictionary that cannot be hashed. Instead deduplicate by making a dictionary and checking
            # for existing keys.
            if asset_dep.asset_key in dep_set.keys():
                raise DagsterInvariantViolationError(
                    f"Cannot set a dependency on asset {asset_dep.asset_key} more than once for"
                    f" spec {key}"
                )
            dep_set[asset_dep.asset_key] = asset_dep

    return list(dep_set.values())
