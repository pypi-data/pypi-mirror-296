import { g as Q, w as p } from "./Index-veqZcu1T.js";
const L = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Checkbox;
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
function D(l, t, o) {
  var r, s = {}, e = null, n = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (r in t) ee.call(t, r) && !ne.hasOwnProperty(r) && (s[r] = t[r]);
  if (l && l.defaultProps) for (r in t = l.defaultProps, t) s[r] === void 0 && (s[r] = t[r]);
  return {
    $$typeof: Z,
    type: l,
    key: e,
    ref: n,
    props: s,
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
  assign: k,
  binding_callbacks: I,
  check_outros: oe,
  component_subscribe: C,
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
  set_custom_element_data: G,
  space: _e,
  transition_in: h,
  transition_out: x,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: ge,
  onDestroy: be,
  setContext: he
} = window.__gradio__svelte__internal;
function R(l) {
  let t, o;
  const r = (
    /*#slots*/
    l[7].default
  ), s = se(
    r,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = F("svelte-slot"), s && s.c(), G(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      b(e, t, n), s && s.m(t, null), l[9](t), o = !0;
    },
    p(e, n) {
      s && s.p && (!o || n & /*$$scope*/
      64) && me(
        s,
        r,
        e,
        /*$$scope*/
        e[6],
        o ? ae(
          r,
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
      o || (h(s, e), o = !0);
    },
    o(e) {
      x(s, e), o = !1;
    },
    d(e) {
      e && g(t), s && s.d(e), l[9](null);
    }
  };
}
function we(l) {
  let t, o, r, s, e = (
    /*$$slots*/
    l[4].default && R(l)
  );
  return {
    c() {
      t = F("react-portal-target"), o = _e(), e && e.c(), r = ce(), G(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      b(n, t, c), l[8](t), b(n, o, c), e && e.m(n, c), b(n, r, c), s = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, c), c & /*$$slots*/
      16 && h(e, 1)) : (e = R(n), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (ue(), x(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(n) {
      s || (h(e), s = !0);
    },
    o(n) {
      x(e), s = !1;
    },
    d(n) {
      n && (g(t), g(o), g(r)), l[8](null), e && e.d(n);
    }
  };
}
function S(l) {
  const {
    svelteInit: t,
    ...o
  } = l;
  return o;
}
function ye(l, t, o) {
  let r, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const c = le(e);
  let {
    svelteInit: d
  } = t;
  const _ = p(S(t)), i = p();
  C(l, i, (u) => o(0, r = u));
  const a = p();
  C(l, a, (u) => o(1, s = u));
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
    _.set(S(t));
  }), be(() => {
    f.forEach((u) => u());
  });
  function q(u) {
    I[u ? "unshift" : "push"](() => {
      r = u, i.set(r);
    });
  }
  function H(u) {
    I[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  return l.$$set = (u) => {
    o(17, t = k(k({}, t), O(u))), "svelteInit" in u && o(5, d = u.svelteInit), "$$scope" in u && o(6, n = u.$$scope);
  }, t = O(t), [r, s, i, a, c, d, n, e, q, H];
}
class ve extends re {
  constructor(t) {
    super(), de(this, t, ye, we, fe, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function xe(l) {
  function t(o) {
    const r = p(), s = new ve({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
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
            createPortal: E,
            node: v
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== r), j({
              createPortal: E,
              node: v
            });
          }), n;
        },
        ...o.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const Ee = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(l) {
  return l ? Object.keys(l).reduce((t, o) => {
    const r = l[o];
    return typeof r == "number" && !Ee.includes(o) ? t[o] = r + "px" : t[o] = r, t;
  }, {}) : {};
}
function M(l) {
  const t = l.cloneNode(!0);
  Object.keys(l.getEventListeners()).forEach((r) => {
    l.getEventListeners(r).forEach(({
      listener: e,
      type: n,
      useCapture: c
    }) => {
      t.addEventListener(n, e, c);
    });
  });
  const o = Array.from(l.children);
  for (let r = 0; r < o.length; r++) {
    const s = o[r], e = M(s);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Ie(l, t) {
  l && (typeof l == "function" ? l(t) : l.current = t);
}
const P = B(({
  slot: l,
  clone: t,
  className: o,
  style: r
}, s) => {
  const e = J();
  return Y(() => {
    var _;
    if (!e.current || !l)
      return;
    let n = l;
    function c() {
      let i = n;
      if (n.tagName.toLowerCase() === "svelte-slot" && n.children.length === 1 && n.children[0] && (i = n.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ie(s, i), o && i.classList.add(...o.split(" ")), r) {
        const a = ke(r);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        n = M(l), n.style.display = "contents", c(), (a = e.current) == null || a.appendChild(n);
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
  }, [l, t, o, r, s]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function W(l, t) {
  return l.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const r = {
      ...o.props
    };
    let s = r;
    Object.keys(o.slots).forEach((n) => {
      if (!o.slots[n] || !(o.slots[n] instanceof Element) && !o.slots[n].el)
        return;
      const c = n.split(".");
      c.forEach((f, y) => {
        s[f] || (s[f] = {}), y !== c.length - 1 && (s = r[f]);
      });
      const d = o.slots[n];
      let _, i, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(P, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(P, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = r;
    });
    const e = "children";
    return o[e] && (r[e] = W(o[e], t)), r;
  });
}
const Oe = xe(({
  onValueChange: l,
  onChange: t,
  elRef: o,
  optionItems: r,
  options: s,
  children: e,
  ...n
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: e
  }), /* @__PURE__ */ m.jsx(V.Group, {
    ...n,
    ref: o,
    options: K(() => s || W(r), [r, s]),
    onChange: (c) => {
      t == null || t(c), l(c);
    }
  })]
}));
export {
  Oe as CheckboxGroup,
  Oe as default
};
