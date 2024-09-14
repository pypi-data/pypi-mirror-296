from __future__ import annotations

import json

from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, TypeVar, overload

from .enums import BackendType

if TYPE_CHECKING:
	from .connection import Cursor

	try:
		from typing import Self

	except ImportError:
		from typing_extensions import Self


T = TypeVar("T")


class Row(dict[str, Any]):
	"Represents a single row of data."

	__slots__ = ("table",)

	table_name: str | None = None
	"Name of the table the row is associated with. Used for subclasses."

	schema_name: str | None = None
	"Name of the schema the table is associated with. Used for subclasses."


	def __init__(self, data: dict[str, Any], table: str | None = None):
		"""
			Create a new row

			:param data: Key/value pairs of data
			:param table: Table name associated with the data
		"""

		dict.__init__(self, data)
		self.table: str | None = table


	def __repr__(self) -> str:
		value_str = ", ".join(f"{key}={repr(value)}" for key, value in self.items())
		return f"Row({value_str})"


	@classmethod
	def get_columns(cls: type[Self]) -> tuple[Column[Any], ...]:
		"Get a tuple of `Column` objects associated with the row if any exist"

		return tuple(value for value in vars(cls).values() if isinstance(value, Column))


	@classmethod
	def to_table(cls: type[Self]) -> Table:
		"Create a ``Table`` object based on the ``Column`` objects attached to the row."

		if not (columns := cls.get_columns()):
			raise TypeError(f"Row class '{cls.__name__}' does not have any columns")

		return Table(
			cls.table_name or cls.__name__.lower(),
			*columns,
			schema_name = cls.schema_name
		)


	@classmethod
	def from_cursor(cls: type[Self], cursor: Cursor, data: Iterable[Any]) -> Self:
		"""
			Create a new Row object from a cursor and data

			:param cursor: Cursor to work with
			:param data: Row to be parsed
		"""

		fields = tuple(column.name for column in cursor.description)
		return cls(dict(zip(fields, data)))


	def to_dict(self, exclude: Sequence[str] | None = None) -> dict[str, Any]:
		new_data: dict[str, Any] = {}

		for key, value in self.items():
			if key not in (exclude or []):
				new_data[key] = value

		return new_data


RowType = TypeVar("RowType", bound = Row)


