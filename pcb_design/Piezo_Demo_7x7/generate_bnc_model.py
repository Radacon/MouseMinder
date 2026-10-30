from math import cos, pi, sin
from pathlib import Path


OUT = Path(__file__).resolve().parent / "piezo_footprints.3dshapes" / "BNC_TEConnectivity_1478204_Vertical.wrl"
SW_OUT = Path(__file__).resolve().parent / "piezo_footprints.3dshapes" / "SW_Push_1P1T_XKB_TS-1187A.wrl"


def cylinder(radius, z0, z1, color, sides=32):
    points = []
    for z in (z0, z1):
        for i in range(sides):
            a = 2 * pi * i / sides
            points.append((radius * cos(a), radius * sin(a), z))
    faces = []
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((i, j, sides + j, sides + i))
    faces.append(tuple(range(sides - 1, -1, -1)))
    faces.append(tuple(sides + i for i in range(sides)))
    point_text = ",\n".join(f"          {x:.6f} {y:.6f} {z:.6f}" for x, y, z in points)
    face_text = ",\n".join("          " + ", ".join(map(str, face)) + ", -1" for face in faces)
    return f"""Shape {{
  appearance Appearance {{ material Material {{ diffuseColor {color} specularColor 0.85 0.85 0.85 shininess 0.75 }} }}
  geometry IndexedFaceSet {{
    solid TRUE
    creaseAngle 0.8
    coord Coordinate {{ point [
{point_text}
    ] }}
    coordIndex [
{face_text}
    ]
  }}
}}"""


def box(x, y, z, sx, sy, sz, color):
    return f"""Transform {{ translation {x} {y} {z} children [ Shape {{
  appearance Appearance {{ material Material {{ diffuseColor {color} specularColor 0.55 0.55 0.55 shininess 0.45 }} }}
  geometry Box {{ size {sx} {sy} {sz} }}
}} ] }}"""


parts = [
    cylinder(2.15, 0.00, 1.00, "0.65 0.67 0.70"),
    cylinder(1.75, 0.90, 6.10, "0.65 0.67 0.70"),
    cylinder(2.15, 5.80, 7.00, "0.65 0.67 0.70"),
    cylinder(1.72, 6.90, 9.30, "0.65 0.67 0.70"),
    cylinder(1.15, 9.30, 9.38, "0.05 0.05 0.05"),
    """Transform { translation 2.35 0 6.40 children [ Shape {
      appearance Appearance { material Material { diffuseColor 0.65 0.67 0.70 } }
      geometry Box { size 0.75 1.10 0.75 }
    } ] }""",
    """Transform { translation -2.35 0 6.40 children [ Shape {
      appearance Appearance { material Material { diffuseColor 0.65 0.67 0.70 } }
      geometry Box { size 0.75 1.10 0.75 }
    } ] }""",
]

OUT.write_text("#VRML V2.0 utf8\n# Simplified TE 1-1478204-0 preview model. Units: 0.1 inch.\n\n" + "\n\n".join(parts) + "\n", encoding="ascii")

switch_parts = [
    box(0, 0, 0.28, 2.05, 1.85, 0.56, "0.72 0.72 0.68"),
    box(0, 0, 0.67, 1.70, 1.55, 0.26, "0.18 0.18 0.18"),
    cylinder(0.39, 0.80, 1.05, "0.08 0.08 0.08", sides=24),
]
for x in (-1.18, 1.18):
    for y in (-0.74, 0.74):
        switch_parts.append(box(x, y, 0.09, 0.64, 0.30, 0.18, "0.78 0.78 0.72"))
SW_OUT.write_text("#VRML V2.0 utf8\n# Simplified XKB TS-1187A preview model. Units: 0.1 inch.\n\n" + "\n\n".join(switch_parts) + "\n", encoding="ascii")
