import { g as J, w as g } from "./Index-C9Kk2Upy.js";
const P = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, M = window.ms_globals.React.useEffect, E = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.FloatButton;
var L = {
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
var Q = P, V = Symbol.for("react.element"), X = Symbol.for("react.fragment"), Z = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, t, r) {
  var o, l = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) Z.call(t, o) && !ee.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: V,
    type: n,
    key: e,
    ref: s,
    props: l,
    _owner: $.current
  };
}
y.Fragment = X;
y.jsx = F;
y.jsxs = F;
L.exports = y;
var _ = L.exports;
const {
  SvelteComponent: te,
  assign: I,
  binding_callbacks: C,
  check_outros: ne,
  component_subscribe: R,
  compute_slots: oe,
  create_slot: re,
  detach: b,
  element: N,
  empty: se,
  exclude_internal_props: S,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: ae,
  insert: w,
  safe_not_equal: ue,
  set_custom_element_data: D,
  space: de,
  transition_in: h,
  transition_out: x,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: me,
  onDestroy: pe,
  setContext: ge
} = window.__gradio__svelte__internal;
function k(n) {
  let t, r;
  const o = (
    /*#slots*/
    n[7].default
  ), l = re(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), l && l.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      w(e, t, s), l && l.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      l && l.p && (!r || s & /*$$scope*/
      64) && fe(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        r ? ie(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : le(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (h(l, e), r = !0);
    },
    o(e) {
      x(l, e), r = !1;
    },
    d(e) {
      e && b(t), l && l.d(e), n[9](null);
    }
  };
}
function be(n) {
  let t, r, o, l, e = (
    /*$$slots*/
    n[4].default && k(n)
  );
  return {
    c() {
      t = N("react-portal-target"), r = de(), e && e.c(), o = se(), D(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      w(s, t, i), n[8](t), w(s, r, i), e && e.m(s, i), w(s, o, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = k(s), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (ce(), x(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(s) {
      l || (h(e), l = !0);
    },
    o(s) {
      x(e), l = !1;
    },
    d(s) {
      s && (b(t), b(r), b(o)), n[8](null), e && e.d(s);
    }
  };
}
function O(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function we(n, t, r) {
  let o, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = oe(e);
  let {
    svelteInit: d
  } = t;
  const m = g(O(t)), c = g();
  R(n, c, (a) => r(0, o = a));
  const u = g();
  R(n, u, (a) => r(1, l = a));
  const f = [], z = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: B,
    subSlotIndex: T
  } = J() || {}, U = d({
    parent: z,
    props: m,
    target: c,
    slot: u,
    slotKey: A,
    slotIndex: B,
    subSlotIndex: T,
    onDestroy(a) {
      f.push(a);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", U), _e(() => {
    m.set(O(t));
  }), pe(() => {
    f.forEach((a) => a());
  });
  function q(a) {
    C[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  function G(a) {
    C[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return n.$$set = (a) => {
    r(17, t = I(I({}, t), S(a))), "svelteInit" in a && r(5, d = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = S(t), [o, l, c, u, i, d, s, e, q, G];
}
class he extends te {
  constructor(t) {
    super(), ae(this, t, we, be, ue, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function ye(n) {
  function t(r) {
    const o = g(), l = new he({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, s], j({
            createPortal: E,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), j({
              createPortal: E,
              node: v
            });
          }), s;
        },
        ...r.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const ve = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const o = n[r];
    return typeof o == "number" && !ve.includes(r) ? t[r] = o + "px" : t[r] = o, t;
  }, {}) : {};
}
function W(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: e,
      type: s,
      useCapture: i
    }) => {
      t.addEventListener(s, e, i);
    });
  });
  const r = Array.from(n.children);
  for (let o = 0; o < r.length; o++) {
    const l = r[o], e = W(l);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Ee(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const p = H(({
  slot: n,
  clone: t,
  className: r,
  style: o
}, l) => {
  const e = K();
  return M(() => {
    var m;
    if (!e.current || !n)
      return;
    let s = n;
    function i() {
      let c = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (c = s.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ee(l, c), r && c.classList.add(...r.split(" ")), o) {
        const u = xe(o);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var u;
        s = W(n), s.style.display = "contents", i(), (u = e.current) == null || u.appendChild(s);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(s) && ((f = e.current) == null || f.removeChild(s)), c();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", i(), (m = e.current) == null || m.appendChild(s);
    return () => {
      var c, u;
      s.style.display = "", (c = e.current) != null && c.contains(s) && ((u = e.current) == null || u.removeChild(s)), d == null || d.disconnect();
    };
  }, [n, t, r, o, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ce = ye(({
  slots: n,
  children: t,
  ...r
}) => {
  var o;
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx(Y, {
      ...r,
      icon: n.icon ? /* @__PURE__ */ _.jsx(p, {
        slot: n.icon
      }) : r.icon,
      description: n.description ? /* @__PURE__ */ _.jsx(p, {
        slot: n.description
      }) : r.description,
      tooltip: n.tooltip ? /* @__PURE__ */ _.jsx(p, {
        slot: n.tooltip
      }) : r.tooltip,
      badge: {
        ...r.badge,
        count: n["badge.count"] ? /* @__PURE__ */ _.jsx(p, {
          slot: n["badge.count"]
        }) : (o = r.badge) == null ? void 0 : o.count
      }
    }), t]
  });
});
export {
  Ce as FloatButton,
  Ce as default
};
