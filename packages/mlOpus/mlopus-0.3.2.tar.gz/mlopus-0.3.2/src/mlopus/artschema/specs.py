"""
Pydantic models for specifying the save/load rules of an artifact,
like where it comes from, which schema is to be used, etc.

Mostly meant for applications that are based on configuration files,
so the logic for loading/saving a run artifact or model version can
be fully encoded in the configuration and there's no need to change
the code when an artifact specification is changed.
"""

import logging
from abc import abstractmethod, ABC
from pathlib import Path
from typing import Dict, Any, Generic, Type, Mapping, Tuple
from typing import TypeVar

from mlopus.lineage import _LineageArg, _ModelLineageArg, _RunLineageArg
from mlopus.mlflow.api.entity import EntityApi
from mlopus.mlflow.api.mv import ModelVersionApi
from mlopus.mlflow.api.run import RunApi
from mlopus.mlflow.traits import MlflowApiMixin
from mlopus.utils import pydantic
from .framework import Schema, _DummySchema, A, D, L
from .helpers import load_artifact, log_model_version, log_run_artifact

T = TypeVar("T", bound=EntityApi)  # Type of entity API
LA = TypeVar("LA", bound=_LineageArg)  # Type of lineage argument

logger = logging.getLogger(__name__)


class ArtifactSubject(MlflowApiMixin, pydantic.EmptyStrAsMissing, ABC, Generic[T, LA]):
    """Specification of an artifact subject."""

    @abstractmethod
    def cache(self) -> Path:
        """Cache subject metadata and artifact."""

    @abstractmethod
    def export(self, target: Path) -> Path:
        """Export subject metadata and artifact cache."""

    @abstractmethod
    def load(self, **kwargs) -> Tuple[LA, Any]:
        """Load artifact."""

    @abstractmethod
    def log(self, **kwargs) -> Tuple[LA, T]:
        """Log artifact."""

    def apply_defaults(self, **defaults):
        """Adjust missing or incomplete params of artifact subject based on provided defaults."""


class ModelVersionArtifact(ArtifactSubject[ModelVersionApi, _ModelLineageArg]):
    """Specification of a model version artifact."""

    model_name: str = pydantic.Field(description="Parent model name.")

    model_version: str | None = pydantic.Field(
        default=None, description="Required when loading, optional when publishing."
    )

    run_id: str = pydantic.Field(default=None, description="Parent run ID. Required when publishing.")

    tags: Mapping | None = pydantic.Field(
        default=None,
        description="Optional, only used when publishing. See :attr:`mlopus.mlflow.schema.ModelVersion.tags`.",
    )

    path_in_run: str | None = pydantic.Field(
        default=None,
        description=(
            "Only used when publishing. See :paramref:`~mlopus.mlflow.BaseMlflowApi.log_model_version.path_in_run`."
        ),
    )

    @property
    def _version_api(self) -> ModelVersionApi:
        return self.mlflow_api.get_model(self.model_name).get_version(self.model_version)

    def cache(self) -> Path:
        """Cache subject metadata and artifact."""
        return self._version_api.cache_meta().cache_artifact()

    def export(self, target: Path) -> Path:
        """Export subject metadata and artifact cache."""
        return self._version_api.export_meta(target).export_artifact(target)

    def load(self, **kwargs) -> Tuple[_ModelLineageArg, Any]:
        """Load artifact."""
        return _ModelLineageArg(self.model_name, self.model_version), load_artifact(self._version_api, **kwargs)

    def log(self, **kwargs) -> Tuple[_ModelLineageArg, ModelVersionApi]:
        """Log artifact."""
        mv = log_model_version(
            **kwargs,
            tags=self.tags,
            run=self.run_id,
            version=self.model_version,
            path_in_run=self.path_in_run,
            model=self.mlflow_api.get_or_create_model(self.model_name),
        )
        return _ModelLineageArg(self.model_name, mv.version), mv

    def apply_defaults(self, run_id: str | None = None, path_in_run: str | None = None, **__):
        """Adjust missing or incomplete params of artifact subject based on provided defaults."""
        self.run_id = self.run_id or run_id


