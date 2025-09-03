# Touchdesigner-x-Midi-Fighter-Twister-Mapping
A TouchDesigner module for mapping, storing, resetting, and recalling knob values. Uses class-based extensions with lookup tables (opfind1 + midi_assignments) to manage parameters dynamically. Ideal for MIDI/OSC workflows and live performance setups.

---

## ✨ Features
- Dynamic operator + parameter mapping via lookup tables  
- Store and recall functionality for parameter values (`midi_assignments` table)  
- Reset system to clear all knob values before applying stored mappings (`opfind1` table)  
- Easy integration with **CHOP Execute DATs** or scripts for MIDI/OSC workflows  
- Clean, object-oriented structure using TouchDesigner’s `EXT` class convention  

---

## ⚙️ How it Works
- **`opfind1` table** → lists all knobs and their parameters (used for reset)  
- **`midi_assignments` table** → stores saved mappings (used for recall)  
- **`MainEXT` class** provides methods:  
  - `reset_knobs()` → clears all knobs to a default value  
  - `apply_assignments()` → recalls and applies stored mappings  
  - `store_data()` → updates an individual parameter dynamically  

---

## 🎛️ Use Cases
- MIDI or OSC controlled installations  
- Live performance setups with dynamic mapping  
- Visual projects requiring quick reset + recall of parameter states  

---

## 📖 Example Workflow
```python
# Reset all knobs to default
op('base1').ext.Main.reset_knobs()

# Apply stored assignments
op('base1').ext.Main.apply_assignments()

# Update a single knob dynamically
op('base1').ext.Main.store_data("knob1", "Knoblevelcolorr", 0.5)


Visual projects requiring quick reset + recall of parameter states
