// =====================================================================
//  Capela Tríptico (oratório de bolso) — para impressão 3D
//  Painel central com moldura rendada, oval para a imagem e cruz;
//  duas portas laterais com dobradiças de pino que fecham sobre o centro.
//
//  Peças:  PART = "centro" | "porta_esq" | "porta_dir" | "placa" |
//                 "aberta" | "fechada"
//  Ex.:    openscad -D 'PART="centro"' -o centro.stl capela.scad
//
//  Unidades em milímetros. Todas as peças são impressas deitadas,
//  com a face decorada para cima. Troca de cor (marrom -> dourado)
//  na altura BASE (2.4 mm) dá o efeito de moldura dourada.
// =====================================================================

PART = "aberta";

/* ---------- dimensões gerais ---------- */
Wc      = 90;     // largura do painel central
Hc_body = 102;    // altura até os "ombros" do painel central
Hc_top  = 128;    // altura total (topo do arco)

BASE    = 2.4;    // espessura da base (cor marrom)
GOLD_C  = 1.2;    // relevo dourado do painel central
RING    = 0.6;    // relevo extra do anel oval / borda (centro)
GOLD_W  = 1.0;    // relevo dourado das portas

/* ---------- dobradiça ---------- */
c_gap   = 0.3;    // meia-folga entre centro e porta no plano (folga total 0.6)
R_kn    = 2.6;    // raio do nó (barril) da dobradiça
R_notch = 3.1;    // raio do rebaixo que dá passagem ao nó vizinho
PIN_D   = 2.0;    // furo do pino (filamento 1.75 mm ou arame/prego 1.8–2 mm)
Y0      = 8;      // início da dobradiça
Y1      = 92;     // fim da dobradiça
N_KN    = 5;      // nº de nós (ímpar: centro fica nas pontas)
G_KN    = 0.5;    // folga entre nós ao longo do eixo

TOP_C   = BASE + GOLD_C + RING;            // topo do centro (4.2)
TOP_W   = BASE + GOLD_W;                    // topo das portas (3.4)
// altura do eixo: porta fechada fica 0.4 mm acima do relevo do centro
Ha      = (TOP_C + 0.4 + TOP_W) / 2;        // = 4.0
XA      = Wc/2 + c_gap;                     // eixo direito (esquerdo = -XA)
Ww      = XA - c_gap - 0.5;                 // largura das portas (fecham com 1 mm de folga no meio)
Hw_in   = 104;    // altura da porta no lado da dobradiça
Hw_out  = 116;    // altura da porta no lado externo (ponta ornamental)

L_KN    = (Y1 - Y0 - (N_KN-1)*G_KN) / N_KN;
function kn_y(i) = Y0 + i*(L_KN + G_KN);

/* ---------- imagem / oval ---------- */
OV_C   = [0, 54];        // centro do oval
OV_IMG = [62, 88];       // janela da imagem (largura, altura)
OV_RNG = [72, 98];       // contorno externo do anel

$fn = 64;

// =====================================================================
//  2D — contornos
// =====================================================================
function arc_pts(c, r, a0, a1, n=24) =
    [for (i=[0:n]) let(a=a0+(a1-a0)*i/n) [c[0]+r*cos(a), c[1]+r*sin(a)]];
function ell_pts(c, rx, ry, a0, a1, n=40) =
    [for (i=[0:n]) let(a=a0+(a1-a0)*i/n) [c[0]+rx*cos(a), c[1]+ry*sin(a)]];

// Painel central: retângulo + ombro côncavo + arco elíptico
module center_outline() {
    sh = 7;   // tamanho do ombro côncavo
    xr = Wc/2;
    right = concat(
        [[ xr, 0]],
        [[ xr, Hc_body]],
        // ombro côncavo (quarto de círculo virado para fora)
        arc_pts([xr, Hc_body+sh], sh, -90, -180, 12),
        // arco até o topo
        ell_pts([0, Hc_body+sh-2], xr-sh, Hc_top-(Hc_body+sh-2), 0, 90, 40)
    );
    left = [for (i=[len(right)-2:-1:0]) [-right[i][0], right[i][1]]];
    polygon(concat(right, left));
}

// Porta (coordenadas locais: dobradiça em x=0, porta para +x)
module wing_outline() {
    x0 = c_gap; x1 = c_gap + Ww;
    sh = 6;
    pts = concat(
        [[x0, 0], [x1, 0], [x1, Hw_out - sh]],
        // ponta ornamental no canto externo
        arc_pts([x1 - sh, Hw_out - sh], sh, 0, 90, 10),
        // curva côncava descendo até o lado da dobradiça
        ell_pts([x0, Hw_out], x1 - sh - x0, Hw_out - Hw_in, 0, -90, 30)
    );
    polygon(pts);
}

