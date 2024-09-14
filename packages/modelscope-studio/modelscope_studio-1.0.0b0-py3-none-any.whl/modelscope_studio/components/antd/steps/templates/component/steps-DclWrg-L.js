import { g as Q, w as p } from "./Index-BXJ-h8YF.js";
const D = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Steps;
var L = {
  exports: {}
}, w = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var X = D, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(s, t, n) {
  var r, l = {}, e = null, o = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) ee.call(t, r) && !ne.hasOwnProperty(r) && (l[r] = t[r]);
  if (s && s.defaultProps) for (r in t = s.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: Z,
    type: s,
    key: e,
    ref: o,
    props: l,
    _owner: te.current
  };
}
w.Fragment = $;
w.jsx = N;
w.jsxs = N;
L.exports = w;
var h = L.exports;
const {
  SvelteComponent: re,
  assign: S,
  binding_callbacks: C,
  check_outros: oe,
  component_subscribe: k,
  compute_slots: se,
  create_slot: le,
  detach: g,
  element: M,
  empty: ce,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: m,
  safe_not_equal: fe,
  set_custom_element_data: W,
  space: _e,
  transition_in: b,
  transition_out: E,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: me,
  onDestroy: be,
  setContext: he
} = window.__gradio__svelte__internal;
function R(s) {
  let t, n;
  const r = (
    /*#slots*/
    s[7].default
  ), l = le(
    r,
    s,
    /*$$scope*/
    s[6],
    null
  );
  return {
    c() {
      t = M("svelte-slot"), l && l.c(), W(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      m(e, t, o), l && l.m(t, null), s[9](t), n = !0;
    },
    p(e, o) {
      l && l.p && (!n || o & /*$$scope*/
      64) && pe(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        n ? ae(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ie(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (b(l, e), n = !0);
    },
    o(e) {
      E(l, e), n = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), s[9](null);
    }
  };
}
function we(s) {
  let t, n, r, l, e = (
    /*$$slots*/
    s[4].default && R(s)
  );
  return {
    c() {
      t = M("react-portal-target"), n = _e(), e && e.c(), r = ce(), W(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      m(o, t, c), s[8](t), m(o, n, c), e && e.m(o, c), m(o, r, c), l = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && b(e, 1)) : (e = R(o), e.c(), b(e, 1), e.m(r.parentNode, r)) : e && (ue(), E(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(o) {
      l || (b(e), l = !0);
    },
    o(o) {
      E(e), l = !1;
    },
    d(o) {
      o && (g(t), g(n), g(r)), s[8](null), e && e.d(o);
    }
  };
}
function j(s) {
  const {
    svelteInit: t,
    ...n
  } = s;
  return n;
}
function ye(s, t, n) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = se(e);
  let {
    svelteInit: d
  } = t;
  const _ = p(j(t)), i = p();
  k(s, i, (u) => n(0, r = u));
  const a = p();
  k(s, a, (u) => n(1, l = u));
  const f = [], y = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: F,
    slotIndex: T,
    subSlotIndex: U
  } = Q() || {}, q = d({
    parent: y,
    props: _,
    target: i,
    slot: a,
    slotKey: F,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(u) {
      f.push(u);
    }
  });
  he("$$ms-gr-antd-react-wrapper", q), ge(() => {
    _.set(j(t));
  }), be(() => {
    f.forEach((u) => u());
  });
  function G(u) {
    C[u ? "unshift" : "push"](() => {
      r = u, i.set(r);
    });
  }
  function H(u) {
    C[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return s.$$set = (u) => {
    n(17, t = S(S({}, t), O(u))), "svelteInit" in u && n(5, d = u.svelteInit), "$$scope" in u && n(6, o = u.$$scope);
  }, t = O(t), [r, l, i, a, c, d, o, e, G, H];
}
class ve extends re {
  constructor(t) {
    super(), de(this, t, ye, we, fe, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ee(s) {
  function t(n) {
    const r = p(), l = new ve({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: s,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? v;
          return c.nodes = [...c.nodes, o], P({
            createPortal: I,
            node: v
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== r), P({
              createPortal: I,
              node: v
            });
          }), o;
        },
        ...n.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(s) {
  return s ? Object.keys(s).reduce((t, n) => {
    const r = s[n];
    return typeof r == "number" && !xe.includes(n) ? t[n] = r + "px" : t[n] = r, t;
  }, {}) : {};
}
function z(s) {
  const t = s.cloneNode(!0);
  Object.keys(s.getEventListeners()).forEach((r) => {
    s.getEventListeners(r).forEach(({
      listener: e,
      type: o,
      useCapture: c
    }) => {
      t.addEventListener(o, e, c);
    });
  });
  const n = Array.from(s.children);
  for (let r = 0; r < n.length; r++) {
    const l = n[r], e = z(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Se(s, t) {
  s && (typeof s == "function" ? s(t) : s.current = t);
}
const x = B(({
  slot: s,
  clone: t,
  className: n,
  style: r
}, l) => {
  const e = J();
  return Y(() => {
    var _;
    if (!e.current || !s)
      return;
    let o = s;
    function c() {
      let i = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (i = o.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Se(l, i), n && i.classList.add(...n.split(" ")), r) {
        const a = Ie(r);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        o = z(s), o.style.display = "contents", c(), (a = e.current) == null || a.appendChild(o);
      };
      i(), d = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(o) && ((f = e.current) == null || f.removeChild(o)), i();
      }), d.observe(s, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(o);
    return () => {
      var i, a;
      o.style.display = "", (i = e.current) != null && i.contains(o) && ((a = e.current) == null || a.removeChild(o)), d == null || d.disconnect();
    };
  }, [s, t, n, r, l]), D.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function A(s, t) {
  return s.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return n;
    const r = {
      ...n.props
    };
    let l = r;
    Object.keys(n.slots).forEach((o) => {
      if (!n.slots[o] || !(n.slots[o] instanceof Element) && !n.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((f, y) => {
        l[f] || (l[f] = {}), y !== c.length - 1 && (l = r[f]);
      });
      const d = n.slots[o];
      let _, i, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), l[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ h.jsx(x, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ h.jsx(x, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = r;
    });
    const e = "children";
    return n[e] && (r[e] = A(n[e], t)), r;
  });
}
const ke = Ee(({
  slots: s,
  items: t,
  slotItems: n,
  ...r
}) => /* @__PURE__ */ h.jsx(V, {
  ...r,
  items: K(() => t || A(n), [t, n]),
  progressDot: s.progressDot ? (l) => s.progressDot ? /* @__PURE__ */ h.jsx(x, {
    slot: s.progressDot
  }) : l : void 0
}));
export {
  ke as Steps,
  ke as default
};
