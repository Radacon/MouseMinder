from pathlib import Path
import csv
import json
import pcbnew


ROOT = Path(__file__).resolve().parent
LIB = ROOT / "piezo_footprints.pretty"
BOARD_PATH = ROOT / "Piezo_Demo_7x7.kicad_pcb"
KICAD_FOOTPRINTS = Path(r"C:\Program Files\KiCad\9.0\share\kicad\footprints")

# Cell, LCSC, MPN, voltage, current, SPL, driver, mount, body, library footprint.
PARTS = [
    ("A1","C530448","GPD3020YB-5V3500","5V","30mA","100dB","Active","THP","D30x20","BUZ-TH_BD30.0-P15.00-D0.8"),
    ("A2","C252966","GPC2416YB-5V3700","1-30V","10mA","85dB","Passive","THP","D24x16","BUZ-TH_BD23.5-P15.00-D0.8-FD"),
    ("A3","C530432","GPD2416YB-3V3500","3V","15mA","90dB","Active","THP","D23.5x16","BUZ-TH_BD23.5-P15.00-D0.8-FD"),
    ("A4","C530428","GPD2316YB-3V3500","3V","15mA","90dB","Active","THP","D23x16","BUZ-TH_BD23.5-P15.00-D0.8-FD"),
    ("A5","C252964","GPC2316YB-5V","1-30V","5mA","100dB","Passive","THP","D23x16.5","BUZ-TH_BD23.0-P15.00-D0.8-FD"),
    ("A6","C530429","GPD2316YB-5V3500","5V","15mA","95dB","Active","THP","D23x16","BUZ-TH_BD23.5-P15.00-D0.8-FD"),
    ("A7","C530425","GPD2310YB-5V3500","5V","15mA","85dB","Active","THP","D23x10","BUZ-TH_BD23.0-P15.00-D0.8-FD"),
    ("B1","C50132443","SFN-1911-0520P20","5V","3mA","85dB","Passive","THP","D19x10.6","BUZ-TH_BD17.0-P10.00-D0.9"),
    ("B2","C129400","HNR-1707","1-30V","5mA","80dB","Passive","THP","D17x8.3","BUZ-TH_BD17.0-P10.00-D0.9"),
    ("B3","C76872","PS1740P02E","3V","-","75dB","Passive","THP","D17x7.5","BUZ-TH_BD17.0-P10.00-D0.8"),
    ("B4","C255339","GSC1750YB-3V4000","1-20V","2.5mA","80dB","Passive","SMD","17x17x5.3","BUZ-SMD_L17.0-W17.0"),
    ("B5","C2972852","FUET-1760","3V","12mA","90dB","-","SMD","D17x6","BUZZ-SMD_FUET-1760"),
    ("B6","C252954","GPC1708AT-5V4000","2-30V","3mA","85dB","Passive","THP","D17x8.5","BUZ-TH_BD17.0-P10.00-D0.9"),
    ("B7","C360608","SFN-17075PA10","5V","5mA","85dB","Passive","THP","D17x8","BUZ-TH_BD17.0-P10.00-D0.9"),
    ("C1","C417416","FSR-1707TP-5V","1-30V","3mA","90dB","Passive","THP","D17x8","BUZ-TH_BD17.0-P10.00-D0.9"),
    ("C2","C128017","HNR-1407A","1-30V","5mA","80dB","Passive","THP","D14.1x7.3","BUZ-TH_BD14.1-P7.62-D1.0-FD"),
    ("C3","C530420","GPD14075YB-3V4000","3V","12mA","85dB","Active","THP","D14x7.5","BUZ-TH_BD14.0-P7.60-D0.7-FD"),
    ("C4","C96060","PS1440P02BT","3V","-","75dB","Passive","THP","D14x8","BUZ-TH_BD14.0-P5.00-D0.7-FD"),
    ("C5","C255337","GSC14045YB-3V4000","3V","2.5mA","75dB","Passive","SMD","14x14x4","BUZ-SMD_L14.1-W14.1-LS14.9"),
    ("C6","C360603","SFN-1407PA7.6","5V","5mA","85dB","Passive","THP","D14x7.5","BUZ-TH_BD14.0-P7.60-D0.7"),
    ("C7","C360604","SFN-14045PA7.6","5V","5mA","85dB","Passive","THP","D14x5","BUZ-TH_BD14.0-P7.60-D0.7"),
    ("D1","C22387762","HNR-1407PA7.5","5V","10mA","94dB","Passive","THP","D14x7","BUZ-TH_BD14.0-P7.60-D0.8-L"),
    ("D2","C511707","SKY-1475-0540-45P7.6","3-14V","6mA","80dB","Active","THP","D14x8","BUZ-TH_BD14.0-P7.60-D1.0-L"),
    ("D3","C417414","FSR-1407TP-5V","1-30V","5mA","85dB","Passive","THP","D14x7.2","BUZ-TH_BD14.0-P7.60-D0.7"),
    ("D4","C255334","GSC1325YB-3V4000","1-30V","3mA","75dB","Passive","SMD","13x13x2.7","BUZ-SMD_L13.0-W13.0"),
    ("D5","C391038","FUET-1325","5V","3mA","75dB","Passive","SMD","13x13x2.5","BUZ-SMD_FST-1325"),
    ("D6","C360605","SFN-1207PA7.6","5V","5mA","80dB","Passive","THP","D12.6x7.5","BUZ-TH_BD12.6-P7.50-D0.9"),
    ("D7","C360607","SFN-12055PA6.5","5V","120mA","80dB","Passive","THP","D12.5x6","BUZ-TH_BD12.5-P6.50-D0.9"),
    ("E1","C22387765","HNR-1207PA6.5","5V","10mA","86dB","Passive","THP","D12.5x7","BUZ-TH_BD12.5-P6.50-D0.9"),
    ("E2","C360618","SFN-1207PA6.5","5V","120mA","80dB","Passive","THP","D12.5x6.8","BUZ-TH_BD12.5-P6.50-D0.9"),
    ("E3","C76871","PS1240P02BT","3V","-","70dB","Passive","THP","D12.2x6.5","BUZ-TH_BD12.5-P5.00-D0.9"),
    ("E4","C42420998","SMD-1230-0340","3V","5mA","75dB","Passive","SMD","12x12x3","BUZ-SMD_L12.0-W12.0"),
    ("E5","C49246959","SMD1230","3V","2mA","78dB","Passive","SMD","12x12x3","BUZ-SMD_L12.0-W12.0"),
    ("E6","C255333","GSC1230YB-3V4000","3V","3mA","75dB","Passive","SMD","12x12x3.3","BUZ-SMD_L12.0-W12.0_CPT-12123-81-SMT-TR"),
    ("E7","C391037","FUET-1230","3V","5mA","75dB","Passive","SMD","12x12x3.3","BUZ-SMD_L12.0-W12.0_FUET-1230"),
    ("F1","C391036","FUET-1109","5V","3mA","70dB","Passive","SMD","11x9x2","BUZ-SMD_FST-1109"),
    ("F2","C255331","GSC1031YB-3V4000","1-30V","3mA","75dB","Passive","SMD","D10x3.1","BUZ-SMD_BD10.0-P8.00-LS11.0"),
    ("F3","C255330","GSC1030RB-3V4000","3V","5mA","72dB","Passive","SMD","10x10x3.3","BUZ-SMD_L10.0-W10.0_GSC1030RB-3V4000"),
    ("F4","C417421","FUET-1030-3V","3V","5mA","75dB","Passive","SMD","D10x3.4","BUZ-SMD_FUET-1030-XXV"),
    ("F5","C49246960","SMD9650-DC3V","3V","30mA","85dB","-","SMD","9.6x9.6x5","BUZ-SMD_L9.6-W9.6-LS10.0-R"),
    ("F6","C49246961","SMD9650-DC5V","5V","30mA","80dB","-","SMD","9.6x9.6x5","BUZ-SMD_L9.6-W9.6-LS10.0-R"),
    ("F7","C49246958","SMD9018","3V","5mA","65dB","Passive","SMD","9x9x1.8","BUZ-SMD_L9.0-W9.0-P8.00-LS9.3"),
    ("G1","C20181991","CPT-9019A-SMT-TR","3V","1mA","75dB","Passive","SMD","9x9x1.9","BUZ-SMD_L9.0-W9.0_CPT-9019A-SMT-TR"),
]


