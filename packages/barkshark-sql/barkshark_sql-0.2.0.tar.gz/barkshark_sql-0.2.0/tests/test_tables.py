import bsql
import unittest

from .data import FILES, TABLES


class TableTest(unittest.TestCase):
	maxDiff = None

	def test_json_import(self):
		tables = bsql.Tables.from_json(FILES["input-tables"])
		self.assertEqual(tables.to_json(), TABLES.to_json())


	def test_json_export(self):
		with FILES["output-tables"].open("r", encoding = "utf-8") as fd:
			self.assertEqual(fd.read(), TABLES.to_json())


	def test_postgresql_build(self):
		with FILES["tables-postgresql"].open("r", encoding = "utf-8") as fd:
			self.assertEqual(fd.read(), "\n\n".join(TABLES.build(bsql.BackendType.POSTGRESQL)))


	def test_sqlite_build(self):
		with FILES["tables-sqlite"].open("r", encoding = "utf-8") as fd:
			self.assertEqual(fd.read(), "\n\n".join(TABLES.build(bsql.BackendType.SQLITE)))
