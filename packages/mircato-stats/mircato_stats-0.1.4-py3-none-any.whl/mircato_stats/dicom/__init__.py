from time import time
from loguru import logger
from functools import partial
from pathlib import Path
from multiprocessing import Pool
from tqdm import tqdm
from .dicom_folder import DicomFolder as DicomFolder


def convert_dicom_folders_to_nifti(
    dicom_folders: list,
    output_dir: Path,
    num_workers: int,
    only_ax: bool,
    no_mip: bool,
    verbose: bool,
):
    """Main function to be passed to mircato CLI to convert DICOM folders to NIfTI
    Parameters
    ----------
    dicom_folders : list
        List of paths to DICOM folders
    output_dir : Path
        Path to the output directory
    num_workers : int
        Number of workers to use for the conversion
    only_ax : bool
        If True, only axial slices will be converted
    verbose : bool
        If True, verbose output will be printed
    """
    converter = partial(
        _process_dicom_folder, output_dir=output_dir, only_ax=only_ax, no_mip=no_mip
    )
    logger.info(
        f"Converting {len(dicom_folders)} dicom folders to nifti with {num_workers} workers"
    )
    start_time = time()
    with Pool(num_workers) as pool:
        if verbose:
            dicom_iterator = pool.imap_unordered(converter, dicom_folders)
        else:
            dicom_iterator = tqdm(
                pool.imap_unordered(converter, dicom_folders),
                total=len(dicom_folders),
                dynamic_ncols=True,
                desc="Converting DICOM folders to NIfTI",
            )
        for _ in dicom_iterator:
            pass
    end_time = time()
    logger.info(
        f"Conversion of {len(dicom_folders)} dicom folders to nifti completed in {end_time - start_time:.2f}s"
    )

def _process_dicom_folder(
    dicom_folder: str, output_dir: Path, only_ax: bool, no_mip: bool
) -> None:
    """Helper function to process a single dicom folder
    Parameters
    ----------
    dicom_folder : str
        Path to the dicom folder
    output_dir : Path
        Path to the output directory
    only_ax : bool
        If True, only axial slices will be converted
    no_mip : bool
        If True, mip series will not be converted
    """
    dicom_folder = DicomFolder(dicom_folder)
    dicom_folder.convert_to_nifti(output_dir, only_ax, no_mip)
