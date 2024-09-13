from pathlib import Path
from typing import List

import mlopus
from mlopus.lineage import _LineageArg
from mlopus.utils import pydantic, paths


class PipelineInput(mlopus.artschema.LoadArtifactSpec, pydantic.EmptyStrAsMissing):
    """Specification of an artifact to be fetched from MLFlow and placed before a pipeline runs.

    See also:
        - :meth:`mlopus.mlflow.BaseMlflowApi.place_run_artifact`
        - :meth:`mlopus.mlflow.BaseMlflowApi.place_model_artifact`

    - If :attr:`schema_` is specified, it is used to verify the artifact after placing it.
    - :attr:`subject` and :attr:`skip_reqs_check` are used if :attr:`schema_` is an alias.
    """

    path: Path = pydantic.Field(description="Local path to place the artifact file or dir.")
    link: bool = pydantic.Field(
        default=True,
        description=(
            "Place artifact file or dir as a symbolic link to the artifacts cache. "
            "If ``false``, make a copy instead."
        ),
    )
    enabled: bool = pydantic.Field(default=True, description="Enable this input.")
    overwrite: bool = pydantic.Field(default=True, description="Overwrite :attr:`path` if exists.")
    log_lineage: bool = pydantic.Field(
        default=True,
        description="Log lineage info in MLFlow run. See also :class:`mlopus.lineage.Lineage`.",
    )
    pipelines: List[str] | None = pydantic.Field(
        default=None,
        description="If specified, enable input for these pipelines only.",
    )

    def used_by(self, pipeline_name: str) -> bool:
        """Check if this input is configured for the specified pipeline."""
        return self.pipelines is None or pipeline_name in self.pipelines

    def setup(self, default_run_id: str) -> _LineageArg:
        """Download, verify and place the artifact."""
        lineage_arg, cached_artifact = self.with_defaults(run_id=default_run_id)._load(dry_run=True)

        paths.place_path(
            tgt=self.path,
            src=cached_artifact,
            overwrite=self.overwrite,
            mode="link" if self.link else "copy",
        )

        if self.path.is_dir() and not self.link:
            paths.rchmod(self.path, paths.Mode.rwx)

        return lineage_arg
