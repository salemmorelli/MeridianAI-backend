// Meridian data is kept separate so you can later replace this with API data.
// Coordinates here are in a simple "authoring space" and then transformed in ModelViewer
// with `lineScale` and `lineOffset` for quick alignment to your GLB body.

export const meridians = {
  liver: {
    id: "liver",
    label: "Liver Meridian",
    color: "#8CFF7B",
    // Foot -> inner leg -> abdomen (mock path; tune as needed for your model).
    points: [
      [0.09, -0.92, 0.06], // big toe area
      [0.08, -0.84, 0.08], // dorsal foot
      [0.09, -0.74, 0.07], // inner ankle
      [0.1, -0.58, 0.08], // inner shin
      [0.11, -0.42, 0.09], // below knee
      [0.12, -0.25, 0.1], // inner thigh low
      [0.13, -0.08, 0.1], // inner thigh high
      [0.12, 0.07, 0.11], // groin
      [0.11, 0.22, 0.12], // lower abdomen
      [0.1, 0.36, 0.12], // upper abdomen/rib edge
    ],
  },
  stomach: {
    id: "stomach",
    label: "Stomach Meridian",
    color: "#FFD166",
    // Face/chest -> anterior leg -> foot (mock path).
    points: [
      [0.1, 0.86, 0.11],
      [0.12, 0.72, 0.12],
      [0.13, 0.54, 0.12],
      [0.13, 0.34, 0.13],
      [0.12, 0.12, 0.13],
      [0.12, -0.1, 0.12],
      [0.13, -0.34, 0.11],
      [0.12, -0.56, 0.1],
      [0.11, -0.76, 0.09],
      [0.1, -0.92, 0.08],
    ],
  },
};

// Pressure points for ModelViewer (authoring space; scaled by lineScale/lineOffset in ModelViewer.jsx).
// Codes and labels mirror `data/points-catalog.json` — tune positions when you change the GLB.
const M = {
  li: "#4ade80",
  pc: "#f472b6",
  gv: "#c4b5fd",
  bl: "#60a5fa",
  gb: "#38bdf8",
  lv: "#8CFF7B",
  st: "#FFD166",
  sp: "#fb7185",
  cv: "#a78bfa",
  ki: "#818cf8",
  ht: "#fda4af",
  si: "#fb923c",
  te: "#2dd4bf",
  lu: "#86efac",
};

export const pressurePoints = [
  { code: "LI4", label: "LI4 (Hegu)", color: M.li, position: [0.14, 0.02, 0.1] },
  { code: "LI11", label: "LI11 (Quchi)", color: M.li, position: [0.17, 0.08, 0.08] },
  { code: "PC6", label: "PC6 (Neiguan)", color: M.pc, position: [0.09, 0.12, 0.1] },
  { code: "PC8", label: "PC8 (Laogong)", color: M.pc, position: [0.12, -0.02, 0.12] },
  { code: "YINTANG", label: "Yin Tang (EX-HN3)", color: M.gv, position: [0, 0.82, 0.14] },
  { code: "GV20", label: "GV20 (Baihui)", color: M.gv, position: [0, 0.95, 0.06] },
  { code: "BL2", label: "BL2 (Zanzhu)", color: M.bl, position: [-0.04, 0.8, 0.12] },
  { code: "GB20", label: "GB20 (Fengchi)", color: M.gb, position: [0.07, 0.62, -0.06] },
  { code: "LV3", label: "LV3 / LR3 (Tai Chong)", color: M.lv, position: [0.08, -0.86, 0.08] },
  { code: "LR14", label: "LR14 (Qimen)", color: M.lv, position: [0.11, 0.28, 0.1] },
  { code: "ST25", label: "ST25 (Tianshu)", color: M.st, position: [0.08, 0.1, 0.12] },
  { code: "CV6", label: "CV6 (Qihai)", color: M.cv, position: [0, 0.06, 0.12] },
  { code: "ST36", label: "ST36 (Zusanli)", color: M.st, position: [0.12, -0.56, 0.1] },
  { code: "ST40", label: "ST40 (Fenglong)", color: M.st, position: [0.14, -0.48, 0.08] },
  { code: "SP6", label: "SP6 (Sanyinjiao)", color: M.sp, position: [0.1, -0.66, 0.07] },
  { code: "GB34", label: "GB34 (Yanglingquan)", color: M.gb, position: [0.13, -0.42, 0.09] },
  { code: "BL60", label: "BL60 (Kunlun)", color: M.bl, position: [0.12, -0.82, 0.04] },
  { code: "KI3", label: "KI3 (Taixi)", color: M.ki, position: [0.07, -0.8, 0.06] },
  { code: "LU7", label: "LU7 (Lieque)", color: M.lu, position: [0.15, 0.14, 0.09] },
  { code: "HT7", label: "HT7 (Shenmen)", color: M.ht, position: [0.06, -0.04, 0.11] },
  { code: "SI3", label: "SI3 (Houxi)", color: M.si, position: [0.05, -0.02, 0.09] },
  { code: "TE5", label: "TE5 (Waiguan)", color: M.te, position: [0.14, 0.1, 0.11] },
];

export const meridianList = Object.values(meridians);
