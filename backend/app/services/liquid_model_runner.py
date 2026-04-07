from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
ALIGNN_ENV_PYTHON = ROOT_DIR / "alignn310" / "Scripts" / "python.exe"
PREDICT_SCRIPT = ROOT_DIR / "training" / "scripts" / "predict_liquid_model.py"
PRIMARY_META_PATH = ROOT_DIR / "models" / "liquid_model_meta.json"
FALLBACK_MODEL_PATH = ROOT_DIR / "models" / "liquid_model_training" / "best_liquid_model.pt"
FALLBACK_META_PATH = ROOT_DIR / "models" / "liquid_model_training" / "liquid_model_meta.json"


class LiquidModelRunner:
    def __init__(self, model_path: Path) -> None:
        self.model_path = model_path

    def _resolved_paths(self) -> tuple[Path | None, Path | None]:
        if self.model_path.exists() and PRIMARY_META_PATH.exists():
            return self.model_path, PRIMARY_META_PATH
        if FALLBACK_MODEL_PATH.exists() and FALLBACK_META_PATH.exists():
            return FALLBACK_MODEL_PATH, FALLBACK_META_PATH
        return None, None

    def available(self) -> bool:
        model_path, meta_path = self._resolved_paths()
        return (
            model_path is not None
            and meta_path is not None
            and ALIGNN_ENV_PYTHON.exists()
            and PREDICT_SCRIPT.exists()
        )

    def predict(self, payload: dict) -> dict | None:
        model_path, meta_path = self._resolved_paths()
        if (
            model_path is None
            or meta_path is None
            or not ALIGNN_ENV_PYTHON.exists()
            or not PREDICT_SCRIPT.exists()
        ):
            return None

        completed = subprocess.run(
            [
                str(ALIGNN_ENV_PYTHON),
                str(PREDICT_SCRIPT),
                json.dumps(payload),
                str(model_path),
                str(meta_path),
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(ROOT_DIR),
        )
        if completed.returncode != 0:
            return None
        try:
            return json.loads(completed.stdout.strip())
        except json.JSONDecodeError:
            return None
