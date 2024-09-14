import { g as Q, w as p } from "./Index-DrUsuILH.js";
const L = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, x = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Segmented;
var N = {
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
function D(l, t, r) {
  var o, s = {}, e = null, n = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (o in t) ee.call(t, o) && !ne.hasOwnProperty(o) && (s[o] = t[o]);
  if (l && l.defaultProps) for (o in t = l.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: Z,
    type: l,
    key: e,
    ref: n,
    props: s,
    _owner: te.current
  };
}
h.Fragment = $;
h.jsx = D;
h.jsxs = D;
N.exports = h;
var m = N.exports;
const {
  SvelteComponent: re,
  assign: I,
  binding_callbacks: S,
  check_outros: oe,
  component_subscribe: k,
  compute_slots: le,
  create_slot: se,
  detach: g,
  element: F,
  empty: ce,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: M,
  space: _e,
  transition_in: w,
  transition_out: E,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: ge,
  onDestroy: be,
  setContext: we
} = window.__gradio__svelte__internal;
function R(l) {
  let t, r;
  const o = (
    /*#slots*/
    l[7].default
  ), s = se(
    o,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = F("svelte-slot"), s && s.c(), M(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      b(e, t, n), s && s.m(t, null), l[9](t), r = !0;
    },
    p(e, n) {
      s && s.p && (!r || n & /*$$scope*/
      64) && me(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? ae(
          o,
          /*$$scope*/
          e[6],
          n,
          null
        ) : ie(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (w(s, e), r = !0);
    },
    o(e) {
      E(s, e), r = !1;
    },
    d(e) {
      e && g(t), s && s.d(e), l[9](null);
    }
  };
}
function he(l) {
  let t, r, o, s, e = (
    /*$$slots*/
    l[4].default && R(l)
  );
  return {
    c() {
      t = F("react-portal-target"), r = _e(), e && e.c(), o = ce(), M(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      b(n, t, c), l[8](t), b(n, r, c), e && e.m(n, c), b(n, o, c), s = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, c), c & /*$$slots*/
      16 && w(e, 1)) : (e = R(n), e.c(), w(e, 1), e.m(o.parentNode, o)) : e && (ue(), E(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(n) {
      s || (w(e), s = !0);
    },
    o(n) {
      E(e), s = !1;
    },
    d(n) {
      n && (g(t), g(r), g(o)), l[8](null), e && e.d(n);
    }
  };
}
function C(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function ye(l, t, r) {
  let o, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const c = le(e);
  let {
    svelteInit: d
  } = t;
  const _ = p(C(t)), i = p();
  k(l, i, (u) => r(0, o = u));
  const a = p();
  k(l, a, (u) => r(1, s = u));
  const f = [], y = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U
  } = Q() || {}, q = d({
    parent: y,
    props: _,
    target: i,
    slot: a,
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(u) {
      f.push(u);
    }
  });
  we("$$ms-gr-antd-react-wrapper", q), pe(() => {
    _.set(C(t));
  }), be(() => {
    f.forEach((u) => u());
  });
  function G(u) {
    S[u ? "unshift" : "push"](() => {
      o = u, i.set(o);
    });
  }
  function H(u) {
    S[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  return l.$$set = (u) => {
    r(17, t = I(I({}, t), O(u))), "svelteInit" in u && r(5, d = u.svelteInit), "$$scope" in u && r(6, n = u.$$scope);
  }, t = O(t), [o, s, i, a, c, d, n, e, G, H];
}
class ve extends re {
  constructor(t) {
    super(), de(this, t, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ee(l) {
  function t(r) {
    const o = p(), s = new ve({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? v;
          return c.nodes = [...c.nodes, n], j({
            createPortal: x,
            node: v
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== o), j({
              createPortal: x,
              node: v
            });
          }), n;
        },
        ...r.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(l) {
  return l ? Object.keys(l).reduce((t, r) => {
    const o = l[r];
    return typeof o == "number" && !xe.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function W(l) {
  const t = l.cloneNode(!0);
  Object.keys(l.getEventListeners()).forEach((o) => {
    l.getEventListeners(o).forEach(({
      listener: e,
      type: n,
      useCapture: c
    }) => {
      t.addEventListener(n, e, c);
    });
  });
  const r = Array.from(l.children);
  for (let o = 0; o < r.length; o++) {
    const s = r[o], e = W(s);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Se(l, t) {
  l && (typeof l == "function" ? l(t) : l.current = t);
}
const P = B(({
  slot: l,
  clone: t,
  className: r,
  style: o
}, s) => {
  const e = J();
  return Y(() => {
    var _;
    if (!e.current || !l)
      return;
    let n = l;
    function c() {
      let i = n;
      if (n.tagName.toLowerCase() === "svelte-slot" && n.children.length === 1 && n.children[0] && (i = n.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Se(s, i), r && i.classList.add(...r.split(" ")), o) {
        const a = Ie(o);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        n = W(l), n.style.display = "contents", c(), (a = e.current) == null || a.appendChild(n);
      };
      i(), d = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(n) && ((f = e.current) == null || f.removeChild(n)), i();
      }), d.observe(l, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      n.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(n);
    return () => {
      var i, a;
      n.style.display = "", (i = e.current) != null && i.contains(n) && ((a = e.current) == null || a.removeChild(n)), d == null || d.disconnect();
    };
  }, [l, t, r, o, s]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function z(l, t) {
  return l.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const o = {
      ...r.props
    };
    let s = o;
    Object.keys(r.slots).forEach((n) => {
      if (!r.slots[n] || !(r.slots[n] instanceof Element) && !r.slots[n].el)
        return;
      const c = n.split(".");
      c.forEach((f, y) => {
        s[f] || (s[f] = {}), y !== c.length - 1 && (s = o[f]);
      });
      const d = r.slots[n];
      let _, i, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(P, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(P, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = o;
    });
    const e = "children";
    return r[e] && (o[e] = z(r[e], t)), o;
  });
}
const Oe = Ee(({
  slotItems: l,
  options: t,
  onChange: r,
  onValueChange: o,
  children: s,
  ...e
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: s
  }), /* @__PURE__ */ m.jsx(V, {
    ...e,
    onChange: (n) => {
      r == null || r(n), o(n);
    },
    options: K(() => t || z(l), [t, l])
  })]
}));
export {
  Oe as Segmented,
  Oe as default
};
