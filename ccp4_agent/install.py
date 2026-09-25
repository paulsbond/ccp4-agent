import shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parent / "ccp4"


def main() -> None:
    for agent_dir in (".agents", ".claude"):
        dest = Path.home() / agent_dir / "skills" / SKILL.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_symlink() or dest.is_file():
            dest.unlink()
        elif dest.is_dir():
            shutil.rmtree(dest)
        try:
            dest.symlink_to(SKILL, target_is_directory=True)
        except OSError:
            shutil.copytree(SKILL, dest)
        print("Finished installing the CCP4 agent skill.")
