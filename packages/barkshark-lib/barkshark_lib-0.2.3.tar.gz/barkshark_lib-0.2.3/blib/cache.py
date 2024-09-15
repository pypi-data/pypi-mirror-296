from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import timedelta
from hashlib import sha1
from typing import Any, Generic, ParamSpec, TypeVar

from .date import Date
from .misc import get_object_name

try:
	from typing import Self

except ImportError:
	from typing_extensions import Self


P = ParamSpec("P")
T = TypeVar("T")


@dataclass()
class CacheItem(Generic[T]):
	key: str
	value: T
	timestamp: Date


class Cache(OrderedDict[str, CacheItem[T]]):
	"Class for caching data"


	def __init__(self, max_items: int = 8192, ttl: timedelta | int = 0) -> None:
		# not sure why mypy is complaining about this one
		OrderedDict.__init__(self) # type: ignore[arg-type]

		self.max_items: int = max_items
		self._ttl: timedelta = timedelta(seconds = ttl) if isinstance(ttl, int) else ttl
		self._wrapped_function: Callable[P, T] | None = None


	def __repr__(self) -> str:
		return f"{get_object_name(self)}(max_items={repr(self.max_items)}, ttl={repr(self.ttl)})"


	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
		if self._wrapped_function is None:
			raise ValueError("No function was wrapped")

		keyhash = sha1()
		data: dict[Any, Any] = {**dict(enumerate(args)), **kwargs}

		for key, value in data.items():
			keyhash.update(bytes(hash(key)))
			keyhash.update(bytes(hash(value)))

		key = keyhash.hexdigest()

		if (item := self.get(key)) is not None:
			return item.value

		return self.store(key, self._wrapped_function(*args, **kwargs))


	@classmethod
	def wrap(
			cls: type[Self],
			max_items: int = 8192,
			ttl: timedelta | int = 0) -> Callable[[Callable[P, T]], Cache[T]]:

		cache = cls(max_items, ttl)

		def wrapper(func: Callable[P, T]) -> Cache[T]:
			# another mypy moment
			cache._wrapped_function = func # type: ignore[assignment]
			cache.__call__.__doc__ = func.__doc__
			cache.__call__.__annotations__ = func.__annotations__
			return cache

		return wrapper


	@property
	def ttl(self) -> int:
		return self._ttl.seconds


	def fetch(self, key: str) -> T:
		if (item := self.get(key)) is None:
			raise KeyError(key)

		if self.ttl > 0:
			if (timestamp := Date.new_utc()) >= item.timestamp:
				del self[key]
				raise KeyError(key)

			item.timestamp = timestamp + self._ttl

		self.move_to_end(key)
		return item.value


	def items(self) -> Iterator[tuple[str, T]]: # type: ignore[override]
		for key, item in OrderedDict.items(self):
			yield key, item.value


	def store(self, key: str, value: T) -> T:
		if self.get(key) is None:
			self[key] = CacheItem(key, value, Date.new_utc() + self._ttl)

		else:
			self[key].value = value

		self.move_to_end(key)
		self._check_size()
		return value


	def _check_size(self) -> None:
		if self.max_items < 1:
			return

		while len(self) > self.max_items:
			self.popitem(last = False)
