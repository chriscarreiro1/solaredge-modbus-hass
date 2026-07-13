#!/usr/bin/env python3
"""Build a signed Apple Wallet .pkpass access badge from config.yaml."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path

import yaml

from generate_assets import generate_all

ROOT = Path(__file__).resolve().parent


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def build_pass_json(config: dict) -> dict:
    p = config["pass"]
    badge = config["badge"]
    contact = config.get("contact", {})
    app = config.get("associated_app", {})
    style = p.get("style", "storeCard")

    pass_doc: dict = {
        "formatVersion": 1,
        "passTypeIdentifier": p["pass_type_identifier"],
        "serialNumber": str(uuid.uuid4()),
        "teamIdentifier": p["team_identifier"],
        "organizationName": p["organization_name"],
        "description": p["description"],
        "logoText": p["logo_text"],
        "foregroundColor": p["foreground_color"],
        "backgroundColor": p["background_color"],
        "labelColor": p["label_color"],
        "barcodes": [
            {
                "format": badge.get("barcode_format", "PKBarcodeFormatQR"),
                "message": badge.get("barcode_message", badge["id"]),
                "messageEncoding": "iso-8859-1",
                "altText": badge["id"],
            }
        ],
    }

    back_fields: list[dict] = []
    if contact.get("phone"):
        back_fields.append({"key": "phone", "label": "", "value": contact["phone"]})
    if contact.get("website"):
        back_fields.append({"key": "website", "label": "", "value": contact["website"]})
    back_fields.extend(
        [
            {"key": "guest_name", "label": "Guest Name", "value": badge["guest_name"]},
            {"key": "affiliation", "label": "Affiliation", "value": badge["affiliation"]},
            {"key": "badge_id", "label": "ID", "value": badge["id"]},
        ]
    )

    if style == "storeCard":
        # Strip image fills the pass front (Millennium Falcon artwork + name footer).
        pass_doc["storeCard"] = {
            "primaryFields": [],
            "secondaryFields": [],
            "backFields": back_fields,
        }
    else:
        pass_doc["generic"] = {
            "primaryFields": [
                {"key": "title", "label": "", "value": p["logo_text"]},
            ],
            "secondaryFields": [
                {"key": "subtitle", "label": "", "value": p["description"]},
            ],
            "backFields": back_fields,
        }

    if app.get("store_identifier"):
        pass_doc["associatedStoreIdentifiers"] = [int(app["store_identifier"])]
    if app.get("launch_url"):
        pass_doc["appLaunchURL"] = app["launch_url"]

    if config.get("locations"):
        pass_doc["locations"] = config["locations"]

    return pass_doc


def write_manifest(work_dir: Path) -> None:
    """SHA-1 manifest of every file except manifest.json and signature."""
    manifest: dict[str, str] = {}
    for path in sorted(work_dir.iterdir()):
        if path.name in ("manifest.json", "signature") or path.is_dir():
            continue
        digest = hashlib.sha1(path.read_bytes()).hexdigest()
        manifest[path.name] = digest
    (work_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def sign_manifest(work_dir: Path, signing: dict) -> None:
    cert = ROOT / signing["certificate"]
    key = ROOT / signing["private_key"]
    wwdr = ROOT / signing["wwdr_certificate"]
    missing = [p for p in (cert, key, wwdr) if not p.exists()]
    if missing:
        names = ", ".join(str(p.relative_to(ROOT)) for p in missing)
        raise FileNotFoundError(
            f"Signing certificates not found: {names}\n"
            "See README.md for Apple Developer certificate setup."
        )

    signature_path = work_dir / "signature"
    cmd = [
        "openssl",
        "smime",
        "-binary",
        "-sign",
        "-certfile",
        str(wwdr),
        "-signer",
        str(cert),
        "-inkey",
        str(key),
        "-in",
        str(work_dir / "manifest.json"),
        "-out",
        str(signature_path),
        "-outform",
        "DER",
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def overlay_custom_assets(assets_dir: Path, work_dir: Path) -> None:
    if not assets_dir.is_dir():
        return
    for png in assets_dir.glob("*.png"):
        shutil.copy2(png, work_dir / png.name)


def create_pkpass(work_dir: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(work_dir.iterdir()):
            if path.is_file():
                zf.write(path, arcname=path.name)


def build(config_path: Path | None = None, unsigned: bool = False) -> Path:
    config = load_config(config_path or ROOT / "config.yaml")
    output = ROOT / config.get("output", "AccessBadge.pkpass")

    with tempfile.TemporaryDirectory(prefix="pkpass-") as tmp:
        work_dir = Path(tmp)

        assets_dir = ROOT / "assets"
        generate_all(
            work_dir,
            guest_name=config["badge"]["guest_name"],
            logo_text=config["pass"]["logo_text"],
        )
        overlay_custom_assets(assets_dir, work_dir)

        pass_json = build_pass_json(config)
        (work_dir / "pass.json").write_text(
            json.dumps(pass_json, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        write_manifest(work_dir)

        if not unsigned:
            try:
                sign_manifest(work_dir, config["signing"])
            except FileNotFoundError as exc:
                print(f"Warning: {exc}", file=sys.stderr)
                print("Building UNSIGNED package (will NOT install on iPhone).", file=sys.stderr)
        else:
            print(
                "Skipping signature (--unsigned). Package will NOT install on iPhone.",
                file=sys.stderr,
            )

        create_pkpass(work_dir, output)

    return output


def main() -> None:
    unsigned = "--unsigned" in sys.argv
    config_arg = next((a for a in sys.argv[1:] if not a.startswith("-")), None)
    config_path = Path(config_arg) if config_arg else ROOT / "config.yaml"

    output = build(config_path, unsigned=unsigned)
    print(f"Created: {output}")
    print(f"Size:    {output.stat().st_size:,} bytes")
    if unsigned or not all(
        (ROOT / p).exists()
        for p in (
            "certs/pass.pem",
            "certs/pass.key",
            "certs/wwdr.pem",
        )
    ):
        print("\nTo install on iPhone you must sign with Apple Developer certificates.")
        print("See wallet-access-badge/README.md for setup instructions.")


if __name__ == "__main__":
  main()
