# pipelinerz

Pipelinerz aims to coordinate different data sources for analysing escape and LSE experiments.
It should allow the user to run specific parts of a common neuroscience analysis pipeline.

Designed to be used alongside SWC Neuroblueprint data organisation principles. 
See: https://neuroblueprint.neuroinformatics.dev/ 

This includes:

**Behavioural recordings analysis**
    - Nidaq data extraction (daq_loader)
    - Tracking using DLC (lmtracker)

**Serial2p image analysis**
    - Brain registration (brainreg)
    - Cellfinder (not implemented)

**Electrophysiology analysis**
    - Preprocessing (Spikewrap)
    - Spike sorting (Spikewrap)
    - Spike train handling (probez)
    - Automated curation tools (bombcell, unitmatch)

The only arguments needed are the root directories for rawdata and processed data
as well as the directory where serial2p images are stored. Data are assumed to follow NIU
blueprint.

- extract sync trigger data
  - assert that the number of frames is consistent across different data sources (i.e. photodiode vs. probe sync TTL)
- transfer relevant data from raw to derivatives
  - convert videos from avi to mp4
  - extract behaviour data on the camera frames only and save as .npy (i.e. photodiode, photometry etc)
- submit DLC tracking job to the swc hpc
- submit spikesorting job with spikewrap to the swc hpc
- submit brain registration job to the swc hpc

Data considered here consist of the following:

#### Behavioural recordings
- camera.avi file of mouse behaviour
- AI.tdms file 
  - stimulus information (photodiode used to get looming stimulus onsets)
  - auditory stimulus (when present)
  - photometry signals and waveform
  - TTL clock (used to trigger camera and synchronise with other sources e.g. npix)

#### Tracking
- Pose estimation and tracking of mouse position over time is carried out using deeplabcut

#### Probe recordings
- Data acquired using neuropixels probes and spikeglx
- .ap.bin files
- Sync channel (of the probe) that receives the same TTL as the camera (at 40 hz)
- All preprocessing and sorting uses spikewrap (and therefore spike-/probe- interface). 
  - See: https://github.com/neuroinformatics-unit/spikewrap

#### Histology
- Brainreg is used to register serial2p images such that they are ready to be used in brainreg-segment
for the reconstruction of probe tracks


### Installation

    pip install pipelinerz
    git clone https://github.com/JoeZiminski/spikewrap.git
    cd spikewrap
    pip install -e .


### Usage from commandline

    pipelinerz_gui

![](../../../../Desktop/Screenshot from 2024-09-17 11-59-41.png)

When you update the rawdata directory all the available mouse ids will be listed.

![](../../../../Desktop/Screenshot from 2024-09-17 12-00-18.png)

The selected mouse ids will be processed when you press "run".

![](../../../../Desktop/Screenshot from 2024-09-17 12-01-37.png)
