#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Ground Truth Establisher (GTE) Module.

Great stuff!

"""

import numpy as np
import pandas as pd
import mne
from mne.simulation import SourceSimulator
from mne.beamformer import Beamformer

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Optional, Union, List, Dict
from typing import get_origin, get_args

from .aux_log import Log0

logZ = Log0()
log0 = logZ.logger


@dataclass
class GTE:
    """
    Ground Truth Establisher (GTE) class for data gathering and simulations.

    This class handles data gathering and performs simulations, primarily using MNE-Python.
    It provides functionality to manage subject directories, individual subject data,
    and MNE objects for simulations.

    Attributes
    ----------
    _subjects_dir : Path or None
        Path to the subjects directory.
    _subject : str or None
        Identifier for the current subject.
    _info0 : mne.Info or None
        MNE Info object loaded from a .fif file.
    _montage0 : mne.channels.DigMontage or None
        MNE DigMontage object loaded from a -montage.fif file.
    _trans0 : mne.transforms.Transform or None
        MNE Transform object loaded from a -trans.fif file.
    _src0 : mne.SourceSpaces or None
        MNE SourceSpaces object loaded from a -src.fif file.
    _bem_model0 : list of mne.bem.ConductorModel or None
        MNE BEM model loaded from a -bem-model.fif file.
    _bem_solution0 : mne.bem.ConductorModel or None
        MNE BEM solution loaded from a -bem-solution.fif file.
    _fwd0 : mne.Forward or None
        MNE Forward solution loaded from a -fwd.fif file.
    _annot0 : str or None
        FreeSurfer's annot (surface labels).
    _labels0 : list of mne.Label or None
        FreeSurfer parcellation labels.
    _label0_names : list of str or None
        FreeSurfer parcellation label names.
    _singularity_events : np.ndarray or None
        Singularity events data.
    _singularity_event_IDs : Dict[str, int] or None
        Mapping of singularity event labels to their numeric codes.
    _singularity_events_desc : Dict[int, str] or None
        Mapping of numeric event codes to their corresponding labels for singularity events.
    _singularity_events_df : pd.DataFrame or None
        DataFrame containing detailed information about singularity events.
    _experimental_events : np.ndarray or None
        Experimental events data.
    _experimental_event_IDs : Dict[str, int] or None
        Mapping of experimental event labels to their numeric codes.
    _experimental_events_desc : Dict[int, str] or None
        Mapping of numeric event codes to their corresponding labels for experimental events.
    _experimental_events_df : pd.DataFrame or None
        DataFrame containing detailed information about experimental events.
    """

    _subjects_dir: Optional[Path] = field(default=None, init=False)
    _subject: Optional[str] = field(default=None, init=False)
    _info0: Optional[mne.Info] = field(default=None, init=False)
    _montage0: Optional[mne.channels.DigMontage] = field(default=None, init=False)
    _trans0: Optional[mne.transforms.Transform] = field(default=None, init=False)
    _src0: Optional[mne.SourceSpaces] = field(default=None, init=False)
    _bem_model0: Optional[list] = field(default=None, init=False)
    _bem_solution0: Optional[mne.bem.ConductorModel] = field(default=None, init=False)
    _fwd0: Optional[mne.Forward] = field(default=None, init=False)
    _genuine_noise_cov0: Optional[mne.Covariance] = None

    _annot0: Optional[str] = field(default=None, init=False)
    _labels0: Optional[List[mne.Label]] = field(default=None, init=False)
    _label0_names: Optional[str] = field(default=None, init=False)
    _labels2: Optional[List[mne.Label]] = field(default=None, init=False)
    _label2_names: Optional[str] = field(default=None, init=False)
    _labels3: Optional[List[mne.Label]] = field(default=None, init=False)
    _label3_names: Optional[str] = field(default=None, init=False)
    _labels4: Optional[List[mne.Label]] = field(default=None, init=False)
    _label4_names: Optional[str] = field(default=None, init=False)

    _singularity_events: Optional[np.ndarray] = field(default=None, init=False)
    _singularity_event_IDs: Optional[Dict[str, int]] = field(default=None, init=False)
    _singularity_events_desc: Optional[Dict[int, str]] = field(default=None, init=False)
    _singularity_events_df: Optional[pd.DataFrame] = field(default=None, init=False)

    _experimental_events: Optional[np.ndarray] = field(default=None, init=False)
    _experimental_event_IDs: Optional[Dict[str, int]] = field(default=None, init=False)
    _experimental_events_desc: Optional[Dict[int, str]] = field(
        default=None, init=False
    )
    _experimental_events_df: Optional[pd.DataFrame] = field(default=None, init=False)
    _activ0: Optional[Dict[str, Dict[str, Dict[str, float]]]] = field(
        default=None, init=False
    )
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
        return path.exists() and (
            path.is_dir() or (path.is_symlink() and path.resolve().is_dir())
        )

    @property
    def subjects_dir(self) -> Optional[Path]:
        """
        Get the subjects directory path.

        Returns
        -------
        Path or None
            The path to the subjects directory if set, otherwise None.
        """
        return self._subjects_dir

    @subjects_dir.setter
    def subjects_dir(self, value: Optional[Path]):
        """
        Set the subjects directory path.

        Parameters
        ----------
        value : Path or None
            The path to set as the subjects directory. If None, the subjects_dir
            will be set to None.

        Raises
        ------
        ValueError
            If the provided path does not exist, is not a directory, or is not
            a symlink to a directory.
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
        Get the current subject identifier.

        Returns
        -------
        str or None
            The identifier of the current subject if set, otherwise None.
        """
        return self._subject

    @subject.setter
    def subject(self, value: Optional[str]):
        """
        Set the current subject identifier.

        Parameters
        ----------
        value : str or None
            The identifier to set as the current subject. If None, the current
            subject will be unset.

        Raises
        ------
        ValueError
            If subjects_dir is not set when trying to set a subject, or if the
            subject directory does not exist, is not a directory, or is not a
            symlink to a directory under subjects_dir.
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
        Path or None
            The path to the current subject's directory if both subjects_dir
            and subject are set, otherwise None.
        """
        if self._subjects_dir is not None and self._subject is not None:
            return (self._subjects_dir / self._subject).resolve()
        return None

    # ... (rest of the code remains the same)

    def story(self) -> pd.DataFrame:
        """
        List all properties of the GTE dataclass object with their declared and actual types.

        Returns
        -------
        pd.DataFrame
            A DataFrame with columns:
            - 'Name': The name of the property (str)
            - 'Declared Type': The type declared in the class definition (str)
            - 'Actual Type': The type of the current value of the property (str)
            - 'Is Optional': Whether the property is declared as Optional (bool)

        Notes
        -----
        This method uses the dataclasses.fields() function to introspect
        the class structure. It includes both regular fields and properties.
        The 'Actual Type' column shows 'None' for properties with no current value.

        Examples
        --------
        >>> gte = GTE()
        >>> gte.subjects_dir = Path("/path/to/subjects")
        >>> properties_df = gte.story()
        >>> print(properties_df)
        """
        properties = []
        for f in fields(self):
            value = getattr(self, f.name)
            declared_type = f.type
            actual_type = type(value).__name__ if value is not None else "None"
            is_optional = False

            # Check if the declared type is Optional
            if get_origin(declared_type) is Union:
                args = get_args(declared_type)
                if type(None) in args:
                    is_optional = True
                    # Remove NoneType from args to get the actual type
                    other_args = [arg for arg in args if arg is not type(None)]
                    declared_type = (
                        other_args[0]
                        if len(other_args) == 1
                        else Union[tuple(other_args)]
                    )

            properties.append(
                {
                    "Name": f.name,
                    "Declared Type": str(declared_type),
                    "Actual Type": actual_type,
                    "Is Optional": is_optional,
                }
            )

        return pd.DataFrame(properties)

    def publish(self):
        """
        Publish. Important method for future implementation.

        Raises
        ------
        NotImplementedError
            This method is not implemented yet.
        """
        raise NotImplementedError(
            "The 'publish' method is not implemented yet. Stay tuned for future updates!"
        )

    def _get_mne_file_path(self, fif_file: Union[str, Path], suffix: str) -> Path:
        """
        Provide helper method to get the full path for MNE files.

        Parameters
        ----------
        fif_file : str or Path
            The filename or path provided by the user.
        suffix : str
            The expected suffix for the file.

        Returns
        -------
        Path
            The full path to the MNE file.

        Raises
        ------
        ValueError
            If the subjects_dir or subject is not set, or if the file does not exist.
        """
        if self.subjects_dir is None or self.subject is None:
            raise ValueError(
                "Both subjects_dir and subject must be set before loading MNE files."
            )

        if isinstance(fif_file, str):
            fif_path = Path(fif_file)
        else:
            fif_path = fif_file

        if not fif_path.is_absolute():
            fif_path = self.subjects_dir / self.subject / "aux" / "mne" / fif_path

        if not fif_path.exists():
            raise ValueError(f"The file '{fif_path}' does not exist.")
        if not fif_path.name.endswith(suffix):
            log0.warning(
                f"The file '{fif_path}' does not end with '{suffix}' in its name. "
                "Please make sure you know what you are doing."
            )

        return fif_path
