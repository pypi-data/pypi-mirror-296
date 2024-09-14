import { g as J, w as g, c as Y } from "./Index-CQ3_unR0.js";
const P = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, M = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.theme, V = window.ms_globals.antd.FloatButton;
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
var X = P, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(t, n, l) {
  var r, s = {}, e = null, o = null;
  l !== void 0 && (e = "" + l), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) ee.call(n, r) && !ne.hasOwnProperty(r) && (s[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) s[r] === void 0 && (s[r] = n[r]);
  return {
    $$typeof: Z,
    type: t,
    key: e,
    ref: o,
    props: s,
    _owner: te.current
  };
}
y.Fragment = $;
y.jsx = N;
y.jsxs = N;
L.exports = y;
var _ = L.exports;
const {
  SvelteComponent: oe,
  assign: E,
  binding_callbacks: C,
  check_outros: re,
  component_subscribe: R,
  compute_slots: se,
  create_slot: le,
  detach: b,
  element: F,
  empty: ie,
  exclude_internal_props: k,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: w,
  safe_not_equal: fe,
  set_custom_element_data: D,
  space: _e,
  transition_in: h,
  transition_out: x,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: ge,
  onDestroy: be,
  setContext: we
} = window.__gradio__svelte__internal;
function S(t) {
  let n, l;
  const r = (
    /*#slots*/
    t[7].default
  ), s = le(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = F("svelte-slot"), s && s.c(), D(n, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      w(e, n, o), s && s.m(n, null), t[9](n), l = !0;
    },
    p(e, o) {
      s && s.p && (!l || o & /*$$scope*/
      64) && me(
        s,
        r,
        e,
        /*$$scope*/
        e[6],
        l ? ae(
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
      l || (h(s, e), l = !0);
    },
    o(e) {
      x(s, e), l = !1;
    },
    d(e) {
      e && b(n), s && s.d(e), t[9](null);
    }
  };
}
function he(t) {
  let n, l, r, s, e = (
    /*$$slots*/
    t[4].default && S(t)
  );
  return {
    c() {
      n = F("react-portal-target"), l = _e(), e && e.c(), r = ie(), D(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, n, i), t[8](n), w(o, l, i), e && e.m(o, i), w(o, r, i), s = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = S(o), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (ue(), x(e, 1, 1, () => {
        e = null;
      }), re());
    },
    i(o) {
      s || (h(e), s = !0);
    },
    o(o) {
      x(e), s = !1;
    },
    d(o) {
      o && (b(n), b(l), b(r)), t[8](null), e && e.d(o);
    }
  };
}
function O(t) {
  const {
    svelteInit: n,
    ...l
  } = t;
  return l;
}
function ye(t, n, l) {
  let r, s, {
    $$slots: e = {},
    $$scope: o
  } = n;
  const i = se(e);
  let {
    svelteInit: d
  } = n;
  const m = g(O(n)), c = g();
  R(t, c, (a) => l(0, r = a));
  const u = g();
  R(t, u, (a) => l(1, s = a));
  const f = [], T = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A
  } = J() || {}, B = d({
    parent: T,
    props: m,
    target: c,
    slot: u,
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A,
    onDestroy(a) {
      f.push(a);
    }
  });
  we("$$ms-gr-antd-react-wrapper", B), pe(() => {
    m.set(O(n));
  }), be(() => {
    f.forEach((a) => a());
  });
  function U(a) {
    C[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function q(a) {
    C[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  return t.$$set = (a) => {
    l(17, n = E(E({}, n), k(a))), "svelteInit" in a && l(5, d = a.svelteInit), "$$scope" in a && l(6, o = a.$$scope);
  }, n = k(n), [r, s, c, u, i, d, o, e, U, q];
}
class ve extends oe {
  constructor(n) {
    super(), de(this, n, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function xe(t) {
  function n(l) {
    const r = g(), s = new ve({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, o], j({
            createPortal: I,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), j({
              createPortal: I,
              node: v
            });
          }), o;
        },
        ...l.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(n);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(t) {
  return t ? Object.keys(t).reduce((n, l) => {
    const r = t[l];
    return typeof r == "number" && !Ie.includes(l) ? n[l] = r + "px" : n[l] = r, n;
  }, {}) : {};
}
function G(t) {
  const n = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: e,
      type: o,
      useCapture: i
    }) => {
      n.addEventListener(o, e, i);
    });
  });
  const l = Array.from(t.children);
  for (let r = 0; r < l.length; r++) {
    const s = l[r], e = G(s);
    n.replaceChild(e, n.children[r]);
  }
  return n;
}
function Ce(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const p = H(({
  slot: t,
  clone: n,
  className: l,
  style: r
}, s) => {
  const e = K();
  return M(() => {
    var m;
    if (!e.current || !t)
      return;
    let o = t;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ce(s, c), l && c.classList.add(...l.split(" ")), r) {
        const u = Ee(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        o = G(t), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(o) && ((f = e.current) == null || f.removeChild(o)), c();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (m = e.current) == null || m.appendChild(o);
    return () => {
      var c, u;
      o.style.display = "", (c = e.current) != null && c.contains(o) && ((u = e.current) == null || u.removeChild(o)), d == null || d.disconnect();
    };
  }, [t, n, l, r, s]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), ke = xe(({
  slots: t,
  style: n,
  shape: l = "circle",
  className: r,
  ...s
}) => {
  var o;
  const {
    token: e
  } = Q.useToken();
  return /* @__PURE__ */ _.jsx(V.Group, {
    ...s,
    shape: l,
    className: Y(r, `ms-gr-antd-float-button-group-${l}`),
    style: {
      ...n,
      "--ms-gr-antd-border-radius-lg": e.borderRadiusLG + "px"
    },
    closeIcon: t.closeIcon ? /* @__PURE__ */ _.jsx(p, {
      slot: t.closeIcon
    }) : s.closeIcon,
    icon: t.icon ? /* @__PURE__ */ _.jsx(p, {
      slot: t.icon
    }) : s.icon,
    description: t.description ? /* @__PURE__ */ _.jsx(p, {
      slot: t.description
    }) : s.description,
    tooltip: t.tooltip ? /* @__PURE__ */ _.jsx(p, {
      slot: t.tooltip
    }) : s.tooltip,
    badge: {
      ...s.badge,
      count: t["badge.count"] ? /* @__PURE__ */ _.jsx(p, {
        slot: t["badge.count"]
      }) : (o = s.badge) == null ? void 0 : o.count
    }
  });
});
export {
  ke as FloatButtonGroup,
  ke as default
};
