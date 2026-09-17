import zipfile
from pathlib import Path
root = Path(r"F:\20K_AI_Vin\day5\Day5-Segmentation-TRAN-DINH-CUONG-2A202602150-Lab-Student")
zip_path = root / "tiers_gt.zip"
out_path = root / "clean_tiers_gt.zip"
with zipfile.ZipFile(zip_path) as zin:
    mapping = {}
    for name in zin.namelist():
        low = name.lower()
        if "__macosx" in low or low.endswith(".ds_store"):
            continue
        if name.startswith("tiers/"):
            rel = name[len("tiers/") :]
            if rel.startswith("easy_semantic/groundtruth/") and rel.endswith(".png"):
                arc = "data/tiers/easy_semantic/groundtruth/" + rel.rsplit("/", 1)[1]
                mapping[arc] = name
            elif rel.startswith("hard_panoptic/groundtruth/png/") and rel.endswith(".png"):
                arc = "data/tiers/hard_panoptic/groundtruth/png/" + rel.rsplit("/", 1)[1]
                mapping[arc] = name
            elif rel == "hard_panoptic/groundtruth/panoptic.json":
                mapping["data/tiers/hard_panoptic/groundtruth/panoptic.json"] = name
            elif rel == "medium_instance/groundtruth/instances.json":
                mapping["data/tiers/medium_instance/groundtruth/instances.json"] = name
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for arc, src in mapping.items():
            zout.writestr(arc, zin.read(src))
    print(f"created {out_path} with {len(mapping)} files")