def mm(x):
    return pcbnew.FromMM(x)


def point(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


def add_line(board, x1, y1, x2, y2, layer, width=0.2):
    shape = pcbnew.PCB_SHAPE(board)
    shape.SetShape(pcbnew.S_SEGMENT)
    shape.SetStart(point(x1, y1))
    shape.SetEnd(point(x2, y2))
    shape.SetLayer(layer)
    shape.SetWidth(mm(width))
    board.Add(shape)


def add_text(board, value, x, y, layer, size=1.15, thickness=0.18, justify=None):
    item = pcbnew.PCB_TEXT(board)
    item.SetText(value)
    item.SetPosition(point(x, y))
    item.SetLayer(layer)
    item.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    item.SetTextThickness(mm(thickness))
    if layer == pcbnew.B_SilkS:
        item.SetMirrored(True)
    if justify is not None:
        item.SetHorizJustify(justify)
    board.Add(item)


def add_track(board, net, x1, y1, x2, y2, layer, width=0.4):
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(point(x1, y1))
    track.SetEnd(point(x2, y2))
    track.SetLayer(layer)
    track.SetWidth(mm(width))
    track.SetNet(net)
    board.Add(track)


def add_via(board, net, x, y, diameter=1.0, drill=0.5):
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(point(x, y))
    via.SetWidth(mm(diameter))
    via.SetDrill(mm(drill))
    via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    via.SetNet(net)
    board.Add(via)


def pads_by_number(footprint, number):
    return [pad for pad in footprint.Pads() if pad.GetNumber() == str(number)]


def pad_xy(pad):
    pos = pad.GetPosition()
    return pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)


