from copy import deepcopy
import csv
from pathlib import Path
import sys
from uuid import uuid4


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]
sys.path.insert(0, str(WORKSPACE / ".tools" / "kiutils"))

from kiutils.items.common import Effects, Font, PageSettings, Position, Property, TitleBlock
from kiutils.items.schitems import LocalLabel, SchematicSymbol, SymbolProjectInstance, SymbolProjectPath, Text
from kiutils.schematic import Schematic
from kiutils.symbol import SymbolLib


PROJECT = "Piezo_Demo_7x7"
OUT = ROOT / f"{PROJECT}.kicad_sch"
KICAD_SYMBOLS = Path(r"C:\Program Files\KiCad\9.0\share\kicad\symbols")


def uid():
    return str(uuid4())


def effects(size=1.0, hide=False, bold=False):
    return Effects(font=Font(height=size, width=size, bold=bold), hide=hide)


def prop(key, value, x, y, hidden=False, size=0.9):
    return Property(key=key, value=value, position=Position(x, y, 0), effects=effects(size, hidden))


def pin_numbers(lib_symbol):
    result = []
    for unit in lib_symbol.units:
        for pin in unit.pins:
            if pin.number not in result:
                result.append(pin.number)
    return result


def pin_offset(lib_symbol, number):
    for unit in lib_symbol.units:
        for pin in unit.pins:
            if pin.number == str(number):
                return pin.position.X, pin.position.Y
    raise KeyError((lib_symbol.libId, number))


def main():
    source = Schematic.from_file(str(ROOT.parent / "MouseMinder.kicad_sch"), encoding="utf-8")
    schematic = Schematic.create_new()
    schematic.version = "20231120"
    schematic.generator = "eeschema"
    schematic.uuid = uid()
    schematic.paper = PageSettings(paperSize="A2")
    schematic.titleBlock = TitleBlock(
        title="43-Piezo Direct Row/Column Selector",
        revision="0.3",
        company="MouseMinder",
        comments={1: "Press one row button and one column button to connect a buzzer to the BNC."},
    )

    libraries = {}
    for lib_id in ("Device:Buzzer", "Switch:SW_Push"):
        item = deepcopy(next(x for x in source.libSymbols if x.libId == lib_id))
        libraries[item.libId] = item

    connector_lib = SymbolLib.from_file(str(KICAD_SYMBOLS / "Connector.kicad_sym"), encoding="utf-8")
    coax = deepcopy(next(x for x in connector_lib.symbols if x.entryName == "Conn_Coaxial"))
    coax.libraryNickname = "Connector"
    libraries[coax.libId] = coax
    schematic.libSymbols = list(libraries.values())

    def add_symbol(lib_id, ref, value, footprint, x, y, description="", extra=None):
        x = round(x / 1.27) * 1.27
        y = round(y / 1.27) * 1.27
        lib_symbol = libraries[lib_id]
        symbol = SchematicSymbol(
            position=Position(x, y, 0), unit=1, inBom=True, onBoard=True,
            uuid=uid(),
            properties=[
                prop("Reference", ref, x, y - 5.0, size=0.8),
                prop("Value", value, x, y + 5.0, size=0.72),
                prop("Footprint", footprint, x, y, hidden=True),
                prop("Datasheet", "~", x, y, hidden=True),
                prop("Description", description, x, y, hidden=True),
            ] + [prop(key, val, x, y, hidden=True) for key, val in (extra or {}).items()],
            pins={number: uid() for number in pin_numbers(lib_symbol)},
            instances=[SymbolProjectInstance(
                name=PROJECT,
                paths=[SymbolProjectPath(sheetInstancePath=f"/{schematic.uuid}", reference=ref, unit=1)],
            )],
        )
        symbol.libId = lib_id
        schematic.schematicSymbols.append(symbol)
        return symbol

    def label_pin(symbol, number, text, size=0.62):
        dx, dy = pin_offset(libraries[symbol.libId], number)
        schematic.labels.append(LocalLabel(
            text=text,
            position=Position(symbol.position.X + dx, symbol.position.Y - dy, 0),
            effects=effects(size),
            uuid=uid(),
        ))

    def note(text, x, y, size=1.2, bold=False):
        schematic.texts.append(Text(
            text=text, position=Position(x, y, 0), effects=effects(size, bold=bold), uuid=uid()
        ))

    note("FUNCTION GENERATOR", 25, 18, 1.2, True)
    j1 = add_symbol(
        "Connector:Conn_Coaxial", "J1", "TE 1-1478204-0",
        "Connector_Coaxial:BNC_TEConnectivity_1478204_Vertical", 35, 30,
        "Vertical BNC input",
    )
    label_pin(j1, "1", "BNC_SIGNAL")
    label_pin(j1, "2", "BNC_RETURN")

    note("ROW SELECT", 80, 18, 1.2, True)
    for index, row_name in enumerate("ABCDEFG"):
        x = 85 + index * 31
        sw = add_symbol(
            "Switch:SW_Push", f"SW{index + 1}", f"ROW {row_name}",
            "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A", x, 30,
            "LCK-TA022H18-2WL row selector", {"MPN": "LCK-TA022H18-2WL", "LCSC": "C51978285"},
        )
        label_pin(sw, "1", "BNC_SIGNAL")
        label_pin(sw, "2", f"ROW_{row_name}")

    note("COLUMN SELECT", 80, 46, 1.2, True)
    for index in range(7):
        x = 85 + index * 31
        sw = add_symbol(
            "Switch:SW_Push", f"SW{index + 8}", f"COLUMN {index + 1}",
            "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A", x, 58,
            "LCK-TA022H18-2WL column selector", {"MPN": "LCK-TA022H18-2WL", "LCSC": "C51978285"},
        )
        label_pin(sw, "1", f"COL_{index + 1}")
        label_pin(sw, "2", "BNC_RETURN")

    note("PIEZO MATRIX", 25, 80, 1.2, True)
    note("Hold one ROW button and one COLUMN button to test that cell. G2-G7 are unused.", 25, 87, 0.9)

    with (ROOT / "Piezo_Demo_7x7_BOM.csv").open(newline="", encoding="utf-8") as handle:
        parts = list(csv.DictReader(handle))

    for index, part in enumerate(parts, 1):
        cell = part["Cell"]
        row = ord(cell[0]) - ord("A")
        col = int(cell[1]) - 1
        x = 55 + col * 51
        y = 110 + row * 38
        buzzer = add_symbol(
            "Device:Buzzer", f"BZ{index}", part["MPN"],
            f"piezo_footprints:{part['Footprint']}", x, y,
            f"{cell}: {part['Voltage']}, {part['Current']}, {part['SPL']}",
            {"LCSC": part["LCSC"], "CELL": cell},
        )
        label_pin(buzzer, "1", f"ROW_{cell[0]}", 0.55)
        label_pin(buzzer, "2", f"COL_{cell[1]}", 0.55)
        note(cell, x - 9, y - 9, 0.72, True)

    schematic.to_file(str(OUT), encoding="utf-8")

    with (ROOT / "Piezo_Demo_7x7_Switching_BOM.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["References", "Quantity", "MPN", "LCSC", "Footprint", "Notes"])
        writer.writerow(["SW1-SW14", 14, "LCK-TA022H18-2WL", "C51978285", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A", "7 row and 7 column selectors"])
        writer.writerow(["J1", 1, "TE 1-1478204-0", "", "Connector_Coaxial:BNC_TEConnectivity_1478204_Vertical", "Function-generator input"])


if __name__ == "__main__":
    main()
