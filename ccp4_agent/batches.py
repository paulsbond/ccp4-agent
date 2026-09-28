from pathlib import Path

import gemmi
import pandas as pd

OUTLIER_FACTOR = 2


def _per_image(path: Path) -> pd.DataFrame:
    mtz = gemmi.read_mtz_file(str(path))
    labels = [column.label for column in mtz.columns]
    data = pd.DataFrame(mtz.array, columns=labels, dtype=float)
    data = data[["H", "K", "L", "BATCH", "I", "SIGI"]]
    mean = data.groupby(["H", "K", "L"])["I"].transform("mean")
    multiplicity = data.groupby(["H", "K", "L"])["I"].transform("size")
    data["deviation"] = (data["I"] - mean).abs().where(multiplicity > 1)
    data["i_over_sigma"] = data["I"] / data["SIGI"]
    images = data.groupby("BATCH").agg(
        observations=("I", "size"),
        i_over_sigma=("i_over_sigma", "mean"),
        deviation=("deviation", "sum"),
        intensity=("I", "sum"),
    )
    images["rmerge"] = images["deviation"] / images["intensity"]
    images.index = images.index.astype(int)
    images.index.name = "image"
    return images[["observations", "i_over_sigma", "rmerge"]]


def _by_range(images: pd.DataFrame, ranges: int) -> pd.DataFrame:
    groups = pd.cut(images.index, bins=min(ranges, len(images)))
    return (
        images.reset_index()
        .groupby(groups, observed=True)
        .agg(
            first_image=("image", "min"),
            last_image=("image", "max"),
            i_over_sigma=("i_over_sigma", "median"),
            rmerge=("rmerge", "median"),
        )
    )


def summarise(mtz: Path, ranges: int) -> None:
    images = _per_image(mtz)
    print("By image range (medians):")
    print(_by_range(images, ranges).round(3).to_string(index=False))

    rmerge, i_over_sigma = images["rmerge"].median(), images["i_over_sigma"].median()
    outliers = images[
        (images["rmerge"] > OUTLIER_FACTOR * rmerge)
        | (images["i_over_sigma"] < i_over_sigma / OUTLIER_FACTOR)
    ]
    print(
        f"\nImages with Rmerge above {OUTLIER_FACTOR} times the median ({rmerge:.3f}) "
        f"or I/sigma below 1/{OUTLIER_FACTOR} of the median ({i_over_sigma:.1f}):"
    )
    print(outliers.round(3).to_string() if len(outliers) else "none")
