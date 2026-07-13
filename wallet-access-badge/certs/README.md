# Place your Apple signing certificates here (never commit real keys).

Required files:

| File | Source |
|------|--------|
| `pass.pem` | Your Pass Type ID certificate (exported from Keychain as .pem) |
| `pass.key` | Private key for the Pass Type ID certificate |
| `wwdr.pem` | [Apple WWDR intermediate certificate](https://www.apple.com/certificateauthority/) |

These files are gitignored. See README.md for the full setup walkthrough.
