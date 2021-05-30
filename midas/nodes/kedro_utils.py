# The following functions have been modified by midas' author
#
# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict


def get_feed_dict(params: dict) -> Dict[str, Any]:
    """Get parameters and return the feed dictionary."""
    feed_dict = {"parameters": params}

    def _add_param_to_feed_dict(param_name, param_value):
        """This recursively adds parameter paths to the `feed_dict`,
        whenever `param_value` is a dictionary itself, so that users can
        specify specific nested parameters in their node inputs.
        Example:
            >>> param_name = "a"
            >>> param_value = {"b": 1}
            >>> _add_param_to_feed_dict(param_name, param_value)
            >>> assert feed_dict["params:a"] == {"b": 1}
            >>> assert feed_dict["params:a.b"] == 1
        """
        key = f"params:{param_name}"
        feed_dict[key] = param_value

        if isinstance(param_value, dict):
            for key, val in param_value.items():
                _add_param_to_feed_dict(f"{param_name}.{key}", val)

    for param_name, param_value in params.items():
        _add_param_to_feed_dict(param_name, param_value)

    return feed_dict
