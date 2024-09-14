"""Additional utility functions for Veles"""

import itertools


def flatten(args: tuple) -> list:
    """Flatten a list of lists or touples"""
    args = [*args]
    args = [[arg] if not isinstance(arg, (list, tuple)) else arg for arg in args]
    return list(itertools.chain.from_iterable(args))


def dict_without_defaults(self) -> dict:
    "Return a dictionary of the changed object's attributes"
    # Values that are set to their default values differently from the SurveyJS default values
    # "attribute": "default value in SurveyJS"
    custom_defaults = {}

    return {
        k: v
        for k, v in vars(self).items()
        if (custom_defaults.get(k) is not None and v != custom_defaults.get(k))
        or (
            k not in ["questions", "pages", "validators", "addCode", "columns", "rows"]
            and v != self.model_fields[k].default
        )
    }
