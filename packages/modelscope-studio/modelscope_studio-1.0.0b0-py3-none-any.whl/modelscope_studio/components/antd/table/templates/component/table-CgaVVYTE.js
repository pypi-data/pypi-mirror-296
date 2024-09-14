import { g as fe, w as S } from "./Index-WkaFB-sw.js";
const X = window.ms_globals.React, ce = window.ms_globals.React.forwardRef, ae = window.ms_globals.React.useRef, ue = window.ms_globals.React.useEffect, v = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, y = window.ms_globals.antd.Table;
var q = {
  exports: {}
}, j = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var de = X, ge = Symbol.for("react.element"), pe = Symbol.for("react.fragment"), _e = Object.prototype.hasOwnProperty, he = de.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, we = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(n, e, l) {
  var o, i = {}, t = null, r = null;
  l !== void 0 && (t = "" + l), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (o in e) _e.call(e, o) && !we.hasOwnProperty(o) && (i[o] = e[o]);
  if (n && n.defaultProps) for (o in e = n.defaultProps, e) i[o] === void 0 && (i[o] = e[o]);
  return {
    $$typeof: ge,
    type: n,
    key: t,
    ref: r,
    props: i,
    _owner: he.current
  };
}
j.Fragment = pe;
j.jsx = K;
j.jsxs = K;
q.exports = j;
var p = q.exports;
const {
  SvelteComponent: be,
  assign: B,
  binding_callbacks: J,
  check_outros: me,
  component_subscribe: G,
  compute_slots: Ce,
  create_slot: ye,
  detach: k,
  element: Y,
  empty: Ee,
  exclude_internal_props: H,
  get_all_dirty_from_scope: Oe,
  get_slot_changes: ve,
  group_outros: Se,
  init: ke,
  insert: x,
  safe_not_equal: xe,
  set_custom_element_data: V,
  space: Ie,
  transition_in: I,
  transition_out: U,
  update_slot_base: Re
} = window.__gradio__svelte__internal, {
  beforeUpdate: je,
  getContext: Ne,
  onDestroy: Le,
  setContext: Pe
} = window.__gradio__svelte__internal;
function Q(n) {
  let e, l;
  const o = (
    /*#slots*/
    n[7].default
  ), i = ye(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = Y("svelte-slot"), i && i.c(), V(e, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      x(t, e, r), i && i.m(e, null), n[9](e), l = !0;
    },
    p(t, r) {
      i && i.p && (!l || r & /*$$scope*/
      64) && Re(
        i,
        o,
        t,
        /*$$scope*/
        t[6],
        l ? ve(
          o,
          /*$$scope*/
          t[6],
          r,
          null
        ) : Oe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (I(i, t), l = !0);
    },
    o(t) {
      U(i, t), l = !1;
    },
    d(t) {
      t && k(e), i && i.d(t), n[9](null);
    }
  };
}
function Te(n) {
  let e, l, o, i, t = (
    /*$$slots*/
    n[4].default && Q(n)
  );
  return {
    c() {
      e = Y("react-portal-target"), l = Ie(), t && t.c(), o = Ee(), V(e, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      x(r, e, s), n[8](e), x(r, l, s), t && t.m(r, s), x(r, o, s), i = !0;
    },
    p(r, [s]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, s), s & /*$$slots*/
      16 && I(t, 1)) : (t = Q(r), t.c(), I(t, 1), t.m(o.parentNode, o)) : t && (Se(), U(t, 1, 1, () => {
        t = null;
      }), me());
    },
    i(r) {
      i || (I(t), i = !0);
    },
    o(r) {
      U(t), i = !1;
    },
    d(r) {
      r && (k(e), k(l), k(o)), n[8](null), t && t.d(r);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...l
  } = n;
  return l;
}
function Fe(n, e, l) {
  let o, i, {
    $$slots: t = {},
    $$scope: r
  } = e;
  const s = Ce(t);
  let {
    svelteInit: f
  } = e;
  const g = S(W(e)), c = S();
  G(n, c, (u) => l(0, o = u));
  const a = S();
  G(n, a, (u) => l(1, i = u));
  const d = [], w = Ne("$$ms-gr-antd-react-wrapper"), {
    slotKey: N,
    slotIndex: L,
    subSlotIndex: m
  } = fe() || {}, P = f({
    parent: w,
    props: g,
    target: c,
    slot: a,
    slotKey: N,
    slotIndex: L,
    subSlotIndex: m,
    onDestroy(u) {
      d.push(u);
    }
  });
  Pe("$$ms-gr-antd-react-wrapper", P), je(() => {
    g.set(W(e));
  }), Le(() => {
    d.forEach((u) => u());
  });
  function T(u) {
    J[u ? "unshift" : "push"](() => {
      o = u, c.set(o);
    });
  }
  function C(u) {
    J[u ? "unshift" : "push"](() => {
      i = u, a.set(i);
    });
  }
  return n.$$set = (u) => {
    l(17, e = B(B({}, e), H(u))), "svelteInit" in u && l(5, f = u.svelteInit), "$$scope" in u && l(6, r = u.$$scope);
  }, e = H(e), [o, i, c, a, s, f, r, t, T, C];
}
class Me extends be {
  constructor(e) {
    super(), ke(this, e, Fe, Te, xe, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, M = window.ms_globals.tree;
function Ue(n) {
  function e(l) {
    const o = S(), i = new Me({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, s = t.parent ?? M;
          return s.nodes = [...s.nodes, r], z({
            createPortal: A,
            node: M
          }), t.onDestroy(() => {
            s.nodes = s.nodes.filter((f) => f.svelteInstance !== o), z({
              createPortal: A,
              node: M
            });
          }), r;
        },
        ...l.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(e);
    });
  });
}
const De = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((e, l) => {
    const o = n[l];
    return typeof o == "number" && !De.includes(l) ? e[l] = o + "px" : e[l] = o, e;
  }, {}) : {};
}
function Z(n) {
  const e = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: t,
      type: r,
      useCapture: s
    }) => {
      e.addEventListener(r, t, s);
    });
  });
  const l = Array.from(n.children);
  for (let o = 0; o < l.length; o++) {
    const i = l[o], t = Z(i);
    e.replaceChild(t, e.children[o]);
  }
  return e;
}
function Be(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const h = ce(({
  slot: n,
  clone: e,
  className: l,
  style: o
}, i) => {
  const t = ae();
  return ue(() => {
    var g;
    if (!t.current || !n)
      return;
    let r = n;
    function s() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Be(i, c), l && c.classList.add(...l.split(" ")), o) {
        const a = Ae(o);
        Object.keys(a).forEach((d) => {
          c.style[d] = a[d];
        });
      }
    }
    let f = null;
    if (e && window.MutationObserver) {
      let c = function() {
        var a;
        r = Z(n), r.style.display = "contents", s(), (a = t.current) == null || a.appendChild(r);
      };
      c(), f = new window.MutationObserver(() => {
        var a, d;
        (a = t.current) != null && a.contains(r) && ((d = t.current) == null || d.removeChild(r)), c();
      }), f.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", s(), (g = t.current) == null || g.appendChild(r);
    return () => {
      var c, a;
      r.style.display = "", (c = t.current) != null && c.contains(r) && ((a = t.current) == null || a.removeChild(r)), f == null || f.disconnect();
    };
  }, [n, e, l, o, i]), X.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Je(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function _(n) {
  return v(() => Je(n), [n]);
}
function R(n, e) {
  return n.filter(Boolean).map((l) => {
    if (typeof l != "object")
      return e != null && e.fallback ? e.fallback(l) : l;
    const o = {
      ...l.props
    };
    let i = o;
    Object.keys(l.slots).forEach((r) => {
      if (!l.slots[r] || !(l.slots[r] instanceof Element) && !l.slots[r].el)
        return;
      const s = r.split(".");
      s.forEach((d, w) => {
        i[d] || (i[d] = {}), w !== s.length - 1 && (i = o[d]);
      });
      const f = l.slots[r];
      let g, c, a = !1;
      f instanceof Element ? g = f : (g = f.el, c = f.callback, a = f.clone || !1), i[s[s.length - 1]] = g ? c ? (...d) => (c(s[s.length - 1], d), /* @__PURE__ */ p.jsx(h, {
        slot: g,
        clone: a || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ p.jsx(h, {
        slot: g,
        clone: a || (e == null ? void 0 : e.clone)
      }) : i[s[s.length - 1]], i = o;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return l[t] && (o[t] = R(l[t], e)), o;
  });
}
function O(n) {
  return typeof n == "object" && n !== null ? n : {};
}
const He = Ue(({
  children: n,
  slots: e,
  columnItems: l,
  columns: o,
  getPopupContainer: i,
  pagination: t,
  loading: r,
  rowKey: s,
  rowSelection: f,
  rowSelectionItems: g,
  expandableItems: c,
  expandable: a,
  sticky: d,
  showSorterTooltip: w,
  onRow: N,
  onHeaderRow: L,
  ...m
}) => {
  const P = _(i), T = e["loading.tip"] || e["loading.indicator"], C = O(r), u = e["pagination.showQuickJumper.goButton"], F = O(t), $ = _(F.showTotal), ee = _(s), te = e["showSorterTooltip.title"] || typeof w == "object", E = O(w), ne = _(E.afterOpenChange), oe = _(E.getPopupContainer), re = typeof d == "object", D = O(d), le = _(D.getContainer), ie = _(N), se = _(L);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ p.jsx(y, {
      ...m,
      columns: v(() => (o == null ? void 0 : o.map((b) => b === "EXPAND_COLUMN" ? y.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? y.SELECTION_COLUMN : b)) || R(l, {
        fallback: (b) => b === "EXPAND_COLUMN" ? y.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? y.SELECTION_COLUMN : b
      }), [l, o]),
      onRow: ie,
      onHeaderRow: se,
      rowSelection: v(() => f || R(g)[0], [f, g]),
      expandable: v(() => a || R(c)[0], [a, c]),
      rowKey: ee || s,
      sticky: re ? {
        ...D,
        getContainer: le
      } : d,
      showSorterTooltip: te ? {
        ...E,
        afterOpenChange: ne,
        getPopupContainer: oe,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ p.jsx(h, {
          slot: e["showSorterTooltip.title"]
        }) : E.title
      } : w,
      pagination: u ? {
        ...F,
        showTotal: $,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ p.jsx(h, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : F.showQuickJumper
      } : t,
      getPopupContainer: P,
      loading: T ? {
        ...C,
        tip: e["loading.tip"] ? /* @__PURE__ */ p.jsx(h, {
          slot: e["loading.tip"]
        }) : C.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ p.jsx(h, {
          slot: e["loading.indicator"]
        }) : C.indicator
      } : r,
      footer: e.footer ? () => e.footer ? /* @__PURE__ */ p.jsx(h, {
        slot: e.footer
      }) : null : m.footer,
      title: e.title ? () => e.title ? /* @__PURE__ */ p.jsx(h, {
        slot: e.title
      }) : null : m.title
    })]
  });
});
export {
  He as Table,
  He as default
};
