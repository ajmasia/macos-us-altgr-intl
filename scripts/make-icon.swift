// Renders the menu-bar badge as a template iconset.
//
// Usage: swift scripts/make-icon.swift TEXT OUTPUT.iconset
//
// The badge is a black rounded rectangle that fills the whole canvas height,
// so it is as tall as the system-drawn badges, with TEXT knocked out
// (transparent). macOS tints template images for light and dark menu bars.
// Pack the result with: iconutil -c icns OUTPUT.iconset -o OUTPUT.icns

import AppKit

let args = CommandLine.arguments
guard args.count == 3 else {
    FileHandle.standardError.write("usage: swift make-icon.swift TEXT OUTPUT.iconset\n".data(using: .utf8)!)
    exit(2)
}
let text = args[1]
let outputDir = args[2]

let entries: [(pixels: Int, file: String)] = [
    (16, "icon_16x16.png"), (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"), (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"), (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"), (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"), (1024, "icon_512x512@2x.png"),
]

func attributedText(_ size: CGFloat) -> NSAttributedString {
    let font = NSFont.systemFont(ofSize: size, weight: .heavy, width: .compressed)
    return NSAttributedString(string: text, attributes: [
        .font: font,
        .foregroundColor: NSColor.black,
        .kern: -size * 0.02,
    ])
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
    let badge = NSRect(x: 0, y: 0, width: side, height: side)
    NSColor.black.setFill()
    NSBezierPath(roundedRect: badge, xRadius: side * 0.2, yRadius: side * 0.2).fill()

    // Largest font size whose text fits the badge with a small margin.
    var fontSize = side
    var label = attributedText(fontSize)
    let fit = min(side * 0.94 / label.size().width, side * 0.84 / label.size().height, 1)
    fontSize *= fit
    label = attributedText(fontSize)

    context.compositingOperation = .destinationOut
    let size = label.size()
    label.draw(at: NSPoint(x: (side - size.width) / 2, y: (side - size.height) / 2))
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
