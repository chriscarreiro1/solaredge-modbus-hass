"""Generate a browser mock of the Wallet pass front + info screen."""

from __future__ import annotations

import base64
import html
from pathlib import Path


def _data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def write_preview(config: dict, assets_dir: Path, output: Path) -> Path:
    badge = config["badge"]
    p = config["pass"]
    contact = config.get("contact", {})
    app = config.get("associated_app", {})

    strip = _data_uri(assets_dir / "strip@2x.png") or _data_uri(assets_dir / "strip.png")
    thumb = _data_uri(assets_dir / "thumbnail@2x.png") or _data_uri(assets_dir / "thumbnail.png")

    guest = html.escape(badge["guest_name"])
    affiliation = html.escape(badge["affiliation"])
    badge_id = html.escape(badge["id"])
    title = html.escape(p["logo_text"])
    subtitle = html.escape(p["description"])
    org = html.escape(p["organization_name"])
    bg = html.escape(p.get("background_color", "rgb(14, 22, 52)"))
    phone = html.escape(contact.get("phone", ""))
    website = html.escape(contact.get("website", ""))
    app_name = "My Disney Experience" if app.get("store_identifier") else ""

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Wallet preview — {title}</title>
<style>
  :root {{
    --bg: {bg};
    --card: #1c1c1e;
    --label: #aeaeb2;
    --text: #ffffff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
    background: #0a0a0a;
    color: var(--text);
    min-height: 100vh;
    padding: 28px 16px 48px;
  }}
  h1 {{
    text-align: center;
    font-size: 15px;
    font-weight: 600;
    color: #8e8e93;
    margin: 0 0 24px;
  }}
  .stage {{
    display: flex;
    flex-wrap: wrap;
    gap: 28px;
    justify-content: center;
    align-items: flex-start;
  }}
  .col {{
    width: min(100%, 340px);
  }}
  .col h2 {{
    font-size: 13px;
    font-weight: 600;
    color: #8e8e93;
    text-align: center;
    margin: 0 0 12px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }}
  .phone {{
    background: #111;
    border: 1px solid #2c2c2e;
    border-radius: 36px;
    padding: 18px 14px 22px;
    box-shadow: 0 20px 50px rgba(0,0,0,.55);
  }}
  .pass-front {{
    background: var(--bg);
    border-radius: 14px;
    overflow: hidden;
    aspect-ratio: 375 / 480;
    display: flex;
    flex-direction: column;
  }}
  .pass-front .strip {{
    width: 100%;
    display: block;
  }}
  .pass-front .barcode-area {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #0b1228;
  }}
  .qr {{
    width: 150px;
    height: 150px;
    background:
      linear-gradient(#fff,#fff) center/66% 66% no-repeat,
      repeating-conic-gradient(#111 0% 25%, #fff 0% 50%) 0 0 / 12px 12px;
    border-radius: 8px;
    border: 10px solid #fff;
  }}
  .info {{
    background: #000;
    border-radius: 14px;
    padding: 18px 16px 22px;
    min-height: 520px;
  }}
  .info .thumb {{
    width: 72px;
    height: 72px;
    border-radius: 10px;
    object-fit: cover;
    display: block;
    margin: 0 auto 14px;
  }}
  .info .title {{
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    margin: 0 0 4px;
  }}
  .info .subtitle {{
    text-align: center;
    color: var(--label);
    font-size: 15px;
    margin: 0 0 16px;
  }}
  .actions {{
    display: flex;
    justify-content: center;
    gap: 18px;
    margin-bottom: 18px;
  }}
  .actions span {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #2c2c2e;
    display: grid;
    place-items: center;
    font-size: 18px;
  }}
  .card {{
    background: #1c1c1e;
    border-radius: 12px;
    padding: 12px 14px;
    margin-bottom: 14px;
  }}
  .app-row {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .app-icon {{
    width: 40px;
    height: 40px;
    border-radius: 9px;
    background: #0a84ff;
    display: grid;
    place-items: center;
    font-size: 18px;
  }}
  .app-row .meta {{ flex: 1; }}
  .app-row .meta strong {{ display: block; font-size: 14px; }}
  .app-row .meta small {{ color: var(--label); font-size: 12px; }}
  .open {{
    border: 0;
    background: #3a3a3c;
    color: #0a84ff;
    border-radius: 999px;
    padding: 6px 14px;
    font-weight: 600;
    font-size: 14px;
  }}
  .row {{
    display: flex;
    justify-content: space-between;
    gap: 12px;
    padding: 11px 0;
    border-bottom: 1px solid #2c2c2e;
    font-size: 15px;
  }}
  .row:last-child {{ border-bottom: 0; }}
  .row .k {{ color: var(--text); }}
  .row .v {{ color: var(--label); text-align: right; }}
  .info-barcode {{
    margin-top: 14px;
    background: #1c1c1e;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
  }}
  .info-barcode .qr {{
    margin: 0 auto 10px;
    width: 120px;
    height: 120px;
  }}
  .info-barcode .alt {{
    color: var(--label);
    font-size: 13px;
    letter-spacing: 0.04em;
  }}
  .hint {{
    max-width: 720px;
    margin: 28px auto 0;
    color: #8e8e93;
    font-size: 13px;
    line-height: 1.5;
    text-align: center;
  }}
  code {{ color: #fff; }}
</style>
</head>
<body>
  <h1>Browser preview (approximate) — not Apple Wallet</h1>
  <div class="stage">
    <div class="col">
      <h2>Pass front</h2>
      <div class="phone">
        <div class="pass-front">
          <img class="strip" src="{strip}" alt="Pass strip" />
          <div class="barcode-area"><div class="qr" aria-hidden="true"></div></div>
        </div>
      </div>
    </div>
    <div class="col">
      <h2>Info (ⓘ) screen</h2>
      <div class="phone">
        <div class="info">
          <img class="thumb" src="{thumb}" alt="Thumbnail" />
          <p class="title">{title}</p>
          <p class="subtitle">{subtitle}</p>
          <div class="actions">
            <span title="{phone}">📞</span>
            <span title="{website}">🧭</span>
          </div>
          {f'''
          <div class="card">
            <div class="app-row">
              <div class="app-icon">🏰</div>
              <div class="meta">
                <strong>{html.escape(app_name)}</strong>
                <small>{org}</small>
              </div>
              <button class="open" type="button">Open</button>
            </div>
          </div>
          ''' if app_name else ''}
          <div class="card">
            <div class="row"><span class="k">Guest Name</span><span class="v">{guest}</span></div>
            <div class="row"><span class="k">Affiliation</span><span class="v">{affiliation}</span></div>
            <div class="row"><span class="k">ID</span><span class="v">{badge_id}</span></div>
          </div>
          <div class="info-barcode">
            <div class="qr" aria-hidden="true"></div>
            <div class="alt">{badge_id}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <p class="hint">
    Open this file in Safari to review look &amp; feel.<br />
    To install on iPhone you still need a signed <code>.pkpass</code>
    (Apple Developer Pass Type ID certificate).
  </p>
</body>
</html>
"""
    output.write_text(doc, encoding="utf-8")
    return output
