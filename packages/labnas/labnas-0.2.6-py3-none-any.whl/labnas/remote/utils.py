import re
from pathlib import Path

from labnas.remote.base import SftpNas


PATTERN = "[0-9]+.[0-9]+.[0-9]+.[0-9]+/"

def trim_path(remote_path: Path) -> Path:
    """Remove IP address etc from a remote path."""
    string = str(remote_path)
    if re.findall(PATTERN, string):
        sub_string = re.split(PATTERN, string)[-1]
        new_path = Path(sub_string)
        return new_path
    else:
        return remote_path


def delete_if_empty(folder: Path, nas: SftpNas, trash: Path) -> None:
    """Delete a remote folder if it is empty."""
    if not nas.is_dir(folder):
        raise FileNotFoundError(f"{folder}")
    if nas.is_empty(folder):
        trash_name = "_".join(folder.parts)
        trash_target = trash / trash_name
        nas.move_folder(folder, trash_target)
        print(f"{folder} deleted.")



def check_eyetracking(recording_folder: Path, nas: SftpNas) -> None:
    """Check whether a remote folder contains subfolders for right and left eye."""
    files, folders = nas.list_files_and_folders(recording_folder)
    has_right = False
    has_left = False
    right_size = None
    left_size = None
    for folder in folders:
        if folder.name == "right_eye":
            has_right = True
        elif folder.name == "left_eye":
            has_left = True
        sub_files, sub_folders = nas.list_files_and_folders(folder)
        for file in sub_files:
            # print(file)
            pass
        for f in sub_folders:
            print(f)
    if not has_right:
        raise FileNotFoundError(f"{recording_folder / 'right_eye'} does not exist.")
    if not has_left:
        raise FileNotFoundError(f"{recording_folder / 'left_eye'} does not exist.")
