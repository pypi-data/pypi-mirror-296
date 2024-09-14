import { g as Q, w as g, d as X, a as m } from "./Index-CJS66Y4b.js";
const I = window.ms_globals.React, N = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, A = window.ms_globals.React.useEffect, V = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, S = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.Space;
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
var $ = I, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, oe = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) ne.call(t, r) && !re.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: oe.current
  };
}
y.Fragment = te;
y.jsx = F;
y.jsxs = F;
D.exports = y;
var p = D.exports;
const {
  SvelteComponent: se,
  assign: E,
  binding_callbacks: C,
  check_outros: le,
  component_subscribe: R,
  compute_slots: ie,
  create_slot: ae,
  detach: w,
  element: M,
  empty: ce,
  exclude_internal_props: k,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: pe,
  insert: b,
  safe_not_equal: _e,
  set_custom_element_data: T,
  space: me,
  transition_in: h,
  transition_out: x,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: he,
  setContext: ye
} = window.__gradio__svelte__internal;
function O(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = ae(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = M("svelte-slot"), l && l.c(), T(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      b(e, t, o), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && ge(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? de(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ue(
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
function ve(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && O(n)
  );
  return {
    c() {
      t = M("react-portal-target"), s = me(), e && e.c(), r = ce(), T(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      b(o, t, i), n[8](t), b(o, s, i), e && e.m(o, i), b(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = O(o), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (fe(), x(e, 1, 1, () => {
        e = null;
      }), le());
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
function xe(n, t, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = ie(e);
  let {
    svelteInit: d
  } = t;
  const _ = g(P(t)), a = g();
  R(n, a, (c) => s(0, r = c));
  const u = g();
  R(n, u, (c) => s(1, l = c));
  const f = [], z = be("$$ms-gr-antd-react-wrapper"), {
    slotKey: U,
    slotIndex: G,
    subSlotIndex: H
  } = Q() || {}, K = d({
    parent: z,
    props: _,
    target: a,
    slot: u,
    slotKey: U,
    slotIndex: G,
    subSlotIndex: H,
    onDestroy(c) {
      f.push(c);
    }
  });
  ye("$$ms-gr-antd-react-wrapper", K), we(() => {
    _.set(P(t));
  }), he(() => {
    f.forEach((c) => c());
  });
  function q(c) {
    C[c ? "unshift" : "push"](() => {
      r = c, a.set(r);
    });
  }
  function B(c) {
    C[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  return n.$$set = (c) => {
    s(17, t = E(E({}, t), k(c))), "svelteInit" in c && s(5, d = c.svelteInit), "$$scope" in c && s(6, o = c.$$scope);
  }, t = k(t), [r, l, a, u, i, d, o, e, q, B];
}
class Ie extends se {
  constructor(t) {
    super(), pe(this, t, xe, ve, _e, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function Se(n) {
  function t(s) {
    const r = g(), l = new Ie({
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
function Ee(n) {
  const [t, s] = J(() => m(n));
  return A(() => {
    let r = !0;
    return n.subscribe((e) => {
      r && (r = !1, e === t) || s(e);
    });
  }, [n]), t;
}
function Ce(n) {
  const t = N(() => X(n, (s) => s), [n]);
  return Ee(t);
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !Re.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function W(n) {
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
    const l = s[r], e = W(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const L = V(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, l) => {
  const e = Y();
  return A(() => {
    var _;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let a = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (a = o.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(l, a), s && a.classList.add(...s.split(" ")), r) {
        const u = ke(r);
        Object.keys(u).forEach((f) => {
          a.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var u;
        o = W(n), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
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
      o.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(o);
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
  const s = N(() => I.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, o) => {
    if (e.props.node.slotIndex && o.props.node.slotIndex) {
      const i = m(e.props.node.slotIndex) || 0, d = m(o.props.node.slotIndex) || 0;
      return i - d === 0 && e.props.node.subSlotIndex && o.props.node.subSlotIndex ? (m(e.props.node.subSlotIndex) || 0) - (m(o.props.node.subSlotIndex) || 0) : i - d;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Ce(s);
}
const Le = Se(({
  slots: n,
  children: t,
  ...s
}) => {
  const r = Pe(t);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx(Z, {
      ...s,
      split: n.split ? /* @__PURE__ */ p.jsx(L, {
        slot: n.split,
        clone: !0
      }) : s.split,
      children: r.map((l, e) => /* @__PURE__ */ p.jsx(L, {
        slot: l
      }, e))
    })]
  });
});
export {
  Le as Space,
  Le as default
};
