// WHO-based reference metadata for channels and selected points used in this app.
// Primary sources:
// 1) WHO Standard Acupuncture Point Locations in the Western Pacific Region (2008/2009)
// 2) Standard Acupuncture Nomenclature (WHO WPRO, 1984)
// 3) WHO Scientific Group report on standard acupuncture nomenclature (1991)

export const whoMeridians = [
  { code: "LU", legacyCode: "L", slug: "lung", name: "Lung Meridian" },
  { code: "LI", legacyCode: "LI", slug: "large-intestine", name: "Large Intestine Meridian" },
  { code: "ST", legacyCode: "S", slug: "stomach", name: "Stomach Meridian" },
  { code: "SP", legacyCode: "Sp", slug: "spleen", name: "Spleen Meridian" },
  { code: "HT", legacyCode: "H", slug: "heart", name: "Heart Meridian" },
  { code: "SI", legacyCode: "SI", slug: "small-intestine", name: "Small Intestine Meridian" },
  { code: "BL", legacyCode: "B", slug: "bladder", name: "Bladder Meridian" },
  { code: "KI", legacyCode: "K", slug: "kidney", name: "Kidney Meridian" },
  { code: "PC", legacyCode: "P", slug: "pericardium", name: "Pericardium Meridian" },
  { code: "TE", legacyCode: "TE", slug: "triple-energizer", name: "Triple Energizer Meridian" },
  { code: "GB", legacyCode: "G", slug: "gallbladder", name: "Gallbladder Meridian" },
  { code: "LR", legacyCode: "Liv", slug: "liver", name: "Liver Meridian" },
  { code: "GV", legacyCode: "GV", slug: "governing-vessel", name: "Governor Vessel Meridian" },
  { code: "CV", legacyCode: "CV", slug: "conception-vessel", name: "Conception Vessel Meridian" },
];

export const whoPointReferences = [
  {
    appId: "LI4",
    whoCode: "LI4",
    pinyin: "Hegu",
    channelCode: "LI",
    notes: "Classical point on the Large Intestine channel.",
  },
  {
    appId: "PC6",
    whoCode: "PC6",
    pinyin: "Neiguan",
    channelCode: "PC",
    notes: "Classical point on the Pericardium channel.",
  },
  {
    appId: "YINTANG",
    whoCode: "EX-HN3",
    pinyin: "Yintang",
    channelCode: "EX",
    notes: "Extra point (head and neck), not one of the 14 regular channel points.",
  },
  {
    appId: "LV3",
    whoCode: "LR3",
    pinyin: "Taichong",
    channelCode: "LR",
    notes: "App keeps LV3 alias for compatibility; WHO standard code is LR3.",
  },
  {
    appId: "ST36",
    whoCode: "ST36",
    pinyin: "Zusanli",
    channelCode: "ST",
    notes: "Classical point on the Stomach channel.",
  },
  {
    appId: "GB20",
    whoCode: "GB20",
    pinyin: "Fengchi",
    channelCode: "GB",
    notes: "Classical point on the Gallbladder channel.",
  },
  { appId: "LI11", whoCode: "LI11", pinyin: "Quchi", channelCode: "LI", notes: "Large Intestine channel; elbow region." },
  { appId: "PC8", whoCode: "PC8", pinyin: "Laogong", channelCode: "PC", notes: "Pericardium channel; palm center." },
  { appId: "GV20", whoCode: "GV20", pinyin: "Baihui", channelCode: "GV", notes: "Governing Vessel; vertex (gentle contact)." },
  { appId: "BL2", whoCode: "BL2", pinyin: "Zanzhu", channelCode: "BL", notes: "Bladder channel; medial eyebrow." },
  { appId: "LR14", whoCode: "LR14", pinyin: "Qimen", channelCode: "LR", notes: "Liver channel; costal region." },
  { appId: "ST25", whoCode: "ST25", pinyin: "Tianshu", channelCode: "ST", notes: "Stomach channel; lateral to umbilicus." },
  { appId: "CV6", whoCode: "CV6", pinyin: "Qihai", channelCode: "CV", notes: "Conception vessel; lower abdomen midline." },
  { appId: "ST40", whoCode: "ST40", pinyin: "Fenglong", channelCode: "ST", notes: "Stomach channel; lower leg." },
  { appId: "SP6", whoCode: "SP6", pinyin: "Sanyinjiao", channelCode: "SP", notes: "Spleen channel; medial lower leg." },
  { appId: "GB34", whoCode: "GB34", pinyin: "Yanglingquan", channelCode: "GB", notes: "Gallbladder channel; below lateral knee." },
  { appId: "BL60", whoCode: "BL60", pinyin: "Kunlun", channelCode: "BL", notes: "Bladder channel; lateral ankle." },
  { appId: "KI3", whoCode: "KI3", pinyin: "Taixi", channelCode: "KI", notes: "Kidney channel; medial ankle." },
  { appId: "LU7", whoCode: "LU7", pinyin: "Lieque", channelCode: "LU", notes: "Lung channel; radial forearm." },
  { appId: "HT7", whoCode: "HT7", pinyin: "Shenmen", channelCode: "HT", notes: "Heart channel; ulnar wrist." },
  { appId: "SI3", whoCode: "SI3", pinyin: "Houxi", channelCode: "SI", notes: "Small Intestine channel; ulnar hand edge." },
  { appId: "TE5", whoCode: "TE5", pinyin: "Waiguan", channelCode: "TE", notes: "Triple Energizer channel; dorsal forearm." },
];

export const whoSourceLinks = {
  pointLocations:
    "https://iris.who.int/bitstream/handle/10665/353407/9789290613831-eng.pdf?sequence=1&isAllowed=y",
  nomenclature1984:
    "https://iris.who.int/bitstream/handle/10665/207652/Standard_acupuncture_nomenclature1984_ser.no.1_eng.pdf?sequence=1&isAllowed=y",
  scientificReport:
    "https://apps.who.int/iris/bitstream/handle/10665/40001/9241544171_eng.pdf",
};
