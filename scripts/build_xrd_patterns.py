#!/usr/bin/env python3
"""Build open reference powder patterns from COD CIFs.

The two phases are:
  - Si, COD 9008565 (Wyckoff 1963; AMCSD 0011243)
  - rutile TiO2, COD 9004141 (Meagher & Lager 1979; AMCSD 0005164)

The calculation is kinematic and uses Cu K-alpha1 (1.5406 A):
  I_rel ~ multiplicity * Lorentz-polarization * |F(hkl)|^2
It does not include instrumental broadening, preferred orientation, absorption,
or thermal diffuse scattering. The output is a schematic/reference pattern,
not a measured diffractogram.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import gemmi

ROOT = Path(__file__).resolve().parents[1]
CIF_DIR = ROOT / "chapters" / "s01" / "assets" / "cif"
OUT_JSON = ROOT / "chapters" / "s01" / "assets" / "xrd_patterns.json"
OUT_TXT = ROOT / "chapters" / "s01" / "assets" / "xrd_patterns.txt"

WAVELENGTH = 1.5406  # Cu K-alpha1, angstrom
TWO_THETA_MIN = 10.0
TWO_THETA_MAX = 100.0
D_MIN = 0.8

PHASES = [
    {
        "id": "Si",
        "name": "单晶硅",
        "formula": "Si",
        "cif": CIF_DIR / "Si_9008565.cif",
        "cod_id": "9008565",
        "source": "COD 9008565; original data from AMCSD 0011243; Wyckoff, Crystal Structures (1963)",
    },
    {
        "id": "rutile",
        "name": "金红石型二氧化钛",
        "formula": "TiO2",
        "cif": CIF_DIR / "Rutile_9004141.cif",
        "cod_id": "9004141",
        "source": "COD 9004141; original data from AMCSD 0005164; Meagher & Lager, Can. Mineral. 17 (1979) 77-85, 25 C",
    },
]


def lorenz_polarization(two_theta_deg: float) -> float:
    theta = math.radians(two_theta_deg / 2.0)
    return (1.0 + math.cos(2.0 * theta) ** 2) / (math.sin(theta) ** 2 * math.cos(theta))


def powder_peaks(cif_path: Path) -> tuple[dict, list[dict]]:
    st = gemmi.read_small_structure(str(cif_path))
    cell = st.cell
    calc = gemmi.StructureFactorCalculatorX(cell)
    sym_ops = st.spacegroup.operations().sym_ops

    raw: list[dict] = []
    for h in range(0, 11):
        for k in range(0, 11):
            for l in range(0, 11):
                if h == k == l == 0:
                    continue
                d = cell.calculate_d([h, k, l])
                if d < D_MIN:
                    continue
                sin_theta = WAVELENGTH / (2.0 * d)
                if sin_theta >= 1.0:
                    continue
                two_theta = 2.0 * math.degrees(math.asin(sin_theta))
                if not (TWO_THETA_MIN <= two_theta <= TWO_THETA_MAX):
                    continue

                equivalents = {tuple(op.apply_to_hkl([h, k, l])) for op in sym_ops}
                multiplicity = len(equivalents)
                sf = calc.calculate_sf_from_small_structure(st, [h, k, l])
                intensity = multiplicity * lorenz_polarization(two_theta) * abs(sf) ** 2
                if intensity <= 1e-8:
                    continue
                raw.append(
                    {
                        "two_theta": two_theta,
                        "h": h,
                        "k": k,
                        "l": l,
                        "d": d,
                        "multiplicity": multiplicity,
                        "intensity_raw": intensity,
                    }
                )

    raw.sort(key=lambda p: p["two_theta"])
    groups: list[list[dict]] = []
    for peak in raw:
        if groups and abs(peak["two_theta"] - groups[-1][0]["two_theta"]) < 0.03:
            groups[-1].append(peak)
        else:
            groups.append([peak])

    peaks: list[dict] = []
    for group in groups:
        best = max(group, key=lambda p: p["intensity_raw"])
        peaks.append(best)

    max_intensity = max((p["intensity_raw"] for p in peaks), default=1.0)
    for peak in peaks:
        peak["intensity"] = round(100.0 * peak["intensity_raw"] / max_intensity, 1)
        peak["two_theta"] = round(peak["two_theta"], 2)
        peak["d"] = round(peak["d"], 4)
        peak["hkl"] = f"{peak['h']}{peak['k']}{peak['l']}"
        del peak["h"], peak["k"], peak["l"], peak["intensity_raw"]

    cell_info = {
        "a": round(cell.a, 4),
        "b": round(cell.b, 4),
        "c": round(cell.c, 4),
        "alpha": round(cell.alpha, 3),
        "beta": round(cell.beta, 3),
        "gamma": round(cell.gamma, 3),
        "volume": round(cell.volume, 3),
        "spacegroup": st.spacegroup_hm,
        "spacegroup_number": st.spacegroup_number,
    }
    return cell_info, peaks


def main() -> int:
    result = {
        "generated_by": "scripts/build_xrd_patterns.py",
        "method": "kinematic powder XRD; Cu K-alpha1 1.5406 A; I_rel ~ multiplicity * LP * |F|^2",
        "caveats": [
            "No instrumental broadening, preferred orientation, absorption, or thermal diffuse scattering.",
            "Calculated reference pattern for science communication; not a measured diffractogram.",
            "Relative intensities are normalized per phase and are not quantitative phase fractions.",
        ],
        "license_note": "COD entries are used with attribution to the original articles; see docs/assets_and_licenses.md.",
        "phases": [],
    }

    lines = [
        "Open calculated powder patterns (Cu K-alpha1 = 1.5406 A)",
        "Kinematic approximation; no instrument broadening / preferred orientation.",
        "",
    ]
    for phase in PHASES:
        cell, peaks = powder_peaks(phase["cif"])
        item = {k: v for k, v in phase.items() if k != "cif"}
        item["cell"] = cell
        item["peaks"] = peaks
        result["phases"].append(item)

        lines.append(f"[{phase['id']}] {phase['name']} ({phase['formula']}) COD {phase['cod_id']}")
        lines.append(f"  space group: {cell['spacegroup']} (#{cell['spacegroup_number']})")
        lines.append(f"  cell: a={cell['a']} b={cell['b']} c={cell['c']} alpha={cell['alpha']} beta={cell['beta']} gamma={cell['gamma']}")
        lines.append("  2theta(deg)  hkl    d(A)   I_rel")
        for p in peaks:
            lines.append(f"  {p['two_theta']:8.2f}   {p['hkl']:<6} {p['d']:6.4f}  {p['intensity']:5.1f}")
        lines.append("")

    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_TXT}")
    for item in result["phases"]:
        print(f"  {item['id']}: {len(item['peaks'])} peaks; strongest {item['peaks'][0]['two_theta']} deg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
