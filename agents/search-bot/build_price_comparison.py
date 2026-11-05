# Builds the Botkin materials price-comparison PDF. Prices are listed
# retailer prices captured 3 Nov 2026. This script does not place orders.
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem,
)

OUT = r"C:\Users\colt3\OpenBot\Shared\SOW-2026-11-03\Botkin_Materials_Price_Comparison.pdf"

HD = "https://www.homedepot.com/p/"
LW = "https://www.lowes.com/pd/"

LINKS = {
    "door": HD + "Masonite-36-in-x-80-in-Utility-Flush-Primed-Steel-Prehung-Front-Door-with-Brickmold-41196/204338575",
    "porch": HD + "Progress-Lighting-Cylinder-Collection-5-White-Modern-Outdoor-Ceiling-Light-P5774-30/100467720",
    "tub_hd": HD + "Bootz-Industries-Aloha-60-in-x-30-in-Alcove-Soaking-Bathtub-with-Left-Drain-in-White-011-3365-00/314614191",
    "tub_lw": LW + "American-Standard-Elevate-60X30-Curved-Bathtub-Right-Hand-Drain/5018810975",
    "van60_hd": HD + "Glacier-Bay-Marcote-60-in-Double-Sink-Freestanding-Bathroom-Vanity-in-Slate-Blue-with-Venato-Engineered-Stone-Top-Assembled-23033-VS60-PSB/332873846",
    "van60_lw": LW + "Woodbridge-Bris-60-in-Black-Gold-Double-Sink-Bathroom-Vanity-with-White-Engineered-Stone-Top/5016583745",
    "van31": HD + "Glacier-Bay-Everdean-31-in-Single-Sink-White-Freestanding-Bath-Vanity-with-White-Cultured-Marble-Top-Assembled-EV30P2-WH/311606054",
    "toilet_hd": HD + "Glacier-Bay-12-inch-Rough-In-Two-Piece-1-1-GPF-1-6-GPF-Dual-Flush-Round-Toilet-in-White-Seat-Included-N2428R-DF/202862164",
    "toilet_lw": LW + "Project-Source-Laporte-Dual-Flush-Oyster-Dual-Elongated-Chair-Height-Back-to-wall-Soft-Close-Toilet-12-in-Rough-In-WaterSense-1-0-1-28-GPF/5015725633",
    "sink_elkay": HD + "Elkay-Avenue-33-in-Drop-In-Undermount-Single-Bowl-18-Gauge-Stainless-Steel-Kitchen-Sink-w-Accessories-HDDSB33229TR3/305917565",
    "sink_dh": HD + "Design-House-Drop-in-Stainless-Steel-33-in-18-Gauge-1-Hole-Single-Bowl-Kitchen-Sink-113118/310242326",
    "dw_hd": HD + "Frigidaire-24-in-White-Front-Control-Smart-Built-In-Tall-Tub-Dishwasher-with-Plastic-Tub-FDPC4221AW/314427469",
    "dw_lw": LW + "Frigidaire-Top-Control-24-in-Built-In-Dishwasher-White-ENERGY-STAR-52-dBA/5014687675",
    "flush": HD + "Commercial-Electric-11-in-Low-Profile-1-Light-White-LED-Puff-Flush-Mount-CE1011B-06/203725984",
    "fanlight": HD + "Broan-NuTone-50-CFM-Ceiling-Bathroom-Exhaust-Fan-with-Light-678/100065621",
    "vanlight": HD + "25-in-4-Light-3CCT-Chrome-LED-Bathroom-Vanity-Light-Over-Mirror-HD4FJF69BLED4CH/329707615",
    "cfan": HD + "Hampton-Bay-Hugger-52-in-LED-Indoor-Brushed-Nickel-Ceiling-Fan-with-Light-Kit-AL383LED-BN/300930186",
    "mirror": HD + "24-in-W-x-36-in-H-Rectangular-Frameless-Beveled-Edge-Wall-Mount-Bathroom-Vanity-Mirror-WM-Z24/321330234",
    "island": HD + "Costway-48-in-White-Rolling-Kitchen-Island-Cart-with-Natural-Wood-Top-and-Knife-Block-QD-614-A78IT/318345965",
    "lock": HD + "Kwikset-660-Series-Venetian-Bronze-Single-Cylinder-Deadbolt-Featuring-SmartKey-Security-66011PSMTRCK3V1/313356701",
    "lvp": HD + "Lifeproof-Banff-Gray-Hickory-30-Mil-x-9-in-W-x-48-in-L-Click-Lock-Waterproof-Luxury-Vinyl-Plank-Flooring-17-98-sq-ft-Case-HLVSPC028-W30/337335514",
    "paint": HD + "BEHR-MARQUEE-1-gal-BXC-41-Charcoal-Semi-Gloss-Enamel-Interior-Paint-Primer-345301/308230780",
    "smoke": HD + "First-Alert-SC5-Hardwire-Smart-Smoke-and-Carbon-Monoxide-Alarm-FSMCO600NVACCL1/337593929",
    "pvc": HD + "Charlotte-Pipe-4-in-x-10-ft-PVC-Schedule-40-DWV-Pipe-PVC074000600/100348477",
    "wh": HD + "Rheem-Performance-Platinum-50-Gal-Tall-40-000-BTU-Natural-Gas-Water-Heater-with-12-Year-Warranty-XG50T12HE40U0/204697785",
}


