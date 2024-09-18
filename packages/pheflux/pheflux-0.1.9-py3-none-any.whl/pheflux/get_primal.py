import polars as pl
import numpy as np
from cobra.core.reaction import Reaction
from cobra.core.model import Model as SBMLModel
from collections import namedtuple
from pheflux.boolean_vector_rule import boolean_vector_rule
from pheflux.get_g import get_expression_value

from gene_rule_parser import (ExpressionParser, tree_analysis)
from collections import namedtuple
from pydantic.dataclasses import dataclass
from functools import lru_cache
##############################################################################
## Obtains a median value of the expression of genes associated with
## metabolism
import ujson
from pathlib import Path
from typing import Any

def get_primal_values(
        model:SBMLModel,
)->dict[str,Any]:
    """
    Input:
        model (cobra.Model): Metabolic model.
        fpkmDic (dict): Dictionary with gene expression values.
    
    Output:
        tuple: Median value of gene expressions, and list of gene expressions for metabolic reactions.
    """
    #parser = ExpressionParser()
    fba_primal = {}
    # this is to obtain primalValues, in this case all together
    # optimize model
    model.optimize()
    
    for i, reaction in enumerate(model.reactions):
        ##########################################################
        ## Gets the GPR and a boolean list with known or unknown genes
        fba_primal[reaction.id] = getattr(model.variables,
                                         reaction.id).primal
        fba_primal[reaction.reverse_id] = getattr(model.variables,
                                                  reaction.reverse_id).primal

    return fba_primal