class RunArtifact(ArtifactSubject[RunApi, _RunLineageArg]):
    """Specification of a run artifact."""

    run_id: str = None
    path_in_run: str = None

    @property
    def _run_api(self) -> RunApi:
        return self.mlflow_api.get_run(self.run_id)

    def cache(self) -> Path:
        """Cache subject metadata and artifact."""
        return self._run_api.cache_meta().cache_artifact(self.path_in_run)

    def export(self, target: Path) -> Path:
        """Export subject metadata and artifact cache."""
        return self._run_api.export_meta(target).export_artifact(target, self.path_in_run)

    def load(self, **kwargs) -> Tuple[_RunLineageArg, Any]:
        """Load artifact."""
        lineage_arg = _RunLineageArg(self.run_id, self.path_in_run)
        return lineage_arg, load_artifact(self._run_api, path_in_run=self.path_in_run, **kwargs)

    def log(self, **kwargs) -> Tuple[_RunLineageArg, RunApi]:
        """Log artifact."""
        log_run_artifact(
            **kwargs,
            path_in_run=self.path_in_run,
            run=(run := self.mlflow_api.get_run(self.run_id)),
        )

        return _RunLineageArg(self.run_id, self.path_in_run), run

    def apply_defaults(self, run_id: str | None = None, path_in_run: str | None = None, **__):
        """Adjust missing or incomplete params of artifact subject based on provided defaults."""
        self.run_id = self.run_id or run_id
        self.path_in_run = self.path_in_run or path_in_run


@pydantic.validate_arguments
def _parse_subject(subj: ModelVersionArtifact | RunArtifact | dict) -> ArtifactSubject:
    """Parse settings dict into instance of `RunArtifact` or `ModelVersionArtifact`."""
    return subj


class LoadArtifactSpec(MlflowApiMixin, Generic[T, LA]):
    """Specification for loading an artifact."""

    schema_: Schema[A, D, L] | Type[Schema[A, D, L]] | str | None = pydantic.Field(
        alias="schema",
        default_factory=_DummySchema,
        description="See :paramref:`~mlopus.artschema.load_artifact.schema`",
    )

    loader_conf: Dict[str, Any] | None = pydantic.Field(
        default=None,
        description="See :paramref:`~mlopus.artschema.Schema.get_loader.loader`",
    )

    skip_reqs_check: bool = pydantic.Field(
        default=False,
        description="See :paramref:`~mlopus.artschema.load_artifact.skip_reqs_check`",
    )

    subject: ArtifactSubject[T, LA] = pydantic.Field(
        description=(
            "Instance (or `dict` to be parsed into instance) of "
            ":class:`~mlopus.artschema.RunArtifact` or :class:`~mlopus.artschema.ModelVersionArtifact`. "
            "See also: :paramref:`~mlopus.artschema.load_artifact.subject`."
        )
    )

    _parse_subject = pydantic.validator("subject", pre=True, allow_reuse=True)(_parse_subject)

    def download(self) -> Path:
        """Cache subject metadata and artifact.

        See also:
            - :meth:`mlopus.mlflow.RunApi.cache_meta`
            - :meth:`mlopus.mlflow.RunApi.cache_artifact`
            - :meth:`mlopus.mlflow.ModelVersionApi.cache_meta`
            - :meth:`mlopus.mlflow.ModelVersionApi.cache_artifact`

        :return: A `Path` to the cached artifact.
        """
        return self.subject.using(self.mlflow_api).cache()

    def export(self, target: Path) -> Path:
        """Export subject metadata and artifact cache.

        See also:
            - :meth:`mlopus.mlflow.RunApi.export_meta`
            - :meth:`mlopus.mlflow.RunApi.export_artifact`
            - :meth:`mlopus.mlflow.ModelVersionApi.export_meta`
            - :meth:`mlopus.mlflow.ModelVersionApi.export_artifact`

        :param target: Target cache export `Path`.
        """
        return self.subject.using(self.mlflow_api).export(target)

    def load(self, schema: Schema[A, D, L] | Type[Schema[A, D, L]] | str | None = None, dry_run: bool = False) -> A:
        """Load artifact.

        See also:
            - :meth:`mlopus.mlflow.RunApi.load_artifact`
            - :meth:`mlopus.mlflow.ModelVersionApi.load_artifact`

        :param schema: | Override :attr:`schema_`
        :param dry_run: | See :paramref:`~mlopus.artschema.Loader.load.dry_run`
        :return:
            - If :paramref:`dry_run` is `True`: A `Path` to the cached artifact.
            - Otherwise: An instance of :attr:`Schema.Artifact`
        """
        return self._load(schema, dry_run)[1]

    def _load(
        self, schema: Schema[A, D, L] | Type[Schema[A, D, L]] | str | None = None, dry_run: bool = False
    ) -> Tuple[LA, A]:
        """Load artifact."""
        return self.subject.using(self.mlflow_api).load(
            dry_run=dry_run,
            loader_conf=self.loader_conf,
            skip_reqs_check=self.skip_reqs_check,
            schema=schema or self.schema_,
        )

    def with_defaults(self, **defaults) -> "LoadArtifactSpec":
        """Adjust missing or incomplete params of artifact subject based on provided defaults."""
        self.subject.apply_defaults(**defaults)
        return self


