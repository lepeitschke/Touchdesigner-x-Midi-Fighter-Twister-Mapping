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
            knob = self.oop(op_path)   # resolve operator
            if knob:
                knob.par[par_name] = val
            else:
                debug(f"OP not found: {op_path}")
        except Exception as e:
            debug(f"Error setting {op_path}.{par_name}: {e}")

    def ApplyAssignments(self):
        """
        Loop over rows in target_table and set parameters.
        Assumes table format: op_path | par_name | val
        """
        for row in self.target_table.rows()[1:]:  # skip header row
            op_path = row[0].val
            par_name = row[1].val
            val = row[2].val
            self.StoreData(op_path, par_name, val)
    
    def Easy(self):
        print("Hello")

        
