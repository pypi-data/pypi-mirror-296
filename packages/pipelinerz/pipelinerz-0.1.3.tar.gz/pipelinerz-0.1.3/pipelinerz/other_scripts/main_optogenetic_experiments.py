import pathlib
import warnings

from looming_spots.db.loom_trial_group import MouseLoomTrialGroup
from looming_spots.loom_io.load import sync_raw_and_processed_data

from npix_lse.metadata.sorting_metadata import SortingMetadata
from npix_lse.slurm.slurm_interfaces.track_mouse_dlc import track_mouse_slurm


def main():
    # sub_ids = [
    #     #"sub-012_id-1121012", # corrupt photodiode for first recordings
    #     "sub-013_id-1121013",
    #     "sub-014_id-1121014",
    #     "sub-016_id-1121016",
    #     "sub-017_id-1121018",
    #     "sub-025_id-1100581",
    #     "sub-026_id-1100580",
    #     "sub-028_id-1100589",
    #     "sub-030_id-1100588",
    # ]
    rawdata_path = pathlib.Path("/ceph/margrie/juliaw/rawdata/optostim_experiments")
    derivatives_path = pathlib.Path("/ceph/margrie/juliaw/derivatives/optostim_experiments")

    #sub_ids = [x.stem for x in rawdata_path.glob("*")]
    sub_ids = [
        # "sub-055_id-1100827",
        # "sub-056_id-1100826",
        # "sub-057_id-1100828",
        # "sub-058_id-1100832",
        # "sub-058_id-1100833",
        # "sub-058_id-1100834",
        # "sub-060_id-1121712",
        # "sub-061_id-1121666",
        # "sub-062_id-1121667",

        #"sub-048_id-1121479",
        # "sub-053_id-1121567",
        # "sub-064_id-1100833",
        # "sub-063_id-1121667",
        # "sub-062_id-1121666",
        # "sub-061_id-1100834",
        # "sub-049_id-1121575",
        # "sub-046_id-1121577",
        # "sub-052_id-1121477",
        # "sub-048_id-1121479",
        # "sub-059_id-1121711",
        "sub-075_id-1101215",
        "sub-074_id-1101216",


    ]

    for mouse_id in sub_ids:
        mtd = SortingMetadata(
            mouse_id,
            root=derivatives_path,
            probe=False,
        )
        if not mtd.mouse_dir.exists():
            warnings.warn("mouse directory not found")
            raise ValueError

        try:
            sync_raw_and_processed_data(mouse_id=mtd.mouse_id, raw_directory=rawdata_path, processed_directory=derivatives_path)
            mtg = MouseLoomTrialGroup(mouse_id, processed_data_dir=derivatives_path)
            track_mouse_slurm(mtd)
        except Exception as e:
            print(e)
        #brainreg_slurm(mtd)


if __name__ == "__main__":
    main()
