from datetime import timedelta

from prometheus_client import metrics
from models.Stats import RunTimeStat
import pytest
import requests

from repositories.stats import SPOTICRON_RUN_TIME, StatsRepository

import prometheus_client

from utils import stats_collection

# pylint was complaingin about func(run_time) being overwritten in functions as an arg.
# However, this is exactly how pytest uses fixtures. Hence we disable it here.

# pylint:disable=redefined-outer-name

@pytest.fixture
def registry() -> prometheus_client.CollectorRegistry:
    yield prometheus_client.REGISTRY

class TestStatsRepository:
    def test_spoticron_run_time(self, registry: prometheus_client.CollectorRegistry):
        assert registry.get_sample_value("spoticron_run_time_sum") == 0.0
        c = 0
        for i in range(10):
            StatsRepository.spoticron_run_time(RunTimeStat(time=i))
            assert registry.get_sample_value("spoticron_run_time_sum") == (c:=c+i)

    def test_user_creation(self, registry: prometheus_client.CollectorRegistry):
        assert registry.get_sample_value("autonoma_user_created_total") == 0.0
        c = 0
        for i in range(10):
            StatsRepository.user_creation()
            assert registry.get_sample_value("autonoma_user_created_total") == (c:=c+1)

    def test_user_deletion(self, registry: prometheus_client.CollectorRegistry):
        assert registry.get_sample_value("autonoma_user_deleted_total") == 0.0
        c = 0
        for i in range(10):
            StatsRepository.user_deletion()
            assert registry.get_sample_value("autonoma_user_deleted_total") == (c:=c+1)

    def test_spotify_request_called(self, registry: prometheus_client.CollectorRegistry):
        assert registry.get_sample_value("autonoma_spotify_request_total") == 0.0
        c = 0
        for i in range(10):
            StatsRepository.spotify_request_called()
            assert registry.get_sample_value("autonoma_spotify_request_total") == (c:=c+1)


    def test_tracks_aded_called(self, registry: prometheus_client.CollectorRegistry):
        assert registry.get_sample_value("spoticron_tracks_added_total") == 0.0
        c = 0
        for i in range(10):
            StatsRepository.spoticron_tracks_added(i)
            assert registry.get_sample_value("spoticron_tracks_added_total") == (c:=c+i)
    
    def test_spoticron_enabled(self, registry: prometheus_client.CollectorRegistry):
        assert registry.get_sample_value("spoticron_enabled_total") == 0.0
        c = 0
        for i in range(10):
            StatsRepository.spoticron_enabled()
            assert registry.get_sample_value("spoticron_enabled_total") == (c:=c+1)
    
    def test_spoticron_disabled(self, registry: prometheus_client.CollectorRegistry):
        assert registry.get_sample_value("spoticron_disabled_total") == 0.0
        c = 0
        for i in range(10):
            StatsRepository.spoticron_disabled()
            assert registry.get_sample_value("spoticron_disabled_total") == (c:=c+1)

    def test_generated(self):
        generated = str(prometheus_client.generate_latest()) # This is the function that collates the /metrics response
        metrics = ["spoticron_disabled_total",
                   "autonoma_user_created_total",
                   "autonoma_user_deleted_total",
                   "autonoma_spotify_request_total",
                   "spoticron_tracks_added_total",
                   "spoticron_enabled_total",
                   "spoticron_disabled_total"]
        assert all([m in generated for m in metrics])

        assert 'thisonedoesntexist' not in generated