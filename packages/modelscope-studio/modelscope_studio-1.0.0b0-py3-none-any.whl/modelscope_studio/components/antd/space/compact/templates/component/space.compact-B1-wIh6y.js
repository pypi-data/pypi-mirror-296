import { g as Y, w as g, d as Q, a as m } from "./Index-Cj0XcYmT.js";
const I = window.ms_globals.React, L = window.ms_globals.React.useMemo, B = window.ms_globals.React.useState, N = window.ms_globals.React.useEffect, J = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, S = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Space;
var A = {
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
var Z = I, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) te.call(t, r) && !oe.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: ne.current
  };
}
y.Fragment = ee;
y.jsx = D;
y.jsxs = D;
A.exports = y;
var _ = A.exports;
const {
  SvelteComponent: re,
  assign: C,
  binding_callbacks: E,
  check_outros: se,
  component_subscribe: R,
  compute_slots: le,
  create_slot: ie,
  detach: w,
  element: F,
  empty: ae,
  exclude_internal_props: k,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ue,
  group_outros: de,
  init: fe,
  insert: b,
  safe_not_equal: pe,
  set_custom_element_data: M,
  space: _e,
  transition_in: h,
  transition_out: x,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: be,
  setContext: he
} = window.__gradio__svelte__internal;
function O(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = ie(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = F("svelte-slot"), l && l.c(), M(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      b(e, t, o), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && me(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? ue(
          r,
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
      s || (h(l, e), s = !0);
    },
    o(e) {
      x(l, e), s = !1;
    },
    d(e) {
      e && w(t), l && l.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && O(n)
  );
  return {
    c() {
      t = F("react-portal-target"), s = _e(), e && e.c(), r = ae(), M(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      b(o, t, i), n[8](t), b(o, s, i), e && e.m(o, i), b(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = O(o), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (de(), x(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(o) {
      l || (h(e), l = !0);
    },
    o(o) {
      x(e), l = !1;
    },
    d(o) {
      o && (w(t), w(s), w(r)), n[8](null), e && e.d(o);
    }
  };
}
function P(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function ve(n, t, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = le(e);
  let {
    svelteInit: d
  } = t;
  const p = g(P(t)), a = g();
  R(n, a, (c) => s(0, r = c));
  const u = g();
  R(n, u, (c) => s(1, l = c));
  const f = [], W = we("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: U,
    subSlotIndex: G
  } = Y() || {}, H = d({
    parent: W,
    props: p,
    target: a,
    slot: u,
    slotKey: z,
    slotIndex: U,
    subSlotIndex: G,
    onDestroy(c) {
      f.push(c);
    }
  });
  he("$$ms-gr-antd-react-wrapper", H), ge(() => {
    p.set(P(t));
  }), be(() => {
    f.forEach((c) => c());
  });
  function K(c) {
    E[c ? "unshift" : "push"](() => {
      r = c, a.set(r);
    });
  }
  function q(c) {
    E[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  return n.$$set = (c) => {
    s(17, t = C(C({}, t), k(c))), "svelteInit" in c && s(5, d = c.svelteInit), "$$scope" in c && s(6, o = c.$$scope);
  }, t = k(t), [r, l, a, u, i, d, o, e, K, q];
}
class xe extends re {
  constructor(t) {
    super(), fe(this, t, ve, ye, pe, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ie(n) {
  function t(s) {
    const r = g(), l = new xe({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, o], j({
            createPortal: S,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), j({
              createPortal: S,
              node: v
            });
          }), o;
        },
        ...s.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(t);
    });
  });
}
function Se(n) {
  const [t, s] = B(() => m(n));
  return N(() => {
    let r = !0;
    return n.subscribe((e) => {
      r && (r = !1, e === t) || s(e);
    });
  }, [n]), t;
}
function Ce(n) {
  const t = L(() => Q(n, (s) => s), [n]);
  return Se(t);
}
const Ee = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !Ee.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function T(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: e,
      type: o,
      useCapture: i
    }) => {
      t.addEventListener(o, e, i);
    });
  });
  const s = Array.from(n.children);
  for (let r = 0; r < s.length; r++) {
    const l = s[r], e = T(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Oe = J(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, l) => {
  const e = V();
  return N(() => {
    var p;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let a = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (a = o.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(l, a), s && a.classList.add(...s.split(" ")), r) {
        const u = Re(r);
        Object.keys(u).forEach((f) => {
          a.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var u;
        o = T(n), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
      };
      a(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(o) && ((f = e.current) == null || f.removeChild(o)), a();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (p = e.current) == null || p.appendChild(o);
    return () => {
      var a, u;
      o.style.display = "", (a = e.current) != null && a.contains(o) && ((u = e.current) == null || u.removeChild(o)), d == null || d.disconnect();
    };
  }, [n, t, s, r, l]), I.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Pe(n, t) {
  const s = L(() => I.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, o) => {
    if (e.props.node.slotIndex && o.props.node.slotIndex) {
      const i = m(e.props.node.slotIndex) || 0, d = m(o.props.node.slotIndex) || 0;
      return i - d === 0 && e.props.node.subSlotIndex && o.props.node.subSlotIndex ? (m(e.props.node.subSlotIndex) || 0) - (m(o.props.node.subSlotIndex) || 0) : i - d;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Ce(s);
}
const Le = Ie(({
  children: n,
  ...t
}) => {
  const s = Pe(n);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ _.jsx(X.Compact, {
      ...t,
      children: s.map((r, l) => /* @__PURE__ */ _.jsx(Oe, {
        slot: r
      }, l))
    })]
  });
});
export {
  Le as Space,
  Le as default
};
