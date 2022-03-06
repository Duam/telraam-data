import telraam_data.query as query
import datetime
import random


def test_query_active_segments():
    segments = query.query_active_segments()
    assert segments["status_code"] == 200
    assert segments["message"] == "ok"
    assert segments["type"] == "FeatureCollection"
    num_segments = len(segments)
    assert num_segments > 0
    idx = random.randrange(1, num_segments) - 1
    assert segments["features"][idx]["type"] == "Feature"
    assert segments["features"][idx]["geometry"]["type"] == "MultiLineString"
    assert "properties" in segments["features"][idx].keys()


def test_query_one_segment():
    # Choose a random segment from the database
    all_segments = query.query_active_segments()
    segment_idx = random.randrange(1, len(all_segments)) - 1
    segment = all_segments["features"][segment_idx]
    segment_id = segment["properties"]["segment_id"]
    segment_last_time = segment["properties"]["last_data_package"]

    # Query that segment for the last live day
    time2 = datetime.datetime.strptime(segment_last_time, "%Y-%m-%d %H:%M:%S.%f%z")
    time1 = time2 - datetime.timedelta(days=1)
    response = query.query_one_segment(segment_id, str(time1), str(time2))

    assert response["status_code"] == 200
    assert response["message"] == "ok"
    num_reports = len(response["report"])
    assert num_reports > 0

    # All listed keys must exist in the queried report
    report_idx = random.randrange(1, num_reports) - 1
    report = response["report"][report_idx]
    required_keys = [
        'instance_id', 'segment_id', 'date', 'interval', 'uptime', 'heavy', 'car', 'bike', 'pedestrian', 'heavy_lft',
        'heavy_rgt', 'car_lft', 'car_rgt', 'bike_lft', 'bike_rgt', 'pedestrian_lft', 'pedestrian_rgt', 'direction',
        'car_speed_hist_0to70plus', 'car_speed_hist_0to120plus', 'timezone', 'v85'
    ]
    assert set(required_keys) == set(required_keys).intersection(report.keys())

