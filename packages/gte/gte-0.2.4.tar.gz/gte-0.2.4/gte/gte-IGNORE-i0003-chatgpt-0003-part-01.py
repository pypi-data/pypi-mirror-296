#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ground Truth Establisher (GTE) Module.

Great stuff!

"""

import random
import numpy as np
import pandas as pd
import nibabel as nib
import pathlib
import mne
from mne.simulation import SourceSimulator
from mne.beamformer import Beamformer

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Optional, Union, List, Dict, Tuple
from typing import get_origin, get_args

from .aux_log import Log0

logZ = Log0()
log0 = logZ.logger


@dataclass
class GTE:
    """
    Ground Truth Establisher (GTE) class for data gathering and simulations.

    This class is designed to handle data gathering and perform simulations,
    primarily using MNE-Python. It provides functionality to manage subject
    directories, individual subject data, and MNE objects for simulations.

    Attributes
    ----------
    _subjects_dir : Optional[Path]
        Private attribute to store the subjects directory path.
    _subject : Optional[str]
        Private attribute to store the current subject identifier.
    _info0 : Optional[mne.Info]
        Private attribute to store the MNE Info object.
    _montage0 : Optional[mne.channels.DigMontage]
        Private attribute to store the MNE DigMontage object.
    _trans0 : Optional[mne.transforms.Transform]
        Private attribute to store the MNE Transform object.
    _src0 : Optional[mne.SourceSpaces]
        Private attribute to store the MNE SourceSpaces object.
    _bem_model0 : Optional[List[mne.bem.ConductorModel]]
        Private attribute to store the MNE BEM model.
    _bem_solution0 : Optional[mne.bem.ConductorModel]
        Private attribute to store the MNE BEM solution.
    _fwd0 : Optional[mne.Forward]
        Private attribute to store the MNE Forward solution.
    _genuine_noise_cov0 : Optional[mne.Covariance]
        Private attribute to store the real noise covariance matrix.
    _annot0 : Optional[str]
        Private attribute to store the FreeSurfer's annot (surface labels).
    _labels0 : Optional[List[mne.Label]]
        FreeSurfer parcellation labels.
    _label0_names : Optional[List[str]]
        FreeSurfer parcellation label names.
    _labels2 : Optional[List[mne.Label]]
        Vertices selected as activity/noise sources.
    _label2_names : Optional[List[str]]
        Label names for vertices selected as activity/noise sources.
    _labels3 : Optional[List[mne.Label]]
        Additional processed labels.
    _label3_names : Optional[List[str]]
        Names of the additional processed labels.
    _labels4 : Optional[List[mne.Label]]
        Final set of labels after processing.
    _label4_names : Optional[List[str]]
        Names of the final set of labels.
    _singularity_events : Optional[np.ndarray]
        Singularity events array.
    _singularity_event_IDs : Optional[Dict[str, int]]
        Mapping of singularity event labels to their numeric codes.
    _singularity_events_desc : Optional[Dict[int, str]]
        Mapping of numeric event codes to their corresponding labels for singularity events.
    _singularity_events_df : Optional[pd.DataFrame]
        DataFrame containing detailed information about singularity events.
    _experimental_events : Optional[np.ndarray]
        Experimental events array.
    _experimental_event_IDs : Optional[Dict[str, int]]
        Mapping of experimental event labels to their numeric codes.
    _experimental_events_desc : Optional[Dict[int, str]]
        Mapping of numeric event codes to their corresponding labels for experimental events.
    _experimental_events_df : Optional[pd.DataFrame]
        DataFrame containing detailed information about experimental events.
    _activ0 : Optional[Dict[str, Dict[str, Dict[str, float]]]]
        Nested dictionary of predefined activations.
    _activ0_labels : Optional[List[str]]
        List of unique activation labels.
    _activ0_events : Optional[List[str]]
        List of activation events.
    _activ0_trial_num_samp : Optional[int]
        Number of samples for the activation trial.
    _times0 : Optional[np.ndarray]
        Array of time points for the activation trial.
    _source_simulator : Optional[SourceSimulator]
        SourceSimulator object for simulations.
    _activ0_stc : Optional[mne.SourceEstimate]
        Cached source estimate (STC).
    _activ0_raw : Optional[mne.io.Raw]
        Cached time course (Raw) without noise.
    _activ2_raw : Optional[mne.io.Raw]
        Cached time course (Raw) with noise added.
    _activ2_epochs : Optional[mne.Epochs]
        Cached time course (Epochs).
    _activ2_evoked : Optional[Dict[str, mne.Evoked]]
        Cached evoked responses.
    _activ2_data_cov : Optional[mne.Covariance]
        Data covariance.
    _activ2_noise_cov : Optional[mne.Covariance]
        Noise covariance.
    _activ2_common_cov : Optional[mne.Covariance]
        Common covariance.
    _filters : Optional[Dict[str, Beamformer]]
        LCMV beamformer filters.
    _stcs : Optional[Dict[str, mne.SourceEstimate]]
        Source estimates computed by applying LCMV beamformer filters.
    """

    _subjects_dir: Optional[Path] = field(default=None, init=False)
    _subject: Optional[str] = field(default=None, init=False)
    _info0: Optional[mne.Info] = field(default=None, init=False)
    _montage0: Optional[mne.channels.DigMontage] = field(default=None, init=False)
    _trans0: Optional[mne.transforms.Transform] = field(default=None, init=False)
    _src0: Optional[mne.SourceSpaces] = field(default=None, init=False)
    _bem_model0: Optional[List[mne.bem.ConductorModel]] = field(default=None, init=False)
    _bem_solution0: Optional[mne.bem.ConductorModel] = field(default=None, init=False)
    _fwd0: Optional[mne.Forward] = field(default=None, init=False)
    _genuine_noise_cov0: Optional[mne.Covariance] = field(default=None, init=False)

    _annot0: Optional[str] = field(default=None, init=False)
    _labels0: Optional[List[mne.Label]] = field(default=None, init=False)
    _label0_names: Optional[List[str]] = field(default=None, init=False)
    _labels2: Optional[List[mne.Label]] = field(default=None, init=False)
    _label2_names: Optional[List[str]] = field(default=None, init=False)
    _labels3: Optional[List[mne.Label]] = field(default=None, init=False)
    _label3_names: Optional[List[str]] = field(default=None, init=False)
    _labels4: Optional[List[mne.Label]] = field(default=None, init=False)
    _label4_names: Optional[List[str]] = field(default=None, init=False)

    _singularity_events: Optional[np.ndarray] = field(default=None, init=False)
    _singularity_event_IDs: Optional[Dict[str, int]] = field(default=None, init=False)
    _singularity_events_desc: Optional[Dict[int, str]] = field(default=None, init=False)
    _singularity_events_df: Optional[pd.DataFrame] = field(default=None, init=False)

    _experimental_events: Optional[np.ndarray] = field(default=None, init=False)
    _experimental_event_IDs: Optional[Dict[str, int]] = field(default=None, init=False)
    _experimental_events_desc: Optional[Dict[int, str]] = field(default=None, init=False)
    _experimental_events_df: Optional[pd.DataFrame] = field(default=None, init=False)
    _activ0: Optional[Dict[str, Dict[str, Dict[str, float]]]] = field(default=None, init=False)
    _activ0_labels: Optional[List[str]] = field(default=None, init=False)
    _activ0_events: Optional[List[str]] = field(default=None, init=False)
    _activ0_trial_num_samp: Optional[int] = field(default=None, init=False)
    _times0: Optional[np.ndarray] = field(default=None, init=False)
    _source_simulator: Optional[SourceSimulator] = field(default=None, init=False)
    _activ0_stc: Optional[mne.SourceEstimate] = field(default=None, init=False)
    _activ0_raw: Optional[mne.io.Raw] = field(default=None, init=False)
    _activ2_raw: Optional[mne.io.Raw] = field(default=None, init=False)
    _activ2_epochs: Optional[mne.Epochs] = field(default=None, init=False)
    _activ2_evoked: Optional[Dict[str, mne.Evoked]] = field(default=None, init=False)
    _activ2_data_cov: Optional[mne.Covariance] = field(default=None, init=False)
    _activ2_noise_cov: Optional[mne.Covariance] = field(default=None, init=False)
    _activ2_common_cov: Optional[mne.Covariance] = field(default=None, init=False)
    _filters: Optional[Dict[str, Beamformer]] = field(default=None, init=False)
    _stcs: Optional[Dict[str, mne.SourceEstimate]] = field(default=None, init=False)

    def __post_init__(self):
        """Post-initialization method to set up default values if needed."""
        pass

    @staticmethod
    def _is_valid_dir(path: Path) -> bool:
        """
        Check if a path is a valid directory or a symlink to a valid directory.

        Parameters
        ----------
        path : Path
            The path to check.

        Returns
        -------
        bool
            True if the path is a valid directory or a symlink to a valid directory,
            False otherwise.
        """
        return path.exists() and (path.is_dir() or (path.is_symlink() and path.resolve().is_dir()))

    @property
    def subjects_dir(self) -> Optional[Path]:
        """
        Get or set the subjects directory path.

        Returns
        -------
        Optional[Path]
            The path to the subjects directory if set, otherwise None.
        """
        return self._subjects_dir

    @subjects_dir.setter
    def subjects_dir(self, value: Optional[Path]):
        """
        Set the subjects directory path.

        Parameters
        ----------
        value : Optional[Path]
            The path to set as the subjects directory. If None, the subjects_dir will be set to None.

        Raises
        ------
        ValueError
            If the provided path does not exist, is not a directory, or is not a symlink to a directory.
        """
        if value is not None:
            path = Path(value).expanduser().resolve()
            if not self._is_valid_dir(path):
                raise ValueError(
                    f"The provided subjects_dir '{path}' does not exist, is not a directory, or is not a symlink to a directory."
                )
            self._subjects_dir = path
        else:
            self._subjects_dir = None

    @property
    def subject(self) -> Optional[str]:
        """
        Get or set the current subject identifier.

        Returns
        -------
        Optional[str]
            The identifier of the current subject if set, otherwise None.
        """
        return self._subject

    @subject.setter
    def subject(self, value: Optional[str]):
        """
        Set the current subject identifier.

        Parameters
        ----------
        value : Optional[str]
            The identifier to set as the current subject. If None, the current subject will be unset.

        Raises
        ------
        ValueError
            If subjects_dir is not set when trying to set a subject, or if the subject directory does not exist.
        """
        if value is not None:
            if self._subjects_dir is None:
                raise ValueError("subjects_dir must be set before setting a subject")
            subject_path = (self._subjects_dir / value).resolve()
            if not self._is_valid_dir(subject_path):
                raise ValueError(
                    f"The subject directory '{subject_path}' does not exist, is not a directory, or is not a symlink to a directory."
                )
        self._subject = value

    @property
    def subject_dir(self) -> Optional[Path]:
        """
        Get the directory path for the current subject.

        Returns
        -------
        Optional[Path]
            The path to the current subject's directory if both subjects_dir and subject are set, otherwise None.
        """
        if self._subjects_dir is not None and self._subject is not None:
            return (self._subjects_dir / self._subject).resolve()
        return None

    @property
    def info0(self) -> Optional[mne.Info]:
        """
        Get or set the MNE Info object.

        Returns
        -------
        Optional[mne.Info]
            The MNE Info object if loaded, otherwise None.
        """
        return self._info0

    @info0.setter
    def info0(self, fif_file: Union[str, Path]):
        """
        Load MNE Info from a .fif file and set it as the current info.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the .fif file to load the MNE Info from.

        Raises
        ------
        ValueError
            If the file does not exist or is not a .fif file.
        RuntimeError
            If there's an error while reading the .fif file.
        """
        fif_path = self._get_mne_file_path(fif_file, "-info.fif")
        try:
            self._info0 = mne.io.read_info(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading .fif file: {str(e)}")

    @property
    def montage0(self) -> Optional[mne.channels.DigMontage]:
        """
        Get or set the MNE DigMontage object.

        Returns
        -------
        Optional[mne.channels.DigMontage]
            The MNE DigMontage object if loaded, otherwise None.
        """
        return self._montage0

    @montage0.setter
    def montage0(self, fif_file: Union[str, Path]):
        """
        Load MNE DigMontage from a -montage.fif file and set it as the current montage.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the -montage.fif file to load the MNE DigMontage from.

        Raises
        ------
        ValueError
            If the file does not exist or is not a -montage.fif file.
        RuntimeError
            If there's an error while reading the .fif file.
        """
        fif_path = self._get_mne_file_path(fif_file, "-montage.fif")
        try:
            self._montage0 = mne.channels.read_dig_fif(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -montage.fif file: {str(e)}")

    @property
    def trans0(self) -> Optional[mne.transforms.Transform]:
        """
        Get or set the MNE Transform object.

        Returns
        -------
        Optional[mne.transforms.Transform]
            The MNE Transform object if loaded, otherwise None.
        """
        return self._trans0

    @trans0.setter
    def trans0(self, fif_file: Union[str, Path]):
        """
        Load MNE Transform from a -trans.fif file and set it as the current trans.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the -trans.fif file to load the MNE Transform from.

        Raises
        ------
        ValueError
            If the file does not exist or is not a .fif file.
        RuntimeError
            If there's an error while reading the .fif file.
        """
        fif_path = self._get_mne_file_path(fif_file, "-trans.fif")
        try:
            self._trans0 = mne.read_trans(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -trans.fif file: {str(e)}")

    @property
    def src0(self) -> Optional[mne.SourceSpaces]:
        """
        Get or set the MNE SourceSpaces object.

        Returns
        -------
        Optional[mne.SourceSpaces]
            The MNE SourceSpaces object if loaded, otherwise None.
        """
        return self._src0

    @src0.setter
    def src0(self, fif_file: Union[str, Path]):
        """
        Load MNE SourceSpaces from a -src.fif file and set it as the current src.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the -src.fif file to load the MNE SourceSpaces from.

        Raises
        ------
        ValueError
            If the file does not exist or is not a .fif file.
        RuntimeError
            If there's an error while reading the .fif file.
        """
        fif_path = self._get_mne_file_path(fif_file, "-src.fif")
        try:
            self._src0 = mne.read_source_spaces(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -src.fif file: {str(e)}")

    @property
    def bem_model0(self) -> Optional[List[mne.bem.ConductorModel]]:
        """
        Get or set the MNE BEM model.

        Returns
        -------
        Optional[List[mne.bem.ConductorModel]]
            The MNE BEM model if loaded, otherwise None.
        """
        return self._bem_model0

    @bem_model0.setter
    def bem_model0(self, fif_file: Union[str, Path]):
        """
        Load MNE BEM model from a -bem-model.fif file and set it as the current bem_model.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the -bem-model.fif file to load the MNE BEM model from.

        Raises
        ------
        ValueError
            If the file does not exist or is not a .fif file.
        RuntimeError
            If there's an error while reading the .fif file.
        """
        fif_path = self._get_mne_file_path(fif_file, "-bem-model.fif")
        try:
            self._bem_model0 = mne.read_bem_surfaces(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -bem-model.fif file: {str(e)}")

    @property
    def bem_solution0(self) -> Optional[mne.bem.ConductorModel]:
        """
        Get or set the MNE BEM solution.

        Returns
        -------
        Optional[mne.bem.ConductorModel]
            The MNE BEM solution if loaded, otherwise None.
        """
        return self._bem_solution0

    @bem_solution0.setter
    def bem_solution0(self, fif_file: Union[str, Path]):
        """
        Load MNE BEM solution from a -bem-solution.fif file and set it as the current bem_solution.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the -bem-solution.fif file to load the MNE BEM solution from.

        Raises
        ------
        ValueError
            If the file does not exist or is not a .fif file.
        RuntimeError
            If there's an error while reading the .fif file.
        """
        fif_path = self._get_mne_file_path(fif_file, "-bem-solution.fif")
        try:
            self._bem_solution0 = mne.read_bem_solution(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -bem-solution.fif file: {str(e)}")

    @property
    def fwd0(self) -> Optional[mne.Forward]:
        """
        Get or set the MNE Forward solution.

        Returns
        -------
        Optional[mne.Forward]
            The MNE Forward solution if loaded, otherwise None.
        """
        return self._fwd0

    @fwd0.setter
    def fwd0(self, fif_file: Union[str, Path]):
        """
        Load MNE Forward solution from a -fwd.fif file and set it as the current fwd.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the -fwd.fif file to load the MNE Forward solution from.

        Raises
        ------
        ValueError
            If the file does not exist or is not a .fif file.
        RuntimeError
            If there's an error while reading the .fif file.
        """
        fif_path = self._get_mne_file_path(fif_file, "-fwd.fif")
        try:
            self._fwd0 = mne.read_forward_solution(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -fwd.fif file: {str(e)}")

    @property
    def genuine_noise_cov0(self) -> Optional[mne.Covariance]:
        """
        Get or set the real noise covariance matrix.

        Returns
        -------
        Optional[mne.Covariance]
            The MNE Covariance object representing the real noise covariance matrix if loaded, otherwise None.

        See Also
        --------
        genuine_noise_cov0.setter : Method to load the real noise covariance matrix from a file.
        """
        return self._genuine_noise_cov0

    @genuine_noise_cov0.setter
    def genuine_noise_cov0(self, fif_file: Union[str, Path]):
        """
        Load the real noise covariance matrix.

        Parameters
        ----------
        fif_file : Union[str, Path]
            Path to the .fif file to load the real noise covariance matrix from.

        Raises
        ------
        ValueError
            If the file does not exist or does not match the expected naming pattern.
        RuntimeError
            If there's an error while reading the .fif file.

        Notes
        -----
        This method uses the `_get_mne_file_path` helper method to resolve the file path and ensure it exists and has the correct suffix.
        """
        fif_path = self._get_mne_file_path(fif_file, "-noise-cov.fif")
        try:
            self._genuine_noise_cov0 = mne.read_cov(fif_path)
            log0.info(f"Real noise covariance matrix loaded from {fif_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading real noise covariance file: {str(e)}")

    @property
    def annot0(self) -> Optional[str]:
        """
        Get or set the annotation string.

        Returns
        -------
        Optional[str]
            The current annotation string.
        """
        return self._annot0

    @annot0.setter
    def annot0(self, value: str):
        """
        Set the annotation string.

        Parameters
        ----------
        value : str
            The annotation string to set.
        """
        self._annot0 = value

    @property
    def labels0(self) -> Optional[List[mne.Label]]:
        """
        Get the annotation labels.

        Returns
        -------
        Optional[List[mne.Label]]
            The current annotation labels, or None if not set.
        """
        return self._labels0

    @property
    def label0_names(self) -> Optional[List[str]]:
        """
        Get the annotation label names.

        Returns
        -------
        Optional[List[str]]
            The current annotation label names, or None if not set.
        """
        return self._label0_names

    @property
    def labels2(self) -> Optional[List[mne.Label]]:
        """
        Get the processed annotation labels.

        Returns
        -------
        Optional[List[mne.Label]]
            The processed annotation labels, or None if not set.
        """
        return self._labels2

    @property
    def label2_names(self) -> Optional[List[str]]:
        """
        Get the processed annotation label names.

        Returns
        -------
        Optional[List[str]]
            The processed annotation label names, or None if not set.
        """
        return self._label2_names

    @property
    def labels3(self) -> Optional[List[mne.Label]]:
        """
        Get the additional processed labels.

        Returns
        -------
        Optional[List[mne.Label]]
            The additional processed labels, or None if not set.
        """
        return self._labels3

    @property
    def label3_names(self) -> Optional[List[str]]:
        """
        Get the names of the additional processed labels.

        Returns
        -------
        Optional[List[str]]
            The names of the additional processed labels, or None if not set.
        """
        return self._label3_names

    @property
    def labels4(self) -> Optional[List[mne.Label]]:
        """
        Get the final set of labels after processing.

        Returns
        -------
        Optional[List[mne.Label]]
            The final set of labels, or None if not set.
        """
        return self._labels4

    @property
    def label4_names(self) -> Optional[List[str]]:
        """
        Get the names of the final set of labels after processing.

        Returns
        -------
        Optional[List[str]]
            The names of the final set of labels, or None if not set.
        """
        return self._label4_names

    def read_labels_from_annot(
        self, regexp: Optional[str] = None, sort: bool = False, verbose: bool = False
    ) -> None:
        """
        Read annotation labels from FreeSurfer parcellation based on the `annot0` property.

        Parameters
        ----------
        regexp : Optional[str], default None
            Regular expression to filter labels.
        sort : bool, default False
            If True, sort the labels by name.
        verbose : bool, default False
            If True, print additional information.

        Raises
        ------
        ValueError
            If `subjects_dir`, `subject`, or `annot0` is not set.
        """
        if self.subjects_dir is None or self.subject is None or not self.annot0:
            raise ValueError(
                "subjects_dir, subject, and annot0 must be set before reading labels."
            )

        try:
            self._labels0 = mne.read_labels_from_annot(
                subject=self.subject,
                parc=self.annot0,
                subjects_dir=self.subjects_dir,
                regexp=regexp,
                sort=sort,
                verbose=verbose,
            )
            self._label0_names = [label.name for label in self._labels0]
            log0.info(
                f"Successfully acquired {len(self._labels0)} labels from annotation {self.annot0}"
            )
        except Exception as e:
            log0.error(f"Error reading labels from annotation: {str(e)}")
            raise

    def process_labels0(
        self, location: str = "center", extent: float = 0.0, verbose: bool = False
    ) -> None:
        """
        Process `labels0` to create `labels2` based on specified parameters.

        Parameters
        ----------
        location : str, default "center"
            The location within each label to select. Options: "center" or "random".
        extent : float, default 0.0
            The extent of the selection in mm.
        verbose : bool, default False
            If True, print progress information.

        Raises
        ------
        ValueError
            If `labels0` is not set or if `location` is invalid.
        """
        if self._labels0 is None:
            raise ValueError("labels0 must be set before processing labels.")

        if location not in ["center", "random"]:
            raise ValueError("location must be either 'center' or 'random'.")

        self._labels2 = []
        total = len(self._labels0)
        leadz = len(str(total))

        for idx0, label0 in enumerate(self._labels0):
            label2 = mne.label.select_sources(
                subject=self.subject,
                label=label0,
                location=location,
                extent=extent,
                subjects_dir=self.subjects_dir,
            )
            # Note: The label name is updated here to match the original label name.
            label2.name = label0.name

            if verbose:
                print(
                    f"[{idx0+1:0{leadz}d}/{total:0{leadz}d}] "
                    f"Processing: {label0.name} [{len(label2)}/{len(label0)}]"
                )

            self._labels2.append(label2)

        self._label2_names = [label.name for label in self._labels2]

        log0.info(
            f"Successfully processed {len(self._labels2)} labels "
            f"with location '{location}' and extent {extent}"
        )

    def make_dummy_events(
        self,
        event_labels: Union[int, List[str]],
        event_repets: int,
        event_interv: int,
        event_begins: int,
    ) -> Tuple[np.ndarray, Dict[str, int], Dict[int, str], pd.DataFrame]:
        """
        Generate dummy events for simulation or testing purposes.

        Parameters
        ----------
        event_labels : Union[int, List[str]]
            If int, number of unique events to generate. Event labels will be created
            automatically as "Ev001", "Ev002", etc.
            If list of str, custom labels for events. Must be unique.
        event_repets : int
            Number of repetitions for each event.
        event_interv : int
            Interval between events in samples.
        event_begins : int
            Sample number at which the first event begins.

        Returns
        -------
        events : np.ndarray
            2D array with columns:
            - Event onset (in samples)
            - Signal value of the immediately preceding sample
            - Event code
        event_id : Dict[str, int]
            Mapping of event labels to their corresponding values.
        event_desc : Dict[int, str]
            Mapping of event values to their corresponding labels.
        df : pd.DataFrame
            DataFrame containing event information with columns:
            - sample_num: Event onset (in samples)
            - preceding_val: Signal value of the immediately preceding sample
            - event_code: Numeric code for the event
            - event_labels: String label for the event

        Notes
        -----
        The method generates dummy events that can be used for simulating
        experiment data or testing event-related functionalities. The events
        are randomly shuffled to simulate a realistic experimental scenario.

        The 'preceding_val' column is set to zero for all events, simulating
        a scenario where events are detected at the rising edge of a trigger signal.

        Raises
        ------
        TypeError
            If event_labels is neither an integer nor a list of strings.
        AssertionError
            If event_labels is a list of strings with non-unique elements.
        """
        if isinstance(event_labels, int):
            n_events = event_labels
            leadz = len(str(n_events + 1))
            event_labels = [f"Ev{ii+1:0{leadz}d}" for ii in range(n_events)]
        elif isinstance(event_labels, list) and all(
            isinstance(item, str) for item in event_labels
        ):
            assert len(event_labels) == len(
                set(event_labels)
            ), "'event_labels' must contain only unique strings"
            n_events = len(event_labels)
        else:
            raise TypeError("'event_labels' must be either an integer or a list of strings")

        event_values = list(range(1, n_events + 1))
        events_total = n_events * event_repets
        log0.debug(f"event_values = {event_values}")
        log0.debug(f"event_labels = {event_labels}")
        log0.debug(f"event_repets = {event_repets}")
        log0.debug(f"events_total = {events_total}")

        event_samp = np.arange(
            event_begins, event_begins + event_interv * events_total, event_interv
        )
        event_prec = np.zeros(events_total, dtype=int)
        event_code = np.repeat(event_values, event_repets)
        np.random.shuffle(event_code)

        events = np.column_stack((event_samp, event_prec, event_code))
        event_id = {key: val for key, val in zip(event_labels, event_values)}
        event_desc = {val: key for key, val in zip(event_labels, event_values)}

        df = pd.DataFrame(
            {
                "sample_num": event_samp,
                "preceding_val": event_prec,
                "event_code": event_code,
            }
        )
        df["event_labels"] = df.event_code.map(event_desc)

        return events, event_id, event_desc, df

    # Other methods remain unchanged...
