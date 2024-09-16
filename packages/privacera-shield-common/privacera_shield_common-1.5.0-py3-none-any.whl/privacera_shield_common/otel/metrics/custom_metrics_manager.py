class CustomMetricsManager:
    """
    A manager class for handling custom OpenTelemetry metrics, including metrics for LRU caches and FastAPI applications

    This class is designed to be used as a singleton, ensuring that metrics are only initialized once per application.

    Attributes:
        _initialized (bool): Indicates whether the manager has been initialized.
        _meter (Optional[Meter]): The OpenTelemetry meter used to record metrics.
        _lru_cache_metrics_manager_dict (dict): A dictionary to store LRU cache metrics managers.
        _fastapi_metrics_manager (Optional[FastAPIMetricsManager]): The metrics manager for FastAPI applications.
    """
    _initialized = False
    _meter = None
    _lru_cache_metrics_manager_dict = {}
    _fastapi_metrics_manager = None

    @classmethod
    def init(cls, application_name: str) -> None:
        """
        Initialize the CustomMetricsManager with a specific application name.

        This method sets up the OpenTelemetry meter provider and creates a meter
        for recording metrics. It must be called before any other methods in this class.

        Args:
            application_name (str): The name of the application, used to create the meter.

        Raises:
            ImportError: If the required OpenTelemetry libraries are not installed.
        """
        if not cls._initialized:
            try:
                from opentelemetry import metrics
                from opentelemetry.sdk.metrics import MeterProvider
            except ImportError as e:
                missing_package = str(e).split("'")[-2]
                raise ImportError(
                    f"The required library '{missing_package}' is not installed. "
                    f"Please install it using the following command:\n\n"
                    f"pip install opentelemetry-sdk"
                ) from e

            metrics.set_meter_provider(MeterProvider())
            cls._meter = metrics.get_meter(application_name)
            cls._initialized = True

    @classmethod
    def register_lru_cache_metrics(cls, lru_cache, metrics_name_prefix: str, attributes: dict) -> None:
        """
        Register an LRU cache for metrics collection.

        This method ensures that the LRU cache metrics manager is created and
        registers the provided LRU cache for metric collection.

        Args:
            lru_cache: The LRU cache instance to register.
            metrics_name_prefix (str): The prefix to use for the metric names.
            attributes (dict): The attributes to associate with the metrics.

        Raises:
            RuntimeError: If the manager has not been initialized.
        """
        if not cls._initialized:
            raise RuntimeError("CustomMetricsManager is not initialized. Call init first.")

        lru_cache_metrics_manager = cls._get_or_create_lru_cache_metrics_manager(metrics_name_prefix)
        lru_cache_metrics_manager.register_for_metrics(lru_cache, attributes)

    @classmethod
    def register_fastapi_metrics(cls, app, service_name: str) -> None:
        """
        Register a FastAPI application for metrics collection.

        This method sets up a FastAPI metrics manager and registers the provided
        FastAPI application for metric collection.

        Args:
            app: The FastAPI application instance to register.
            service_name (str): The name of the service to associate with the metrics.

        Raises:
            RuntimeError: If the manager has not been initialized.
            ImportError: If the required FastAPI metrics manager module is not installed.
        """
        if not cls._initialized:
            raise RuntimeError("CustomMetricsManager is not initialized. Call init first.")

        if cls._fastapi_metrics_manager is None:
            from .fastapi_metrics_manager import FastAPIMetricsManager

            cls._fastapi_metrics_manager = FastAPIMetricsManager(cls._meter)
            cls._fastapi_metrics_manager.register_for_metrics(app, service_name)

    @classmethod
    def _get_or_create_lru_cache_metrics_manager(cls, metrics_name_prefix: str):
        """
        Get or create an LRU cache metrics manager.

        This method retrieves an existing LRU cache metrics manager from the
        internal dictionary or creates a new one if it does not exist.

        Args:
            metrics_name_prefix (str): The prefix to use for the metric names.

        Returns:
            LRUCacheMetricsManager: The LRU cache metrics manager instance.

        Raises:
            RuntimeError: If the manager has not been initialized.
            ImportError: If the required LRU cache metrics manager module is not installed.
        """
        if not cls._initialized:
            raise RuntimeError("CustomMetricsManager is not initialized. Call init first.")

        if metrics_name_prefix in cls._lru_cache_metrics_manager_dict:
            return cls._lru_cache_metrics_manager_dict[metrics_name_prefix]

        from .lru_cache_metrics_manager import LRUCacheMetricsManager

        lru_cache_metrics_manager = LRUCacheMetricsManager(cls._meter, metrics_name_prefix)
        cls._lru_cache_metrics_manager_dict[metrics_name_prefix] = lru_cache_metrics_manager
        return lru_cache_metrics_manager
