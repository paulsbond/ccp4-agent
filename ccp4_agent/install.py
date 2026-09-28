import os
import shutil
import stat
import subprocess
from pathlib import Path

SKILL = Path(__file__).resolve().parent / "ccp4"
MARKER = "source: ccp4-agent"
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


def _dest(agent_dir: str) -> Path:
    return Path.home() / agent_dir / "skills" / SKILL.name


def _is_link(path: Path) -> bool:
    return path.is_symlink() or _is_reparse_point(path)


def _is_ours(path: Path) -> bool:
    skill = path / "SKILL.md"
    if skill.is_file():
        return MARKER in skill.read_text()
    return _is_link(path)


def _link(dest: Path) -> None:
    if os.name == "nt":
        command = ["cmd", "/c", "mklink", "/J", str(dest), str(SKILL)]
        subprocess.run(command, check=True, capture_output=True)
    else:
        dest.symlink_to(SKILL, target_is_directory=True)


def install() -> None:
    copied = False
    installed = []
    others = []
    for agent_dir, agents in AGENTS.items():
        dest = _dest(agent_dir)
        if (dest.exists() or _is_link(dest)) and not _is_ours(dest):
            others.append(dest)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        _remove(dest)
        try:
            _link(dest)
        except (OSError, subprocess.CalledProcessError):
            shutil.copytree(SKILL, dest)
            copied = True
        installed.append((dest, agents))

    for dest in others:
        print(f"{dest} holds a different skill, so it was left unchanged.")
        print("To install this one there, rename or remove that skill first.\n")
    if not installed:
        raise SystemExit(1)

    print("Installed the ccp4 skill for your agents:")
    for dest, agents in installed:
        print(f"  {dest} ({agents})")
    if copied:
        print(f"\nThese are copies of {SKILL}, because links could not be made.")
        print("Run ccp4-agent install again after every CCP4 update.")
    else:
        print(f"\nThese link to {SKILL},")
        print("so updates to this CCP4 installation also update the skill.")
        print("After installing a new CCP4 version, run its ccp4-agent install.")
    print("\nIf your agent does not support skills, tell it to read")
    print(installed[0][0] / "SKILL.md")


def uninstall() -> None:
    removed = False
    for agent_dir in AGENTS:
        dest = _dest(agent_dir)
        if not (dest.exists() or _is_link(dest)):
            continue
        if _is_ours(dest):
            _remove(dest)
            print(f"Removed {dest}")
            removed = True
        else:
            print(f"{dest} holds a different skill, so it was left unchanged.")
    if not removed:
        print("The ccp4 skill was not installed.")
