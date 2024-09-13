from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING, Any, Iterable, Mapping, NamedTuple, Optional, Sequence, Set

import dagster._check as check
from dagster._annotations import PublicAttr, experimental_param
from dagster._core.definitions.auto_materialize_policy import AutoMaterializePolicy
from dagster._core.definitions.declarative_automation.automation_condition import (
    AutomationCondition,
)
from dagster._core.definitions.events import AssetKey, CoercibleToAssetKey
from dagster._core.definitions.freshness_policy import FreshnessPolicy
from dagster._core.definitions.partition import PartitionsDefinition
from dagster._core.definitions.partition_mapping import PartitionMapping
from dagster._core.definitions.utils import (
    resolve_automation_condition,
    validate_asset_owner,
    validate_group_name,
    validate_tags_strict,
)
from dagster._core.errors import DagsterInvalidDefinitionError
from dagster._core.storage.tags import KIND_PREFIX
from dagster._serdes.serdes import whitelist_for_serdes
from dagster._utils.internal_init import IHasInternalInit

if TYPE_CHECKING:
    from dagster._core.definitions.asset_dep import AssetDep, CoercibleToAssetDep

# SYSTEM_METADATA_KEY_ASSET_EXECUTION_TYPE lives on the metadata of an asset
# (which currently ends up on the Output associated with the asset key)
# whih encodes the execution type the of asset. "Unexecutable" assets are assets
# that cannot be materialized in Dagster, but can have events in the event
# log keyed off of them, making Dagster usable as a observability and lineage tool
# for externally materialized assets.
SYSTEM_METADATA_KEY_ASSET_EXECUTION_TYPE = "dagster/asset_execution_type"


# SYSTEM_METADATA_KEY_IO_MANAGER_KEY lives on the metadata of an asset without a node def and
# determines the io_manager_key that can be used to load it. This is necessary because IO manager
# keys are otherwise encoded inside OutputDefinitions within NodeDefinitions.
SYSTEM_METADATA_KEY_IO_MANAGER_KEY = "dagster/io_manager_key"

# SYSTEM_METADATA_KEY_AUTO_OBSERVE_INTERVAL_MINUTES lives on the metadata of
# external assets resulting from a source asset conversion. It contains the
# `auto_observe_interval_minutes` value from the source asset and is consulted
# in the auto-materialize daemon. It should eventually be eliminated in favor
# of an implementation of `auto_observe_interval_minutes` in terms of
# `AutoMaterializeRule`.
SYSTEM_METADATA_KEY_AUTO_OBSERVE_INTERVAL_MINUTES = "dagster/auto_observe_interval_minutes"

# SYSTEM_METADATA_KEY_AUTO_CREATED_STUB_ASSET lives on the metadata of external assets that are
# created for undefined but referenced assets during asset graph normalization. For example, in the
# below definitions, `foo` is referenced by upstream `bar` but has no corresponding definition:
#
#
#     @asset(deps=["foo"])
#     def bar(context: AssetExecutionContext):
#         ...
#
#     defs=Definitions(assets=[bar])
#
# During normalization we create a "stub" definition for `foo` and attach this metadata to it.
SYSTEM_METADATA_KEY_AUTO_CREATED_STUB_ASSET = "dagster/auto_created_stub_asset"


@whitelist_for_serdes
class AssetExecutionType(Enum):
    OBSERVATION = "OBSERVATION"
    UNEXECUTABLE = "UNEXECUTABLE"
    MATERIALIZATION = "MATERIALIZATION"


