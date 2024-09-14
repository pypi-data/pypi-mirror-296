import { b as me } from "./Index-iA4II6DV.js";
const te = window.ms_globals.React, _e = window.ms_globals.React.forwardRef, pe = window.ms_globals.React.useRef, ge = window.ms_globals.React.useEffect;
function R() {
}
function be(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function he(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return R;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function g(t) {
  let e;
  return he(t, (o) => e = o)(), e;
}
const b = [];
function p(t, e = R) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function r(l) {
    if (be(t, l) && (t = l, o)) {
      const c = !b.length;
      for (const d of n)
        d[1](), b.push(d, t);
      if (c) {
        for (let d = 0; d < b.length; d += 2)
          b[d][0](b[d + 1]);
        b.length = 0;
      }
    }
  }
  function s(l) {
    r(l(t));
  }
  function i(l, c = R) {
    const d = [l, c];
    return n.add(d), n.size === 1 && (o = e(r, s) || R), l(t), () => {
      n.delete(d), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: r,
    update: s,
    subscribe: i
  };
}
const {
  getContext: ne,
  setContext: q
} = window.__gradio__svelte__internal, we = "$$ms-gr-antd-slots-key";
function ye() {
  const t = p({});
  return q(we, t);
}
const xe = "$$ms-gr-antd-context-key";
function Ie(t) {
  var l;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = oe(), o = Ce({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    o.slotKey.set(c);
  }), Se();
  const n = ne(xe), r = ((l = g(n)) == null ? void 0 : l.as_item) || t.as_item, s = n ? r ? g(n)[r] : g(n) : {}, i = p({
    ...t,
    ...s
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: d
    } = g(i);
    d && (c = c[d]), i.update((f) => ({
      ...f,
      ...c
    }));
  }), [i, (c) => {
    const d = c.as_item ? g(n)[c.as_item] : g(n);
    return i.set({
      ...c,
      ...d
    });
  }]) : [i, (c) => {
    i.set(c);
  }];
}
const re = "$$ms-gr-antd-slot-key";
function Se() {
  q(re, p(void 0));
}
function oe() {
  return ne(re);
}
const ve = "$$ms-gr-antd-component-slot-context-key";
function Ce({
  slot: t,
  index: e,
  subIndex: o
}) {
  return q(ve, {
    slotKey: p(t),
    slotIndex: p(e),
    subSlotIndex: p(o)
  });
}
function Ee(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Oe(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var se = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Pe = te, Re = Symbol.for("react.element"), je = Symbol.for("react.fragment"), ke = Object.prototype.hasOwnProperty, Fe = Pe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ie(t, e, o) {
  var n, r = {}, s = null, i = null;
  o !== void 0 && (s = "" + o), e.key !== void 0 && (s = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (n in e) ke.call(e, n) && !Ne.hasOwnProperty(n) && (r[n] = e[n]);
  if (t && t.defaultProps) for (n in e = t.defaultProps, e) r[n] === void 0 && (r[n] = e[n]);
  return {
    $$typeof: Re,
    type: t,
    key: s,
    ref: i,
    props: r,
    _owner: Fe.current
  };
}
k.Fragment = je;
k.jsx = ie;
k.jsxs = ie;
se.exports = k;
var F = se.exports;
const Le = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Me(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const n = t[o];
    return typeof n == "number" && !Le.includes(o) ? e[o] = n + "px" : e[o] = n, e;
  }, {}) : {};
}
function le(t) {
  const e = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((n) => {
    t.getEventListeners(n).forEach(({
      listener: s,
      type: i,
      useCapture: l
    }) => {
      e.addEventListener(i, s, l);
    });
  });
  const o = Array.from(t.children);
  for (let n = 0; n < o.length; n++) {
    const r = o[n], s = le(r);
    e.replaceChild(s, e.children[n]);
  }
  return e;
}
function qe(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const N = _e(({
  slot: t,
  clone: e,
  className: o,
  style: n
}, r) => {
  const s = pe();
  return ge(() => {
    var d;
    if (!s.current || !t)
      return;
    let i = t;
    function l() {
      let f = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (f = i.children[0], f.tagName.toLowerCase() === "react-portal-target" && f.children[0] && (f = f.children[0])), qe(r, f), o && f.classList.add(...o.split(" ")), n) {
        const a = Me(n);
        Object.keys(a).forEach((m) => {
          f.style[m] = a[m];
        });
      }
    }
    let c = null;
    if (e && window.MutationObserver) {
      let f = function() {
        var a;
        i = le(t), i.style.display = "contents", l(), (a = s.current) == null || a.appendChild(i);
      };
      f(), c = new window.MutationObserver(() => {
        var a, m;
        (a = s.current) != null && a.contains(i) && ((m = s.current) == null || m.removeChild(i)), f();
      }), c.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", l(), (d = s.current) == null || d.appendChild(i);
    return () => {
      var f, a;
      i.style.display = "", (f = s.current) != null && f.contains(i) && ((a = s.current) == null || a.removeChild(i)), c == null || c.disconnect();
    };
  }, [t, e, o, n, r]), te.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  });
});
function L(t, e) {
  return t.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const n = {
      ...o.props
    };
    let r = n;
    Object.keys(o.slots).forEach((i) => {
      if (!o.slots[i] || !(o.slots[i] instanceof Element) && !o.slots[i].el)
        return;
      const l = i.split(".");
      l.forEach((m, w) => {
        r[m] || (r[m] = {}), w !== l.length - 1 && (r = n[m]);
      });
      const c = o.slots[i];
      let d, f, a = !1;
      c instanceof Element ? d = c : (d = c.el, f = c.callback, a = c.clone || !1), r[l[l.length - 1]] = d ? f ? (...m) => (f(l[l.length - 1], m), /* @__PURE__ */ F.jsx(N, {
        slot: d,
        clone: a || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ F.jsx(N, {
        slot: d,
        clone: a || (e == null ? void 0 : e.clone)
      }) : r[l[l.length - 1]], r = n;
    });
    const s = "children";
    return o[s] && (n[s] = L(o[s], e)), n;
  });
}
function P(t, e) {
  return t ? /* @__PURE__ */ F.jsx(N, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
var ce = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function o() {
      for (var s = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (s = r(s, n(l)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return o.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var i = "";
      for (var l in s)
        e.call(s, l) && s[l] && (i = r(i, l));
      return i;
    }
    function r(s, i) {
      return i ? s ? s + " " + i : s + i : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(ce);
var Ke = ce.exports;
const Ae = /* @__PURE__ */ Oe(Ke), {
  getContext: Be,
  setContext: ze
} = window.__gradio__svelte__internal;
function ue(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function o(r = ["default"]) {
    const s = r.reduce((i, l) => (i[l] = p([]), i), {});
    return ze(e, {
      itemsMap: s,
      allowedSlots: r
    }), s;
  }
  function n() {
    const {
      itemsMap: r,
      allowedSlots: s
    } = Be(e);
    return function(i, l, c) {
      r && (i ? r[i].update((d) => {
        const f = [...d];
        return s.includes(i) ? f[l] = c : f[l] = void 0, f;
      }) : s.includes("default") && r.default.update((d) => {
        const f = [...d];
        return f[l] = c, f;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: n
  };
}
const {
  getItems: Te,
  getSetItemFn: ot
} = ue("menu"), {
  getItems: st,
  getSetItemFn: We
} = ue("breadcrumb"), {
  SvelteComponent: De,
  check_outros: Ge,
  component_subscribe: h,
  create_slot: He,
  detach: Ue,
  empty: Ve,
  flush: _,
  get_all_dirty_from_scope: Je,
  get_slot_changes: Ye,
  group_outros: Qe,
  init: Xe,
  insert: Ze,
  safe_not_equal: $e,
  transition_in: j,
  transition_out: M,
  update_slot_base: et
} = window.__gradio__svelte__internal;
function ee(t) {
  let e;
  const o = (
    /*#slots*/
    t[22].default
  ), n = He(
    o,
    t,
    /*$$scope*/
    t[21],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(r, s) {
      n && n.m(r, s), e = !0;
    },
    p(r, s) {
      n && n.p && (!e || s & /*$$scope*/
      2097152) && et(
        n,
        o,
        r,
        /*$$scope*/
        r[21],
        e ? Ye(
          o,
          /*$$scope*/
          r[21],
          s,
          null
        ) : Je(
          /*$$scope*/
          r[21]
        ),
        null
      );
    },
    i(r) {
      e || (j(n, r), e = !0);
    },
    o(r) {
      M(n, r), e = !1;
    },
    d(r) {
      n && n.d(r);
    }
  };
}
function tt(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[0].visible && ee(t)
  );
  return {
    c() {
      n && n.c(), e = Ve();
    },
    m(r, s) {
      n && n.m(r, s), Ze(r, e, s), o = !0;
    },
    p(r, [s]) {
      /*$mergedProps*/
      r[0].visible ? n ? (n.p(r, s), s & /*$mergedProps*/
      1 && j(n, 1)) : (n = ee(r), n.c(), j(n, 1), n.m(e.parentNode, e)) : n && (Qe(), M(n, 1, 1, () => {
        n = null;
      }), Ge());
    },
    i(r) {
      o || (j(n), o = !0);
    },
    o(r) {
      M(n), o = !1;
    },
    d(r) {
      r && Ue(e), n && n.d(r);
    }
  };
}
function nt(t, e, o) {
  let n, r, s, i, l, c, {
    $$slots: d = {},
    $$scope: f
  } = e, {
    gradio: a
  } = e, {
    props: m = {}
  } = e;
  const w = p(m);
  h(t, w, (u) => o(20, c = u));
  let {
    _internal: I = {}
  } = e, {
    title: y = ""
  } = e, {
    as_item: S
  } = e, {
    visible: v = !0
  } = e, {
    elem_id: C = ""
  } = e, {
    elem_classes: E = []
  } = e, {
    elem_style: O = {}
  } = e;
  const K = oe();
  h(t, K, (u) => o(17, s = u));
  const [A, de] = Ie({
    gradio: a,
    props: c,
    _internal: I,
    visible: v,
    elem_id: C,
    elem_classes: E,
    elem_style: O,
    as_item: S,
    title: y
  });
  h(t, A, (u) => o(0, r = u));
  const B = ye();
  h(t, B, (u) => o(16, n = u));
  const fe = We(), {
    "menu.items": z,
    "dropdownProps.menu.items": T
  } = Te(["menu.items", "dropdownProps.menu.items"]);
  return h(t, z, (u) => o(19, l = u)), h(t, T, (u) => o(18, i = u)), t.$$set = (u) => {
    "gradio" in u && o(7, a = u.gradio), "props" in u && o(8, m = u.props), "_internal" in u && o(9, I = u._internal), "title" in u && o(10, y = u.title), "as_item" in u && o(11, S = u.as_item), "visible" in u && o(12, v = u.visible), "elem_id" in u && o(13, C = u.elem_id), "elem_classes" in u && o(14, E = u.elem_classes), "elem_style" in u && o(15, O = u.elem_style), "$$scope" in u && o(21, f = u.$$scope);
  }, t.$$.update = () => {
    var u, W, D, G, H, U, V, J, Y, Q, X;
    if (t.$$.dirty & /*props*/
    256 && w.update((x) => ({
      ...x,
      ...m
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, title*/
    1113728 && de({
      gradio: a,
      props: c,
      _internal: I,
      visible: v,
      elem_id: C,
      elem_classes: E,
      elem_style: O,
      as_item: S,
      title: y
    }), t.$$.dirty & /*$mergedProps, $menuItems, $slots, $dropdownMenuItems, title, $slotKey*/
    984065) {
      const x = {
        ...r.props.menu || {},
        items: (u = r.props.menu) != null && u.items || l.length > 0 ? L(l) : void 0,
        expandIcon: P(n["menu.expandIcon"], {
          clone: !0
        }) || ((W = r.props.menu) == null ? void 0 : W.expandIcon),
        overflowedIndicator: P(n["menu.overflowedIndicator"]) || ((D = r.props.menu) == null ? void 0 : D.overflowedIndicator)
      }, ae = {
        ...((G = r.props.dropdownProps) == null ? void 0 : G.menu) || {},
        items: (U = (H = r.props.dropdownProps) == null ? void 0 : H.menu) != null && U.items || i.length > 0 ? L(i) : void 0,
        expandIcon: P(n["dropdownProps.menu.expandIcon"], {
          clone: !0
        }) || ((J = (V = r.props.dropdownProps) == null ? void 0 : V.menu) == null ? void 0 : J.expandIcon),
        overflowedIndicator: P(n["dropdownProps.menu.overflowedIndicator"]) || ((Q = (Y = r.props.dropdownProps) == null ? void 0 : Y.menu) == null ? void 0 : Q.overflowedIndicator)
      }, Z = {
        ...r.props.dropdownProps || {},
        dropdownRender: Ee((X = r.props.dropdownProps) == null ? void 0 : X.dropdownRender),
        menu: Object.values(ae).filter(Boolean).length > 0 ? x : void 0
      }, $ = {
        ...r,
        props: {
          ...r.props,
          title: r.props.title || y,
          menu: Object.values(x).filter(Boolean).length > 0 ? x : void 0,
          dropdownProps: Object.values(Z).filter(Boolean).length > 0 ? Z : void 0
        }
      };
      fe(s, r._internal.index || 0, {
        props: {
          style: r.elem_style,
          className: Ae(r.elem_classes, "ms-gr-antd-breadcrumb-item"),
          id: r.elem_id,
          ...$.props,
          ...me($)
        },
        slots: {
          title: n.title
        }
      });
    }
  }, [r, w, K, A, B, z, T, a, m, I, y, S, v, C, E, O, n, s, i, l, c, f, d];
}
class it extends De {
  constructor(e) {
    super(), Xe(this, e, nt, tt, $e, {
      gradio: 7,
      props: 8,
      _internal: 9,
      title: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), _();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), _();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), _();
  }
  get title() {
    return this.$$.ctx[10];
  }
  set title(e) {
    this.$$set({
      title: e
    }), _();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), _();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), _();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), _();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), _();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), _();
  }
}
export {
  it as default
};
