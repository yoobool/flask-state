import redis

from src.flask_state.exceptions import ErrorResponse, SuccessResponse
from src.flask_state.models import model_init_app
from src.flask_state.services import host_status, redis_conn


def test_redis(app):
    """
    Test whether the custom redis class method can be used normally
    """
    app.config["REDIS_CONF"] = {
        "REDIS_STATUS": True,
        "REDIS_HOST": "192.168.0.2",
        "REDIS_PORT": 16379,
        "REDIS_PASSWORD": "fish09",
    }
    redis_state = app.config["REDIS_CONF"]
    redis_conf = {
        "REDIS_HOST": redis_state.get("REDIS_HOST"),
        "REDIS_PORT": redis_state.get("REDIS_PORT"),
        "REDIS_PASSWORD": redis_state.get("REDIS_PASSWORD"),
    }
    redis_conn.set_redis(redis_conf)

    # get redis
    assert isinstance(redis_conn.get_redis(), redis.Redis)


def test_control_return_count():
    """
    Test whether the number of query returns is controlled correctly
    """
    len_list = {1: 1, 100: 100, 480: 480, 500: 480, 1000: 480}
    for key in len_list:
        assert len_list.get(key) == len(host_status.control_result_counts(list([0]) * key))


def test_query_flask_state_host(app):
    """
    Tests whether the query data returns to the specified format
    """
    model_init_app(app)
    test_right_day = [1, 3, 7, 30]
    test_error_day = [5, 10, 31, 100]
    with app.app_context():
        for day in test_right_day:
            response_content = host_status.query_flask_state_host(day)
            assert 200 == response_content.get_code()
            assert "Search success" == response_content.get_msg()
            assert isinstance(response_content.data.get("currentStatistic"), dict)
            assert isinstance(response_content.data.get("items"), list)
            assert isinstance(response_content, SuccessResponse)

        for day in test_error_day:
            response_content = host_status.query_flask_state_host(day)
            assert isinstance(response_content.get_code(), int)
            assert isinstance(response_content.get_msg(), str)
            assert isinstance(response_content, ErrorResponse)