@experimental_param(param="owners")
@experimental_param(param="tags")
class AssetSpec(
    NamedTuple(
        "_AssetSpec",
        [
            ("key", PublicAttr[AssetKey]),
            ("deps", PublicAttr[Iterable["AssetDep"]]),
            ("description", PublicAttr[Optional[str]]),
            ("metadata", PublicAttr[Mapping[str, Any]]),
            ("group_name", PublicAttr[Optional[str]]),
            ("skippable", PublicAttr[bool]),
            ("code_version", PublicAttr[Optional[str]]),
            ("freshness_policy", PublicAttr[Optional[FreshnessPolicy]]),
            ("automation_condition", PublicAttr[Optional[AutomationCondition]]),
            ("owners", PublicAttr[Sequence[str]]),
            ("tags", PublicAttr[Mapping[str, str]]),
            ("partitions_def", PublicAttr[Optional[PartitionsDefinition]]),
        ],
    ),
    IHasInternalInit,
):
    """Specifies the core attributes of an asset, except for the function that materializes or
    observes it.

    An asset spec plus any materialization or observation function for the asset constitutes an
    "asset definition".

    Attributes:
        key (AssetKey): The unique identifier for this asset.
        deps (Optional[AbstractSet[AssetKey]]): The asset keys for the upstream assets that
            materializing this asset depends on.
        description (Optional[str]): Human-readable description of this asset.
        metadata (Optional[Dict[str, Any]]): A dict of static metadata for this asset.
            For example, users can provide information about the database table this
            asset corresponds to.
        skippable (bool): Whether this asset can be omitted during materialization, causing downstream
            dependencies to skip.
        group_name (Optional[str]): A string name used to organize multiple assets into groups. If
            not provided, the name "default" is used.
        code_version (Optional[str]): The version of the code for this specific asset,
            overriding the code version of the materialization function
        freshness_policy (Optional[FreshnessPolicy]): (Deprecated) A policy which indicates how up
            to date this asset is intended to be.
        auto_materialize_policy (Optional[AutoMaterializePolicy]): AutoMaterializePolicy to apply to
            the specified asset.
        backfill_policy (Optional[BackfillPolicy]): BackfillPolicy to apply to the specified asset.
        owners (Optional[Sequence[str]]): A list of strings representing owners of the asset. Each
            string can be a user's email address, or a team name prefixed with `team:`,
            e.g. `team:finops`.
        tags (Optional[Mapping[str, str]]): Tags for filtering and organizing. These tags are not
            attached to runs of the asset.
        partitions_def (Optional[PartitionsDefinition]): Defines the set of partition keys that
            compose the asset.
    """

    def __new__(
        cls,
        key: CoercibleToAssetKey,
        *,
        deps: Optional[Iterable["CoercibleToAssetDep"]] = None,
        description: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        skippable: bool = False,
        group_name: Optional[str] = None,
        code_version: Optional[str] = None,
        freshness_policy: Optional[FreshnessPolicy] = None,
        automation_condition: Optional[AutomationCondition] = None,
        owners: Optional[Sequence[str]] = None,
        tags: Optional[Mapping[str, str]] = None,
        # TODO: FOU-243
        auto_materialize_policy: Optional[AutoMaterializePolicy] = None,
        partitions_def: Optional[PartitionsDefinition] = None,
    ):
        from dagster._core.definitions.asset_dep import coerce_to_deps_and_check_duplicates

        key = AssetKey.from_coercible(key)
        asset_deps = coerce_to_deps_and_check_duplicates(deps, key)

        validate_group_name(group_name)

        owners = check.opt_sequence_param(owners, "owners", of_type=str)
        for owner in owners:
            validate_asset_owner(owner, key)

        kind_tags = {tag_key for tag_key in (tags or {}).keys() if tag_key.startswith(KIND_PREFIX)}
        if kind_tags is not None and len(kind_tags) > 2:
            raise DagsterInvalidDefinitionError("Assets can have at most two kinds currently.")

        return super().__new__(
            cls,
            key=key,
            deps=asset_deps,
            description=check.opt_str_param(description, "description"),
            metadata=check.opt_mapping_param(metadata, "metadata", key_type=str),
            skippable=check.bool_param(skippable, "skippable"),
            group_name=check.opt_str_param(group_name, "group_name"),
            code_version=check.opt_str_param(code_version, "code_version"),
            freshness_policy=check.opt_inst_param(
                freshness_policy,
                "freshness_policy",
                FreshnessPolicy,
            ),
            automation_condition=check.opt_inst_param(
                resolve_automation_condition(automation_condition, auto_materialize_policy),
                "automation_condition",
                AutomationCondition,
            ),
            owners=owners,
            tags=validate_tags_strict(tags) or {},
            partitions_def=check.opt_inst_param(
                partitions_def, "partitions_def", PartitionsDefinition
            ),
        )

    @staticmethod
    def dagster_internal_init(
        *,
        key: CoercibleToAssetKey,
        deps: Optional[Iterable["CoercibleToAssetDep"]],
        description: Optional[str],
        metadata: Optional[Mapping[str, Any]],
        skippable: bool,
        group_name: Optional[str],
        code_version: Optional[str],
        freshness_policy: Optional[FreshnessPolicy],
        automation_condition: Optional[AutomationCondition],
        owners: Optional[Sequence[str]],
        tags: Optional[Mapping[str, str]],
        auto_materialize_policy: Optional[AutoMaterializePolicy],
        partitions_def: Optional[PartitionsDefinition],
    ) -> "AssetSpec":
        check.invariant(auto_materialize_policy is None)
        return AssetSpec(
            key=key,
            deps=deps,
            description=description,
            metadata=metadata,
            skippable=skippable,
            group_name=group_name,
            code_version=code_version,
            freshness_policy=freshness_policy,
            automation_condition=automation_condition,
            owners=owners,
            tags=tags,
            partitions_def=partitions_def,
        )

    @cached_property
    def partition_mappings(self) -> Mapping[AssetKey, PartitionMapping]:
        return {
            dep.asset_key: dep.partition_mapping
            for dep in self.deps
            if dep.partition_mapping is not None
        }

    @property
    def auto_materialize_policy(self) -> Optional[AutoMaterializePolicy]:
        # TODO: FOU-243
        return (
            self.automation_condition.as_auto_materialize_policy()
            if self.automation_condition
            else None
        )

    @cached_property
    def kinds(self) -> Set[str]:
        return {tag[len(KIND_PREFIX) :] for tag in self.tags if tag.startswith(KIND_PREFIX)}
