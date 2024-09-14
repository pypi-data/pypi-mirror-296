import { g as Q, w as p } from "./Index-CirkNL_m.js";
const L = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useEffect, K = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Descriptions;
var D = {
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
function N(r, t, n) {
  var o, s = {}, e = null, l = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (o in t) ee.call(t, o) && !ne.hasOwnProperty(o) && (s[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: Z,
    type: r,
    key: e,
    ref: l,
    props: s,
    _owner: te.current
  };
}
y.Fragment = $;
y.jsx = N;
y.jsxs = N;
D.exports = y;
var m = D.exports;
const {
  SvelteComponent: re,
  assign: C,
  binding_callbacks: k,
  check_outros: oe,
  component_subscribe: O,
  compute_slots: le,
  create_slot: se,
  detach: g,
  element: F,
  empty: ie,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: M,
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
function S(r) {
  let t, n;
  const o = (
    /*#slots*/
    r[7].default
  ), s = se(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = F("svelte-slot"), s && s.c(), M(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      b(e, t, l), s && s.m(t, null), r[9](t), n = !0;
    },
    p(e, l) {
      s && s.p && (!n || l & /*$$scope*/
      64) && me(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        n ? ae(
          o,
          /*$$scope*/
          e[6],
          l,
          null
        ) : ce(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (h(s, e), n = !0);
    },
    o(e) {
      E(s, e), n = !1;
    },
    d(e) {
      e && g(t), s && s.d(e), r[9](null);
    }
  };
}
function we(r) {
  let t, n, o, s, e = (
    /*$$slots*/
    r[4].default && S(r)
  );
  return {
    c() {
      t = F("react-portal-target"), n = _e(), e && e.c(), o = ie(), M(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      b(l, t, i), r[8](t), b(l, n, i), e && e.m(l, i), b(l, o, i), s = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = S(l), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (ue(), E(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(l) {
      s || (h(e), s = !0);
    },
    o(l) {
      E(e), s = !1;
    },
    d(l) {
      l && (g(t), g(n), g(o)), r[8](null), e && e.d(l);
    }
  };
}
function j(r) {
  const {
    svelteInit: t,
    ...n
  } = r;
  return n;
}
function ye(r, t, n) {
  let o, s, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = le(e);
  let {
    svelteInit: d
  } = t;
  const _ = p(j(t)), c = p();
  O(r, c, (u) => n(0, o = u));
  const a = p();
  O(r, a, (u) => n(1, s = u));
  const f = [], v = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U
  } = Q() || {}, q = d({
    parent: v,
    props: _,
    target: c,
    slot: a,
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(u) {
      f.push(u);
    }
  });
  he("$$ms-gr-antd-react-wrapper", q), pe(() => {
    _.set(j(t));
  }), be(() => {
    f.forEach((u) => u());
  });
  function G(u) {
    k[u ? "unshift" : "push"](() => {
      o = u, c.set(o);
    });
  }
  function H(u) {
    k[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  return r.$$set = (u) => {
    n(17, t = C(C({}, t), R(u))), "svelteInit" in u && n(5, d = u.svelteInit), "$$scope" in u && n(6, l = u.$$scope);
  }, t = R(t), [o, s, c, a, i, d, l, e, G, H];
}
class ve extends re {
  constructor(t) {
    super(), de(this, t, ye, we, fe, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, x = window.ms_globals.tree;
function xe(r) {
  function t(n) {
    const o = p(), s = new ve({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? x;
          return i.nodes = [...i.nodes, l], P({
            createPortal: I,
            node: x
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), P({
              createPortal: I,
              node: x
            });
          }), l;
        },
        ...n.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const Ee = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(r) {
  return r ? Object.keys(r).reduce((t, n) => {
    const o = r[n];
    return typeof o == "number" && !Ee.includes(n) ? t[n] = o + "px" : t[n] = o, t;
  }, {}) : {};
}
function W(r) {
  const t = r.cloneNode(!0);
  Object.keys(r.getEventListeners()).forEach((o) => {
    r.getEventListeners(o).forEach(({
      listener: e,
      type: l,
      useCapture: i
    }) => {
      t.addEventListener(l, e, i);
    });
  });
  const n = Array.from(r.children);
  for (let o = 0; o < n.length; o++) {
    const s = n[o], e = W(s);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Ce(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const w = B(({
  slot: r,
  clone: t,
  className: n,
  style: o
}, s) => {
  const e = J();
  return Y(() => {
    var _;
    if (!e.current || !r)
      return;
    let l = r;
    function i() {
      let c = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (c = l.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ce(s, c), n && c.classList.add(...n.split(" ")), o) {
        const a = Ie(o);
        Object.keys(a).forEach((f) => {
          c.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var a;
        l = W(r), l.style.display = "contents", i(), (a = e.current) == null || a.appendChild(l);
      };
      c(), d = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(l) && ((f = e.current) == null || f.removeChild(l)), c();
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(l);
    return () => {
      var c, a;
      l.style.display = "", (c = e.current) != null && c.contains(l) && ((a = e.current) == null || a.removeChild(l)), d == null || d.disconnect();
    };
  }, [r, t, n, o, s]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function z(r, t) {
  return r.filter(Boolean).map((n) => {
    if (typeof n != "object")
      return n;
    const o = {
      ...n.props
    };
    let s = o;
    Object.keys(n.slots).forEach((l) => {
      if (!n.slots[l] || !(n.slots[l] instanceof Element) && !n.slots[l].el)
        return;
      const i = l.split(".");
      i.forEach((f, v) => {
        s[f] || (s[f] = {}), v !== i.length - 1 && (s = o[f]);
      });
      const d = n.slots[l];
      let _, c, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, c = d.callback, a = d.clone || !1), s[i[i.length - 1]] = _ ? c ? (...f) => (c(i[i.length - 1], f), /* @__PURE__ */ m.jsx(w, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(w, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : s[i[i.length - 1]], s = o;
    });
    const e = "children";
    return n[e] && (o[e] = z(n[e], t)), o;
  });
}
const Oe = xe(({
  slots: r,
  items: t,
  slotItems: n,
  children: o,
  ...s
}) => /* @__PURE__ */ m.jsxs(m.Fragment, {
  children: [/* @__PURE__ */ m.jsx("div", {
    style: {
      display: "none"
    },
    children: o
  }), /* @__PURE__ */ m.jsx(V, {
    ...s,
    extra: r.extra ? /* @__PURE__ */ m.jsx(w, {
      slot: r.extra
    }) : s.extra,
    title: r.title ? /* @__PURE__ */ m.jsx(w, {
      slot: r.title
    }) : s.title,
    items: K(() => t || z(n), [t, n])
  })]
}));
export {
  Oe as Descriptions,
  Oe as default
};
