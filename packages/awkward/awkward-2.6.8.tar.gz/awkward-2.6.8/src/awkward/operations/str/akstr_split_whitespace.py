# BSD 3-Clause License; see https://github.com/scikit-hep/awkward/blob/main/LICENSE

from __future__ import annotations

import awkward as ak
from awkward._dispatch import high_level_function
from awkward._layout import HighLevelContext

__all__ = ("split_whitespace",)


@high_level_function(module="ak.str")
def split_whitespace(
    array, *, max_splits=None, reverse=False, highlevel=True, behavior=None, attrs=None
):
    """
    Args:
        array: Array-like data (anything #ak.to_layout recognizes).
        max_splits (None or int): Maximum number of splits for each input
            value. If None, unlimited.
        reverse (bool): If True, start splitting from the end of each input
            value; otherwise, start splitting from the beginning of each
            value. This flag only has an effect if `max_splits` is not None.
        highlevel (bool): If True, return an #ak.Array; otherwise, return
            a low-level #ak.contents.Content subclass.
        behavior (None or dict): Custom #ak.behavior for the output array, if
            high-level.
        attrs (None or dict): Custom attributes for the output array, if
            high-level.

    Splits any string or bytestring-valued data into a list of substrings
    according to any non-zero length sequence of
    whitespace characters.

    For strings, a split is performed for every sequence of Unicode whitespace
    characters; for bytestrings, splitting is performed for sequences of ascii
    whitespace characters.

    The `max_splits`, and `reverse` arguments are scalars; they cannot be
    different for each string/bytestring in the sample.

    Note: this function does not raise an error if the `array` does not
    contain any string or bytestring data.

    Requires the pyarrow library and calls
    [pyarrow.compute.utf8_split_whitespace](https://arrow.apache.org/docs/python/generated/pyarrow.compute.utf8_split_whitespace.html)
    or [pyarrow.compute.ascii_split_whitespace](https://arrow.apache.org/docs/python/generated/pyarrow.compute.ascii_split_whitespace.html)
    on strings and bytestrings, respectively.

    See also: #ak.str.split_pattern, #ak.str.split_pattern_regex.
    """
    # Dispatch
    yield (array,)

    # Implementation
    return _impl(array, max_splits, reverse, highlevel, behavior, attrs)


def _impl(array, max_splits, reverse, highlevel, behavior, attrs):
    from awkward._connect.pyarrow import import_pyarrow_compute

    pc = import_pyarrow_compute("ak.str.split_whitespace")

    with HighLevelContext(behavior=behavior, attrs=attrs) as ctx:
        layout = ctx.unwrap(
            array,
            allow_record=False,
            allow_unknown=False,
            primitive_policy="error",
            string_policy="as-characters",
        )

    action = ak.operations.str._get_split_action(
        pc.utf8_split_whitespace,
        pc.ascii_split_whitespace,
        max_splits=max_splits,
        reverse=reverse,
        bytestring_to_string=True,
    )
    out = ak._do.recursively_apply(layout, action)

    return ctx.wrap(out, highlevel=highlevel)
