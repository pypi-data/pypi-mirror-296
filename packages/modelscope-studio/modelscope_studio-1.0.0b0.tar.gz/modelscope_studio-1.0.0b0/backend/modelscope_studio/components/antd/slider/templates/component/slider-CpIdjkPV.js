import { g as Q, w as p } from "./Index-C8a23pPN.js";
const L = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, N = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Slider;
var v = {
  exports: {}
}, h = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var X = L, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(r, n, t) {
  var s, l = {}, e = null, o = null;
  t !== void 0 && (e = "" + t), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (s in n) ee.call(n, s) && !ne.hasOwnProperty(s) && (l[s] = n[s]);
  if (r && r.defaultProps) for (s in n = r.defaultProps, n) l[s] === void 0 && (l[s] = n[s]);
  return {
    $$typeof: Z,
    type: r,
    key: e,
    ref: o,
    props: l,
    _owner: te.current
  };
}
h.Fragment = $;
h.jsx = D;
h.jsxs = D;
v.exports = h;
var m = v.exports;
const {
  SvelteComponent: re,
  assign: S,
  binding_callbacks: C,
  check_outros: oe,
  component_subscribe: I,
  compute_slots: se,
  create_slot: le,
  detach: g,
  element: M,
  empty: ie,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: W,
  space: _e,
  transition_in: w,
  transition_out: x,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: ge,
  onDestroy: be,
  setContext: we
} = window.__gradio__svelte__internal;
function k(r) {
  let n, t;
  const s = (
    /*#slots*/
    r[7].default
  ), l = le(
    s,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      n = M("svelte-slot"), l && l.c(), W(n, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      b(e, n, o), l && l.m(n, null), r[9](n), t = !0;
    },
    p(e, o) {
      l && l.p && (!t || o & /*$$scope*/
      64) && me(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        t ? ae(
          s,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ce(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      t || (w(l, e), t = !0);
    },
    o(e) {
      x(l, e), t = !1;
    },
    d(e) {
      e && g(n), l && l.d(e), r[9](null);
    }
  };
}
function he(r) {
  let n, t, s, l, e = (
    /*$$slots*/
    r[4].default && k(r)
  );
  return {
    c() {
      n = M("react-portal-target"), t = _e(), e && e.c(), s = ie(), W(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      b(o, n, i), r[8](n), b(o, t, i), e && e.m(o, i), b(o, s, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && w(e, 1)) : (e = k(o), e.c(), w(e, 1), e.m(s.parentNode, s)) : e && (ue(), x(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(o) {
      l || (w(e), l = !0);
    },
    o(o) {
      x(e), l = !1;
    },
    d(o) {
      o && (g(n), g(t), g(s)), r[8](null), e && e.d(o);
    }
  };
}
function O(r) {
  const {
    svelteInit: n,
    ...t
  } = r;
  return t;
}
function ye(r, n, t) {
  let s, l, {
    $$slots: e = {},
    $$scope: o
  } = n;
  const i = se(e);
  let {
    svelteInit: d
  } = n;
  const _ = p(O(n)), c = p();
  I(r, c, (u) => t(0, s = u));
  const a = p();
  I(r, a, (u) => t(1, l = u));
  const f = [], A = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: G,
    slotIndex: T,
    subSlotIndex: U
  } = Q() || {}, q = d({
    parent: A,
    props: _,
    target: c,
    slot: a,
    slotKey: G,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(u) {
      f.push(u);
    }
  });
  we("$$ms-gr-antd-react-wrapper", q), pe(() => {
    _.set(O(n));
  }), be(() => {
    f.forEach((u) => u());
  });
  function H(u) {
    C[u ? "unshift" : "push"](() => {
      s = u, c.set(s);
    });
  }
  function K(u) {
    C[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return r.$$set = (u) => {
    t(17, n = S(S({}, n), R(u))), "svelteInit" in u && t(5, d = u.svelteInit), "$$scope" in u && t(6, o = u.$$scope);
  }, n = R(n), [s, l, c, a, i, d, o, e, H, K];
}
class xe extends re {
  constructor(n) {
    super(), de(this, n, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, y = window.ms_globals.tree;
function Ee(r) {
  function n(t) {
    const s = p(), l = new xe({
      ...t,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? y;
          return i.nodes = [...i.nodes, o], P({
            createPortal: E,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== s), P({
              createPortal: E,
              node: y
            });
          }), o;
        },
        ...t.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((t) => {
    window.ms_globals.initializePromise.then(() => {
      t(n);
    });
  });
}
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ce(r) {
  return r ? Object.keys(r).reduce((n, t) => {
    const s = r[t];
    return typeof s == "number" && !Se.includes(t) ? n[t] = s + "px" : n[t] = s, n;
  }, {}) : {};
}
function z(r) {
  const n = r.cloneNode(!0);
  Object.keys(r.getEventListeners()).forEach((s) => {
    r.getEventListeners(s).forEach(({
      listener: e,
      type: o,
      useCapture: i
    }) => {
      n.addEventListener(o, e, i);
    });
  });
  const t = Array.from(r.children);
  for (let s = 0; s < t.length; s++) {
    const l = t[s], e = z(l);
    n.replaceChild(e, n.children[s]);
  }
  return n;
}
function Ie(r, n) {
  r && (typeof r == "function" ? r(n) : r.current = n);
}
const j = B(({
  slot: r,
  clone: n,
  className: t,
  style: s
}, l) => {
  const e = J();
  return Y(() => {
    var _;
    if (!e.current || !r)
      return;
    let o = r;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ie(l, c), t && c.classList.add(...t.split(" ")), s) {
        const a = Ce(s);
        Object.keys(a).forEach((f) => {
          c.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var a;
        o = z(r), o.style.display = "contents", i(), (a = e.current) == null || a.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(o) && ((f = e.current) == null || f.removeChild(o)), c();
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(o);
    return () => {
      var c, a;
      o.style.display = "", (c = e.current) != null && c.contains(o) && ((a = e.current) == null || a.removeChild(o)), d == null || d.disconnect();
    };
  }, [r, n, t, s, l]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Re(r) {
  try {
    return typeof r == "string" ? new Function(`return (...args) => (${r})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function F(r) {
  return N(() => Re(r), [r]);
}
const ke = (r) => r.reduce((n, t) => {
  const s = t == null ? void 0 : t.props.number;
  return s !== void 0 && (n[s] = (t == null ? void 0 : t.slots.label) instanceof Element ? {
    ...t.props,
    label: /* @__PURE__ */ m.jsx(j, {
      slot: t == null ? void 0 : t.slots.label
    })
  } : (t == null ? void 0 : t.slots.children) instanceof Element ? /* @__PURE__ */ m.jsx(j, {
    slot: t == null ? void 0 : t.slots.children
  }) : {
    ...t == null ? void 0 : t.props
  }), n;
}, {}), Pe = Ee(({
  marks: r,
  markItems: n,
  children: t,
  onValueChange: s,
  onChange: l,
  elRef: e,
  tooltip: o,
  ...i
}) => {
  const d = (a) => {
    l == null || l(a), s(a);
  }, _ = F(o == null ? void 0 : o.getPopupContainer), c = F(o == null ? void 0 : o.formatter);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ m.jsx(V, {
      ...i,
      tooltip: {
        ...o,
        getPopupContainer: _,
        formatter: c
      },
      marks: N(() => r || ke(n), [n, r]),
      ref: e,
      onChange: d
    })]
  });
});
export {
  Pe as Slider,
  Pe as default
};
