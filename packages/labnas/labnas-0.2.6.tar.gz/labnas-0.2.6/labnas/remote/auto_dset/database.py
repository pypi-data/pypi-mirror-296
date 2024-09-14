import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

from labnas.remote.imaging import ImagingNas
from labnas.remote.auto_dset.utils import scan_multipage_tiffs, check_file_name_for_disqualifiers, check_file_name_with_list

ALLOWED_SESSIONS = [
    "flashes",
    "cfs",
    "conflict",
    "alternations",
    "ori",
]

LOCAL_DIR = Path("/home/mathis/Code/gitlab/labnas/data/temp")

class DataBase:
    def __init__(
            self,
            source_dir: Path,
            target_dir: Path,
            source_nas: ImagingNas,
            target_nas: ImagingNas,
    ) -> None:
        # params
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.source_nas = source_nas
        self.target_nas = target_nas

        # other
        self.tif_files = []
        self.stim_types = []
        self.dset_names = []
        self.df = None

    def run(self) -> None:
        self.scan_tifs()
        self.load_database()
        self.iter_tifs()

    def scan_tifs(self) -> None:
        """Look for 2p recording tifs that could be the basis of a dataset"""
        print("Looking for multipage tiffs")
        tif_candidates = scan_multipage_tiffs(self.source_dir, self.source_nas)
        print(f"TIFFs in multipage folders: {len(tif_candidates)}")
        selected = []
        stim_types = []
        for file in tif_candidates:
            file_name = file.name
            is_ok = check_file_name_for_disqualifiers(file_name)
            is_relevant, stim_type = check_file_name_with_list(file_name, ALLOWED_SESSIONS)
            if is_ok & is_relevant:
                selected.append(file)
                stim_types.append(stim_type)
        print(f"Selected TIFFs for auto-dset: {len(selected)}")
        self.tif_files = selected
        self.stim_types = stim_types

    def load_database(self) -> None:
        csv_file = self.target_dir / "database.csv"
        if self.target_nas.is_file(csv_file):
            local_copy = LOCAL_DIR / csv_file.name
            self.target_nas.download_file(csv_file, local_copy, overwrite=True)
            self.df = pd.read_csv(local_copy)
            os.remove(local_copy)
            print(f"Entries in database: {self.df.shape[0]}")
        else:
            print("Could not load database file.")

    def iter_tifs(self) -> None:
        for file, stim_type in zip(self.tif_files, self.stim_types):
            dset_name = self.get_dset_name(file, stim_type)
            print(f"---{dset_name}---")
            if self.df is not None:
                if dset_name in self.df["dset_name"].values:
                    print(f"{dset_name}: already in database")
            self.check_files(dset_name)

    def get_dset_name(self, tif_file: Path, stim_type: str) -> str:
        """Get a unique name for a recording."""
        count = 0
        mouse_name = tif_file.parts[3]
        date_string = tif_file.parts[4]
        short_date = date_string.replace("-", "")
        dset_name = f"{short_date}_{mouse_name}_{stim_type}_{count}"
        if dset_name in self.dset_names:
            while dset_name in self.dset_names:
                count += 1
                dset_name = f"{short_date}_{mouse_name}_{stim_type}_{count}"
        self.dset_names.append(dset_name)
        return dset_name

    def check_files(self, dset_name: str) -> None:
        dset_folder = self.target_dir / dset_name
        if not self.target_nas.is_dir(dset_folder):
            self.target_nas.create_empty_folder(dset_folder)

        self.check_target(dset_folder)

    def check_target(self, dset_folder: Path) -> None:
        frame_info_file = dset_folder / "frame_info.csv"
        if not self.target_nas.is_file(frame_info_file):
            print("No frame_info file yet.")
            self.generate_frame_info(dset_folder)

    def generate_frame_info(self, dset_folder: Path) -> None:
        stim_folder = dset_folder / "stim"
        if self.target_nas.is_dir(stim_folder):
            self._process_stim(dset_folder)
        else:
            print("No stim folder on target NAS yet.")
            self.find_raw_stim()
            # self._process_stim(dset_folder)

    def _process_stim(self, dset_folder: Path) -> None:
        stim_folder = dset_folder / "stim"
        daq_file = stim_folder / "daq.csv"

        if self.target_nas.is_file(daq_file):
            print("Downloading stim folder for processing")
            local_folder = LOCAL_DIR / "stim"
            stim_type = dset_folder.name.split("_")[2]
            if local_folder.is_dir():
                shutil.rmtree(local_folder)
            self.target_nas.download_folder(stim_folder, local_parent=LOCAL_DIR, verbose=False)

            print("Creating frame info file.")
            local_daq_file = local_folder / "daq.csv"
            daq_df = pl.read_csv(local_daq_file)

            local_flip_file = local_folder / "flip_info.csv"
            flip_df = pd.read_csv(local_flip_file)

            frame_info = self._subsample_daq(daq_df, flip_df)
            print(f"Frame info: {frame_info.shape[0]} rows")

            local_frame_file = local_folder / "frame_info.csv"
            frame_info.to_csv(local_frame_file)

            remote_file = dset_folder / "frame_info.csv"
            self.target_nas.upload_file(local_frame_file, remote_file)
            print(f"Uploaded {remote_file.name}")

            shutil.rmtree(local_folder)

    def _subsample_daq(self, daq_df: pl.DataFrame, flip_df: pd.DataFrame) -> pd.DataFrame:
        """
        TODO:
        - remove invalid rows (erroneous 2p triggers etc)
        - add info from flip_df
        """
        frame_info = daq_df.filter(pl.col(f"interval_twophoton_scanner").is_not_null())
        frame_info = frame_info.to_pandas()

        intervals = frame_info["interval_twophoton_scanner"].values
        intervals = intervals.astype(np.float32)
        median_interval = np.median(intervals)

        deviations = (intervals - median_interval) / median_interval
        abs_deviations = np.abs(deviations)
        is_faulty = abs_deviations > 0.25
        n_faulty = np.sum(is_faulty)
        print(f"{n_faulty} rows have deviating trigger intervals.")
        return frame_info

    def find_raw_stim(self) -> None:
        pass