# Piezo Demo 7x7

- KiCad 9 schematic and fully routed two-layer PCB.
- 224 mm x 224 mm board with a 7 x 7 grid of 32 mm cells.
- 43 buzzer footprints, two rows of seven MouseMinder SMD selector buttons, a vertical BNC input, and a reserved switching/MCU cell.
- Available EasyEDA 3D bodies are included and linked project-relatively.
- The BNC includes a simplified project-local preview body based on the TE product envelope.
- Front silkscreen: cell and MPN.
- Back silkscreen: MPN, LCSC number, live LCSC 1-piece/500-piece unit pricing, voltage, current, SPL, driver type, mount, and body size.

Five unavailable EasyEDA records use same-family fallback geometry. Verify every footprint against the purchased part's current datasheet before fabrication.

The schematic directly connects the BNC through one selected row switch and one selected column switch. Press one button from each bank to connect the corresponding buzzer. G2-G7 are unused.

ERC and PCB DRC both pass with zero violations and zero unconnected pads. JLCPCB-ready Gerbers are in `fabrication/Piezo_Demo_7x7_JLCPCB_Gerbers.zip`.

Regenerate with KiCad's bundled Python:

```powershell
python .\generate_bnc_model.py
& 'C:\Program Files\KiCad\9.0\bin\python.exe' .\generate_piezo_demo_board.py
python .\generate_piezo_demo_schematic.py
```
