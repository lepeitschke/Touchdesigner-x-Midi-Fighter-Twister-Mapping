class MainEXT:
    def __init__(self, ownerCOMP):
        self.ownerCOMP = ownerCOMP
        oop = self.ownerCOMP.op
        self.oop = oop

        # references to your tables
        self.source_table = self.oop("opfind1")
        self.target_table = self.oop("midi_assignments")

    def GetColIndex(self, table, col_name):
        """Return the index of col_name in the first row of the table"""
        header_row = table.rows()[0]  # first row
        for i, cell in enumerate(header_row):
            if cell.val == col_name:
                return i
        return None  # not found

    def StoreCurrentValues(self, param_name):
        """
        Store current value of `param_name` from each knob listed in self.source_table (opfind1)
        into the corresponding row in self.target_table without deleting rows.
        """
        print("store data")
        if not self.target_table or not self.source_table:
            print("[MyExt] source_table or target_table not found")
            return

        # find column index in target_table
        col_index = self.GetColIndex(self.target_table, param_name)
        if col_index is None:
            print(f"[MyExt] Column '{param_name}' not found in target_table")
            return

        # find column index in source_table for knob names
        name_col_index = self.GetColIndex(self.source_table, "name")
        if name_col_index is None:
            print("[MyExt] Column 'name' not found in source_table")
            return

        # loop over knobs listed in source_table
        for i, row in enumerate(self.source_table.rows()[1:]):  # skip header
            knob_name = row[name_col_index].val
            knob = self.oop(knob_name)
            if not knob:
                print(f"[MyExt] Knob '{knob_name}' not found, skipping")
                continue

            # access parameter safely with exact case
            par = getattr(knob.par, param_name, None)
            if par is not None:  # check the object, not its value
                self.target_table[i + 1, col_index] = par.eval()
            else:
                print(f"[MyExt] Knob '{knob_name}' has no parameter '{param_name}'")

    def StoreData(self, op_path, par_name, val):
        """
        Set the parameter on a dynamically referenced operator.
        op_path: "knob1" (not op('knob1'))
        par_name: parameter name string
        val: value to set
        """

        try:
            knob = self.oop(op_path)  # resolve operator
            if knob:
                knob.par[par_name] = val
            else:
                debug(f"OP not found: {op_path}")
        except Exception as e:
            debug(f"Error setting {op_path}.{par_name}: {e}")

    def ApplyAssignments(self):
        """
        Loop over rows in target_table and set parameters.
        Works with replicants: uses stable identifiers to match the operator.
        Assumes table format:
            stack | # | ... | param columns ...
        """
        print("applying assignments")
        table = self.target_table
        num_rows = table.numRows
        num_cols = table.numCols

        # find column indices
        stack_col = 0  # assuming first col is 'stack'
        id_col = 1  # assuming second col is '#'
        # other columns are parameters
        param_cols = [c for c in range(num_cols) if c not in (stack_col, id_col)]

        for r in range(1, num_rows):  # skip header
            stack_val = table[r, stack_col].val
            knob_id = table[r, id_col].val

            # find the replicant by some stable identifier
            # example: name = knob_id or combine stack+id
            op_path = knob_id  # adjust if needed
            knob = self.oop(op_path)
            if not knob:
                debug(f"Replicant {op_path} not found, skipping row {r}")
                continue

            # apply stored parameter values
            for c in param_cols:
                par_name = table[0, c].val  # header row = parameter name
                val = table[r, c].val
                try:
                    self.StoreData(op_path, par_name, val)
                except Exception as e:
                    debug(f"Error applying {op_path}.{par_name} = {val}: {e}")

    def ResetKnobs(self, reset_val=""):
        """
        Reset all knob-related values in target_table, except the 'stack' and '#' columns.
        Keeps header row intact. Default reset value = 0.
        Works by indexing through the table like op('tableDAT')[row, col].
        """
        table = self.target_table
        num_rows = table.numRows
        num_cols = table.numCols

        # find indices of columns to skip by checking header row (row 0)
        skip_cols = []
        for c in range(num_cols):
            header_val = table[0, c].val
            if header_val in ["stack", "#"]:
                skip_cols.append(c)

        # iterate over data rows (skip header row)
        for r in range(1, num_rows):
            for c in range(num_cols):
                if c not in skip_cols:
                    try:
                        table[r, c] = reset_val
                    except Exception as e:
                        debug(f"Error resetting cell {r},{c}: {e}")
