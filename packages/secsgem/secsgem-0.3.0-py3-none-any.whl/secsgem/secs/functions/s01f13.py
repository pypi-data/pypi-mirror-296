#####################################################################
# s01f13.py
#
# (c) Copyright 2021, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################
"""Class for stream 01 function 13."""

from secsgem.secs.functions.base import SecsStreamFunction


class SecsS01F13(SecsStreamFunction):
    """establish communication - request.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F13
        [
            MDLN: A[20]
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS01F13(["secsgem", "0.0.6"]) # E->H
        S1F13 W
          <L [2]
            <A "secsgem">
            <A "0.0.6">
          > .
        >>> secsgem.secs.functions.SecsS01F13() # H->E
        S1F13 W
          <L> .

    Data Items:
        - :class:`MDLN <secsgem.secs.data_items.MDLN>`

    .. caution::

        This Stream/function has different structures depending on the source.
        If it is sent from the eqipment side it has the structure below, if it
        is sent from the host it is an empty list.
        Be sure to fill the array accordingly.

    **Structure E->H**::

        {
            MDLN: A[20]
            SOFTREV: A[20]
        }

    """

    _stream = 1
    _function = 13

    _data_format = """
    < L
      < MDLN >
    >
    """

    _to_host = True
    _to_equipment = True

    _has_reply = True
    _is_reply_required = True

    _is_multi_block = False
