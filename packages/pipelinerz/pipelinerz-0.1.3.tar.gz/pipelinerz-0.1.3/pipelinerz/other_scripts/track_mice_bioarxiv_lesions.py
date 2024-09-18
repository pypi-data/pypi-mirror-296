import pathlib

from looming_spots.db.loom_trial_group import MouseLoomTrialGroup
from looming_spots.loom_io.load import sync_raw_and_processed_data

from npix_lse.metadata.sorting_metadata import SortingMetadata
from npix_lse.slurm.slurm_interfaces.track_mouse_dlc import track_mouse_slurm


def main():
    sub_ids = [
    # "CA451A_2",
    # "CA451A_3",
    # "CA451A_4",
    # "CA507_1",
    # "CA507_3",
    # "CA507_4",
    # "CA493_1",
    # "CA493_2",
    # "CA459A_2",
    # "CA478_3",
    # "CA476_5",
    # "CA507_2",
    # "CA507_5",
    # "CA493_3",
    # "CA493_4",

    # "sub-064_id-1101073",
    # "sub-065_id-1101072",
    # "sub-066_id-1101057",
    # "sub-068_id-1101074",
    # "sub-067_id-1101075",
    # "sub-069_id-1101058",
    # "sub-072_id-1101189",
    # "sub-073_id-1101185",
    #"sub-076_id-1122311",
    #"sub-077_id-1101326",
    #"sub-078_id-1101447",
    "sub-079_id-1101446",
    ]
    root = pathlib.Path("/ceph/margrie/slenzi/loomer/")
    rawdata_root = root / "rawdata"
    processed_data_root = root / "derivatives"

    for mouse_id in sub_ids:
        mtd = SortingMetadata(
            mouse_id,
            root=processed_data_root,
            probe=False,
            make_mouse_dirs=False,
        )

        sync_raw_and_processed_data(mouse_id=mtd.mouse_id,
                                    raw_directory=rawdata_root,
                                    processed_directory=processed_data_root,
                                    )

        mtg = MouseLoomTrialGroup(mouse_id,
                                  processed_data_dir=str(processed_data_root),
                                  photometry=False,
                                  )
        track_mouse_slurm(mtd,
                          skip_video_processing=False)


if __name__ == "__main__":
    main()
