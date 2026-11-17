// pdfpng render <pdf> <first> <last> <dpi> <outdir> [prefix]   -> outdir/<prefix><page>.png (gray)
// pdfpng crop <src.png> <dst.png> <x0> <y0> <x1> <y1> [scale]  (fractions 0-1 or pixels; scale enlarges)
// pdfpng info <pdf>
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

func save(_ img: CGImage, _ path: String) {
    let url = URL(fileURLWithPath: path) as CFURL
    let dest = CGImageDestinationCreateWithURL(url, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dest, img, nil)
    CGImageDestinationFinalize(dest)
}
let a = CommandLine.arguments
if a[1] == "info" {
    let doc = CGPDFDocument(URL(fileURLWithPath: a[2]) as CFURL)!
    print("pages", doc.numberOfPages)
    let p = doc.page(at: 1)!
    print("mediabox", p.getBoxRect(.mediaBox))
} else if a[1] == "render" {
    let doc = CGPDFDocument(URL(fileURLWithPath: a[2]) as CFURL)!
    let first = Int(a[3])!, last = Int(a[4])!, dpi = Double(a[5])!, out = a[6]
    let prefix = a.count > 7 ? a[7] : "p"
    for n in first...last {
        guard let page = doc.page(at: n) else { continue }
        let box = page.getBoxRect(.mediaBox)
        let s = dpi / 72.0
        let w = Int(box.width * s), h = Int(box.height * s)
        let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
                            space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
        ctx.setFillColor(gray: 1, alpha: 1)
        ctx.fill(CGRect(x: 0, y: 0, width: w, height: h))
        ctx.interpolationQuality = .high
        ctx.scaleBy(x: s, y: s)
        ctx.translateBy(x: -box.origin.x, y: -box.origin.y)
        ctx.drawPDFPage(page)
        save(ctx.makeImage()!, "\(out)/\(prefix)\(String(format: "%03d", n)).png")
        print("\(prefix)\(n)", w, h)
    }
} else if a[1] == "bounds" {
    // bounds <src.png> <x0> <y0> <x1> <y1> : the box of dark ink inside the region (columns/rows with >= 3 dark px)
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    let W = img.width, H = img.height
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W,
                        space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
    ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))
    let buf = ctx.data!.bindMemory(to: UInt8.self, capacity: W * H)
    func f(_ v: String, _ n: Int) -> Int { let d = Double(v)!; return d <= 1.0 ? Int(d * Double(n)) : Int(d) }
    let x0 = f(a[3], W), y0 = f(a[4], H), x1 = f(a[5], W), y1 = f(a[6], H)
    var cols = [Int](repeating: 0, count: W), rows = [Int](repeating: 0, count: H)
    for y in y0..<y1 { for x in x0..<x1 { if buf[y * W + x] < 90 { cols[x] += 1; rows[y] += 1 } } }
    let cx = (x0..<x1).filter { cols[$0] >= 3 }, ry = (y0..<y1).filter { rows[$0] >= 3 }
    print(cx.first ?? -1, ry.first ?? -1, cx.last ?? -1, ry.last ?? -1, W, H)
} else if a[1] == "lines" {
    // lines <src.png> : ink line boxes of the text block (x 0.08-0.95): y0 y1 x0 x1 ink
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    let W = img.width, H = img.height
    let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W,
                        space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
    ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))
    let buf = ctx.data!.bindMemory(to: UInt8.self, capacity: W * H)
    let xa = Int(0.08 * Double(W)), xb = Int(0.95 * Double(W))
    var rows = [Int](repeating: 0, count: H)
    for y in 0..<H { for x in xa..<xb { if buf[y * W + x] < 90 { rows[y] += 1 } } }
    var y = 0
    while y < H {
        if rows[y] < 3 { y += 1; continue }
        var e = y, gap = 0
        while e < H && gap < 12 { if rows[e] >= 3 { gap = 0 } else { gap += 1 }; e += 1 }
        let y1 = e - gap
        var x0 = W, x1 = 0, ink = 0
        for yy in y..<y1 { for x in xa..<xb { if buf[yy * W + x] < 90 { ink += 1; if x < x0 { x0 = x }; if x > x1 { x1 = x } } } }
        if y1 - y >= 8 { print(y, y1, x0, x1, ink) }
        y = e
    }
} else if a[1] == "crop" {
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    let W = Double(img.width), H = Double(img.height)
    func f(_ v: String, _ n: Double) -> Double { let d = Double(v)!; return d <= 1.0 ? d * n : d }
    let x0 = f(a[4], W), y0 = f(a[5], H), x1 = f(a[6], W), y1 = f(a[7], H)
    let scale = a.count > 8 ? Double(a[8])! : 1.0
    let c = img.cropping(to: CGRect(x: x0, y: y0, width: x1 - x0, height: y1 - y0))!
    let w = Int(Double(c.width) * scale), h = Int(Double(c.height) * scale)
    let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
                        space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
    ctx.interpolationQuality = .high
    ctx.draw(c, in: CGRect(x: 0, y: 0, width: w, height: h))
    save(ctx.makeImage()!, a[3])
    print(a[3], Int(x0), Int(y0), Int(x1), Int(y1), w, h)
}
