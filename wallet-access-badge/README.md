# Apple Wallet Access Badge Builder

Build a single `.pkpass` file you can share via iMessage, AirDrop, or email. When opened on iPhone, it adds to Apple Wallet and the **info (ⓘ) screen** matches the Disney MagicMobile layout:

- Pass thumbnail and title at the top
- Phone and website quick-action buttons
- Companion app card with **Open** button
- Guest Name, Affiliation, and ID rows
- QR code with your badge ID at the bottom

## Quick start

```bash
cd wallet-access-badge
pip3 install -r requirements.txt

# Edit your badge details
nano config.yaml

# Build (unsigned preview — won't install on iPhone yet)
python3 build_pass.py --unsigned
```

Output: `AccessBadge.pkpass`

## Customize your badge

Edit `config.yaml`:

| Section | What it controls |
|---------|------------------|
| `pass.*` | Title, colors, organization name |
| `badge.*` | Guest name, affiliation, ID, QR code |
| `contact.*` | Phone and website icons on the info screen |
| `associated_app.*` | App Store link card (like "My Disney Experience") |

Replace placeholder images by dropping PNGs into `assets/` (see `assets/README.md`).

## Install on iPhone (requires Apple Developer)

Apple Wallet **only accepts signed passes**. You need:

1. An [Apple Developer Program](https://developer.apple.com/programs/) membership ($99/year)
2. A **Pass Type ID** certificate from [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/identifiers/list/passTypeId)

### One-time certificate setup

1. **Create a Pass Type ID**  
   Identifiers → Pass Type IDs → `+`  
   Example: `pass.com.yourname.accessbadge`

2. **Create a certificate** for that Pass Type ID and download it.

3. **Export from Keychain (Mac)**  
   - Import the `.cer` into Keychain Access  
   - Expand the cert, select cert + private key → Export as `.p12`  
   - Convert to PEM:

   ```bash
   openssl pkcs12 -in Certificates.p12 -clcerts -nokeys -out certs/pass.pem
   openssl pkcs12 -in Certificates.p12 -nocerts -nodes -out certs/pass.key
   ```

4. **Download WWDR intermediate**  
   Get the current [Apple WWDR certificate](https://www.apple.com/certificateauthority/) (G4) and save as `certs/wwdr.pem`.

5. **Update `config.yaml`** with your real values:

   ```yaml
   pass:
     pass_type_identifier: "pass.com.yourname.accessbadge"
     team_identifier: "ABCDE12345"   # 10-char Team ID from developer.apple.com
   ```

6. **Build signed pass:**

   ```bash
   python3 build_pass.py
   ```

## Share via text

1. AirDrop or iMessage the `.pkpass` file to your iPhone.
2. Tap the attachment → **Add** to Wallet.
3. Open Wallet → tap your pass → tap **ⓘ** to see the info screen.

> **Note:** Standard SMS/MMS often strips `.pkpass` attachments. Use **iMessage**, AirDrop, or email for reliable delivery.

## Info screen layout

The builder uses Apple's `storeCard` pass style so a full-width **strip image** fills the pass front (the Millennium Falcon artwork). The info (ⓘ) screen uses `backFields`:

```
┌─────────────────────────────┐
│  [strip — pass front art]   │  ← strip.png (before tapping ⓘ)
│  Christopher C              │
└─────────────────────────────┘

Info (ⓘ) screen:
┌─────────────────────────────┐
│  [thumbnail]                │
│  Disney MagicMobile Pass    │  ← logoText + primaryFields
│  Access Badge               │  ← description + secondaryFields
│  (📞)  (🌐)                  │  ← backFields: phone + website
│  ┌─────────────────────┐    │
│  │ My Disney Experience │   │  ← associatedStoreIdentifiers
│  │            [Open]    │   │
│  └─────────────────────┘    │
│  Guest Name    Christopher C│  ← backFields
│  Affiliation   DVC ND       │
│  ID            03A1762410A8  │
│  ┌─────────────────────┐    │
│  │      [QR CODE]       │   │  ← barcodes
│  │   03A1762410A8       │   │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Pass won't add to Wallet | Must be signed with a valid Pass Type ID cert |
| Wrong colors | Use `rgb(r, g, b)` format — hex colors are ignored by iOS |
| QR won't scan | Check `badge.barcode_message` matches your reader's expected format |
| App card missing | Set `associated_app.store_identifier` to a real App Store ID |

## File structure

```
wallet-access-badge/
├── config.yaml          # Your badge settings
├── build_pass.py        # Build + sign script
├── generate_assets.py   # Placeholder image generator
├── assets/              # Optional custom PNGs
├── certs/               # Signing certificates (gitignored)
└── AccessBadge.pkpass   # Output file
```

## Legal note

The default config uses Disney-style field names for demonstration. Use your own organization name, branding, and assets unless you have rights to use third-party trademarks.
