import os  # NOQA

from mock import patch
import pytest

import confluent.docker_utils.dub as dub

def test_exit_if_all_absent():
    """Should exit when none of enviroments are present"""

    all_absent_envs = ["NOT_PRESENT_1", "NOT_PRESENT_2"]

    with patch.dict("os.environ", {}):
        assert dub.exit_if_all_absent(all_absent_envs) == False

    fake_environ = {
        all_absent_envs[0]: "PRESENT",
    }

    with patch.dict("os.environ", fake_environ):
        assert dub.exit_if_all_absent(all_absent_envs)


def test_env_to_props():

    fake_environ = {
        "KAFKA_FOO": "foo",
        "KAFKA_FOO_BAR": "bar",
        "KAFKA_IGNORED": "ignored",
        "KAFKA_WITH__UNDERSCORE": "with underscore",
        "KAFKA_WITH__UNDERSCORE_AND_MORE": "with underscore and more",
        "KAFKA_WITH___DASH": "with dash",
        "KAFKA_WITH___DASH_AND_MORE": "with dash and more"
    }

    with patch.dict('os.environ', fake_environ):
        result = dub.env_to_props("KAFKA_", "kafka.", exclude = ["KAFKA_IGNORED"])
        assert "kafka.foo" in result
        assert "kafka.foo.bar" in result
        assert "kafka.ignored" not in result
        assert "kafka.with_underscore" in result
        assert "kafka.with_underscore.and.more" in result
        assert "kafka.with-dash" in result
        assert "kafka.with-dash.and.more" in result


def test_parse_log4j_loggers():
    assert dub.parse_log4j_loggers("") == {}
    assert dub.parse_log4j_loggers("foo.bar=DEBUG") == {'foo.bar': "DEBUG"}
    assert dub.parse_log4j_loggers("foo.bar=DEBUG,baz.bam=TRACE") == {'foo.bar': "DEBUG", 'baz.bam': 'TRACE'}