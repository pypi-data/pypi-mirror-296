from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, Protocol, TypeVar


T = TypeVar("T")
P = TypeVar("P")


def boolean(value: Any) -> bool:
	"""
		Convert any object into a boolean

		:param value: The object to convert
	"""

	if isinstance(value, str):
		if value.lower() in {'on', 'y', 'yes', 'true', 'enable', 'enabled', '1'}:
			return True

		if value.lower() in {'off', 'n', 'no', 'false', 'disable', 'disabled', '0'}:
			return False

		raise TypeError(f'Cannot parse string "{value}" as a boolean')

	if isinstance(value, int):
		if value == 1:
			return True

		if value == 0:
			return False

		raise ValueError('Integer value must be 1 or 0')

	if value is None:
		return False

	return bool(value)


class ClassProperty:
	def __init__(self,
				func_get: Callable[[type[T]], P],
				func_set: Callable[[type[T], P], None] | None = None):

		self.func_get: Callable[[type[T]], P] = func_get
		self.func_set: Callable[[type[T], P], None] | None = func_set


	def __get__(self, obj: T, cls: type[T]) -> Any:
		return self.func_get(cls or type(obj))


	def __set__(self, obj: T, value: Any) -> None:
		if not self.func_set:
			raise AttributeError("Cannot set attribute")

		return self.func_set(type(obj), value)


	def setter(self, func_set: Callable[[type[T], P], None]) -> ClassProperty:
		self.func_set = func_set
		return self


class ColumnDescription:
	"""
		Describes a column returned by :attr:`Cursor.description`

		.. note:: Most of the types were guessed since the spec does not list the types.
	"""

	def __init__(self,
				name: str,
				type_code: int,
				display_size: int | None = None,
				internal_size: int | None = None,
				precision: int | None = None,
				scale: int | None = None,
				null_ok: bool | None = None):
		"""
			Create a new column description object

			:param name: Name of the column
			:param type_code: Code of the column's type
			:param display_size: n/a
			:param internal_size: n/a
			:param precision: n/a
			:param scale: n/a
			:param null_ok: Whether or not the column can be null
		"""

		self.name: str = name
		self.type_code: int = type_code
		self.display_size: int | None = display_size
		self.internal_size: int | None = internal_size
		self.precision: int | None = precision
		self.scale: int | None = scale
		self.null_ok: bool | None = null_ok


class ConnectionProto(Protocol):
	"Represents a module's ``Connection`` class"

	def close(self) -> None: ...
	def commit(self) -> None: ...
	def rollback(self) -> None: ...
	def cursor(self) -> CursorProto: ...


class CursorProto(Protocol):
	"Represents a module's ``Cursor`` class"

	@property
	def description(self) -> tuple[tuple[Any, ...], ...]: ...

	@property
	def rowcount(self) -> int: ...

	def close(self) -> None: ...
	def execute(self, query: str, params: dict[str, Any]) -> None: ...
	def executemany(self, query: str, params: Iterable[dict[str, Any]]) -> None: ...
	def fetchone(self) -> tuple[Any, ...] | None: ...
	def fetchmany(self, size: int = 1) -> tuple[tuple[Any, ...], ...]: ...
	def fetchall(self) -> tuple[tuple[Any, ...], ...]: ...


class StatementParsingError(Exception):
	def __init__(self, message: str, name: str, row: int, column: int):
		self.message: str = message
		"Error message"

		self.name: str = name
		"Name of the statement"

		self.row: int = row
		"Index of the line with the error"

		self.column: int = column
		"Index of the character where the error starts"


	def __str__(self) -> str:
		return f"{self.message}: (name = '{self.name}', row = {self.row}, column = {self.column})"
