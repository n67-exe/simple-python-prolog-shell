"""
A command‑line interactive Prolog REPL shell built with PySwip.
"""



import argparse
from collections.abc import Generator
from pyswip.prolog import Prolog, PrologError



class PrologShell:
	"""Interactive Prolog shell with lazy solution enumeration."""

	prolog: Prolog
	_active_generator: Generator | None


	def __init__(self) -> None:
		"""Initialize the Prolog engine."""

		self.prolog = Prolog()
		self._active_generator = None


	def _close_active_query(self) -> None:
		"""Close the currently open query by discarding the generator."""

		if self._active_generator is not None:
			# Discard the generator
			self._active_generator = None


	def consult_file(self, filename: str) -> None:
		"""Consult a Prolog file, print success or error."""

		try:
			self.prolog.consult(filename)
			print(f"Loaded: {filename}")
		except PrologError as e:
			print(f"Error consulting {filename}: {e}")


	@staticmethod
	def _format_bindings(bindings: dict) -> str:
		"""Format a dictionary of variable bindings for output."""

		if not bindings:
			return "true."

		parts = [f"{var} = {val}" for var, val in bindings.items()]

		return ", ".join(parts)


	def run_new_query(self, query_str: str) -> bool:
		"""
		Execute a new Prolog query, print the first solution,
		and keep the generator open for further ';' commands.

		Returns True if the query was started successfully.
		"""

		# Close any previous active query
		self._close_active_query()

		# Ensure query ends with a period
		query_str = query_str.strip()

		if not query_str:
			return False

		if not query_str.endswith('.'):
			query_str += '.'

		try:
			# Create the generator
			active_generator = self.prolog.query(query_str)

			self._active_generator = active_generator

			# Try to get the first solution
			try:
				first_solution = next(active_generator)
				print(self._format_bindings(first_solution))
				return True
			except StopIteration:
				# No solutions at all
				print("false.")
				self._close_active_query()
				return True
			except PrologError as e:
				print(f"ERROR: {e}")
				self._close_active_query()
				return True

		except PrologError as e:
			print(f"ERROR: {e}")
			self._close_active_query()
			return True
		except Exception as e:
			print(f"Unexpected error: {e}")
			self._close_active_query()
			return False


	def get_next_solution(self) -> None:
		"""Print the next solution of the active query, if any."""

		if self._active_generator is None:
			print("No active query. Start a new query first.")
			return

		try:
			solution = next(self._active_generator)
			print(self._format_bindings(solution))
		except StopIteration:
			print("No more solutions.")
			self._close_active_query()
		except PrologError as e:
			print(f"ERROR: {e}")
			self._close_active_query()
		except Exception as e:
			print(f"Unexpected error: {e}")
			self._close_active_query()


	def repl(self) -> None:
		"""Main Read-Eval-Print Loop."""

		print("Prolog Shell (pyswip) – type 'exit' to quit, '?' for help.")
		print("After a solution, type ';' to get the next one.")
		print("Type 'run_tests' to run tests.")

		while True:
			try:
				user_input = input("?- ").strip()
			except:
				self._close_active_query()
				raise

			if not user_input:
				continue

			# Special commands
			if user_input.lower() in ('exit.', 'exit'):
				print("Exiting.")
				break
			if user_input.lower() in ('?.', '?'):
				print("Enter any Prolog query.")
				print("After a solution, type ';' to get the next solution.")
				print("Special commands: 'exit' , '?'")
				continue
			if user_input == ';':
				self.get_next_solution()
				continue

			# Normal query
			self.run_new_query(user_input)



def main() -> None:
	parser = argparse.ArgumentParser(description=__doc__)

	parser.suggest_on_error = True

	parser.add_argument("file", nargs="?", help="Prolog source file to consult at startup")
	args = parser.parse_args()

	shell = PrologShell()

	if args.file:
		shell.consult_file(args.file)

	shell.repl()


if __name__ == "__main__":
	main()