// =====================================================================
//  2D — ornamentos (rendado)
// =====================================================================
// "C" de voluta: crescente
module crescent(r, t=0.32) {
    difference() {
        circle(r);
        translate([r*t, r*0.12]) circle(r*(1-t*0.75));
    }
}
// voluta em "S": duas crescentes opostas + gota
module scroll(s=1) {
    scale(s) {
        translate([-3.2, 0]) rotate(20)  crescent(3.4);
        translate([ 3.2, 0]) rotate(200) crescent(3.4);
    }
}
module teardrop(r=1.6, l=4) {
    hull() { circle(r); translate([l, 0]) circle(0.35); }
}
// cruz com pontas trevadas
module cross2d(h=17, w=12, t=2.8) {
    union() {
        translate([-t/2, -h/2]) square([t, h]);
        translate([-w/2, h/2 - h*0.34 - t/2]) square([w, t]);
        for (p = [[0, h/2], [0, -h/2], [-w/2, h/2 - h*0.34], [w/2, h/2 - h*0.34]])
            translate(p) circle(t*0.85);
    }
}

// buracos do rendado do painel central (metade direita; espelhada)
module center_lace_half() {
    // cantos inferiores
    translate([34.5, 10.5]) rotate(65)  scroll(0.95);
    translate([24, 4.4])   rotate(0)    teardrop(1.4, 5);
    translate([39.6, 25])  rotate(95)   teardrop(1.4, 5);
    translate([29.5, 18.5]) circle(1.0);
    translate([18, 3.9])   circle(0.9);
    // laterais
    for (y = [36, 50, 64]) translate([39.6, y]) rotate(90) teardrop(1.2, 4.5);
    for (y = [43, 57, 71]) translate([39.7, y]) circle(0.9);
    // ombros
    translate([35.5, 89])  rotate(115)  scroll(0.95);
    translate([39.6, 78])  rotate(-90)  teardrop(1.3, 4.5);
    translate([29, 97.5])  circle(1.0);
    // arco superior
    translate([22.5, 110]) rotate(150)  scroll(0.85);
    translate([33.5, 101.5]) rotate(-125) teardrop(1.2, 4);
    translate([12.5, 105.5]) circle(1.0);
    translate([14.5, 120.2]) rotate(172) teardrop(1.2, 4);
}

// buracos do rendado da porta (coordenadas locais)
module wing_lace() {
    xm = c_gap + Ww/2;
    translate([xm + 7, 104.5]) rotate(30)  scroll(0.8);
    translate([xm - 9, 100.3]) rotate(-8) teardrop(1.3, 5);
    translate([xm - 1.5, 99.6]) circle(0.9);
    translate([xm + 16, 111]) rotate(70) teardrop(1.2, 3.2);
    // filete de pontos nas laterais da moldura
    for (y = [14 : 12 : 86]) {
        translate([c_gap + 2.6, y]) circle(0.7);
        translate([c_gap + Ww - 2.6, y]) circle(0.7);
    }
    // cantos inferiores da moldura
    translate([c_gap + 4.2, 3.1]) circle(1.1);
    translate([c_gap + Ww - 4.2, 3.1]) circle(1.1);
}

// =====================================================================
//  Painel central
// =====================================================================
module center_gold_2d() {
    difference() {
        offset(r=-1.4) center_outline();
        translate(OV_C) scale([OV_IMG[0]/2, OV_IMG[1]/2]) circle(1, $fn=120);
        // rendado: só na área entre a borda e o anel oval
        intersection() {
            union() { center_lace_half(); mirror([1,0]) center_lace_half(); }
            difference() {
                offset(r=-4.2) center_outline();
                translate(OV_C) scale([OV_RNG[0]/2 + 1.6, OV_RNG[1]/2 + 1.6]) circle(1, $fn=120);
            }
        }
        translate([0, 115]) cross2d(h=14.5, w=10.5, t=2.4);
    }
}
// relevo extra: anel oval + filete da borda
module center_ring_2d() {
    difference() {
        translate(OV_C) scale([OV_RNG[0]/2, OV_RNG[1]/2]) circle(1, $fn=120);
        translate(OV_C) scale([OV_IMG[0]/2, OV_IMG[1]/2]) circle(1, $fn=120);
    }
    difference() {
        offset(r=-1.4) center_outline();
        offset(r=-3.0) center_outline();
    }
    // aro em volta da cruz
    translate([0, 115]) difference() { circle(9.6); circle(8.5); }
}

