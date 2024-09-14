# Copyright (c) 2021-2022  The University of Texas Southwestern Medical Center.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted for academic and research use only (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:

#      * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#      * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.

#      * Neither the name of the copyright holders nor the names of its
#      contributors may be used to endorse or promote products derived from this
#      software without specific prior written permission.

# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

#  Standard Library Imports
import logging

# Third Party Imports

# Local Imports

# Logger Setup
p = __name__.split(".")[1]
logger = logging.getLogger(p)


class FilterWheelBase:
    """FilterWheelBase - Parent class for controlling filter wheels."""

    def __init__(self, device_connection, device_config):
        """Initialize the FilterWheelBase class.

        Parameters
        ----------
        device_connection : dict
            Dictionary of device connections.
        device_config : dict
            Dictionary of device configuration parameters.
        """

        #: dict: Dictionary of filters available on the filter wheel.
        self.filter_dictionary = device_config["available_filters"]

        #: int: Filter wheel position.
        self.wheel_position = 0

        #: int: index of filter wheel
        self.filter_wheel_number = device_config["hardware"]["wheel_number"]

    def check_if_filter_in_filter_dictionary(self, filter_name):
        """Checks if the filter designation (string) given exists in the
        filter dictionary

        Parameters
        ----------
        filter_name : str
            Name of filter.

        Returns
        -------
        filter_exists : bool
            Flag if filter exists in the filter dictionary.

        Raises
        ------
        ValueError
            If filter name is not in the filter dictionary.

        """
        if filter_name in self.filter_dictionary:
            filter_exists = True
        else:
            filter_exists = False
            logger.debug("Filter Name not in the Filter Dictionary")
            raise ValueError("Filter Name not in the Filter Dictionary.")
        return filter_exists
