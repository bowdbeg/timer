import dataclasses
import time
from logging import INFO, Formatter, Logger, StreamHandler, getLogger

logger = getLogger(__name__)
logger.setLevel(INFO)
handler = StreamHandler()
formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


@dataclasses.dataclass
class Timer:
    """
    Timer class to measure time of each step in a program.

    Attributes
    ----------
    logger : Logger
        Logger object to log messages.
    digits : int
        Number of digits to display the time.
    """

    logger: Logger = logger
    digits: int = 4

    def __post_init__(self):
        self.start()

    def __repr__(self) -> str:
        return f"Timer"

    def _process_key(self, container: dict[str | int, float], key: str | None = None) -> str:
        if key != "" and key not in container:
            return key
        count = 1
        orig_key = key if key is not None else ""
        while True:
            key = orig_key
            if orig_key == "":
                key += str(count)
            else:
                key += "_" + str(count)
            if key not in container:
                break
            count += 1
        return key

    def _push(
        self, container: dict[str | int, float], t: float, key: str | None = None
    ) -> tuple[dict[str | int, float], float, str]:
        key = self._process_key(container, key)
        container[key] = t
        return container, t, key

    def _push_lap(self, t: float, key: str | None = None) -> tuple[float, str]:
        self._laps, t, key = self._push(self._laps, t, key)
        return t, key

    def _push_split(self, t: float, key: str | None = None) -> tuple[float, str]:
        self._splits, t, key = self._push(self._splits, t, key)
        return t, key

    def _format_time(self, t: float) -> str:
        return f"{t:.{self.digits}f}"

    def start(self):
        """
        Start or restart the timer. This method resets the timer.

        Returns
        -------
        None
        """

        self._start_time = time.time()
        self._ptime = self._start_time
        self._laps: dict[str | int, float] = {}
        self._splits: dict[str | int, float] = {}
        logger.info("Timer started")

    def lap(self, key: str | None = None) -> float:
        """
        Measure the time since the last lap or the start of the timer.

        Parameters
        ----------
        key : str, optional
            Key to identify the lap. If not provided, key will be a count.
        """

        t = time.time()
        lap = t - self._ptime
        self._ptime = t

        lap, key = self._push_lap(lap, key)
        logger.info(f"Lap {key}:\t{self._format_time(lap)}")
        return lap

    def split(self, key: str | None = None) -> float:
        """
        Measure the time since the start of the timer.

        Parameters
        ----------
        key : str, optional
            Key to identify the split. If not provided, key will be a count.
        """

        t = time.time()
        sp = t - self._start_time
        sp, key = self._push_split(sp, key)
        logger.info(f"Split {key}:\t{self._format_time(sp)}")
        return sp

    @property
    def laps(self) -> dict[str | int, float]:
        """
        Return the laps.

        Returns
        -------
        dict
            Dictionary containing the laps.
        """
        return self._laps

    @property
    def splits(self) -> dict[str | int, float]:
        """
        Return the splits.

        Returns
        -------
        dict
            Dictionary containing the splits.
        """

        return self._splits

    def report(self, sort_key: bool = False) -> str:
        """
        Generate a report of the timer.

        Parameters
        ----------
        sort_key : bool, optional
            Flag to sort the keys in alphabetical order. Default is False.

        Returns
        -------
        str
            Report of the timer.
        """

        text = f"Timer report\n"
        text += f"Total time:\t{self._format_time(time.time() - self._start_time)}\n"
        text += "\nLaps:\n"
        keys = sorted(self._laps.keys()) if sort_key else self._laps.keys()
        for key in keys:
            text += f"{key}:\t{self._format_time(self.laps[key])}\n"
        text += "\nSplits:\n"
        keys = sorted(self._splits.keys()) if sort_key else self._splits.keys()
        for key in keys:
            text += f"{key}:\t{self._format_time(self.splits[key])}\n"
        return text
