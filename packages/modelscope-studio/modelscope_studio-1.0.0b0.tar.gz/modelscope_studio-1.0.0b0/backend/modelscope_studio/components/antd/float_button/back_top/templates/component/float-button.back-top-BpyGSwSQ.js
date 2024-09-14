import { g as Y, w as g } from "./Index-MpG4siE8.js";
const P = window.ms_globals.React, G = window.ms_globals.React.forwardRef, H = window.ms_globals.React.useRef, K = window.ms_globals.React.useEffect, J = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.FloatButton;
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
var V = P, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), $ = Object.prototype.hasOwnProperty, ee = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, te = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function L(t, n, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (o in n) $.call(n, o) && !te.hasOwnProperty(o) && (l[o] = n[o]);
  if (t && t.defaultProps) for (o in n = t.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: X,
    type: t,
    key: e,
    ref: r,
    props: l,
    _owner: ee.current
  };
}
y.Fragment = Z;
y.jsx = L;
y.jsxs = L;
F.exports = y;
var _ = F.exports;
const {
  SvelteComponent: ne,
  assign: I,
  binding_callbacks: C,
  check_outros: oe,
  component_subscribe: R,
  compute_slots: re,
  create_slot: se,
  detach: b,
  element: N,
  empty: le,
  exclude_internal_props: k,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ce,
  group_outros: ae,
  init: ue,
  insert: w,
  safe_not_equal: de,
  set_custom_element_data: B,
  space: fe,
  transition_in: h,
  transition_out: x,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: me,
  getContext: pe,
  onDestroy: ge,
  setContext: be
} = window.__gradio__svelte__internal;
function S(t) {
  let n, s;
  const o = (
    /*#slots*/
    t[7].default
  ), l = se(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = N("svelte-slot"), l && l.c(), B(n, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      w(e, n, r), l && l.m(n, null), t[9](n), s = !0;
    },
    p(e, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && _e(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? ce(
          o,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ie(
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
      e && b(n), l && l.d(e), t[9](null);
    }
  };
}
function we(t) {
  let n, s, o, l, e = (
    /*$$slots*/
    t[4].default && S(t)
  );
  return {
    c() {
      n = N("react-portal-target"), s = fe(), e && e.c(), o = le(), B(n, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      w(r, n, i), t[8](n), w(r, s, i), e && e.m(r, i), w(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = S(r), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (ae(), x(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(r) {
      l || (h(e), l = !0);
    },
    o(r) {
      x(e), l = !1;
    },
    d(r) {
      r && (b(n), b(s), b(o)), t[8](null), e && e.d(r);
    }
  };
}
function O(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function he(t, n, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = n;
  const i = re(e);
  let {
    svelteInit: d
  } = n;
  const m = g(O(n)), c = g();
  R(t, c, (a) => s(0, o = a));
  const u = g();
  R(t, u, (a) => s(1, l = a));
  const f = [], T = pe("$$ms-gr-antd-react-wrapper"), {
    slotKey: M,
    slotIndex: W,
    subSlotIndex: z
  } = Y() || {}, A = d({
    parent: T,
    props: m,
    target: c,
    slot: u,
    slotKey: M,
    slotIndex: W,
    subSlotIndex: z,
    onDestroy(a) {
      f.push(a);
    }
  });
  be("$$ms-gr-antd-react-wrapper", A), me(() => {
    m.set(O(n));
  }), ge(() => {
    f.forEach((a) => a());
  });
  function U(a) {
    C[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  function q(a) {
    C[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return t.$$set = (a) => {
    s(17, n = I(I({}, n), k(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, n = k(n), [o, l, c, u, i, d, r, e, U, q];
}
class ye extends ne {
  constructor(n) {
    super(), ue(this, n, he, we, de, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(t) {
  function n(s) {
    const o = g(), l = new ye({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, r], j({
            createPortal: E,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), j({
              createPortal: E,
              node: v
            });
          }), r;
        },
        ...s.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(n);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const o = t[s];
    return typeof o == "number" && !xe.includes(s) ? n[s] = o + "px" : n[s] = o, n;
  }, {}) : {};
}
function D(t) {
  const n = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: e,
      type: r,
      useCapture: i
    }) => {
      n.addEventListener(r, e, i);
    });
  });
  const s = Array.from(t.children);
  for (let o = 0; o < s.length; o++) {
    const l = s[o], e = D(l);
    n.replaceChild(e, n.children[o]);
  }
  return n;
}
function Ie(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const p = G(({
  slot: t,
  clone: n,
  className: s,
  style: o
}, l) => {
  const e = H();
  return K(() => {
    var m;
    if (!e.current || !t)
      return;
    let r = t;
    function i() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ie(l, c), s && c.classList.add(...s.split(" ")), o) {
        const u = Ee(o);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        r = D(t), r.style.display = "contents", i(), (u = e.current) == null || u.appendChild(r);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(r) && ((f = e.current) == null || f.removeChild(r)), c();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (m = e.current) == null || m.appendChild(r);
    return () => {
      var c, u;
      r.style.display = "", (c = e.current) != null && c.contains(r) && ((u = e.current) == null || u.removeChild(r)), d == null || d.disconnect();
    };
  }, [t, n, s, o, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Ce(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Re(t) {
  return J(() => Ce(t), [t]);
}
const Se = ve(({
  slots: t,
  children: n,
  target: s,
  ...o
}) => {
  var e;
  const l = Re(s);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx(Q.BackTop, {
      ...o,
      target: l,
      icon: t.icon ? /* @__PURE__ */ _.jsx(p, {
        slot: t.icon
      }) : o.icon,
      description: t.description ? /* @__PURE__ */ _.jsx(p, {
        slot: t.description
      }) : o.description,
      tooltip: t.tooltip ? /* @__PURE__ */ _.jsx(p, {
        slot: t.tooltip
      }) : o.tooltip,
      badge: {
        ...o.badge,
        count: t["badge.count"] ? /* @__PURE__ */ _.jsx(p, {
          slot: t["badge.count"]
        }) : (e = o.badge) == null ? void 0 : e.count
      }
    }), n]
  });
});
export {
  Se as FloatButtonBackTop,
  Se as default
};
