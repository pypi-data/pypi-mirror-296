import functools
import os
from dataclasses import dataclass
from typing import Optional, Callable

import polars as pl

from more_polars_utils.common.io import write_parquet, read_parquet, file_exists


class AssetManager:
    def __init__(self):
        self.assets = dict()

    def register(self, key, asset):
        self.assets[key] = asset


ASSET_MANAGER = AssetManager()


@dataclass(frozen=True)
class ProjectConfiguration:
    project_name: str
    asset_path: str
    scratch_path: str


class Project:
    def __init__(self):
        self._project_name = None
        self._asset_path = None
        self._scratch_path = None

    def set_configuration(self, configuration: ProjectConfiguration):
        self.project_name = configuration.project_name
        self.asset_path = configuration.asset_path
        self.scratch_path = configuration.scratch_path

    @staticmethod
    def _test_path(path: str) -> str:
        if path and not os.path.isdir(path):
            os.makedirs(path)
        return path

    @property
    def asset_path(self) -> str:
        assert (self._asset_path is not None)
        return self._asset_path

    @asset_path.setter
    def asset_path(self, path: str):
        self._asset_path = self._test_path(path)

    @property
    def scratch_path(self) -> str:
        assert (self._scratch_path is not None)
        return self._scratch_path

    @scratch_path.setter
    def scratch_path(self, path: str):
        self._scratch_path = self._test_path(path)

    @property
    def project_name(self) -> str:
        assert (self._project_name is not None)
        return self._project_name

    @project_name.setter
    def project_name(self, name: str):
        self._project_name = name


ACTIVE_PROJECT = Project()


class PolarsParquetAsset:

    def __init__(
            self,
            func: Optional[Callable] = None,
            *,
            project: Project = ACTIVE_PROJECT,
            asset_name: str = None,
            verbose=False,
            is_temporary: bool = False,
            force_reload: bool = False):
        self.func = func
        self.asset_name = asset_name
        self.verbose = verbose
        self.project = project
        self.force_reload = force_reload
        self.is_temporary = is_temporary

        # By default, use the function name as the asset name
        if asset_name is None:
            self.asset_name = func.__name__ if func is not None else "UNKNOWN"
        else:
            self.asset_name = asset_name

        if func is not None:
            functools.update_wrapper(self, func)

        self._register()

    def _register(self):
        ASSET_MANAGER.register(self.asset_name, self)

    def _verbose_log(self, message: str):
        if self.verbose:
            print(message)

    def parquet_path(self):
        if self.is_temporary:
            return f"{self.project.scratch_path}/{self.asset_name}.parquet"
        else:
            asset_path = self.project.asset_path
            path = f"{asset_path}/{self.asset_name}.parquet"
            return path

    def materialize(self, *args, **kwargs) -> pl.DataFrame:
        assert (self.func is not None)
        return self.func(*args, **kwargs)

    def _load_from_cache(self) -> pl.DataFrame:
        return read_parquet(self.parquet_path())

    def _write_to_cache(self, df: pl.DataFrame):
        write_parquet(df, self.parquet_path())

    def __call__(self, *args, **kwargs) -> pl.DataFrame:

        # Check to see if the asset needs to be built then cached, before loading from cache
        if self.force_reload or not file_exists(self.parquet_path()):
            self._verbose_log(f"Cache miss for {self.parquet_path()}")
            df = self.materialize(*args, **kwargs)

            self._verbose_log(f"Writing to {self.parquet_path()}")
            self._write_to_cache(df)

        return self._load_from_cache()

    @classmethod
    def decorator(cls, **kwargs):
        def wrapper(func):
            obj = cls(func, **kwargs)
            return obj

        return wrapper
