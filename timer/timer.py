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
    logger: Logger = logger

    def __post_init__(self):
        self.start()

    def __repr__(self) -> str:
        return f"Timer"

    def _process_key(self, container: dict[str | int, float], key: str | None = None) -> str:
        count = 0
        orig_key = key if key is not None else ""
        while True:
            key = orig_key
            if orig_key == "":
                key += str(count)
            else:
                key += "_" + str(count)
            count += 1
            if key not in container:
                break
        return key

    def _push(
        self, container: dict[str | int, float], t: float, key: str | None = None
    ) -> tuple[dict[str | int, float], float, str]:
        key = self._process_key(container, key)
        container[key] = t
        return container, t, key

    def push_lap(self, t: float, key: str | None = None) -> tuple[float, str]:
        self._laps, t, key = self._push(self._laps, t, key)
        return t, key

    def push_split(self, t: float, key: str | None = None) -> tuple[float, str]:
        self._splits, t, key = self._push(self._splits, t, key)
        return t, key

    def start(self):
        self._start_time = time.time()
        self._ptime = self._start_time
        self._laps: dict[str | int, float] = {}
        self._splits: dict[str | int, float] = {}
        logger.info("Timer started")

    def lap(self, key: str | None = None) -> float:
        t = time.time()
        lap = t - self._ptime
        self._ptime = t

        lap, key = self.push_lap(lap, key)
        logger.info(f"Lap {key}: {lap}")
        return lap

    def split(self, key: str | None = None) -> float:
        t = time.time()
        sp = t - self._start_time
        sp, key = self.push_split(sp, key)
        logger.info(f"Split {key}: {sp}")
        return sp

    @property
    def laps(self) -> dict[str | int, float]:
        return self._laps

    @property
    def splits(self) -> dict[str | int, float]:
        return self._splits

    def report(self, sort_key: bool = False) -> str:
        text = f"Timer report\n"
        text += f"Total time: {time.time() - self._start_time}\n"
        text += "\nLaps:\n"
        keys = sorted(self._laps.keys()) if sort_key else self._laps.keys()
        for key in keys:
            text += f"{key}: {self.laps[key]}\n"
        text += "\nSplits:\n"
        keys = sorted(self._splits.keys()) if sort_key else self._splits.keys()
        for key in keys:
            text += f"{key}: {self.splits[key]}\n"
        return text
