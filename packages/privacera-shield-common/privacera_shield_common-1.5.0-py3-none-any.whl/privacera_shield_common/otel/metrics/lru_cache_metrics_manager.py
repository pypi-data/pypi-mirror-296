from opentelemetry.metrics import Meter, Observation
from ...lru_cache import LRUCache


class LRUCacheMetricsManager:
    """
    A manager class for handling OpenTelemetry metrics related to an LRU (Least Recently Used) cache.

    This class allows for the creation and registration of observable gauges that track cache metrics such as
    cache size, cache hit ratio, and cache eviction rate.

    Attributes:
        meter (Meter): The OpenTelemetry meter used to record metrics.
        metrics_name_prefix (str): The prefix used for the names of the metrics.
        cache_size_metric_callbacks (list): List of callbacks for cache size metrics.
        cache_hit_ratio_metric_callbacks (list): List of callbacks for cache hit ratio metrics.
        cache_eviction_rate_metric_callbacks (list): List of callbacks for cache eviction rate metrics.
    """

    def __init__(self, meter: Meter, metrics_name_prefix: str):
        """
        Initialize the LRUCacheMetricsManager with a given OpenTelemetry meter and metrics name prefix.

        Args:
            meter (Meter): The OpenTelemetry meter used to record metrics.
            metrics_name_prefix (str): The prefix used for the names of the metrics.
        """
        self.meter = meter
        self.metrics_name_prefix = metrics_name_prefix
        self._setup()

    def _setup(self) -> None:
        """
        Set up the observable gauges for cache metrics.

        This method initializes lists to hold the callbacks for each metric and creates the observable gauges
        with these callbacks.
        """
        # Initialize lists to hold callbacks for gauges
        self.cache_size_metric_callbacks = []
        self.cache_hit_ratio_metric_callbacks = []
        self.cache_eviction_rate_metric_callbacks = []

        # Create observable gauges with callbacks
        self.cache_size_metric = self.meter.create_observable_gauge(
            name=f"{self.metrics_name_prefix}_cache_size",
            callbacks=[self._execute_callbacks(self.cache_size_metric_callbacks)],
            description="The current size of the cache"
        )

        self.cache_hit_ratio_metric = self.meter.create_observable_gauge(
            name=f"{self.metrics_name_prefix}_cache_hit_ratio",
            callbacks=[self._execute_callbacks(self.cache_hit_ratio_metric_callbacks)],
            description="The cache hit ratio"
        )

        self.cache_eviction_rate_metric = self.meter.create_observable_gauge(
            name=f"{self.metrics_name_prefix}_cache_eviction_rate",
            callbacks=[self._execute_callbacks(self.cache_eviction_rate_metric_callbacks)],
            description="The cache eviction rate"
        )

    def _execute_callbacks(self, callbacks) -> callable:
        """
        Helper function to execute multiple callbacks.

        Args:
            callbacks (list): A list of callback functions to be executed.

        Returns:
            callable: A function that when called, executes all provided callbacks and aggregates their observations.
        """

        def _callback(options):
            observations = []
            for cb in callbacks:
                observations.extend(cb(options))
            return observations

        return _callback

    def register_for_metrics(self, lru_cache: LRUCache, attributes: dict = {}) -> None:
        """
        Register an LRU cache for metrics collection.

        This method registers the provided LRU cache instance for metric collection by adding
        callbacks that compute and return observations for cache size, hit ratio, and eviction rate.

        Args:
            lru_cache (LRUCache): The LRU cache instance to register.
            attributes (dict): Additional attributes to associate with the metrics.
        """

        def get_cache_size(options):
            with lru_cache.lock:
                return [Observation(value=len(lru_cache.cache), attributes=attributes)]

        def get_cache_hit_ratio(options):
            with lru_cache.lock:
                total_accesses = lru_cache.hits + lru_cache.misses
                if total_accesses == 0:
                    return [Observation(value=0.0, attributes=attributes)]
                return [Observation(value=lru_cache.hits / total_accesses, attributes=attributes)]

        def get_cache_eviction_rate(options):
            with lru_cache.lock:
                total_accesses = lru_cache.hits + lru_cache.misses
                if total_accesses == 0:
                    return [Observation(value=0.0, attributes=attributes)]
                return [Observation(value=lru_cache.evictions / total_accesses, attributes=attributes)]

        # Registering the callbacks with the attributes for this particular LRUCache instance
        self.cache_size_metric_callbacks.append(get_cache_size)
        self.cache_hit_ratio_metric_callbacks.append(get_cache_hit_ratio)
        self.cache_eviction_rate_metric_callbacks.append(get_cache_eviction_rate)