def money(n):
    return f"${n:,.2f}"


def link(url, label):
    return f'<link href="{url}" color="blue">{label}</link>'


# qty is the multiplier used for the illustrative extension.
# kind: counted | approx
PRICED = [
    ("Back exterior door", "1", 1, "counted",
     "36 x 80 in primed steel prehung, no glass. Hand, swing, and jamb are not in the takeoff.",
     ("Home Depot", 246.00, "Masonite 41196", LINKS["door"]),
     None),
    ("Front porch ceiling light", "1", 1, "counted",
     "White outdoor ceiling light. Bulb not included. Page also says see low price in cart, so the cart price may be lower than the listed price.",
     ("Home Depot", 173.00, "Progress P5774-30", LINKS["porch"]),
     None),
    ("60 in bathtub", "1", 1, "counted",
     "Alcove soaking tub, 60 x 30 in. Drain hand and material differ between the two listings.",
     ("Home Depot", 249.00, "Bootz Aloha 011-3365-00, left drain, steel", LINKS["tub_hd"]),
     ("Lowe's", 339.00, "American Standard Elevate, right drain", LINKS["tub_lw"])),
    ("Upstairs double vanity", "1", 1, "counted",
     "Width is TBD. Both examples are 60 in double-sink vanities with tops. Faucets are not included.",
     ("Home Depot", 929.00, "Glacier Bay Marcote 23033-VS60-PSB", LINKS["van60_hd"]),
     ("Lowe's", 1159.00, "Woodbridge Bris 60 in", LINKS["van60_lw"])),
    ("Downstairs single vanity", "1", 1, "counted",
     "Width is TBD. Example is a 31 in single-sink vanity with top. Faucet is not included.",
     ("Home Depot", 329.00, "Glacier Bay Everdean EV30P2-WH", LINKS["van31"]),
     None),
    ("Toilet", "1", 1, "counted",
     "Rough-in and bowl shape are TBD. These two listings are not the same bowl.",
     ("Home Depot", 99.00, "Glacier Bay N2428R-DF, round, white", LINKS["toilet_hd"]),
     ("Lowe's", 259.28, "Project Source, elongated, oyster, 1-piece", LINKS["toilet_lw"])),
    ("Kitchen sink", "1", 1, "counted",
     "33 in 18-gauge stainless, single bowl. Drop-in versus drop-in/undermount. Faucet not included on the lower listing.",
     ("Home Depot", 149.00, "Elkay Avenue HDDSB33229TR3, was $319.00", LINKS["sink_elkay"]),
     ("Home Depot", 186.99, "Design House 113118, 1-hole", LINKS["sink_dh"])),
    ("Dishwasher", "1", 1, "counted",
     "24 in built-in. Owner-supplied versus contractor-supplied is not confirmed. Models differ.",
     ("Home Depot", 329.00, "Frigidaire FDPC4221AW, white, was $399.00", LINKS["dw_hd"]),
     ("Lowe's", 449.00, "Frigidaire FDPH4316AW, white, top control", LINKS["dw_lw"])),
    ("Kitchen flush-mount lights", "about 8", 8, "approx",
     "11 in low-profile LED puff. Count is approximate, not an order quantity.",
     ("Home Depot", 29.96, "Commercial Electric CE1011B-06", LINKS["flush"]),
     None),
    ("Brick-alcove flush-mount light", "1", 1, "counted",
     "Same 11 in LED reference fixture as the kitchen ceiling lights.",
     ("Home Depot", 29.96, "Commercial Electric CE1011B-06", LINKS["flush"]),
     None),
    ("Downstairs bath fan with light", "1", 1, "counted",
     "50 CFM fan/light. A larger room may need a higher CFM unit.",
     ("Home Depot", 50.01, "Broan-NuTone 678", LINKS["fanlight"]),
     None),
    ("Upstairs bath fan with light", "1", 1, "counted",
     "Same 50 CFM reference. Room size is not measured.",
     ("Home Depot", 50.01, "Broan-NuTone 678", LINKS["fanlight"]),
     None),
    ("Upstairs vanity light", "1", 1, "counted",
     "25 in bar. A 60 in double vanity may need a longer bar.",
     ("Home Depot", 114.96, "JAZAVA HD4FJF69BLED4CH", LINKS["vanlight"]),
     None),
    ("Upstairs bedroom ceiling fans", "3", 3, "counted",
     "52 in hugger fan with LED light. Ceiling height and finish are not selected.",
     ("Home Depot", 59.97, "Hampton Bay AL383LED-BN", LINKS["cfan"]),
     None),
    ("Basement light fixtures", "at least 2", 2, "approx",
     "Two named locations only. Added locations are not priced. Same 11 in LED reference.",
     ("Home Depot", 29.96, "Commercial Electric CE1011B-06", LINKS["flush"]),
     None),
    ("Bathroom mirrors", "2", 2, "counted",
     "One downstairs and one upstairs. Size is TBD. Example is 24 x 36 in. A double vanity may need a wider mirror.",
     ("Home Depot", 89.99, "Frameless WM-Z24", LINKS["mirror"]),
     None),
    ("Movable kitchen island", "1", 1, "counted",
     "Takeoff asks for a movable butcher-block island. This listing is a 48 in rolling cart with a wood top, used as a stand-in.",
     ("Home Depot", 367.09, "Costway QD-614-A78IT", LINKS["island"]),
     None),
]