@pydantic.validate_arguments
def parse_load_specs(specs: Dict[str, LoadArtifactSpec | dict]) -> Dict[str, LoadArtifactSpec]:
    """Parse settings dict into mapping of `LoadArtifactSpec`."""
    return specs


class LogArtifactSpec(MlflowApiMixin, Generic[T, LA]):
    """Specification for logging an artifact."""

    schema_: Schema[A, D, L] | Type[Schema[A, D, L]] | str | None = pydantic.Field(
        alias="schema",
        default_factory=_DummySchema,
        description="See :paramref:`~mlopus.artschema.load_artifact.schema`",
    )

    dumper_conf: Dict[str, Any] | None = pydantic.Field(
        default=None,
        description="See :paramref:`~mlopus.artschema.Schema.get_dumper.dumper`",
    )

    skip_reqs_check: bool = pydantic.Field(
        default=False,
        description="See :paramref:`~mlopus.artschema.load_artifact.skip_reqs_check`",
    )

    auto_register: bool | Dict[str, Any] = pydantic.Field(
        default=False,
        description=(
            "See :paramref:`mlopus.artschema.log_run_artifact.auto_register` "
            "and :paramref:`mlopus.artschema.log_model_version.auto_register`"
        ),
    )

    keep_the_source: bool | None = pydantic.Field(
        default=None,
        description="See :paramref:`~mlopus.mlflow.BaseMlflowApi.log_run_artifact.keep_the_source`",
    )

    allow_duplication: bool | None = pydantic.Field(
        default=None,
        description="See :paramref:`~mlopus.mlflow.BaseMlflowApi.log_run_artifact.allow_duplication`",
    )

    use_cache: bool | None = pydantic.Field(
        default=None,
        description="See :paramref:`~mlopus.mlflow.BaseMlflowApi.log_run_artifact.use_cache`",
    )

    subject: ArtifactSubject[T, LA] = pydantic.Field(
        description=(
            "Instance (or `dict` to be parsed into instance) of :class:`RunArtifact` or :class:`ModelVersionArtifact`. "
            "See also: :paramref:`~mlopus.artschema.load_artifact.subject`."
        )
    )

    _parse_subject = pydantic.validator("subject", pre=True, allow_reuse=True)(_parse_subject)

    def log(self, artifact: A | dict | Path, schema: Schema[A, D, L] | Type[Schema[A, D, L]] | str | None = None) -> T:
        """Log artifact.

        See also:
            - :meth:`mlopus.mlflow.RunApi.log_artifact`
            - :meth:`mlopus.mlflow.ModelApi.log_version`

        :param schema: | Override :attr:`schema_`
        :param artifact: | See :paramref:`Schema.get_dumper.artifact`
        """
        return self._log(artifact, schema)[1]

    def _log(
        self, artifact: A | dict | Path, schema: Schema[A, D, L] | Type[Schema[A, D, L]] | str | None = None
    ) -> Tuple[LA, T]:
        """Log artifact."""
        return self.subject.using(self.mlflow_api).log(
            artifact=artifact,
            schema=schema or self.schema_,
            dumper_conf=self.dumper_conf,
            skip_reqs_check=self.skip_reqs_check,
            auto_register=self.auto_register,
            keep_the_source=self.keep_the_source,
            allow_duplication=self.allow_duplication,
            use_cache=self.use_cache,
        )

    def with_defaults(self, **defaults) -> "LogArtifactSpec":
        """Adjust missing or incomplete params of artifact subject based on provided defaults."""
        self.subject.apply_defaults(**defaults)
        return self


@pydantic.validate_arguments
def parse_logart_specs(specs: Dict[str, LogArtifactSpec | dict]) -> Dict[str, LogArtifactSpec]:
    """Parse settings dict into mapping of `LogArtifactSpec`."""
    return specs
