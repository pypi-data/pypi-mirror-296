from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import Literal, final

from ..._constant import Constant
from ..._identification import (
    ColumnIdentifier,
    ExternalColumnIdentifier,
    ExternalTableIdentifier,
    Identifiable,
    TableIdentifier,
    identify,
)
from ..._operation import Condition
from ._external_measure import ExternalMeasure

_Filter = Condition[
    ColumnIdentifier,
    Literal["eq", "isin"],
    Constant,
    Literal["and"] | None,
]


@final
@dataclass(frozen=True, init=False, kw_only=True)
class ExternalAggregateTable:
    """An external aggregate table is a table in the external database containing aggregated data.

    It is used to feed some partial providers faster.
    For instance, if the same aggregate query is run every day to feed the same partial provider with the same data, the result of the query can instead be stored into an external table and this table used to feed the provider every day.
    """

    _granular_table: TableIdentifier
    _aggregate_table: ExternalTableIdentifier
    _mapping: Mapping[ColumnIdentifier, ExternalColumnIdentifier]
    _measures: tuple[ExternalMeasure, ...]
    _filter: _Filter | None = None

    def __init__(
        self,
        *,
        granular_table: Identifiable[TableIdentifier],
        aggregate_table: Identifiable[ExternalTableIdentifier],
        mapping: Mapping[
            Identifiable[ColumnIdentifier],
            Identifiable[ExternalColumnIdentifier],
        ],
        measures: Collection[ExternalMeasure],
        filter: _Filter | None = None,  # noqa: A002
    ):
        """Initialize an external aggregate table.

        Args:
            granular_table: The table containing the granular facts, i.e. the fact table of which the data have been aggregated into the aggregate table.
            aggregate_table: The aggregate table.
            mapping: The mapping from one column in *granular_table* (or a table joined to it) to the corresponding column in *aggregate_table*.
            measures: The measures provided by *aggregate_table*.
            filter: The condition on the granular columns describing which facts have been pre-aggregated into the external table.
                The columns used in the condition must be keys of *mapping*.
        """
        object.__setattr__(self, "_granular_table", identify(granular_table))
        object.__setattr__(self, "_aggregate_table", identify(aggregate_table))
        object.__setattr__(
            self,
            "_mapping",
            {
                identify(granular_column): identify(aggregate_column)
                for granular_column, aggregate_column in mapping.items()
            },
        )
        object.__setattr__(self, "_measures", tuple(measures))
        object.__setattr__(self, "_filter", filter)