class Column(Generic[T]):
	"Represents a column in a table"

	__slots__ = (
		"name", "data_type", "nullable", "autoincrement", "primary_key",
		"default", "unique", "foreign_key", "deserializer", "serializer"
	)


	def __init__(self,
				name: str,
				data_type: str,
				nullable: bool = True,
				autoincrement: bool = False,
				primary_key: bool = False,
				default: str | None = None,
				unique: bool = False,
				foreign_key: tuple[str, str] | None = None,
				deserializer: Callable[[Any], T] | None = None,
				serializer: Callable[[T], Any] | None = None) -> None:
		"""
			Create a new ``Column`` object

			:param name: Name of the column
			:param data_type: Type of data to be stored in the column
			:param nullable: Whether or not the data for the column can be ``NULL``
			:param autoincrement: Ensure an ``INTEGER PRIMARY KEY`` column does not reuse numbers
				(sqlite-only)
			:param primary_key: Set the column to be a primary column
			:param default: Value to set for a row if the value is ``NULL``
			:param unique: Ensure every row for this column has a unique value
			:param foreign_key: Column from another table this column should reference
			:param deserializer: Method to use when converting a value to a python type.
				Only used when `Column` is a descriptor
			:param serializer: Method to use when converting a value to an SQL type.
				Only used when `Column` is a descriptor
		"""

		self.name: str = name
		"Name of the column"

		self.data_type: str = data_type.upper()
		"Type of data to be stored in the column"

		self.nullable: bool = nullable
		"Whether or not the data for the column can be ``NULL``"

		self.autoincrement: bool = autoincrement
		"Ensure an ``INTEGER PRIMARY KEY`` column does not reuse numbers (sqlite-only)"

		self.primary_key: bool = primary_key
		"Set the column to be a primary column"

		self.default: str | None = default
		"Value to set for a row if the value is ``NULL``"

		self.unique: bool = unique
		"Ensure every row for this column has a unique value"

		self.foreign_key: tuple[str, str] | None = foreign_key
		"Column from another table this column should reference"

		self.deserializer: Callable[[Any], T] | None = deserializer
		"Method to use when converting a value to a python type"

		self.serializer: Callable[[T], Any] | None = serializer
		"Method to use when converting a value to an SQL type"


	def __repr__(self) -> str:
		props = [f"{key}={repr(getattr(self, key))}" for key in self.__slots__]
		prop_str = ", ".join(props)

		return f"Column({prop_str})"


	@overload
	def __get__(self, obj: None, cls: type[RowType] | None) -> Self:
		...


	@overload
	def __get__(self, obj: RowType, cls: type[RowType]) -> T:
		...


	def __get__(self, obj: RowType | None, cls: Any) -> T | Self:
		if obj is None:
			return self

		if self.deserializer is not None:
			return self.deserializer(obj[self.name])

		return obj[self.name] # type: ignore[no-any-return]


	def __set__(self, obj: RowType, value: T) -> None:
		if self.serializer is not None:
			value = self.serializer(value)

		obj[self.name] = value


	def __delete__(self, obj: RowType) -> None:
		obj[self.name] = self.default


	def build(self, btype: BackendType) -> str:
		"""
			Convert the column object into an SQL query string to be used in a ``CREATE TABLE``
			query

			:param btype: Backend database type to build the query for
		"""

		data = [f"\"{self.name}\""]

		if self.data_type == "SERIAL":
			if btype == BackendType.POSTGRESQL:
				data.extend([self.data_type, "PRIMARY KEY"])

			else:
				data.extend(["INTEGER", "UNIQUE", "PRIMARY KEY"])

			return " ".join(data)

		data.append(self.data_type)

		if not self.nullable:
			data.append("NOT NULL")

		if self.unique:
			data.append("UNIQUE")

		if self.primary_key:
			data.append("PRIMARY KEY")

		if self.autoincrement and btype == BackendType.SQLITE:
			data.append("AUTOINCREMENT")

		if self.default is not None:
			data.append(f"DEFAULT {repr(self.default)}")

		return " ".join(data)


class Table(dict[str, Column[Any]]):
	"Represents a table"

	def __init__(self, name: str, *columns: Column[Any], schema_name: str | None = None):
		"""
			Create a new ``Table`` object

			:param name: Name of the table
			:param columns: Columns of the table
			:param schema_name: Schema name to use
		"""

		dict.__init__(self, {column.name: column for column in columns})

		self.name: str = name
		self.schema_name: str | None = schema_name


	def __repr__(self) -> str:
		cols = ", ".join(column for column in self)
		return f"Table(name={repr(self.name)}, schema_name={repr(self.schema_name)}, columns={cols})"


	def add_column(self, column: Column[T]) -> Column[T]:
		"""
			Append an existing ``Column`` object to the table

			:param column: Column to append
		"""

		self[column.name] = column
		return column


	def new_column(self, name: str, *args: Any, **kwargs: Any) -> Column[Any]:
		"""
			Append a new ``Column`` object to the table

			:param name: Name of the column
			:param args: Positional arguments to pass to :meth:`Column.__init__`
			:param kwargs: Keyword arguments to pass to :meth:`Column.__init__`
		"""

		self[name] = Column(name, *args, **kwargs)
		return self[name]


	def build(self, btype: BackendType) -> str:
		"""
			Convert the table object into an SQL query string

			:param btype: Backend database type to build the query for
		"""

		foreign_keys: list[str] = []
		columns: list[str] = []

		for column in self.values():
			columns.append(column.build(btype))

			if column.foreign_key:
				table, col = column.foreign_key

				fkey_string = f"\tFOREIGN KEY (\"{column.name}\")\n"
				fkey_string += f"\t\tREFERENCES \"{table}\" (\"{col}\")\n"
				fkey_string += "\t\t\tON DELETE CASCADE"

				foreign_keys.append(fkey_string)

		column_string = "\t" + ",\n\t".join(columns)

		if foreign_keys:
			column_string += ",\n" + ", ".join(foreign_keys)

		if self.schema_name is not None:
			table_name = f"\"{self.schema_name}\".\"{self.name}\""

		else:
			table_name = f"\"{self.name}\""

		return f"CREATE TABLE IF NOT EXISTS {table_name} (\n{column_string}\n);"