module center_body() {
    linear_extrude(BASE) center_outline();
    translate([0,0,BASE-0.01]) linear_extrude(GOLD_C+0.01) center_gold_2d();
    translate([0,0,BASE+GOLD_C-0.01]) linear_extrude(RING+0.01) center_ring_2d();
}

// =====================================================================
//  Dobradiça (perfil no plano XZ, eixo em x=0, z=Ha)
// =====================================================================
module extrude_y(y, l) { translate([0, y + l, 0]) rotate([90,0,0]) linear_extrude(l) children(); }

// nó preso ao lado "side" (-1 = lado do centro, +1 = lado da porta)
module knuckle_profile(side) {
    translate([0, Ha]) circle(R_kn);
    intersection() {
        hull() {
            translate([0, Ha]) circle(R_kn);
            translate([side < 0 ? -R_kn : 0, 0]) square([R_kn, BASE]);
        }
        translate([side < 0 ? -50 : c_gap, -1]) square([50 - c_gap, 50]);
    }
}
module knuckles(side, first) {   // first = 0 (pares) ou 1 (ímpares)
    for (i = [first : 2 : N_KN-1]) extrude_y(kn_y(i), L_KN) knuckle_profile(side);
}
module notches(first) {
    for (i = [first : 2 : N_KN-1])
        extrude_y(kn_y(i) - G_KN/2, L_KN + G_KN) translate([0, Ha]) circle(R_notch);
}
module pin_hole() {
    extrude_y(Y0 - 1, Y1 - Y0 + 2) translate([0, Ha]) circle(PIN_D/2, $fn=24);
}

// =====================================================================
//  Peças
// =====================================================================
module center_part() {
    difference() {
        union() {
            difference() {
                center_body();
                // folga plana junto aos eixos
                for (s=[-1,1]) translate([s*XA, 0, 0]) translate([-c_gap, -1, -1]) cube([2*c_gap, 200, 20]);
                // rebaixos para os nós das portas
                for (s=[-1,1]) translate([s*XA, 0, 0]) mirror([s<0?1:0,0,0]) notches(1);
            }
            for (s=[-1,1]) translate([s*XA, 0, 0]) mirror([s<0?1:0,0,0]) knuckles(-1, 0);
        }
        for (s=[-1,1]) translate([s*XA, 0, 0]) pin_hole();
    }
}

module wing_gold_2d() {
    xi = c_gap + 4.5; xo = c_gap + Ww - 4.5;
    difference() {
        offset(r=-1.2) wing_outline();
        // janela da imagem
        translate([xi, 6.5]) offset(r=1.5) offset(r=-1.5) square([xo - xi, 88]);
        wing_lace();
    }
}

module wing_part() {   // porta direita, coordenadas locais (eixo em x=0)
    difference() {
        union() {
            difference() {
                union() {
                    linear_extrude(BASE) wing_outline();
                    translate([0,0,BASE-0.01]) linear_extrude(GOLD_W+0.01) wing_gold_2d();
                }
                notches(0);
            }
            knuckles(+1, 1);
        }
        pin_hole();
    }
}

module wing_right_placed() { translate([XA, 0, 0]) wing_part(); }
module wing_left_placed()  { mirror([1,0,0]) wing_right_placed(); }

// porta girada em torno do eixo (ang = 0 aberta, 180 fechada)
module wing_rot(ang) {
    translate([XA, 0, Ha]) rotate([0, -ang, 0]) translate([0, 0, -Ha]) wing_part();
}

if (PART == "centro")    center_part();
if (PART == "porta_dir") wing_part();
if (PART == "porta_esq") mirror([1,0,0]) wing_part();
if (PART == "placa") {   // as três peças numa mesa só, já espaçadas
    center_part();
    translate([XA + 6, 0, 0]) wing_part();
    translate([-XA - 6, 0, 0]) mirror([1,0,0]) wing_part();
}
if (PART == "aberta") {
    color([0.36,0.22,0.12]) center_part();
    color([0.45,0.29,0.16]) { wing_right_placed(); wing_left_placed(); }
}
if (PART == "fechada") {
    color([0.36,0.22,0.12]) center_part();
    color([0.45,0.29,0.16]) { wing_rot(178); mirror([1,0,0]) wing_rot(178); }
}
