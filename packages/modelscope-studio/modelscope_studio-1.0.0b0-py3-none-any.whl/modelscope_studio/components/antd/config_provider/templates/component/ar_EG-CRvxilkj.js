import { a as b } from "./Index-D21tLoTw.js";
import { i as o } from "./interopRequireDefault-BJV_i6Nz.js";
import { o as Y, c as g } from "./common-DBXquc-F.js";
function x(c, f) {
  for (var s = 0; s < f.length; s++) {
    const a = f[s];
    if (typeof a != "string" && !Array.isArray(a)) {
      for (const t in a)
        if (t !== "default" && !(t in c)) {
          const p = Object.getOwnPropertyDescriptor(a, t);
          p && Object.defineProperty(c, t, p.get ? p : {
            enumerable: !0,
            get: () => a[t]
          });
        }
    }
  }
  return Object.freeze(Object.defineProperty(c, Symbol.toStringTag, {
    value: "Module"
  }));
}
var n = {}, i = {};
Object.defineProperty(i, "__esModule", {
  value: !0
});
i.default = void 0;
var y = {
  // Options
  items_per_page: "/ الصفحة",
  jump_to: "الذهاب إلى",
  jump_to_confirm: "تأكيد",
  page: "الصفحة",
  // Pagination
  prev_page: "الصفحة السابقة",
  next_page: "الصفحة التالية",
  prev_5: "خمس صفحات سابقة",
  next_5: "خمس صفحات تالية",
  prev_3: "ثلاث صفحات سابقة",
  next_3: "ثلاث صفحات تالية",
  page_size: "مقاس الصفحه"
};
i.default = y;
var d = {}, r = {}, u = {}, M = o.default;
Object.defineProperty(u, "__esModule", {
  value: !0
});
u.default = void 0;
var _ = M(Y), D = g, h = (0, _.default)((0, _.default)({}, D.commonLocale), {}, {
  locale: "ar_EG",
  today: "اليوم",
  now: "الأن",
  backToToday: "العودة إلى اليوم",
  ok: "تأكيد",
  clear: "مسح",
  month: "الشهر",
  year: "السنة",
  timeSelect: "اختيار الوقت",
  dateSelect: "اختيار التاريخ",
  monthSelect: "اختيار الشهر",
  yearSelect: "اختيار السنة",
  decadeSelect: "اختيار العقد",
  dateFormat: "M/D/YYYY",
  dateTimeFormat: "M/D/YYYY HH:mm:ss",
  previousMonth: "الشهر السابق (PageUp)",
  nextMonth: "الشهر التالى(PageDown)",
  previousYear: "العام السابق (Control + left)",
  nextYear: "العام التالى (Control + right)",
  previousDecade: "العقد السابق",
  nextDecade: "العقد التالى",
  previousCentury: "القرن السابق",
  nextCentury: "القرن التالى"
});
u.default = h;
var l = {};
Object.defineProperty(l, "__esModule", {
  value: !0
});
l.default = void 0;
const E = {
  placeholder: "اختيار الوقت"
};
l.default = E;
var $ = o.default;
Object.defineProperty(r, "__esModule", {
  value: !0
});
r.default = void 0;
var j = $(u), P = $(l);
const T = {
  lang: Object.assign({
    placeholder: "اختيار التاريخ",
    rangePlaceholder: ["البداية", "النهاية"],
    yearFormat: "YYYY",
    dateFormat: "D/M/YYYY",
    dayFormat: "D",
    dateTimeFormat: "DD/MM/YYYY HH:mm:ss",
    monthFormat: "MMMM",
    monthBeforeYear: !0,
    shortWeekDays: ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
    shortMonths: ["يناير", "فبراير", "مارس", "إبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
  }, j.default),
  timePickerLocale: Object.assign({}, P.default),
  dateFormat: "DD-MM-YYYY",
  monthFormat: "MM-YYYY",
  dateTimeFormat: "DD-MM-YYYY HH:mm:ss",
  weekFormat: "wo-YYYY"
};
r.default = T;
var G = o.default;
Object.defineProperty(d, "__esModule", {
  value: !0
});
d.default = void 0;
var F = G(r);
d.default = F.default;
var m = o.default;
Object.defineProperty(n, "__esModule", {
  value: !0
});
n.default = void 0;
var O = m(i), k = m(d), S = m(r), w = m(l);
const e = "ليس ${label} من نوع ${type} صالحًا", C = {
  locale: "ar",
  Pagination: O.default,
  DatePicker: S.default,
  TimePicker: w.default,
  Calendar: k.default,
  global: {
    placeholder: "يرجى التحديد"
  },
  Table: {
    filterTitle: "الفلاتر",
    filterConfirm: "تأكيد",
    filterReset: "إعادة ضبط",
    selectAll: "اختيار الكل",
    selectInvert: "إلغاء الاختيار",
    selectionAll: "حدد جميع البيانات",
    sortTitle: "رتب",
    expand: "توسيع الصف",
    collapse: "طي الصف",
    triggerDesc: "ترتيب تنازلي",
    triggerAsc: "ترتيب تصاعدي",
    cancelSort: "إلغاء الترتيب"
  },
  Modal: {
    okText: "تأكيد",
    cancelText: "إلغاء",
    justOkText: "تأكيد"
  },
  Popconfirm: {
    okText: "تأكيد",
    cancelText: "إلغاء"
  },
  Transfer: {
    titles: ["", ""],
    searchPlaceholder: "ابحث هنا",
    itemUnit: "عنصر",
    itemsUnit: "عناصر"
  },
  Upload: {
    uploading: "جاري الرفع...",
    removeFile: "احذف الملف",
    uploadError: "مشكلة فى الرفع",
    previewFile: "استعرض الملف",
    downloadFile: "تحميل الملف"
  },
  Empty: {
    description: "لا توجد بيانات"
  },
  Icon: {
    icon: "أيقونة"
  },
  Text: {
    edit: "تعديل",
    copy: "نسخ",
    copied: "نقل",
    expand: "وسع"
  },
  Form: {
    defaultValidateMessages: {
      default: "خطأ في حقل الإدخال ${label}",
      required: "يرجى إدخال ${label}",
      enum: "${label} يجب أن يكون واحدا من [${enum}]",
      whitespace: "${label} لا يمكن أن يكون حرفًا فارغًا",
      date: {
        format: "${label} تنسيق التاريخ غير صحيح",
        parse: "${label} لا يمكن تحويلها إلى تاريخ",
        invalid: "تاريخ ${label} غير صحيح"
      },
      types: {
        string: e,
        method: e,
        array: e,
        object: e,
        number: e,
        date: e,
        boolean: e,
        integer: e,
        float: e,
        regexp: e,
        email: e,
        url: e,
        hex: e
      },
      string: {
        len: "يجب ${label} ان يكون ${len} أحرف",
        min: "${label} على الأقل ${min} أحرف",
        max: "${label} يصل إلى ${max} أحرف",
        range: "يجب ${label} ان يكون مابين ${min}-${max} أحرف"
      },
      number: {
        len: "${len} ان يساوي ${label} يجب",
        min: "${min} الأدنى هو ${label} حد",
        max: "${max} الأقصى هو ${label} حد",
        range: "${max}-${min} ان يكون مابين ${label} يجب"
      },
      array: {
        len: "يجب أن يكون ${label} طوله ${len}",
        min: "يجب أن يكون ${label} طوله الأدنى ${min}",
        max: "يجب أن يكون ${label} طوله الأقصى ${max}",
        range: "يجب أن يكون ${label} طوله مابين ${min}-${max}"
      },
      pattern: {
        mismatch: "لا يتطابق ${label} مع ${pattern}"
      }
    }
  }
};
n.default = C;
var v = n;
const q = /* @__PURE__ */ b(v), U = /* @__PURE__ */ x({
  __proto__: null,
  default: q
}, [v]);
export {
  U as a
};
