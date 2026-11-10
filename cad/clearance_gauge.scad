// Calibrador de folga (clearance) -- OpenSCAD
//
// Uma placa com 5 furos de diametro crescente + um pino de 8 mm.
// Imprima, descubra em qual furo o pino entra com aperto suave e use
// essa folga como padrao em todas as pecas com encaixe.
//
// Render pela linha de comando:
//   openscad -o clearance_plate.stl -D 'parte="placa"' clearance_gauge.scad
//   openscad -o clearance_pin.stl   -D 'parte="pino"'  clearance_gauge.scad
//
// Ou abra na GUI e use o Customizer.

PIN_D      = 8.0;
CLEARANCES = [0.10, 0.15, 0.20, 0.30, 0.40];
PLATE_T    = 4.0;
GAP        = 6.0;
MARGIN     = 6.0;
R_CANTO    = 3.0;

parte = "placa";   // [placa, pino]

// OpenSCAD nao tem sum() embutido
function sumv(v, i = 0, acc = 0) =
    i >= len(v) ? acc : sumv(v, i + 1, acc + v[i]);

hole_ds = [for (c = CLEARANCES) PIN_D + 2 * c];
largura = MARGIN * 2 + sumv(hole_ds) + GAP * (len(hole_ds) - 1);
altura  = PIN_D + MARGIN * 2;

// centro X de cada furo, na ordem de CLEARANCES
xs = [for (i = [0 : len(hole_ds) - 1])
         -largura / 2 + MARGIN
         + sumv([for (j = [0 : i - 1]) hole_ds[j] + GAP])
         + hole_ds[i] / 2];

module placa() {
    difference() {
        hull() {
            for (dx = [-largura / 2 + R_CANTO, largura / 2 - R_CANTO])
                for (dy = [-altura / 2 + R_CANTO, altura / 2 - R_CANTO])
                    translate([dx, dy, 0])
                        cylinder(r = R_CANTO, h = PLATE_T, $fn = 64);
        }
        for (i = [0 : len(hole_ds) - 1])
            translate([xs[i], 0, -1])
                cylinder(d = hole_ds[i], h = PLATE_T + 2, $fn = 64);
    }
}

module pino() {
    cylinder(d = PIN_D, h = 18, $fn = 64);
    translate([0, 0, 18])
        cylinder(d = PIN_D + 6, h = 3, $fn = 64);
}

if (parte == "placa") placa();
else pino();

echo(str("placa ", largura, " x ", altura, " x ", PLATE_T, " mm"));
echo(str("furos: ", hole_ds));