class Tables(dict[str, Table]):
	"Holds the table layouts for a database"

	def __init__(self, *tables: Table):
		"""
			Create a new ``Tables`` object

			:param tables: ``Table`` objects to initiate with
		"""

		dict.__init__(self, {table.name: table for table in tables})


	def __repr__(self) -> str:
		tables = ", ".join(repr(table) for table in self)
		return f"Tables({tables})"


	@classmethod
	def from_json(cls: type[Tables], raw_data: Path | str | dict[str, Any]) -> Tables:
		"""
			Create a new ``Tables`` object from a JSON file, JSON string, or ``dict`` object

			:param raw_data: Data to parse into tables
		"""

		tables = cls()
		tables.load_json(raw_data)

		return tables


	def add_row(self, row: type[RowType]) -> type[RowType]:
		"""
			Add a subclassed `Row` object as a table

			:param row: Row class to turn into a table
		"""

		self.add_table(row.to_table())
		return row


	def add_table(self, table: Table) -> None:
		"""
			Append a table to the list of tables

			:param table: The table to add
		"""

		self[table.name] = table


	def new_table(self, name: str, *columns: Column[Any], schema: str | None = None) -> Table:
		"""
			Create a new table and append it to the list of tables

			:param name: Name of the table to create
			:param columns: List of ``Column`` objects for the table
		"""

		self[name] = Table(name, *columns, schema_name = schema)
		return self[name]


	def build(self, btype: BackendType) -> tuple[str, ...]:
		"""
			Convert each table object into an SQL query string

			:param btype: Backend database type to build the query for
		"""

		return tuple(table.build(btype) for table in self.values())


	def load_json(self, raw_data: Path | str | dict[str, Any]) -> None:
		"""
			Load new ``Table`` objects from a JSON file, JSON string, or ``dict`` object

			:param raw_data: Data to parse into tables
		"""

		if isinstance(raw_data, str):
			if (path := Path(raw_data).expanduser().resolve()).exists():
				raw_data = path

			else:
				data = json.loads(raw_data)

		if isinstance(raw_data, Path):
			with raw_data.open("r", encoding = "utf-8") as fd:
				data = json.load(fd)

		elif not isinstance(raw_data, dict):
			raise TypeError("Data is not a Path, str, or dict")

		else:
			data = raw_data

		for table_name, table in data.items():
			self.new_table(table_name)

			for column_name, column in table.items():
				self[table_name].new_column(column_name, column.pop("type"), **column)


	def to_dict(self) -> dict[str, Any]:
		"""
			Convert all tables to a ``dict`` object that can later be loaded with
			:meth:`Tables.load_json` or :meth:`Tables.from_json`
		"""

		data: dict[str, Any] = {}

		for table in self.values():
			data[table.name] = {}

			for column in table.values():
				data[table.name][column.name] = {
					"type": column.data_type,
					"nullable": column.nullable,
					"autoincrement": column.autoincrement,
					"primary_key": column.primary_key,
					"default": column.default,
					"unique": column.unique,
					"foreign_key": column.foreign_key
				}

		return data


	def to_json(self, path: Path | str | None = None, indent: int | str | None = "\t") -> str:
		"""
			Dump the tables to a JSON string and optionally to a file

			:param path: Path to store the tables as a JSON file
			:param indent: Number of spaces (int) or string (str) to use for indentions in the
				resulting JSON data
		"""

		if isinstance(path, str):
			path = Path(path).expanduser().resolve()

		if path:
			with path.open("w", encoding = "utf-8") as fd:
				json.dump(self.to_dict(), fd, indent = indent)

		return json.dumps(self.to_dict(), indent = indent)
