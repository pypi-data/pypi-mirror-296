import pathlib

from looming_spots.db.loom_trial_group import MouseLoomTrialGroup
from looming_spots.loom_io.load import sync_raw_and_processed_data

from npix_lse.slurm.slurm_interfaces.bombcell import bombcell_slurm
from npix_lse.metadata.sorting_metadata import SortingMetadata
from npix_lse.slurm.slurm_interfaces.track_mouse_dlc import track_mouse_slurm


def main():
    sub_ids = [
        "sub-001_id-T10",
        "sub-002_id-T11",
        "sub-003_id-T12",
        "sub-004_id-T13",
        # "sub-005_id-TS24",
        "sub-006_id-TS26",
        "sub-007_id-TS33",
        "sub-008_id-TS34",
    ]
    root = pathlib.Path("/ceph/margrie/slenzi/2023/msj_photometry/")
    rawdata_root = root / "rawdata"
    processed_data_root = root / "derivatives"

    for mouse_id in sub_ids:
        mtd = SortingMetadata(
            mouse_id,
            root=processed_data_root,
        )

        sync_raw_and_processed_data(mouse_id=mtd.mouse_id,
                                    raw_directory=rawdata_root,
                                    processed_directory=processed_data_root,
                                    )

        mtg = MouseLoomTrialGroup(mouse_id,
                                  processed_data_dir=str(processed_data_root),
                                  photometry=False,
                                  )
        track_mouse_slurm(mtd)


def bombcell_all_sessions(mtd):
    for s in mtd.sessions:
        if s.kilosort_dir:
            bombcell_slurm(s)


if __name__ == "__main__":
    main()
