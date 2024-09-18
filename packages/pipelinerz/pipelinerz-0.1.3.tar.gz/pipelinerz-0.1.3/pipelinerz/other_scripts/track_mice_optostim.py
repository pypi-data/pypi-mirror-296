import pathlib

from looming_spots.db.loom_trial_group import MouseLoomTrialGroup
from looming_spots.loom_io.load import sync_raw_and_processed_data

from npix_lse.slurm.slurm_interfaces.bombcell import bombcell_slurm
from npix_lse.metadata.sorting_metadata import SortingMetadata
from npix_lse.slurm.slurm_interfaces.track_mouse_dlc import track_mouse_slurm


def main():
    sub_ids = [
        #"sub-012_id-1121012",
        # "sub-013_id-1121013",
        # "sub-014_id-1121014",
        # "sub-016_id-1121016",
        # "sub-017_id-1121018",
        # "sub-025_id-1100581",
        # "sub-026_id-1100580",
        # "sub-028_id-1100589",
        #"sub-030_id-1100588",
        "sub-032_id-1100586",
        "sub-034_id-1100587",
        "sub-036_id-1100709",
        "sub-038_id-1100710",
        "sub-033_id-1100586_positive_control",
        "sub-035_id-1100587_positive_control",
        "sub-037_id-1100709_positive_control",
        "sub-039_id-1100710_positive_control",
    ]
    root = pathlib.Path("/ceph/margrie/slenzi/2023/julia_optostim/")
    rawdata_root = root / "rawdata"
    processed_data_root = root / "derivatives"

    for mouse_id in sub_ids:
        mtd = SortingMetadata(
            mouse_id,
            root=processed_data_root,
            probe=False,
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