def price_line(price_data):
    if not price_data or price_data.get("error"):
        return "1pc N/A | 500pc N/A"
    one = price_data.get("qty_1_unit_usd")
    five_hundred = price_data.get("qty_500_unit_usd")
    tiers = price_data.get("price_tiers") or []
    if one is None and tiers:
        one_text = f"1pc N/A (MOQ {tiers[0]['ladder']})"
    else:
        one_text = f"1pc ${one:.4f}" if one is not None else "1pc N/A"
    five_text = f"500pc ${five_hundred:.4f}/ea" if five_hundred is not None else "500pc N/A"
    return f"{one_text} | {five_text}"


def add_standard_footprint(board, library, name, reference, value, cx, cy, center_offset=(0, 0)):
    fp = pcbnew.FootprintLoad(str(KICAD_FOOTPRINTS / f"{library}.pretty"), name)
    if fp is None:
        raise RuntimeError(f"Cannot load standard footprint: {library}:{name}")
    fp.SetReference(reference)
    fp.SetValue(value)
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    fp.SetPosition(point(cx - center_offset[0], cy - center_offset[1]))
    board.Add(fp)
    return fp


def main():
    board = pcbnew.BOARD()
    board.GetDesignSettings().SetBoardThickness(mm(1.6))
    price_path = ROOT / "lcsc_prices.json"
    prices = json.loads(price_path.read_text(encoding="utf-8"))["prices"] if price_path.exists() else {}

    left = top = 20.0
    pitch = 32.0
    right = bottom = left + 7 * pitch

    # 224 x 224 mm board outline.
    add_line(board, left, top, right, top, pcbnew.Edge_Cuts, 0.05)
    add_line(board, right, top, right, bottom, pcbnew.Edge_Cuts, 0.05)
    add_line(board, right, bottom, left, bottom, pcbnew.Edge_Cuts, 0.05)
    add_line(board, left, bottom, left, top, pcbnew.Edge_Cuts, 0.05)

    # Front-silkscreen cell grid.
    for i in range(1, 7):
        add_line(board, left + i * pitch, top + 0.5, left + i * pitch, bottom - 0.5, pcbnew.F_SilkS)
        add_line(board, left + 0.5, top + i * pitch, right - 0.5, top + i * pitch, pcbnew.F_SilkS)

    rows = {c: i for i, c in enumerate("ABCDEFG")}
    for index, part in enumerate(PARTS, 1):
        cell, lcsc, mpn, voltage, current, spl, driver, mount, body, footprint_name = part
        row = rows[cell[0]]
        col = int(cell[1]) - 1
        cx = left + (col + 0.5) * pitch
        cy = top + (row + 0.5) * pitch

        fp = pcbnew.FootprintLoad(str(LIB), footprint_name)
        if fp is None:
            raise RuntimeError(f"Cannot load footprint: {footprint_name}")
        fp.SetReference(f"BZ{index}")
        fp.SetValue(mpn)
        fp.SetPosition(point(cx, cy))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)
        if fp.HasFieldByName("LCSC Part"):
            fp.GetFieldByName("LCSC Part").SetText(lcsc)
        for graphic in list(fp.GraphicalItems()):
            if graphic.GetLayer() in (pcbnew.F_CrtYd, pcbnew.B_CrtYd):
                fp.Remove(graphic)
            elif lcsc == "C511707" and graphic.GetLayer() == pcbnew.F_SilkS and isinstance(graphic, pcbnew.PCB_SHAPE) and graphic.GetShape() == pcbnew.S_SEGMENT:
                fp.Remove(graphic)
            elif lcsc == "C530420" and graphic.GetLayer() == pcbnew.F_SilkS and hasattr(graphic, "GetText") and graphic.GetText() == "+":
                fp.Remove(graphic)
        source_models = list(fp.Models())
        fp.Models().clear()
        for model in source_models:
            model_name = Path(model.m_Filename).stem
            step_path = ROOT / "piezo_footprints.3dshapes" / f"{model_name}.step"
            wrl_path = ROOT / "piezo_footprints.3dshapes" / f"{model_name}.wrl"
            linked_model = pcbnew.FP_3DMODEL()
            linked_model.m_Offset = model.m_Offset
            linked_model.m_Rotation = model.m_Rotation
            linked_model.m_Scale = model.m_Scale
            linked_model.m_Opacity = model.m_Opacity
            linked_model.m_Show = model.m_Show
            if step_path.exists():
                linked_model.m_Filename = f"${{KIPRJMOD}}/piezo_footprints.3dshapes/{model_name}.step"
            elif wrl_path.exists():
                linked_model.m_Filename = f"${{KIPRJMOD}}/piezo_footprints.3dshapes/{model_name}.wrl"
            else:
                linked_model.m_Filename = f"${{KIPRJMOD}}/piezo_footprints.3dshapes/{model_name}.step"
            fp.Add3DModel(linked_model)
        board.Add(fp)

        # Front cell ID stays clear of the body; full data is on the back.
        add_text(board, cell, left + col * pitch + 2.0, top + row * pitch + 2.0,
                 pcbnew.F_SilkS, 1.0, justify=pcbnew.GR_TEXT_H_ALIGN_LEFT)
        mpn_y = cy - 5.5 if row == 0 else top + row * pitch + 5.0
        add_text(board, mpn, cx, mpn_y, pcbnew.F_SilkS, 0.9, 0.15)

        add_text(board, f"{cell}  {mpn}", cx, cy - 12.0, pcbnew.B_SilkS, 1.05)
        add_text(board, lcsc, cx, cy - 9.0, pcbnew.B_SilkS, 1.05)
        add_text(board, price_line(prices.get(lcsc)), cx, cy + 6.0, pcbnew.B_SilkS, 0.8, 0.13)
        add_text(board, f"{voltage} | {current} | {spl}", cx, cy + 9.0, pcbnew.B_SilkS, 1.05)
        add_text(board, f"{driver} | {mount} | {body} mm", cx, cy + 12.0, pcbnew.B_SilkS, 0.95)

    # Controls occupy the remaining bottom-row cells.
    for col in range(1, 7):
        cell = f"G{col + 1}"
        add_text(board, cell, left + col * pitch + 2.0, top + 6 * pitch + 2.0,
                 pcbnew.F_SilkS, 1.0, justify=pcbnew.GR_TEXT_H_ALIGN_LEFT)

    button_defs = []
    for index, label in enumerate("ABCDEFG"):
        x = 60 + index * 16
        button_defs.append((f"SW{index + 1}", f"ROW {label}", x, 223, x, 216.5))
    for index in range(7):
        x = 60 + index * 16
        button_defs.append((f"SW{index + 8}", f"COL {index + 1}", x, 235, x, 241.0))
    for reference, label, cx, cy, tx, ty in button_defs:
        switch = add_standard_footprint(
            board, "Button_Switch_SMD", "SW_Push_1P1T_XKB_TS-1187A", reference,
            "LCK-TA022H18-2WL", cx, cy
        )
        switch.Models().clear()
        switch_model = pcbnew.FP_3DMODEL()
        switch_model.m_Filename = "${KIPRJMOD}/piezo_footprints.3dshapes/SW_Push_1P1T_XKB_TS-1187A.wrl"
        switch.Add3DModel(switch_model)
        add_text(board, label, tx, ty, pcbnew.F_SilkS, 0.8, 0.13)

    bnc = add_standard_footprint(
        board, "Connector_Coaxial", "BNC_TEConnectivity_1478204_Vertical",
        "J1", "1-1478204-0", 196, 228
    )
    bnc.Models().clear()
    bnc_model = pcbnew.FP_3DMODEL()
    bnc_model.m_Filename = "${KIPRJMOD}/piezo_footprints.3dshapes/BNC_TEConnectivity_1478204_Vertical.wrl"
    bnc.Add3DModel(bnc_model)
    add_text(board, "BNC INPUT", 196, 216.0, pcbnew.F_SilkS, 1.1, 0.18)
    add_text(board, "DIRECT MATRIX", 228, 225.0, pcbnew.F_SilkS, 1.25, 0.20)
    add_text(board, "PRESS 1 ROW + 1 COL", 228, 231.0, pcbnew.F_SilkS, 0.80, 0.13)

    add_text(board, "ROW SELECT A-G", 84, 228, pcbnew.B_SilkS, 1.15, 0.18)
    add_text(board, "COLUMN SELECT 1-7", 148, 228, pcbnew.B_SilkS, 1.15, 0.18)
    add_text(board, "J1 FUNCTION GENERATOR", 196, 239, pcbnew.B_SilkS, 0.95, 0.15)
    add_text(board, "DIRECT SWITCH MATRIX", 228, 225, pcbnew.B_SilkS, 0.86, 0.15)
    add_text(board, "PRESS 1 ROW + 1 COL", 228, 231, pcbnew.B_SilkS, 0.80, 0.13)

    # Electrical nets match the schematic exactly.
    net_names = ["BNC_SIGNAL", "BNC_RETURN"]
    net_names += [f"ROW_{letter}" for letter in "ABCDEFG"]
    net_names += [f"COL_{index}" for index in range(1, 8)]
    nets = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net

    # Assign every footprint pad to its schematic net.
    for index, part in enumerate(PARTS, 1):
        cell = part[0]
        footprint = board.FindFootprintByReference(f"BZ{index}")
        for pad in pads_by_number(footprint, 1):
            pad.SetNet(nets[f"ROW_{cell[0]}"])
        for pad in pads_by_number(footprint, 2):
            pad.SetNet(nets[f"COL_{cell[1]}"])

    for index, letter in enumerate("ABCDEFG", 1):
        footprint = board.FindFootprintByReference(f"SW{index}")
        for pad in pads_by_number(footprint, 1):
            pad.SetNet(nets["BNC_SIGNAL"])
        for pad in pads_by_number(footprint, 2):
            pad.SetNet(nets[f"ROW_{letter}"])

    for column in range(1, 8):
        footprint = board.FindFootprintByReference(f"SW{column + 7}")
        for pad in pads_by_number(footprint, 1):
            pad.SetNet(nets[f"COL_{column}"])
        for pad in pads_by_number(footprint, 2):
            pad.SetNet(nets["BNC_RETURN"])

    for pad in pads_by_number(bnc, 1):
        pad.SetNet(nets["BNC_SIGNAL"])
    for pad in pads_by_number(bnc, 2):
        pad.SetNet(nets["BNC_RETURN"])

    # Row buses use front copper. Rows A-F transition to ordered back-copper
    # trunks at the left edge; G1 routes directly beneath its SMD footprint.
    for row, letter in enumerate("ABCDEF"):
        net = nets[f"ROW_{letter}"]
        bus_y = 25.0 + row * pitch
        trunk_x = 22.0 + row * 1.4
        row_parts = [(index, part) for index, part in enumerate(PARTS, 1) if part[0][0] == letter]
        escapes = []
        for index, part in row_parts:
            footprint = board.FindFootprintByReference(f"BZ{index}")
            pad1 = pads_by_number(footprint, 1)[0]
            pad2 = pads_by_number(footprint, 2)[0]
            x1, y1 = pad_xy(pad1)
            x2, _ = pad_xy(pad2)
            column = int(part[0][1]) - 1
            escape_x = left + column * pitch + (28.0 if x1 > x2 else 4.0)
            escapes.append(escape_x)
            add_track(board, net, x1, y1, escape_x, y1, pcbnew.F_Cu)
            add_track(board, net, escape_x, y1, escape_x, bus_y, pcbnew.F_Cu)
        add_track(board, net, min(trunk_x, min(escapes)), bus_y, max(escapes), bus_y, pcbnew.F_Cu)
        add_via(board, net, trunk_x, bus_y)
        add_track(board, net, trunk_x, bus_y, trunk_x, 200.0, pcbnew.B_Cu)
        add_via(board, net, trunk_x, 200.0, 0.6, 0.3)

        switch = board.FindFootprintByReference(f"SW{row + 1}")
        pad2s = pads_by_number(switch, 2)
        left_x, target_y = pad_xy(min(pad2s, key=lambda pad: pad.GetPosition().x))
        right_x, _ = pad_xy(max(pad2s, key=lambda pad: pad.GetPosition().x))
        launch_x = 33.0 + row * 3.0
        launch_y = 212.0 - row * 0.5
        add_track(board, net, trunk_x, 200.0, launch_x, launch_y, pcbnew.F_Cu, 0.3)
        add_via(board, net, launch_x, launch_y, 0.6, 0.3)
        add_track(board, net, launch_x, launch_y, left_x, target_y, pcbnew.B_Cu, 0.3)
        add_via(board, net, left_x, target_y)
        add_track(board, net, left_x, target_y, right_x, target_y, pcbnew.F_Cu, 0.3)

    row_g = nets["ROW_G"]
    bz43_pad1 = pads_by_number(board.FindFootprintByReference("BZ43"), 1)[0]
    g_x, g_y = pad_xy(bz43_pad1)
    add_via(board, row_g, g_x, g_y)
    sw7_pad2s = pads_by_number(board.FindFootprintByReference("SW7"), 2)
    sw7_left_x, sw7_y = pad_xy(min(sw7_pad2s, key=lambda pad: pad.GetPosition().x))
    sw7_right_x, _ = pad_xy(max(sw7_pad2s, key=lambda pad: pad.GetPosition().x))
    add_track(board, row_g, g_x, g_y, g_x, 225.75, pcbnew.B_Cu, 0.3)
    add_track(board, row_g, g_x, 225.75, sw7_left_x, 225.75, pcbnew.B_Cu, 0.3)
    add_track(board, row_g, sw7_left_x, 225.75, sw7_left_x, sw7_y, pcbnew.B_Cu, 0.3)
    add_via(board, row_g, sw7_left_x, sw7_y)
    add_track(board, row_g, sw7_left_x, sw7_y, sw7_right_x, sw7_y, pcbnew.F_Cu, 0.3)

    # Column buses use back copper through rows A-F. Each then changes to front
    # copper outside the switch bank, drops below it, and fans back to its button.
    column_shift_x = {2: 165.0, 3: 170.0, 4: 175.0}
    column_shift_y = {2: 214.0, 3: 213.0, 4: 212.0}
    column_return_y = {2: 226.0, 3: 227.0, 4: 228.0}
    for column in range(1, 8):
        net = nets[f"COL_{column}"]
        bus_x = 49.0 + (column - 1) * pitch
        add_track(board, net, bus_x, 36.0, bus_x, 202.0, pcbnew.B_Cu)
        for index, part in enumerate(PARTS, 1):
            if int(part[0][1]) != column or part[0][0] == "G":
                continue
            pad = pads_by_number(board.FindFootprintByReference(f"BZ{index}"), 2)[0]
            x, y = pad_xy(pad)
            if pad.GetAttribute() == pcbnew.PAD_ATTRIB_SMD:
                add_via(board, net, x, y)
            add_track(board, net, x, y, bus_x, y, pcbnew.B_Cu)

        add_via(board, net, bus_x, 202.0)
        bottom_x = bus_x
        if column in column_shift_y:
            shift_y = column_shift_y[column]
            shift_x = column_shift_x[column]
            return_y = column_return_y[column]
            add_track(board, net, bus_x, 202.0, bus_x, shift_y, pcbnew.F_Cu, 0.3)
            add_track(board, net, bus_x, shift_y, shift_x, shift_y, pcbnew.F_Cu, 0.3)
            add_track(board, net, shift_x, shift_y, shift_x, return_y, pcbnew.F_Cu, 0.3)
            add_track(board, net, shift_x, return_y, bus_x, return_y, pcbnew.F_Cu, 0.3)
            add_track(board, net, bus_x, return_y, bus_x, 230.0, pcbnew.F_Cu, 0.3)
        else:
            add_track(board, net, bus_x, 202.0, bottom_x, 230.0, pcbnew.F_Cu, 0.3)
        add_via(board, net, bottom_x, 230.0)

        switch = board.FindFootprintByReference(f"SW{column + 7}")
        pad1s = pads_by_number(switch, 1)
        left_x, target_y = pad_xy(min(pad1s, key=lambda pad: pad.GetPosition().x))
        right_x, _ = pad_xy(max(pad1s, key=lambda pad: pad.GetPosition().x))
        if column <= 5:
            add_track(board, net, bottom_x, 230.0, left_x, target_y, pcbnew.B_Cu, 0.3)
        elif column == 6:
            add_track(board, net, bottom_x, 230.0, bottom_x, 240.5, pcbnew.B_Cu, 0.3)
            add_track(board, net, bottom_x, 240.5, 160.0, 240.5, pcbnew.B_Cu, 0.3)
            add_via(board, net, 160.0, 240.5)
            add_track(board, net, 160.0, 240.5, left_x, 240.5, pcbnew.F_Cu, 0.3)
            add_via(board, net, left_x, 240.5)
            add_track(board, net, left_x, 240.5, left_x, target_y, pcbnew.B_Cu, 0.3)
        else:
            add_track(board, net, bottom_x, 230.0, bottom_x, 242.0, pcbnew.B_Cu, 0.3)
            add_track(board, net, bottom_x, 242.0, left_x, 242.0, pcbnew.B_Cu, 0.3)
            add_track(board, net, left_x, 242.0, left_x, target_y, pcbnew.B_Cu, 0.3)
        add_via(board, net, left_x, target_y)
        add_track(board, net, left_x, target_y, right_x, target_y, pcbnew.F_Cu, 0.3)

    # G1 joins column 1 directly in the control region.
    col1 = nets["COL_1"]
    bz43_pad2 = pads_by_number(board.FindFootprintByReference("BZ43"), 2)[0]
    g2_x, g2_y = pad_xy(bz43_pad2)
    add_via(board, col1, g2_x, g2_y)
    add_track(board, col1, g2_x, g2_y, 57.0, 233.125, pcbnew.B_Cu, 0.3)

    # BNC signal ties all row-switch inputs together on the front layer.
    signal = nets["BNC_SIGNAL"]
    add_track(board, signal, 57.0, 221.125, 159.0, 221.125, pcbnew.F_Cu)
    add_via(board, signal, 159.0, 221.125)
    add_track(board, signal, 196.0, 228.0, 159.0, 221.125, pcbnew.B_Cu, 0.3)

    # BNC return ties all column-switch returns together on the front layer.
    return_net = nets["BNC_RETURN"]
    add_track(board, return_net, 57.0, 236.875, 159.0, 236.875, pcbnew.F_Cu)
    for column in range(1, 8):
        right_x = 63.0 + (column - 1) * 16.0
        left_x = right_x - 6.0
        add_track(board, return_net, left_x, 236.875, right_x, 236.875, pcbnew.F_Cu, 0.3)
    # Join all four mechanical shield pads, then escape below the connector.
    add_track(board, return_net, 192.825, 224.825, 199.175, 224.825, pcbnew.F_Cu)
    add_track(board, return_net, 199.175, 224.825, 199.175, 231.175, pcbnew.F_Cu)
    add_track(board, return_net, 199.175, 231.175, 192.825, 231.175, pcbnew.F_Cu)
    add_track(board, return_net, 192.825, 231.175, 192.825, 224.825, pcbnew.F_Cu)
    add_track(board, return_net, 192.825, 231.175, 192.825, 239.0, pcbnew.F_Cu)
    add_track(board, return_net, 192.825, 239.0, 159.0, 239.0, pcbnew.F_Cu)
    add_track(board, return_net, 159.0, 239.0, 159.0, 236.875, pcbnew.F_Cu)

    board.BuildListOfNets()

    pcbnew.SaveBoard(str(BOARD_PATH), board)

    with (ROOT / "Piezo_Demo_7x7_BOM.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Reference","Cell","LCSC","MPN","Voltage","Current","SPL","Driver","Mount","Body_mm","Qty1_USD_each","Qty500_USD_each","Footprint"])
        for index, part in enumerate(PARTS, 1):
            cell, lcsc, mpn, voltage, current, spl, driver, mount, body, footprint_name = part
            price = prices.get(lcsc, {})
            writer.writerow([f"BZ{index}",cell,lcsc,mpn,voltage,current,spl,driver,mount,body,price.get("qty_1_unit_usd"),price.get("qty_500_unit_usd"),footprint_name])

    with (ROOT / "Piezo_Demo_7x7_Controls_BOM.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["References", "Quantity", "Description", "Value", "Footprint"])
        writer.writerow(["SW1-SW14", 14, "MouseMinder SMD tactile button", "LCK-TA022H18-2WL / C51978285", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A"])
        writer.writerow(["J1", 1, "Vertical PCB BNC connector", "TE 1-1478204-0", "Connector_Coaxial:BNC_TEConnectivity_1478204_Vertical"])

    (ROOT / "Piezo_Demo_7x7.kicad_pro").write_text(json.dumps({"board": {}, "meta": {"filename": "Piezo_Demo_7x7.kicad_pro", "version": 1}}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
