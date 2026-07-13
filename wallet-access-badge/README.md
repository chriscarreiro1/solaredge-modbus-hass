# Apple Wallet Access Badge Builder

Build a single `.pkpass` file you can share via iMessage or AirDrop. The pass uses **similar** Disney MagicMobile styling — dark navy theme, space-battle pass front, and an info screen with guest details and QR code. Not a pixel-perfect replica; close enough for a personal access badge.

- Pass thumbnail and title at the top
- Phone and website quick-action buttons
- Companion app card with **Open** button
- Guest Name, Affiliation, and ID rows
- QR code with your badge ID at the bottom

## Quick start

```bash
cd wallet-access-badge

# Install for the same python3 you'll run (important on macOS)
python3 -m pip install -r requirements.txt

# Edit your badge details
nano config.yaml

# Build (unsigned preview — won't install on iPhone yet)
python3 build_pass.py --unsigned
```

Output: `AccessBadge.pkpass`

## Preview on your Mac (no Apple cert needed)

```bash
cd ~/solaredge-modbus-hass/wallet-access-badge
python3 -m pip install -r requirements.txt
python3 build_pass.py --unsigned
open preview.html
```

That opens a Safari mock of the **pass front** and **info (ⓘ)** screens so you can judge the look before signing.

## Customize your badge

Edit `config.yaml`:

| Section | What it controls |
|---------|------------------|
| `pass.*` | Title, colors, organization name |
| `badge.*` | Guest name, affiliation, ID, QR code |
| `contact.*` | Phone and website icons on the info screen |
| `associated_app.*` | App Store link card (like "My Disney Experience") |

Replace placeholder images by dropping PNGs into `assets/` (see `assets/README.md`).

## Signing for iPhone (step-by-step)

Apple Wallet **only installs signed** `.pkpass` files. You need an [Apple Developer Program](https://developer.apple.com/programs/) membership ($99/year).

### 1. Create a Pass Type ID

1. Open [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/identifiers/list/passTypeId)
2. Click **Identifiers** → **+**
3. Choose **Pass Type IDs** → Continue
4. Description: `Access Badge`
5. Identifier: `pass.com.yourname.accessbadge` (must start with `pass.`)
6. Register

### 2. Create the certificate

1. Still in the portal → **Certificates** → **+**
2. Under Services choose **Pass Type ID Certificate** → Continue
3. Select the Pass Type ID you just created
4. Follow the CSR steps:
   - On your Mac: open **Keychain Access** → menu **Keychain Access → Certificate Assistant → Request a Certificate From a Certificate Authority…**
   - Email = yours, Common Name = `Access Badge`, choose **Saved to disk**
   - Upload that `.certSigningRequest` in the portal
5. Download the resulting `.cer` and double-click it to install into **login** keychain

### 3. Export PEM files into this project

1. Open **Keychain Access** → **My Certificates**
2. Find the Pass Type ID cert (name looks like `Pass Type ID: pass.com…`)
3. Click the disclosure triangle so the private key is visible
4. Select the cert (and key) → right-click → **Export 2 items…** → format **Personal Information Exchange (.p12)**
5. Set a temporary password, save as `Certificates.p12` on Desktop
6. In Terminal:

```bash
cd ~/solaredge-modbus-hass/wallet-access-badge
mkdir -p certs

# Convert the .p12 (enter the export password when asked)
openssl pkcs12 -in ~/Desktop/Certificates.p12 -clcerts -nokeys -out certs/pass.pem -legacy
openssl pkcs12 -in ~/Desktop/Certificates.p12 -nocerts -nodes -out certs/pass.key -legacy
```

If `-legacy` errors on older OpenSSL, drop that flag and try again.

### 4. Download Apple’s WWDR intermediate

```bash
curl -L -o certs/AppleWWDRCAG4.cer https://www.apple.com/certificateauthority/AppleWWDRCAG4.cer
openssl x509 -inform DER -in certs/AppleWWDRCAG4.cer -out certs/wwdr.pem
```

### 5. Put your IDs in `config.yaml`

On [Membership details](https://developer.apple.com/account#MembershipDetailsCard) copy your **Team ID**.

```yaml
pass:
  pass_type_identifier: "pass.com.yourname.accessbadge"  # exact ID from step 1
  team_identifier: "ABCDE12345"                           # your 10-char Team ID
```

### 6. Build signed + AirDrop to iPhone

```bash
python3 build_pass.py
open .
# AirDrop AccessBadge.pkpass to your iPhone → tap → Add
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
