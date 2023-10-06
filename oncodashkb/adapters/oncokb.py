import types as pytypes
import logging
import ontoweaver

from typing import Optional
from collections.abc import Iterable

import pandas as pd



class OncoKB(ontoweaver.tabular.PandasAdapter):

    def __init__(self,
        df: pd.DataFrame,
        config: dict,
        node_types : Optional[Iterable[ontoweaver.Node]] = None,
        node_fields: Optional[list[str]] = None,
        edge_types : Optional[Iterable[ontoweaver.Edge]] = None,
        edge_fields: Optional[list[str]] = None,
    ):
        # Default mapping as a simple config.
        from . import types
        mapping = self.configure(config, types)

        if not node_types:
            node_types  = types.all.nodes()
            logging.debug(f"node_types: {node_types}")

        if not node_fields:
            node_fields = types.all.node_fields()
            logging.debug(f"node_fields: {node_fields}")

        if not edge_types:
            edge_types  = types.all.edges()
            logging.debug(f"edge_types: {edge_types}")

        if not edge_fields:
            edge_fields = types.all.edge_fields()
            logging.debug(f"edge_fields: {edge_fields}")

        # Declare types defined in the config.
        super().__init__(
            df,
            *mapping,
            node_types,
            node_fields,
            edge_types,
            edge_fields,
        )

    def source_type(self, row):
        from . import types
        if row["alteration"].lower() == "amplification":
            return types.amplification # Declared in the oncokb.types module.
        elif row["alteration"].lower() == "deletion":
            return types.deletion
        elif row["alteration"].lower() == "gain":
            return types.gain
        elif row["alteration"].lower() == "loss":
            return types.loss
        else:
            logging.debug(f"Source type is `variant`")
            return types.variant # Declared dynamically through the config oncokb.yaml.

