import os
import shutil
import stat
import subprocess
from pathlib import Path

SKILL = Path(__file__).resolve().parent / "ccp4"
AGENTS = {
    ".agents": "Codex, Gemini CLI, Cursor, Copilot and others",
    ".claude": "Claude Code",
}


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (FileNotFoundError, AttributeError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _remove(path: Path) -> None:
    if _is_reparse_point(path):
        path.rmdir()
    elif path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _link(dest: Path) -> None:
    if os.name == "nt":
        command = ["cmd", "/c", "mklink", "/J", str(dest), str(SKILL)]
        subprocess.run(command, check=True, capture_output=True)
    else:
        dest.symlink_to(SKILL, target_is_directory=True)


def main() -> None:
    copied = False
    installed = []
    for agent_dir, agents in AGENTS.items():
        dest = Path.home() / agent_dir / "skills" / SKILL.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        _remove(dest)
        try:
            _link(dest)
        except (OSError, subprocess.CalledProcessError):
            shutil.copytree(SKILL, dest)
            copied = True
        installed.append(f"  {dest} ({agents})")

    print("Installed the ccp4 skill for your agents:")
    print("\n".join(installed))
    if copied:
        print(f"\nThese are copies of {SKILL}, because links could not be made.")
        print("Run ccp4-agent-install again after every CCP4 update.")
    else:
        print(f"\nThese link to {SKILL},")
        print("so updates to this CCP4 installation also update the skill.")
        print("After installing a new CCP4 version, run its ccp4-agent-install.")
    print("\nIf your agent does not support skills, tell it to read")
    print(Path.home() / ".agents" / "skills" / SKILL.name / "SKILL.md")