DECISIONS = [
    ("Front exterior door", "1 or 0",
     "Buy only if replacement wins over sand and paint. Same door family as the back door.",
     "Home Depot", 246.00, "Masonite 41196", LINKS["door"]),
    ("Front SmartKey lock", "up to 1",
     "Decision item. Confirm it is not already included with a new door.",
     "Home Depot", 19.97, "Kwikset 660 deadbolt", LINKS["lock"]),
    ("Kitchen sink light", "1",
     "One pendant or one downlight, not both. Downlight reference only. No pendant price was captured.",
     "Home Depot", 29.96, "Commercial Electric CE1011B-06", LINKS["flush"]),
    ("Water heater", "0 base; 1 contingent",
     "Excluded. Existing unit stays unless a documented failure. Fuel and size are not specified. Example is gas, 50 gal.",
     "Home Depot", 949.00, "Rheem XG50T12HE40U0", LINKS["wh"]),
]

UNITS = [
    ("LVP plank", "sq ft TBD",
     "Lifeproof Banff Gray Hickory, 30 mil, waterproof click. $3.59 per sq ft, $64.55 per 17.98 sq ft case. Waste not included. Room areas are unmeasured, so there is no case count.",
     LINKS["lvp"]),
    ("Interior wall paint", "gallons TBD",
     "BEHR MARQUEE 1 gal semi-gloss paint and primer, sample color Charcoal, $62.98. One gallon is not a whole-house quantity. Coverage, coats, and colors are unmeasured.",
     LINKS["paint"]),
    ("Smoke and CO alarm", "count TBD",
     "First Alert SC5 hardwire smart combination alarm, $128.77 each. Code layout is not done, so this is a unit price only.",
     LINKS["smoke"]),
    ("4 in PVC DWV pipe", "length TBD",
     "Charlotte Pipe 4 in x 10 ft Schedule 40 DWV, $77.13 per stick ($7.71 per ft). The sewer segment is about 3 ft and the stack length is unmeasured. Diameter is TBD, so neither is extended. A 10 ft stick is the listed package.",
     LINKS["pvc"]),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#444444"))
    canvas.drawString(0.45 * inch, 0.28 * inch,
                      "Not an order. Listed prices, 3 Nov 2026. Tax, delivery, and labor excluded.")
    canvas.drawRightString(landscape(letter)[0] - 0.45 * inch, 0.28 * inch, f"Page {doc.page}")
    canvas.restoreState()


def main():
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                        fontSize=16, leading=19, textColor=colors.HexColor("#1a1a1a"), spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                        fontSize=12, leading=15, textColor=colors.HexColor("#1f3b5b"),
                        spaceBefore=10, spaceAfter=4)
    body = ParagraphStyle("body", parent=styles["BodyText"], fontName="Helvetica",
                          fontSize=8.5, leading=11, textColor=colors.black)
    small = ParagraphStyle("small", parent=body, fontSize=7.5, leading=9.5)
    cell = ParagraphStyle("cell", parent=body, fontSize=7, leading=9)
    hdr = ParagraphStyle("hdr", parent=cell, fontName="Helvetica-Bold", textColor=colors.white)
    money_s = ParagraphStyle("money", parent=cell, fontName="Helvetica-Bold", alignment=2)

    story = []
    story.append(Paragraph("Botkin draft materials: online price comparison", h1))
    story.append(Paragraph(
        "Source: Botkin_93_Main_Materials_Takeoff_112_Entries.csv (112 data rows), 3 November 2026. "
        "Formatted list: Botkin_93_Main_Final_Materials_List_Corrected.pdf. "
        "Draft label only: 93 Main Avenue, New Brighton, PA. The 1,640 sq ft figure was not used. "
        "Nothing in this PDF was purchased.",
        body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("How to read the totals", h2))
    notes = [
        "The illustrative total adds only lines that have both a stated count and a price read from a product page on 3 November 2026.",
        "Home Depot and Lowe's list prices are national online prices. A New Brighton-area store can differ. Stock was not checked.",
        "Pennsylvania sales tax, delivery, and labor are excluded.",
        "No waste allowance is added. The takeoff says waste stays separate until a rate is approved.",
        "Decision, optional, conditional, contingency, overlap-hold, and verify-openings lines are excluded from the total.",
        "Where two products differ in size, color, bowl shape, or features, the lower price is not a like-for-like winner.",
        "Approximate and at-least counts are extended only as labeled illustrations.",
        "112 takeoff lines were reviewed. Most have no field measurement, so they have no purchase total.",
    ]
    for t in notes:
        story.append(Paragraph("- " + t, body))

    low_total = 0.0
    alt_total = 0.0
    rows = [[
        Paragraph("Item", hdr), Paragraph("Qty", hdr), Paragraph("Spec used", hdr),
        Paragraph("Lower listing", hdr), Paragraph("Other listing", hdr),
        Paragraph("Low ext.", hdr), Paragraph("Other ext.", hdr),
    ]]
    for item, qty_label, qty, kind, spec, low, alt in PRICED:
        low_ext = qty * low[1]
        low_total += low_ext
        if alt:
            alt_ext = qty * alt[1]
            alt_cell = Paragraph(
                f'{alt[0]} {money(alt[1])}<br/>{alt[2]}<br/>{link(alt[3], "Open listing")}', cell)
            alt_ext_cell = Paragraph(money(alt_ext), money_s)
        else:
            alt_ext = low_ext
            alt_cell = Paragraph("No second product page captured.", cell)
            alt_ext_cell = Paragraph(money(alt_ext), money_s)
        alt_total += alt_ext
        flag = " Approximate." if kind == "approx" else ""
        rows.append([
            Paragraph(item, cell),
            Paragraph(qty_label, cell),
            Paragraph(spec + flag, cell),
            Paragraph(f'{low[0]} {money(low[1])}<br/>{low[2]}<br/>{link(low[3], "Open listing")}', cell),
            alt_cell,
            Paragraph(money(low_ext), money_s),
            alt_ext_cell,
        ])

    rows.append([
        Paragraph("<b>Illustrative total</b>", cell),
        Paragraph("", cell),
        Paragraph("Counted and labeled approximate lines above. Tax and delivery excluded.", cell),
        Paragraph("", cell), Paragraph("", cell),
        Paragraph(f"<b>{money(low_total)}</b>", money_s),
        Paragraph(f"<b>{money(alt_total)}</b>", money_s),
    ])

    col_w = [1.35*inch, 0.7*inch, 2.35*inch, 1.85*inch, 1.85*inch, 0.75*inch, 0.75*inch]
    table = Table(rows, colWidths=col_w, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3b5b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e7eef5")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b7c3d0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#f6f8fa")]),
    ]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Priced lines with a count", h2))
    story.append(Paragraph(
        f"Lower-listing illustrative total: <b>{money(low_total)}</b>. "
        f"If each line uses the other listing when one exists: <b>{money(alt_total)}</b>.",
        body))
    story.append(Spacer(1, 4))
    story.append(table)

    story.append(Paragraph("Priced, but not in the total", h2))
    story.append(Paragraph(
        "These have a product-page price. The takeoff keeps them out of a committed order.",
        body))
    drows = [[
        Paragraph("Item", hdr), Paragraph("Qty", hdr), Paragraph("Why it is out", hdr),
        Paragraph("Listing", hdr), Paragraph("Price", hdr),
    ]]
    for item, qty, why, store, price, model, url in DECISIONS:
        drows.append([
            Paragraph(item, cell), Paragraph(qty, cell), Paragraph(why, cell),
            Paragraph(f"{store}<br/>{model}<br/>{link(url, 'Open listing')}", cell),
            Paragraph(money(price), money_s),
        ])
    dtable = Table(drows, colWidths=[1.5*inch, 1.15*inch, 3.6*inch, 2.4*inch, 0.85*inch], repeatRows=1)
    dtable.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5c4a32")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d5c7b2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fbf7f1")),
    ]))
    story.append(Spacer(1, 4))
    story.append(dtable)

    story.append(Paragraph("Unit prices only (quantity still TBD)", h2))
    story.append(Paragraph(
        "Do not multiply these into a project total until the area, length, or device count is measured.",
        body))
    urows = [[Paragraph("Item", hdr), Paragraph("Quantity", hdr), Paragraph("Listing", hdr)]]
    for item, qty, text, url in UNITS:
        urows.append([
            Paragraph(item, cell), Paragraph(qty, cell),
            Paragraph(text + "<br/>" + link(url, "Open listing"), cell),
        ])
    utable = Table(urows, colWidths=[1.6*inch, 1.1*inch, 6.8*inch], repeatRows=1)
    utable.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3b5b")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#b7c3d0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fa")]),
    ]))
    story.append(Spacer(1, 4))
    story.append(utable)

    story.append(Paragraph("Not priced, and why", h2))
    blocks = [
        ("Needs a measurement before any total",
         "Roof shingles and starter, roofing nails, soffit and fascia, siding repair, exterior shutter and porch-floor coatings, coil trim, house-number characters, sewer couplings, tank lid, faucets and traps, interior supply and waste piping, receptacles, switches, GFCI devices, living and upstairs pancake counts, cable and boxes, ducts, dryer vent, framing lumber, insulation, drywall sheets and finish materials, transom panel, interior doors and hardware, trim, baseboard, wainscot, pantry shelves, closet inserts, handrail length, stair and masonry and floor coatings, garage wall paint, cabinets, countertops, LVP transitions, subfloor patch, mulch, and gravel."),
        ("Windows stay unpriced",
         "Twelve non-basement location mentions are not confirmed as twelve unique openings, and no rough-opening sizes were given. Basement glass block is 4 units plus 1 possible overlap. Plastic covers for those units were not matched to a product page. Window-well covers are a different item and were not used as a substitute."),
        ("Held by the takeoff",
         "Front door versus paint, SmartKey lock, kitchen pendant versus downlight, register covers, wallpaper versus skim coat, under-stair closure, garden edging, weed barrier, geotextile, gravel base, roof underlayment, concrete-post mix, sewer bedding, washer and dryer, water heater, furnace, panel breakers, headers, vapor barrier, and LVP underlayment. Services (labor, permits, dumpsters, tree work, washing, cleaning) are excluded."),
        ("Zero-purchase lines",
         "Replacement shrubs and pruning consumables are 0 base. No plant list was specified."),
        ("Category listings that did not show a price on the product-page fetch",
         "A Home Depot category page listed Owens Corning Duration shingles near $47.97 per 32.8 sq ft bundle, and USG Sheetrock UltraLight 1/2 in x 4 ft x 8 ft near $12.48. Those figures are not in the total because the opened product pages did not display a price in the fetch."),
    ]
    for title, text in blocks:
        story.append(Paragraph(title, ParagraphStyle("h3", parent=h2, fontSize=10, leading=12, spaceBefore=6)))
        story.append(Paragraph(text, body))

    doc = SimpleDocTemplate(
        OUT, pagesize=landscape(letter),
        leftMargin=0.4 * inch, rightMargin=0.4 * inch,
        topMargin=0.4 * inch, bottomMargin=0.45 * inch,
        title="Botkin materials price comparison",
        author="Search Bot",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)

if __name__ == "__main__":
    main()
