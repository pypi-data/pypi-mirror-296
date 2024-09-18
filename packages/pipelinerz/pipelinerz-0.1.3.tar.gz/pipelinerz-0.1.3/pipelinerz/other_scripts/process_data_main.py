
import warnings

from looming_spots.db.loom_trial_group import MouseLoomTrialGroup
from looming_spots.loom_io.load import sync_raw_and_processed_data
from magicgui import magicgui

from npix_lse.slurm.slurm_interfaces.bombcell import bombcell_slurm
from npix_lse.slurm.slurm_interfaces.brainreg import brainreg_slurm
from npix_lse.metadata.sorting_metadata import SortingMetadata
from npix_lse.slurm.slurm_interfaces.sort import (
    run_full_sorting_pipeline_on_mouse,
)
from npix_lse.load_sync_channels.extract_sync_channel import extract_all_sync_channels
from npix_lse.slurm.slurm_interfaces.track_mouse_dlc import track_mouse_slurm


def main():
    pipeline.show()


@magicgui
def pipeline(mouse_ids:list =["hello", "bye"],
             derivatives_directory: str ="/ceph/margrie/slenzi/2024/SC/derivatives/",
             rawdata_directory: str = "/ceph/margrie/slenzi/2024/SC/rawdata/",
             brainreg:bool =True,
             behaviour:bool =True,
             spikesorting:bool=True,
             bombcell:bool=True,
             ):

    for mouse_id in mouse_ids:
        mtd = SortingMetadata(
            mouse_id,
            root=derivatives_directory,
        )
        if not mtd.mouse_dir.exists():
            warnings.warn("mouse directory not found")
            raise ValueError

        print("syncing data...")
        sync_raw_and_processed_data(mouse_id=mtd.mouse_id,
                                    raw_directory=rawdata_directory,
                                    processed_directory=derivatives_directory)

        if brainreg:
            print("brainreg job setup...")
            brainreg_slurm(mtd)

        if behaviour:
            mtg = MouseLoomTrialGroup(mouse_id,  #necessary to initialise data
                                      processed_data_dir=derivatives_directory)

            print("tracking job setup...")
            track_mouse_slurm(mtd)

            print("extract sync channels...")
            extract_all_sync_channels(mtd)

        if spikesorting:
            print("sorting job setup...")
            run_full_sorting_pipeline_on_mouse(mtd)

        if bombcell:
            print("running bombcell...")
            bombcell_slurm(mtd.sessions[-1], overwrite=True)
            bombcell_all_sessions(mtd,
                                  overwrite=True
                                  )

if __name__ == "__main__":
    pipeline.show()
    print("")

    # mouse_ids = [
    #     "sub-016_id-1121662",
    # ]
    # derivatives_directory = pathlib.Path("/ceph/margrie/slenzi/2024/SC/derivatives/")
    # rawdata_directory = pathlib.Path("/ceph/margrie/slenzi/2024/SC/rawdata/")
    #
    # pipeline_kwargs = {
    #                     "brainreg": True,
    #                     "behaviour": True,
    #                     "spikesorting": True,
    #                     "bombcell": True,
    # }

# def bombcell_all_sessions(mtd, overwrite=False):
#     for s in mtd.sessions:
#         if s.kilosort_dir:
#             bombcell_slurm(s, overwrite)
