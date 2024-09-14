import { g as Q, w as p } from "./Index-CXaGlC1c.js";
const L = window.ms_globals.React, H = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Breadcrumb;
var N = {
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
var X = L, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(s, t, n) {
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
w.jsx = D;
w.jsxs = D;
N.exports = w;
var m = N.exports;
const {
  SvelteComponent: re,
  assign: C,
  binding_callbacks: k,
  check_outros: oe,
  component_subscribe: O,
  compute_slots: se,
  create_slot: le,
  detach: g,
  element: B,
  empty: ce,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: F,
  space: _e,
  transition_in: h,
  transition_out: E,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: ge,
  onDestroy: be,
  setContext: he
} = window.__gradio__svelte__internal;
function S(s) {
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
      t = B("svelte-slot"), l && l.c(), F(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      b(e, t, o), l && l.m(t, null), s[9](t), n = !0;
    },
    p(e, o) {
      l && l.p && (!n || o & /*$$scope*/
      64) && me(
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
      n || (h(l, e), n = !0);
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
    s[4].default && S(s)
  );
  return {
    c() {
      t = B("react-portal-target"), n = _e(), e && e.c(), r = ce(), F(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      b(o, t, c), s[8](t), b(o, n, c), e && e.m(o, c), b(o, r, c), l = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && h(e, 1)) : (e = S(o), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (ue(), E(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(o) {
      l || (h(e), l = !0);
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
  O(s, i, (u) => n(0, r = u));
  const a = p();
  O(s, a, (u) => n(1, l = u));
  const f = [], y = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T
  } = Q() || {}, U = d({
    parent: y,
    props: _,
    target: i,
    slot: a,
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T,
    onDestroy(u) {
      f.push(u);
    }
  });
  he("$$ms-gr-antd-react-wrapper", U), pe(() => {
    _.set(j(t));
  }), be(() => {
    f.forEach((u) => u());
  });
  function q(u) {
    k[u ? "unshift" : "push"](() => {
      r = u, i.set(r);
    });
  }
  function G(u) {
    k[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return s.$$set = (u) => {
    n(17, t = C(C({}, t), R(u))), "svelteInit" in u && n(5, d = u.svelteInit), "$$scope" in u && n(6, o = u.$$scope);
  }, t = R(t), [r, l, i, a, c, d, o, e, q, G];
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
function M(s) {
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
    const l = n[r], e = M(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Ce(s, t) {
  s && (typeof s == "function" ? s(t) : s.current = t);
}
const x = H(({
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
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (i = o.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ce(l, i), n && i.classList.add(...n.split(" ")), r) {
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
        o = M(s), o.style.display = "contents", c(), (a = e.current) == null || a.appendChild(o);
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
  }, [s, t, n, r, l]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function W(s, t) {
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
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), l[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(x, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(x, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = r;
    });
    const e = "children";
    return n[e] && (r[e] = W(n[e], t)), r;
  });
}
const Oe = Ee(({
  slots: s,
  items: t,
  slotItems: n,
  children: r,
  ...l
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: r
  }), /* @__PURE__ */ m.jsx(V, {
    ...l,
    items: K(() => t || W(n), [t, n]),
    separator: s.separator ? /* @__PURE__ */ m.jsx(x, {
      slot: s.separator,
      clone: !0
    }) : l.separator
  })]
}));
export {
  Oe as Breadcrumb,
  Oe as default
};
