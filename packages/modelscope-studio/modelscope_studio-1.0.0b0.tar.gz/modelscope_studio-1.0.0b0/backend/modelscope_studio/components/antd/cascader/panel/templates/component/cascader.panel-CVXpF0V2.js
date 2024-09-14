import { g as Q, w as p } from "./Index-Be6dfZoQ.js";
const L = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Cascader;
var F = {
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
var X = L, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(o, t, l) {
  var r, s = {}, e = null, n = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (r in t) ee.call(t, r) && !ne.hasOwnProperty(r) && (s[r] = t[r]);
  if (o && o.defaultProps) for (r in t = o.defaultProps, t) s[r] === void 0 && (s[r] = t[r]);
  return {
    $$typeof: Z,
    type: o,
    key: e,
    ref: n,
    props: s,
    _owner: te.current
  };
}
y.Fragment = $;
y.jsx = N;
y.jsxs = N;
F.exports = y;
var m = F.exports;
const {
  SvelteComponent: re,
  assign: C,
  binding_callbacks: k,
  check_outros: oe,
  component_subscribe: O,
  compute_slots: le,
  create_slot: se,
  detach: g,
  element: D,
  empty: ce,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ie,
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
function S(o) {
  let t, l;
  const r = (
    /*#slots*/
    o[7].default
  ), s = se(
    r,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), s && s.c(), M(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      b(e, t, n), s && s.m(t, null), o[9](t), l = !0;
    },
    p(e, n) {
      s && s.p && (!l || n & /*$$scope*/
      64) && me(
        s,
        r,
        e,
        /*$$scope*/
        e[6],
        l ? ie(
          r,
          /*$$scope*/
          e[6],
          n,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (w(s, e), l = !0);
    },
    o(e) {
      E(s, e), l = !1;
    },
    d(e) {
      e && g(t), s && s.d(e), o[9](null);
    }
  };
}
function he(o) {
  let t, l, r, s, e = (
    /*$$slots*/
    o[4].default && S(o)
  );
  return {
    c() {
      t = D("react-portal-target"), l = _e(), e && e.c(), r = ce(), M(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      b(n, t, c), o[8](t), b(n, l, c), e && e.m(n, c), b(n, r, c), s = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, c), c & /*$$slots*/
      16 && w(e, 1)) : (e = S(n), e.c(), w(e, 1), e.m(r.parentNode, r)) : e && (ue(), E(e, 1, 1, () => {
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
      n && (g(t), g(l), g(r)), o[8](null), e && e.d(n);
    }
  };
}
function j(o) {
  const {
    svelteInit: t,
    ...l
  } = o;
  return l;
}
function ye(o, t, l) {
  let r, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const c = le(e);
  let {
    svelteInit: i
  } = t;
  const _ = p(j(t)), a = p();
  O(o, a, (d) => l(0, r = d));
  const u = p();
  O(o, u, (d) => l(1, s = d));
  const f = [], v = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U
  } = Q() || {}, q = i({
    parent: v,
    props: _,
    target: a,
    slot: u,
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(d) {
      f.push(d);
    }
  });
  we("$$ms-gr-antd-react-wrapper", q), pe(() => {
    _.set(j(t));
  }), be(() => {
    f.forEach((d) => d());
  });
  function G(d) {
    k[d ? "unshift" : "push"](() => {
      r = d, a.set(r);
    });
  }
  function H(d) {
    k[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  return o.$$set = (d) => {
    l(17, t = C(C({}, t), R(d))), "svelteInit" in d && l(5, i = d.svelteInit), "$$scope" in d && l(6, n = d.$$scope);
  }, t = R(t), [r, s, a, u, c, i, n, e, G, H];
}
class ve extends re {
  constructor(t) {
    super(), de(this, t, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, x = window.ms_globals.tree;
function xe(o) {
  function t(l) {
    const r = p(), s = new ve({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, n], P({
            createPortal: I,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), P({
              createPortal: I,
              node: x
            });
          }), n;
        },
        ...l.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Ee = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(o) {
  return o ? Object.keys(o).reduce((t, l) => {
    const r = o[l];
    return typeof r == "number" && !Ee.includes(l) ? t[l] = r + "px" : t[l] = r, t;
  }, {}) : {};
}
function W(o) {
  const t = o.cloneNode(!0);
  Object.keys(o.getEventListeners()).forEach((r) => {
    o.getEventListeners(r).forEach(({
      listener: e,
      type: n,
      useCapture: c
    }) => {
      t.addEventListener(n, e, c);
    });
  });
  const l = Array.from(o.children);
  for (let r = 0; r < l.length; r++) {
    const s = l[r], e = W(s);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Ce(o, t) {
  o && (typeof o == "function" ? o(t) : o.current = t);
}
const h = B(({
  slot: o,
  clone: t,
  className: l,
  style: r
}, s) => {
  const e = J();
  return Y(() => {
    var _;
    if (!e.current || !o)
      return;
    let n = o;
    function c() {
      let a = n;
      if (n.tagName.toLowerCase() === "svelte-slot" && n.children.length === 1 && n.children[0] && (a = n.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ce(s, a), l && a.classList.add(...l.split(" ")), r) {
        const u = Ie(r);
        Object.keys(u).forEach((f) => {
          a.style[f] = u[f];
        });
      }
    }
    let i = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var u;
        n = W(o), n.style.display = "contents", c(), (u = e.current) == null || u.appendChild(n);
      };
      a(), i = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(n) && ((f = e.current) == null || f.removeChild(n)), a();
      }), i.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      n.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(n);
    return () => {
      var a, u;
      n.style.display = "", (a = e.current) != null && a.contains(n) && ((u = e.current) == null || u.removeChild(n)), i == null || i.disconnect();
    };
  }, [o, t, l, r, s]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function z(o, t) {
  return o.filter(Boolean).map((l) => {
    if (typeof l != "object")
      return l;
    const r = {
      ...l.props
    };
    let s = r;
    Object.keys(l.slots).forEach((n) => {
      if (!l.slots[n] || !(l.slots[n] instanceof Element) && !l.slots[n].el)
        return;
      const c = n.split(".");
      c.forEach((f, v) => {
        s[f] || (s[f] = {}), v !== c.length - 1 && (s = r[f]);
      });
      const i = l.slots[n];
      let _, a, u = !1;
      i instanceof Element ? _ = i : (_ = i.el, a = i.callback, u = i.clone || !1), s[c[c.length - 1]] = _ ? a ? (...f) => (a(c[c.length - 1], f), /* @__PURE__ */ m.jsx(h, {
        slot: _,
        clone: u || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(h, {
        slot: _,
        clone: u || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = r;
    });
    const e = "children";
    return l[e] && (r[e] = z(l[e], t)), r;
  });
}
const Oe = xe(({
  slots: o,
  children: t,
  onValueChange: l,
  onChange: r,
  onLoadData: s,
  optionItems: e,
  options: n,
  ...c
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ m.jsx(V.Panel, {
    ...c,
    options: K(() => n || z(e), [n, e]),
    loadData: s,
    onChange: (i, ..._) => {
      r == null || r(i, ..._), l(i);
    },
    expandIcon: o.expandIcon ? /* @__PURE__ */ m.jsx(h, {
      slot: o.expandIcon
    }) : c.expandIcon,
    notFoundContent: o.notFoundContent ? /* @__PURE__ */ m.jsx(h, {
      slot: o.notFoundContent
    }) : c.notFoundContent
  })]
}));
export {
  Oe as CascaderPanel,
  Oe as default
};
