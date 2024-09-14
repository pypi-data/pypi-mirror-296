# import multiprocessing as mp
# from pathlib import Path
from .core import segment_niftis as segment_niftis


def segment_niftis_cli(
    nifti_list: list[str],
    task_list: list[str],
    devices: list[str],
    cache_num: int,
    sw_batch_size: int,
    threads: int,
    num_dataloader_workers: int,
) -> None:
    """Segment niftis using the CLI
    Parameters
    ----------
    nifti_list : list[str]
        The list of nifti files to segment
    task_list : list[str]
        The list of tasks to segment
    devices : list[str]
        The list of devices to segment on
    cache_num : int
        The number of nifti files to cache at one time for inference
    sw_batch_size : int
        The sliding window batch size during inference
    threads : int
        The number of threads for multi-threaded ops
    num_dataloader_workers : int
        The number of worker processes to use loading images
    """
    pass
