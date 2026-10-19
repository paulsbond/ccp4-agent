import re
from pathlib import Path

import gemmi
import numpy as np
import pandas as pd

FREE_LABEL = re.compile("free|test", re.IGNORECASE)


def _flag_columns(mtz: gemmi.Mtz) -> list[str]:
    return [
        c.label for c in mtz.columns if c.type == "I" and FREE_LABEL.search(c.label)
    ]


def _observed(mtz: gemmi.Mtz, data: pd.DataFrame) -> pd.Series:
    labels = [c.label for c in mtz.columns if c.type in "FJ"]
    if not labels:
        return pd.Series(True, index=data.index)
    return data[labels].notna().any(axis=1)


def _free_value(counts: pd.Series) -> int | None:
    below_half = counts[counts < counts.sum() / 2]
    return None if below_half.empty else int(below_half.index.min())


def _convention(values: list[int], free: int) -> str:
    if free == 0 and values[-1] > 1:
        return f"CCP4 (flags {values[0]} to {values[-1]}, 0 is free)"
    if free == 0:
        return "0 is free, 1 is working"
    if values == [0, 1]:
        return "Phenix (1 is free, 0 is working)"
    return f"{free} is free"


def check(path: Path, label: str | None, output: Path | None) -> None:
    mtz = gemmi.read_mtz_file(str(path))
    if label is None:
        labels = _flag_columns(mtz)
        if not labels:
            print("No free-R flag column. Add one with freerflag.")
            return
        if len(labels) > 1:
            print(f"Several free-R flag columns: {', '.join(labels)}.")
            print("Run again with --label to choose one.")
            return
        label = labels[0]
    data = pd.DataFrame(mtz.array, columns=[c.label for c in mtz.columns], dtype=float)
    flags = data[label]
    counts = flags.dropna().astype(int).value_counts().sort_index()
    free = _free_value(counts)
    print(f"Column: {label}")
    if free is None:
        print("All flags are the same: there is no free set. Add one with freerflag.")
        return
    n_free, n_flagged = counts[free], counts.sum()
    print(f"Convention: {_convention(list(counts.index), free)}")
    print(
        f"Free reflections: {n_free} of {n_flagged} ({100 * n_free / n_flagged:.1f}%)"
    )
    unflagged = (flags.isna() & _observed(mtz, data)).sum()
    print(f"Observed reflections without a flag: {unflagged}")
    if unflagged:
        print("Give them flags with freerflag COMPLETE, keeping the others.")
    if free == 0:
        print("Already in the CCP4 convention: use this file as it is.")
        return
    if label != "FreeR_flag" and mtz.column_with_label("FreeR_flag"):
        print("The file also has a FreeR_flag column. Check which one is right.")
        return
    output = output or path.with_name(f"{path.stem}_freer.mtz")
    data[label] = np.where(flags.isna(), np.nan, np.where(flags == free, 0, 1))
    mtz.set_data(data.to_numpy(dtype=np.float32))
    mtz.column_with_label(label).label = "FreeR_flag"
    mtz.history += [
        f"ccp4-agent freer: free set {label}={free} written as FreeR_flag=0"
    ]
    mtz.write_to_file(str(output))
    print(
        f"Wrote {output}, with {label} replaced by FreeR_flag (0 is free, 1 working)."
    )
