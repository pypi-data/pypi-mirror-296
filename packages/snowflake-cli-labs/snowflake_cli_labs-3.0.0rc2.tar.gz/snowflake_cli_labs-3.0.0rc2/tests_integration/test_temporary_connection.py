# Copyright (c) 2024 Snowflake Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import tempfile

import pytest
import os
from unittest import mock


@pytest.mark.integration
@pytest.mark.no_qa
@mock.patch.dict(
    os.environ,
    {
        "SNOWFLAKE_CONNECTIONS_INTEGRATION_ACCOUNT": os.environ.get(
            "SNOWFLAKE_CONNECTIONS_INTEGRATION_ACCOUNT", None
        ),
        "SNOWFLAKE_CONNECTIONS_INTEGRATION_USER": os.environ.get(
            "SNOWFLAKE_CONNECTIONS_INTEGRATION_USER", None
        ),
        "SNOWFLAKE_CONNECTIONS_INTEGRATION_PRIVATE_KEY_RAW": os.environ.get(
            "SNOWFLAKE_CONNECTIONS_INTEGRATION_PRIVATE_KEY_RAW",
        ),
    },
    clear=True,
)
def test_temporary_connection(runner, snapshot):

    with tempfile.TemporaryDirectory() as tmp_dir:
        private_key_path = os.path.join(tmp_dir, "private_key.p8")
        with open(private_key_path, "w") as f:
            f.write(os.environ["SNOWFLAKE_CONNECTIONS_INTEGRATION_PRIVATE_KEY_RAW"])

        result = runner.invoke(
            [
                "sql",
                "-q",
                "select 1",
                "--temporary-connection",
                "--authenticator",
                "SNOWFLAKE_JWT",
                "--account",
                os.environ["SNOWFLAKE_CONNECTIONS_INTEGRATION_ACCOUNT"],
                "--user",
                os.environ["SNOWFLAKE_CONNECTIONS_INTEGRATION_USER"],
                "--private-key-file",
                str(private_key_path),
            ]
        )
        assert result.exit_code == 0
        assert result.output == snapshot
