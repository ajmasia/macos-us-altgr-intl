// Renders the menu-bar badge as a template iconset.
//
// Usage: swift scripts/make-icon.swift TEXT OUTPUT.iconset
//
// The badge is a black rounded rectangle with the aspect ratio of the
// system-drawn input source badges, spanning the full width of the square
// canvas, with TEXT knocked out (transparent). macOS tints template images
// for light and dark menu bars.
// Pack the result with: iconutil -c icns OUTPUT.iconset -o OUTPUT.icns

import AppKit

let args = CommandLine.arguments
guard args.count == 3 else {
    FileHandle.standardError.write("usage: swift make-icon.swift TEXT OUTPUT.iconset\n".data(using: .utf8)!)
    exit(2)
}
let text = args[1]
let outputDir = args[2]

// Measured on a native badge in the macOS 27 menu: 44x32 px, with a
// capital letter 17 px tall.
let badgeAspect: CGFloat = 44.0 / 32.0
let capHeightRatio: CGFloat = 17.0 / 32.0
let cornerRatio: CGFloat = 0.2

let entries: [(pixels: Int, file: String)] = [
    (16, "icon_16x16.png"), (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"), (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"), (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"), (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"), (1024, "icon_512x512@2x.png"),
]

func font(capHeight: CGFloat) -> NSFont {
    let reference = NSFont.systemFont(ofSize: 100, weight: .bold)
    return NSFont.systemFont(ofSize: 100 * capHeight / reference.capHeight, weight: .bold)
}

func render(_ pixels: Int) -> Data? {
    guard let rep = NSBitmapImageRep(
        bitmapDataPlanes: nil, pixelsWide: pixels, pixelsHigh: pixels,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0),
        let context = NSGraphicsContext(bitmapImageRep: rep)
    else { return nil }

    NSGraphicsContext.saveGraphicsState()
    defer { NSGraphicsContext.restoreGraphicsState() }
    NSGraphicsContext.current = context

    let side = CGFloat(pixels)
    let height = side / badgeAspect
    let badge = NSRect(x: 0, y: (side - height) / 2, width: side, height: height)
    NSColor.black.setFill()
    NSBezierPath(roundedRect: badge, xRadius: height * cornerRatio,
                 yRadius: height * cornerRatio).fill()

    // Capital letters as tall, relative to the badge, as on native badges,
    // centered on their cap height.
    let labelFont = font(capHeight: height * capHeightRatio)
    let label = NSAttributedString(string: text, attributes: [
        .font: labelFont, .foregroundColor: NSColor.black,
    ])
    let baseline = badge.midY - labelFont.capHeight / 2
    context.compositingOperation = .destinationOut
    label.draw(at: NSPoint(x: badge.midX - label.size().width / 2,
                           y: baseline + labelFont.descender))
    return rep.representation(using: .png, properties: [:])
}

do {
    try FileManager.default.createDirectory(atPath: outputDir, withIntermediateDirectories: true)
    for entry in entries {
        guard let png = render(entry.pixels) else {
            throw NSError(domain: "make-icon", code: 1,
                          userInfo: [NSLocalizedDescriptionKey: "cannot render \(entry.file)"])
        }
        try png.write(to: URL(fileURLWithPath: outputDir).appendingPathComponent(entry.file))
    }
} catch {
    FileHandle.standardError.write("error: \(error.localizedDescription)\n".data(using: .utf8)!)
    exit(1)
}
print("wrote \(entries.count) images to \(outputDir)")
