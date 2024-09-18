#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random
import numpy as np
import pandas as pd
import mne
from mne.simulation import SourceSimulator
from mne.beamformer import Beamformer

from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Optional, Union, List, Dict, Tuple, Callable
from typing import get_origin, get_args

from .aux_log import Log0

logZ = Log0()
log0 = logZ.logger


@dataclass
class GTE:
    _subjects_dir: Optional[Path] = field(default=None, init=False)
    _subject: Optional[str] = field(default=None, init=False)
    _info0: Optional[mne.Info] = field(default=None, init=False)
    _montage0: Optional[mne.channels.DigMontage] = field(default=None, init=False)
    _trans0: Optional[mne.transforms.Transform] = field(default=None, init=False)
    _src0: Optional[mne.SourceSpaces] = field(default=None, init=False)
    _bem_model0: Optional[List[Dict]] = field(default=None, init=False)

    _bem_solution0: Optional[mne.bem.ConductorModel] = field(default=None, init=False)
    _fwd0: Optional[mne.Forward] = field(default=None, init=False)
    _genuine_noise_cov0: Optional[mne.Covariance] = field(default=None, init=False)

    _annot0: Optional[str] = field(default=None, init=False)
    _labels0: Optional[List[mne.Label]] = field(default=None, init=False)
    _labels2: Optional[List[mne.Label]] = field(default=None, init=False)
    _labels3: Optional[List[mne.Label]] = field(default=None, init=False)
    _labels4: Optional[List[mne.Label]] = field(default=None, init=False)
    _label0_names: Optional[List[str]] = field(default=None, init=False)
    _label2_names: Optional[List[str]] = field(default=None, init=False)
    _label3_names: Optional[List[str]] = field(default=None, init=False)
    _label4_names: Optional[List[str]] = field(default=None, init=False)

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
    _bf_filters: Optional[Dict[str, Beamformer]] = field(default=None, init=False)
    _stcs: Optional[Dict[str, mne.SourceEstimate]] = field(default=None, init=False)

    def __post_init__(self):
        pass

    @staticmethod
    def _is_valid_dir(path: Path) -> bool:
        return path.exists() and (
            path.is_dir() or (path.is_symlink() and path.resolve().is_dir())
        )

    @property
    def subjects_dir(self) -> Optional[Path]:
        return self._subjects_dir

    @subjects_dir.setter
    def subjects_dir(self, value: Optional[Path]):
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
        return self._subject

    @subject.setter
    def subject(self, value: Optional[str]):
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
        if self._subjects_dir is not None and self._subject is not None:
            return (self._subjects_dir / self._subject).resolve()
        return None

    @property
    def info0(self) -> Optional[mne.Info]:
        return self._info0

    @info0.setter
    def info0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-info.fif")
        try:
            self._info0 = mne.io.read_info(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading .fif file: {str(e)}")

    @property
    def montage0(self) -> Optional[mne.channels.DigMontage]:
        return self._montage0

    @montage0.setter
    def montage0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-montage.fif")
        try:
            self._montage0 = mne.channels.read_dig_fif(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -montage.fif file: {str(e)}")

    @property
    def trans0(self) -> Optional[mne.transforms.Transform]:
        return self._trans0

    @trans0.setter
    def trans0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-trans.fif")
        try:
            self._trans0 = mne.read_trans(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -trans.fif file: {str(e)}")

    @property
    def src0(self) -> Optional[mne.SourceSpaces]:
        return self._src0

    @src0.setter
    def src0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-src.fif")
        try:
            self._src0 = mne.read_source_spaces(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -src.fif file: {str(e)}")

    @property
    def bem_model0(self) -> Optional[List[Dict]]:
        return self._bem_model0

    @bem_model0.setter
    def bem_model0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-bem-model.fif")
        try:
            self._bem_model0 = mne.read_bem_surfaces(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -bem-model.fif file: {str(e)}")

    @property
    def bem_solution0(self) -> Optional[mne.bem.ConductorModel]:
        return self._bem_solution0

    @bem_solution0.setter
    def bem_solution0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-bem-solution.fif")
        try:
            self._bem_solution0 = mne.read_bem_solution(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -bem-solution.fif file: {str(e)}")

    @property
    def fwd0(self) -> Optional[mne.Forward]:
        return self._fwd0

    @fwd0.setter
    def fwd0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-fwd.fif")
        try:
            self._fwd0 = mne.read_forward_solution(fif_path)
        except Exception as e:
            raise RuntimeError(f"Error reading -fwd.fif file: {str(e)}")

    @property
    def genuine_noise_cov0(self) -> Optional[mne.Covariance]:
        return self._genuine_noise_cov0

    @genuine_noise_cov0.setter
    def genuine_noise_cov0(self, fif_file: Union[str, Path]):
        fif_path = self._get_mne_file_path(fif_file, "-noise-cov.fif")
        try:
            self._genuine_noise_cov0 = mne.read_cov(fif_path)
            log0.info(f"Real noise covariance matrix loaded from {fif_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading real noise covariance file: {str(e)}")

    @property
    def annot0(self) -> Optional[str]:
        return self._annot0

    @annot0.setter
    def annot0(self, value: str):
        self._annot0 = value

    @property
    def labels0(self) -> Optional[List[mne.Label]]:
        return self._labels0

    @property
    def label0_names(self) -> Optional[List[str]]:
        return self._label0_names

    @property
    def labels2(self) -> Optional[List[mne.Label]]:
        return self._labels2

    @property
    def label2_names(self) -> Optional[List[str]]:
        return self._label2_names

    @property
    def labels3(self) -> Optional[List[mne.Label]]:
        return self._labels3

    @property
    def label3_names(self) -> Optional[List[str]]:
        return self._label3_names

    @property
    def labels4(self) -> Optional[List[mne.Label]]:
        return self._labels4

    @property
    def label4_names(self) -> Optional[List[str]]:
        return self._label4_names

    def read_labels_from_annot(
        self, regexp: Optional[str] = None, sort: bool = False, verbose: bool = False
    ) -> None:
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
        if self._labels0 is None:
            raise ValueError("labels0 must be set before processing labels.")

        if location not in ["center", "random"]:
            raise ValueError("location must be either 'center' or 'random'.")

        self._labels2 = []
        total = len(self._labels0)
        leadz = len(str(total))

        for idx0, label0 in enumerate(self._labels0):
            # Using mne.label.select_sources to get labels
            # containing limited/restricted number of vertices
            label2 = mne.label.select_sources(
                subject=self.subject,
                label=label0,
                location=location,
                extent=extent,
                subjects_dir=self.subjects_dir,
            )
            # CONSIDER: in labels4 we use name property so changing it here is
            # not recommended, in future we may consider implementation based on
            # "".endswith() "".startswith() or "".contains(), but it may also be
            # more error prone
            # label2.name = f"source-label-{location}-{label0.name}"
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
        if isinstance(event_labels, int):
            n_events = event_labels
            leadz = len(str(n_events + 1)) + 1
            event_labels = [f"Ev{ii:0{leadz}d}" for ii in range(1, n_events + 1)]
        elif isinstance(event_labels, list) and all(
            isinstance(item, str) for item in event_labels
        ):
            if len(event_labels) != len(set(event_labels)):
                raise ValueError("'event_labels' must contain only unique strings")
            n_events = len(event_labels)
        else:
            raise TypeError(
                "'event_labels' must be either an integer or a list of strings"
            )

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

    def make_singularity_events(
        self,
        event_labels: Union[int, List[str]] = ["singularity"],
        event_repets: int = 1,
        event_interv: int = 1000,
        event_begins: int = 5000,
    ):
        (
            self._singularity_events,
            self._singularity_event_IDs,
            self._singularity_events_desc,
            self._singularity_events_df,
        ) = self.make_dummy_events(
            event_labels=event_labels,
            event_repets=event_repets,
            event_interv=event_interv,
            event_begins=event_begins,
        )
        log0.info("Singularity events generated and stored.")

    def make_experimental_events(
        self,
        event_labels: Union[int, List[str]] = ["Ev01", "Ev02"],
        event_repets: int = 100,
        event_interv: int = 2000,
        event_begins: int = 5000,
    ):
        (
            self._experimental_events,
            self._experimental_event_IDs,
            self._experimental_events_desc,
            self._experimental_events_df,
        ) = self.make_dummy_events(
            event_labels=event_labels,
            event_repets=event_repets,
            event_interv=event_interv,
            event_begins=event_begins,
        )
        log0.info("Experimental events generated and stored.")

    @property
    def singularity_events(self) -> Optional[np.ndarray]:
        return self._singularity_events

    @property
    def singularity_event_IDs(self) -> Optional[Dict[str, int]]:
        return self._singularity_event_IDs

    @property
    def singularity_events_desc(self) -> Optional[Dict[int, str]]:
        return self._singularity_events_desc

    @property
    def singularity_events_df(self) -> Optional[pd.DataFrame]:
        return self._singularity_events_df

    @property
    def experimental_events(self) -> Optional[np.ndarray]:
        return self._experimental_events

    @property
    def experimental_event_IDs(self) -> Optional[Dict[str, int]]:
        return self._experimental_event_IDs

    @property
    def experimental_events_desc(self) -> Optional[Dict[int, str]]:
        return self._experimental_events_desc

    @property
    def experimental_events_df(self) -> Optional[pd.DataFrame]:
        return self._experimental_events_df

    def generate_waveform(
        self,
        times: np.ndarray,
        latency: float = 0.25,
        duration: float = 0.20,
        amplitude: float = 1,
        scale: float = 1e-9,
        rng: Optional[np.random.Generator] = None,
    ) -> np.ndarray:
        # Define the oscillation frequency (e.g., beta band)
        f = 15  # Hz
        # Generate the sinusoidal component (oscillatory activity)
        sinusoid = np.sin(2 * np.pi * f * (times - latency))
        # Standard deviation for the Gaussian envelope
        sigma = 0.100 * duration
        # Generate the Gaussian envelope
        # - Adding a small random jitter to the peak time
        if rng is not None:
            jitter = (sigma / 4.0) * rng.random()
        else:
            jitter = (sigma / 4.0) * np.random.rand()

        # Example boundary check (CONSIDER implementing clip)
        # jitter = min(max(jitter, -times.max()), times.max())
        # jitter = np.clip(jitter, -sigma, sigma)

        gf = np.exp(-((times - latency - jitter) ** 2) / (2 * (sigma**2)))

        # Combine sinusoid and Gaussian, and scale to nanoamperes
        wf0 = sinusoid * gf * scale * amplitude
        return wf0

    @property
    def activ0(self) -> Optional[Dict[str, Dict[str, Dict[str, float]]]]:
        return self._activ0

    @property
    def activ0_labels(self) -> Optional[List[str]]:
        return self._activ0_labels

    @property
    def activ0_events(self) -> Optional[List[str]]:
        return self._activ0_events

    def set_predefined_activations(
        self,
        activations: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None,
        event_repets: int = 100,
        event_interv: int = 2000,
        event_begins: int = 5000,
    ) -> None:
        if activations is None:
            activations = {
                "Ev01": {
                    "frontalpole_1-lh": dict(lat=0.35, dur=0.20, amp=300),
                    "superiorfrontal_1-lh": dict(lat=0.25, dur=0.40, amp=320),
                    "rostralmiddlefrontal_7-lh": dict(lat=0.45, dur=0.20, amp=320),
                    "superiorparietal_3-rh": dict(lat=0.25, dur=0.60, amp=320),
                },
                "Ev02": {
                    "superiorfrontal_1-lh": dict(lat=0.35, dur=0.20, amp=320),
                    "superiorparietal_1-rh": dict(lat=0.45, dur=0.20, amp=440),
                    "superiortemporal_1-lh": dict(lat=0.25, dur=0.40, amp=320),
                    "precentral_13-lh": dict(lat=0.35, dur=0.20, amp=320),
                    "lateraloccipital_2-rh": dict(lat=0.45, dur=0.30, amp=440),
                    "lateraloccipital_4-lh": dict(lat=0.25, dur=0.20, amp=320),
                },
            }

        self._activ0 = activations
        self._activ0_labels = sorted(
            set(key for inner_dict in activations.values() for key in inner_dict)
        )
        self._activ0_events = list(activations.keys())

        self.make_experimental_events(
            event_labels=self._activ0_events,
            event_repets=event_repets,
            event_interv=event_interv,
            event_begins=event_begins,
        )

        self._labels4 = [
            label for label in self._labels2 if label.name in self._activ0_labels
        ]
        self._label4_names = self._activ0_labels

    def set_randomized_activations(
        self,
        num_labels: int,
        num_labels_per_event: int,
        event_labels: Union[int, List[str]],
        event_repets: int = 100,
        event_interv: int = 2000,
        event_begins: int = 5000,
        allow_label_repetition: bool = True,
    ):
        # FIXME IMPORTANT

        # Validate inputs
        if isinstance(event_labels, int):
            num_events = event_labels
            leadz = len(str(num_events + 1)) + 1
            event_names = [f"Ev{ii:0{leadz}d}" for ii in range(1, num_events + 1)]
        elif isinstance(event_labels, list) and all(
            isinstance(label, str) for label in event_labels
        ):
            event_names = event_labels
            num_events = len(event_names)
        else:
            raise ValueError(
                "event_labels must be either an integer or a list of strings"
            )

        if len(self._label0_names) < num_labels:
            raise ValueError(
                f"Not enough labels. Required: {num_labels}, Available: {len(self._label0_names)}"
            )

        if not allow_label_repetition:
            if num_labels_per_event * num_events > num_labels:
                raise ValueError(
                    f"Too many labels per event. Max possible: {num_labels // num_events} "
                    "when allow_label_repetition is False"
                )
            # Additional logic to prevent label reuse across events
            sampled_labels = random.sample(
                self._label0_names, num_labels_per_event * num_events
            )
            label_iterator = iter(sampled_labels)
        else:
            sampled_labels = random.sample(self._label0_names, num_labels)

        # Generate experimental events
        self.make_experimental_events(
            event_labels=event_names,
            event_repets=event_repets,
            event_interv=event_interv,
            event_begins=event_begins,
        )

        # Sample labels

        # Initialize the activations dictionary
        activations = {event: {} for event in event_names}

        # Assign labels to events
        for event in event_names:
            if allow_label_repetition:
                event_labels = random.choices(sampled_labels, k=num_labels_per_event)
            else:
                # event_labels = random.sample(sampled_labels, num_labels_per_event) # FIXED
                event_labels = [
                    next(label_iterator) for _ in range(num_labels_per_event)
                ]
            for label in event_labels:
                activations[event][label] = {
                    "lat": round(random.uniform(0.1, 0.4), 2),
                    "dur": round(random.uniform(0.1, 0.4), 2),
                    "amp": round(random.uniform(200, 500), 2),
                }

        # Update class properties
        self._activ0 = activations
        self._activ0_labels = sorted(
            set(label for event in activations.values() for label in event)
        )
        self._activ0_events = event_names
        self._labels4 = [
            label for label in self._labels2 if label.name in self._activ0_labels
        ]
        self._label4_names = self._activ0_labels

        log0.info(
            f"Randomized activations set for {num_events} events with {num_labels} total labels."
        )

    def activations_to_dataframe(self) -> pd.DataFrame:
        if self._activ0 is None:
            raise ValueError(
                "Activations have not been set. Use set_predefined_activations() or "
                "set_randomized_activations() first."
            )

        data = []
        for event, regions in self._activ0.items():
            for region, params in regions.items():
                data.append(
                    {
                        "Event": event,
                        "Region": region,
                        "Latency": params["lat"],
                        "Duration": params["dur"],
                        "Amplitude": params["amp"],
                    }
                )

        return pd.DataFrame(data)

    @property
    def activ0_trial_num_samp(self) -> int:
        if self._activ0_trial_num_samp is None:
            self._activ0_trial_num_samp = 1000  # Default value
        return self._activ0_trial_num_samp

    @activ0_trial_num_samp.setter
    def activ0_trial_num_samp(self, value: int):
        self._activ0_trial_num_samp = value

    @property
    def times0(self) -> np.ndarray:
        if self._info0 is None:
            raise ValueError("The _info0 property must be set before accessing times0.")

        return (
            np.arange(self._activ0_trial_num_samp, dtype=np.float64)
            / self._info0["sfreq"]
        )

    @times0.setter
    def times0(self, value: np.ndarray):
        # self._times0 = value
        raise NotImplementedError("The 'times0' SETTER method is not implemented yet.")

    @property
    def source_simulator(self) -> Optional[SourceSimulator]:
        return self._source_simulator

    def initialize_source_simulator(self):
        if self._src0 is None:
            raise ValueError(
                "Source space (_src0) must be set before initializing SourceSimulator."
            )
        if self._info0 is None:
            raise ValueError(
                "Measurement info (_info0) must be set before initializing SourceSimulator."
            )

        src = self._src0
        tstep = 1 / self._info0["sfreq"]

        try:
            self._source_simulator = SourceSimulator(src, tstep=tstep)
            log0.info(f"SourceSimulator initialized with tstep={tstep:.6f}s")
        except Exception as e:
            log0.error(f"Failed to initialize SourceSimulator: {str(e)}")
            raise

    def add_data_to_source_simulator(self):
        if self._source_simulator is None:
            raise ValueError(
                "Source simulator is not initialized. Call initialize_source_simulator first."
            )

        if self._activ0 is None:
            raise ValueError(
                "Activation data (_activ0) is not set. Set activations before calling this method."
            )

        if self._experimental_event_IDs is None or self._experimental_events is None:
            raise ValueError(
                "Experimental events (_experimental_event_IDs or _experimental_events) are not set."
            )

        for act_idx, (act_key, act_val) in enumerate(self._activ0.items()):
            # Get the event code corresponding to the activation key
            act_code = self._experimental_event_IDs.get(act_key)
            if act_code is None:
                raise ValueError(
                    f"Activation key '{act_key}' not found in experimental_event_IDs."
                )
            # Filter events for the current activation key
            tmp_events = self._experimental_events[
                np.where(self._experimental_events[:, 2] == act_code)[0], :
            ]
            log0.warning(f"{act_idx}: {act_key} [{act_code}] {tmp_events.shape}")

            # Loop through each label and add data to the source simulator
            for lab_idx, (lab_name, lab_params) in enumerate(act_val.items()):
                log0.warning(f"- {lab_idx}: {lab_name} --- {lab_params}")

                # Find the corresponding label in the labels4 (self._labels4)
                tmp_label = [label for label in self._labels4 if label.name == lab_name]
                if len(tmp_label) != 1:
                    raise ValueError(f"PROBLEM with label {lab_name!r} selection!")
                tmp_label = tmp_label[0]
                log0.warning(f"  - {tmp_label = }")

                # Extract activation parameters
                tmp_lat = lab_params["lat"]
                tmp_dur = lab_params["dur"]
                tmp_amp = lab_params["amp"]
                log0.warning(f"  - {tmp_lat = }, {tmp_dur = }, {tmp_amp = }")

                # Generate the waveform for this label's activation
                tmp_wf = self.generate_waveform(
                    times=self.times0,
                    latency=tmp_lat,
                    duration=tmp_dur,
                    amplitude=tmp_amp,
                )

                # Add data to the source simulator
                self._source_simulator.add_data(tmp_label, tmp_wf, tmp_events)
                log0.warning(
                    f"  - data added source waveform to source simulator for {lab_name}"
                )

    @property
    def activ0_stc(self) -> Optional[mne.SourceEstimate]:
        if self._activ0_stc is None:
            raise ValueError(
                "activ0_stc has not been extracted yet. Use extract_activ0_stc to set it."
            )
        return self._activ0_stc

    def extract_activ0_stc(self):
        if self._source_simulator is None:
            raise ValueError(
                "Source simulator is not initialized. Call initialize_source_simulator first."
            )

        self._activ0_stc = self._source_simulator.get_stc()

    @property
    def activ0_raw(self) -> Optional[mne.io.Raw]:
        if self._activ0_raw is None:
            raise ValueError(
                "activ0_raw has not been extracted yet. Use extract_activ0_raw to set it."
            )
        return self._activ0_raw

    @property
    def activ2_raw(self) -> Optional[mne.io.Raw]:
        if self._activ2_raw is None:
            raise ValueError(
                "activ2_raw has not been extracted yet. Use extract_activ2_raw to set it."
            )
        return self._activ2_raw

    def extract_activ0_raw(self):
        if self._source_simulator is None:
            raise ValueError(
                "Source simulator is not initialized. Call initialize_source_simulator first."
            )
        if self._info0 is None:
            raise ValueError(
                "Measurement info (_info0) must be set before simulating raw data."
            )
        if self._fwd0 is None:
            raise ValueError(
                "Forward solution (_fwd0) must be set before simulating raw data."
            )

        self._activ0_raw = mne.simulation.simulate_raw(
            info=self._info0,
            stc=self._source_simulator,  # an instance of mne.SourceEstimate or mne.simulation.SourceSimulator
            src=None,  # Can be None if forward is provided.
            bem=None,  # Can be None if forward is provided.
            forward=self._fwd0,
            verbose=True,
            n_jobs=12,
        )
        events_annot4x0 = mne.annotations_from_events(
            events=self._experimental_events,
            sfreq=self._activ0_raw.info["sfreq"],
            event_desc=self.experimental_events_desc,
        )
        self._activ0_raw.set_annotations(events_annot4x0)
        self._activ0_raw.set_eeg_reference(projection=True)

    def extract_activ2_raw(self):
        if self._activ0_raw is None:
            raise ValueError(
                "Clean _activ0_raw data is not initialized. Call extract_activ0_raw first."
            )

        self._activ2_raw = self._activ0_raw.copy()
        mne.simulation.add_noise(
            self._activ2_raw, cov=self._genuine_noise_cov0, random_state=0
        )
        mne.simulation.add_eog(self._activ2_raw, random_state=0)
        if len(mne.pick_types(self._activ2_raw.info, meg=True)) > 0:
            mne.simulation.add_ecg(self._activ2_raw, random_state=0)

    @property
    def activ2_epochs(self) -> Optional[mne.Epochs]:
        if self._activ2_epochs is None:
            raise ValueError(
                "activ2_epochs has not been extracted yet. Use extract_activ2_epochs_and_evoked to set it."
            )
        return self._activ2_epochs

    @property
    def activ2_evoked(self) -> Optional[Dict[str, mne.Evoked]]:
        if self._activ2_evoked is None:
            raise ValueError(
                "activ2_evoked has not been extracted yet. Use extract_activ2_epochs_and_evoked to set it."
            )
        return self._activ2_evoked

    def extract_activ2_epochs_and_evoked(
        self,
        tmin: float = -0.4,  # Added as parameter
        tmax: float = 1.2,  # Added as parameter
        baseline: Tuple[Optional[float], Optional[float]] = (
            None,
            0,
        ),
    ):
        if self._activ2_raw is None:
            raise ValueError(
                "Clean _activ2_raw data is not initialized. Call extract_activ2_raw first."
            )

        self._activ2_epochs = mne.Epochs(
            self._activ2_raw,
            self._experimental_events,
            self._experimental_event_IDs,
            tmin=tmin,  # Use parameter
            tmax=tmax,  # Use parameter
            baseline=baseline,  # Use parameter
        )

        self._activ2_evoked = {}
        for ev in self._experimental_event_IDs.keys():
            self._activ2_evoked[ev] = self._activ2_epochs[ev].average()

    @property
    def activ2_data_cov(self) -> Optional[mne.Covariance]:
        return self._activ2_data_cov

    @property
    def activ2_noise_cov(self) -> Optional[mne.Covariance]:
        return self._activ2_noise_cov

    @property
    def activ2_common_cov(self) -> Optional[mne.Covariance]:
        return self._activ2_common_cov

    def compute_covariances(
        self,
        data_tmin: float = 0.01,
        data_tmax: float = 0.60,
        noise_tmin: Optional[float] = None,
        noise_tmax: float = 0,  # This value is reasonably set to the onset of trial/stimuli
        method: str = "empirical",
    ):
        if self._activ2_epochs is None:
            raise ValueError("_activ2_epochs must be set before computing covariances.")

        self._activ2_data_cov = mne.compute_covariance(
            self._activ2_epochs, tmin=data_tmin, tmax=data_tmax, method=method
        )

        self._activ2_noise_cov = mne.compute_covariance(
            self._activ2_epochs, tmin=noise_tmin, tmax=noise_tmax, method=method
        )

        self._activ2_common_cov = self._activ2_data_cov + self._activ2_noise_cov

        log0.info("Data, noise, and common covariances computed and set.")

    @property
    def bf_filters(self) -> Optional[Dict[str, Beamformer]]:
        return self._bf_filters

    @property
    def stcs(self) -> Optional[Dict[str, mne.SourceEstimate]]:
        return self._stcs

    def compute_lcmv_bf_filters(
        self,
        pick_ori: str = "vector",
        weight_norm: str = "unit-noise-gain-invariant",
        reg: float = 0.05,
        lcmv_func: Callable = mne.beamformer.make_lcmv,
    ):
        if (
            self._activ2_evoked is None
            or self._fwd0 is None
            or self._activ2_data_cov is None
            or self._activ2_noise_cov is None
        ):
            raise ValueError(
                "Evoked data, forward solution, and covariances must be set before computing filters."
            )

        self._bf_filters = {}
        for key, val in self._activ2_evoked.items():
            self._bf_filters[key] = lcmv_func(
                info=val.info,
                forward=self._fwd0,
                data_cov=self._activ2_data_cov,
                reg=reg,
                noise_cov=self._activ2_noise_cov,
                pick_ori=pick_ori,
                weight_norm=weight_norm,
                rank=None,
            )

        log0.info(
            f"LCMV beamformer filters computed for {len(self._bf_filters)} conditions "
            f"with pick_ori='{pick_ori}' and weight_norm='{weight_norm}'."
        )

    def apply_lcmv_bf_filters(self):
        if self._bf_filters is None or self._activ2_evoked is None:
            raise ValueError(
                "Filters and evoked data must be set before applying filters."
            )

        self._stcs = {}
        for key, bf_filter in self._bf_filters.items():
            self._stcs[key] = mne.beamformer.apply_lcmv(
                self._activ2_evoked[key], bf_filter
            )

        log0.info(
            f"LCMV beamformer applied to {len(self._stcs)} conditions. "
            "Source estimates stored in stcs property."
        )

    def story(self) -> pd.DataFrame:
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
        raise NotImplementedError(
            "The 'publish' method is not implemented yet. Stay tuned for future updates!"
        )

    def _get_mne_file_path(self, fif_file: Union[str, Path], suffix: str) -> Path:
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
