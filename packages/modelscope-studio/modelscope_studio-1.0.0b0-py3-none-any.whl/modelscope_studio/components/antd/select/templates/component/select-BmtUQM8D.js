import { g as te, w as p } from "./Index-Cp45H5WP.js";
const A = window.ms_globals.React, Z = window.ms_globals.React.forwardRef, $ = window.ms_globals.React.useRef, ee = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Select;
var q = {
  exports: {}
}, y = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var re = A, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, e, o) {
  var l, s = {}, t = null, r = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (l in e) se.call(e, l) && !ie.hasOwnProperty(l) && (s[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) s[l] === void 0 && (s[l] = e[l]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: r,
    props: s,
    _owner: ce.current
  };
}
y.Fragment = le;
y.jsx = G;
y.jsxs = G;
q.exports = y;
var m = q.exports;
const {
  SvelteComponent: ae,
  assign: L,
  binding_callbacks: N,
  check_outros: ue,
  component_subscribe: T,
  compute_slots: de,
  create_slot: fe,
  detach: I,
  element: H,
  empty: _e,
  exclude_internal_props: D,
  get_all_dirty_from_scope: me,
  get_slot_changes: ge,
  group_outros: we,
  init: be,
  insert: v,
  safe_not_equal: he,
  set_custom_element_data: B,
  space: pe,
  transition_in: x,
  transition_out: j,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: ve,
  getContext: xe,
  onDestroy: ye,
  setContext: Ce
} = window.__gradio__svelte__internal;
function M(n) {
  let e, o;
  const l = (
    /*#slots*/
    n[7].default
  ), s = fe(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = H("svelte-slot"), s && s.c(), B(e, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      v(t, e, r), s && s.m(e, null), n[9](e), o = !0;
    },
    p(t, r) {
      s && s.p && (!o || r & /*$$scope*/
      64) && Ie(
        s,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? ge(
          l,
          /*$$scope*/
          t[6],
          r,
          null
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (x(s, t), o = !0);
    },
    o(t) {
      j(s, t), o = !1;
    },
    d(t) {
      t && I(e), s && s.d(t), n[9](null);
    }
  };
}
function Re(n) {
  let e, o, l, s, t = (
    /*$$slots*/
    n[4].default && M(n)
  );
  return {
    c() {
      e = H("react-portal-target"), o = pe(), t && t.c(), l = _e(), B(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      v(r, e, c), n[8](e), v(r, o, c), t && t.m(r, c), v(r, l, c), s = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, c), c & /*$$slots*/
      16 && x(t, 1)) : (t = M(r), t.c(), x(t, 1), t.m(l.parentNode, l)) : t && (we(), j(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(r) {
      s || (x(t), s = !0);
    },
    o(r) {
      j(t), s = !1;
    },
    d(r) {
      r && (I(e), I(o), I(l)), n[8](null), t && t.d(r);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function Se(n, e, o) {
  let l, s, {
    $$slots: t = {},
    $$scope: r
  } = e;
  const c = de(t);
  let {
    svelteInit: d
  } = e;
  const _ = p(W(e)), i = p();
  T(n, i, (u) => o(0, l = u));
  const a = p();
  T(n, a, (u) => o(1, s = u));
  const f = [], h = xe("$$ms-gr-antd-react-wrapper"), {
    slotKey: C,
    slotIndex: g,
    subSlotIndex: R
  } = te() || {}, S = d({
    parent: h,
    props: _,
    target: i,
    slot: a,
    slotKey: C,
    slotIndex: g,
    subSlotIndex: R,
    onDestroy(u) {
      f.push(u);
    }
  });
  Ce("$$ms-gr-antd-react-wrapper", S), ve(() => {
    _.set(W(e));
  }), ye(() => {
    f.forEach((u) => u());
  });
  function E(u) {
    N[u ? "unshift" : "push"](() => {
      l = u, i.set(l);
    });
  }
  function k(u) {
    N[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  return n.$$set = (u) => {
    o(17, e = L(L({}, e), D(u))), "svelteInit" in u && o(5, d = u.svelteInit), "$$scope" in u && o(6, r = u.$$scope);
  }, e = D(e), [l, s, i, a, c, d, r, t, E, k];
}
class Ee extends ae {
  constructor(e) {
    super(), be(this, e, Se, Re, he, {
      svelteInit: 5
    });
  }
}
const z = window.ms_globals.rerender, O = window.ms_globals.tree;
function ke(n) {
  function e(o) {
    const l = p(), s = new Ee({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? O;
          return c.nodes = [...c.nodes, r], z({
            createPortal: P,
            node: O
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== l), z({
              createPortal: P,
              node: O
            });
          }), r;
        },
        ...o.props
      }
    });
    return l.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const l = n[o];
    return typeof l == "number" && !Oe.includes(o) ? e[o] = l + "px" : e[o] = l, e;
  }, {}) : {};
}
function J(n) {
  const e = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: t,
      type: r,
      useCapture: c
    }) => {
      e.addEventListener(r, t, c);
    });
  });
  const o = Array.from(n.children);
  for (let l = 0; l < o.length; l++) {
    const s = o[l], t = J(s);
    e.replaceChild(t, e.children[l]);
  }
  return e;
}
function Fe(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const b = Z(({
  slot: n,
  clone: e,
  className: o,
  style: l
}, s) => {
  const t = $();
  return ee(() => {
    var _;
    if (!t.current || !n)
      return;
    let r = n;
    function c() {
      let i = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (i = r.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Fe(s, i), o && i.classList.add(...o.split(" ")), l) {
        const a = je(l);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var a;
        r = J(n), r.style.display = "contents", c(), (a = t.current) == null || a.appendChild(r);
      };
      i(), d = new window.MutationObserver(() => {
        var a, f;
        (a = t.current) != null && a.contains(r) && ((f = t.current) == null || f.removeChild(r)), i();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", c(), (_ = t.current) == null || _.appendChild(r);
    return () => {
      var i, a;
      r.style.display = "", (i = t.current) != null && i.contains(r) && ((a = t.current) == null || a.removeChild(r)), d == null || d.disconnect();
    };
  }, [n, e, o, l, s]), A.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Pe(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function w(n) {
  return U(() => Pe(n), [n]);
}
function Y(n, e) {
  return n.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return e != null && e.fallback ? e.fallback(o) : o;
    const l = {
      ...o.props
    };
    let s = l;
    Object.keys(o.slots).forEach((r) => {
      if (!o.slots[r] || !(o.slots[r] instanceof Element) && !o.slots[r].el)
        return;
      const c = r.split(".");
      c.forEach((f, h) => {
        s[f] || (s[f] = {}), h !== c.length - 1 && (s = l[f]);
      });
      const d = o.slots[r];
      let _, i, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(b, {
        slot: _,
        clone: a || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ m.jsx(b, {
        slot: _,
        clone: a || (e == null ? void 0 : e.clone)
      }) : s[c[c.length - 1]], s = l;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return o[t] && (l[t] = Y(o[t], e)), l;
  });
}
const Ne = ke(({
  slots: n,
  children: e,
  onValueChange: o,
  filterOption: l,
  onChange: s,
  options: t,
  optionItems: r,
  getPopupContainer: c,
  dropdownRender: d,
  optionRender: _,
  tagRender: i,
  labelRender: a,
  filterSort: f,
  maxTagPlaceholder: h,
  elRef: C,
  ...g
}) => {
  const R = w(c), S = w(l), E = w(d), k = w(f), u = w(_), K = w(i), Q = w(a), V = w(h);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ m.jsx(ne, {
      ...g,
      ref: C,
      options: U(() => t || Y(r, {
        children: "options",
        clone: !0
      }), [r, t]),
      onChange: (F, ...X) => {
        s == null || s(F, ...X), o(F);
      },
      allowClear: n["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(b, {
          slot: n["allowClear.clearIcon"]
        })
      } : g.allowClear,
      removeIcon: n.removeIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: n.removeIcon
      }) : g.removeIcon,
      suffixIcon: n.suffixIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: n.suffixIcon
      }) : g.suffixIcon,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ m.jsx(b, {
        slot: n.notFoundContent
      }) : g.notFoundContent,
      menuItemSelectedIcon: n.menuItemSelectedIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: n.menuItemSelectedIcon
      }) : g.menuItemSelectedIcon,
      filterOption: S || l,
      maxTagPlaceholder: V || (n.maxTagPlaceholder ? /* @__PURE__ */ m.jsx(b, {
        slot: n.maxTagPlaceholder
      }) : h),
      getPopupContainer: R,
      dropdownRender: E,
      optionRender: u,
      tagRender: K,
      labelRender: Q,
      filterSort: k
    })]
  });
});
export {
  Ne as Select,
  Ne as default
};
