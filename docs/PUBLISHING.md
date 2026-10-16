# Publishing

The learning lab is a static site. `index.html` is the front door. A service worker and `manifest.webmanifest` make it installable as a PWA in supporting browsers.

## Prepared, not built

- **Chrome extension.** The static files can be packed later as an extension that opens `index.html`. No extension manifest is shipped in this change.
- **Capacitor iOS and Android.** The same folder can be wrapped later with Capacitor. No native project is generated here.
- **Embed widget.** A host page could iframe `index.html`. No separate widget script is published here.

## What is built

The pages, the guide, the downloads, and the offline zip are in this repository. Serve the folder over HTTP. `file://` will not register the service worker.
