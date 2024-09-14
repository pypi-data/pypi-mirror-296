import { a as R } from "./Index-D21tLoTw.js";
import { i as l } from "./interopRequireDefault-BJV_i6Nz.js";
import { o as g, c as y } from "./common-DBXquc-F.js";
function b(c, p) {
  for (var f = 0; f < p.length; f++) {
    const e = p[f];
    if (typeof e != "string" && !Array.isArray(e)) {
      for (const t in e)
        if (t !== "default" && !(t in c)) {
          const _ = Object.getOwnPropertyDescriptor(e, t);
          _ && Object.defineProperty(c, t, _.get ? _ : {
            enumerable: !0,
            get: () => e[t]
          });
        }
    }
  }
  return Object.freeze(Object.defineProperty(c, Symbol.toStringTag, {
    value: "Module"
  }));
}
var o = {}, u = {};
Object.defineProperty(u, "__esModule", {
  value: !0
});
u.default = void 0;
var j = {
  // Options
  items_per_page: "/ σελίδα",
  jump_to: "Μετάβαση",
  jump_to_confirm: "επιβεβαιώνω",
  page: "",
  // Pagination
  prev_page: "Προηγούμενη Σελίδα",
  next_page: "Επόμενη Σελίδα",
  prev_5: "Προηγούμενες 5 Σελίδες",
  next_5: "Επόμενες 5 σελίδες",
  prev_3: "Προηγούμενες 3 Σελίδες",
  next_3: "Επόμενες 3 Σελίδες",
  page_size: "Μέγεθος σελίδας"
};
u.default = j;
var d = {}, a = {}, i = {}, P = l.default;
Object.defineProperty(i, "__esModule", {
  value: !0
});
i.default = void 0;
var s = P(g), G = y, $ = (0, s.default)((0, s.default)({}, G.commonLocale), {}, {
  locale: "el_GR",
  today: "Σήμερα",
  now: "Τώρα",
  backToToday: "Πίσω στη σημερινή μέρα",
  ok: "OK",
  clear: "Καθαρισμός",
  month: "Μήνας",
  year: "Έτος",
  timeSelect: "Επιλογή ώρας",
  dateSelect: "Επιλογή ημερομηνίας",
  monthSelect: "Επιλογή μήνα",
  yearSelect: "Επιλογή έτους",
  decadeSelect: "Επιλογή δεκαετίας",
  dateFormat: "D/M/YYYY",
  dateTimeFormat: "D/M/YYYY HH:mm:ss",
  previousMonth: "Προηγούμενος μήνας (PageUp)",
  nextMonth: "Επόμενος μήνας (PageDown)",
  previousYear: "Προηγούμενο έτος (Control + αριστερά)",
  nextYear: "Επόμενο έτος (Control + δεξιά)",
  previousDecade: "Προηγούμενη δεκαετία",
  nextDecade: "Επόμενη δεκαετία",
  previousCentury: "Προηγούμενος αιώνας",
  nextCentury: "Επόμενος αιώνας"
});
i.default = $;
var r = {};
Object.defineProperty(r, "__esModule", {
  value: !0
});
r.default = void 0;
const x = {
  placeholder: "Επιλέξτε ώρα"
};
r.default = x;
var v = l.default;
Object.defineProperty(a, "__esModule", {
  value: !0
});
a.default = void 0;
var O = v(i), D = v(r);
const T = {
  lang: Object.assign({
    placeholder: "Επιλέξτε ημερομηνία",
    rangePlaceholder: ["Αρχική ημερομηνία", "Τελική ημερομηνία"]
  }, O.default),
  timePickerLocale: Object.assign({}, D.default)
};
a.default = T;
var M = l.default;
Object.defineProperty(d, "__esModule", {
  value: !0
});
d.default = void 0;
var h = M(a);
d.default = h.default;
var n = l.default;
Object.defineProperty(o, "__esModule", {
  value: !0
});
o.default = void 0;
var Y = n(u), k = n(d), S = n(a), C = n(r);
const F = {
  locale: "el",
  Pagination: Y.default,
  DatePicker: S.default,
  TimePicker: C.default,
  Calendar: k.default,
  Table: {
    filterTitle: "Μενού φίλτρων",
    filterConfirm: "ΟΚ",
    filterReset: "Επαναφορά",
    selectAll: "Επιλογή τρέχουσας σελίδας",
    selectInvert: "Αντιστροφή τρέχουσας σελίδας"
  },
  Modal: {
    okText: "ΟΚ",
    cancelText: "Άκυρο",
    justOkText: "ΟΚ"
  },
  Popconfirm: {
    okText: "ΟΚ",
    cancelText: "Άκυρο"
  },
  Transfer: {
    titles: ["", ""],
    searchPlaceholder: "Αναζήτηση",
    itemUnit: "αντικείμενο",
    itemsUnit: "αντικείμενα"
  },
  Upload: {
    uploading: "Μεταφόρτωση...",
    removeFile: "Αφαίρεση αρχείου",
    uploadError: "Σφάλμα μεταφόρτωσης",
    previewFile: "Προεπισκόπηση αρχείου",
    downloadFile: "Λήψη αρχείου"
  },
  Empty: {
    description: "Δεν υπάρχουν δεδομένα"
  }
};
o.default = F;
var m = o;
const q = /* @__PURE__ */ R(m), A = /* @__PURE__ */ b({
  __proto__: null,
  default: q
}, [m]);
export {
  A as e
};
