import { g as Q, w as g } from "./Index-CZ3ZsrG7.js";
const F = window.ms_globals.React, K = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, J = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, C = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Drawer;
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
var X = F, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(t, n, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (o in n) ee.call(n, o) && !ne.hasOwnProperty(o) && (l[o] = n[o]);
  if (t && t.defaultProps) for (o in n = t.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: Z,
    type: t,
    key: e,
    ref: r,
    props: l,
    _owner: te.current
  };
}
y.Fragment = $;
y.jsx = D;
y.jsxs = D;
L.exports = y;
var m = L.exports;
const {
  SvelteComponent: re,
  assign: E,
  binding_callbacks: R,
  check_outros: oe,
  component_subscribe: O,
  compute_slots: se,
  create_slot: le,
  detach: w,
  element: N,
  empty: ie,
  exclude_internal_props: S,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: M,
  space: _e,
  transition_in: h,
  transition_out: I,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: ge,
  onDestroy: we,
  setContext: be
} = window.__gradio__svelte__internal;
function k(t) {
  let n, s;
  const o = (
    /*#slots*/
    t[7].default
  ), l = le(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = N("svelte-slot"), l && l.c(), M(n, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      b(e, n, r), l && l.m(n, null), t[9](n), s = !0;
    },
    p(e, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && me(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? ae(
          o,
          /*$$scope*/
          e[6],
          r,
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
      I(l, e), s = !1;
    },
    d(e) {
      e && w(n), l && l.d(e), t[9](null);
    }
  };
}
function he(t) {
  let n, s, o, l, e = (
    /*$$slots*/
    t[4].default && k(t)
  );
  return {
    c() {
      n = N("react-portal-target"), s = _e(), e && e.c(), o = ie(), M(n, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      b(r, n, i), t[8](n), b(r, s, i), e && e.m(r, i), b(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = k(r), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (ue(), I(e, 1, 1, () => {
        e = null;
      }), oe());
    },
    i(r) {
      l || (h(e), l = !0);
    },
    o(r) {
      I(e), l = !1;
    },
    d(r) {
      r && (w(n), w(s), w(o)), t[8](null), e && e.d(r);
    }
  };
}
function P(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function ye(t, n, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = n;
  const i = se(e);
  let {
    svelteInit: d
  } = n;
  const _ = g(P(n)), c = g();
  O(t, c, (a) => s(0, o = a));
  const u = g();
  O(t, u, (a) => s(1, l = a));
  const f = [], z = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U
  } = Q() || {}, q = d({
    parent: z,
    props: _,
    target: c,
    slot: u,
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(a) {
      f.push(a);
    }
  });
  be("$$ms-gr-antd-react-wrapper", q), pe(() => {
    _.set(P(n));
  }), we(() => {
    f.forEach((a) => a());
  });
  function G(a) {
    R[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  function H(a) {
    R[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return t.$$set = (a) => {
    s(17, n = E(E({}, n), S(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, n = S(n), [o, l, c, u, i, d, r, e, G, H];
}
class ve extends re {
  constructor(n) {
    super(), de(this, n, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function xe(t) {
  function n(s) {
    const o = g(), l = new ve({
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
            createPortal: C,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), j({
              createPortal: C,
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
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ce(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const o = t[s];
    return typeof o == "number" && !Ie.includes(s) ? n[s] = o + "px" : n[s] = o, n;
  }, {}) : {};
}
function W(t) {
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
    const l = s[o], e = W(l);
    n.replaceChild(e, n.children[o]);
  }
  return n;
}
function Ee(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const p = K(({
  slot: t,
  clone: n,
  className: s,
  style: o
}, l) => {
  const e = B();
  return J(() => {
    var _;
    if (!e.current || !t)
      return;
    let r = t;
    function i() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ee(l, c), s && c.classList.add(...s.split(" ")), o) {
        const u = Ce(o);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        r = W(t), r.style.display = "contents", i(), (u = e.current) == null || u.appendChild(r);
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
      r.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(r);
    return () => {
      var c, u;
      r.style.display = "", (c = e.current) != null && c.contains(r) && ((u = e.current) == null || u.removeChild(r)), d == null || d.disconnect();
    };
  }, [t, n, s, o, l]), F.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Re(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function x(t) {
  return Y(() => Re(t), [t]);
}
const Se = xe(({
  slots: t,
  afterOpenChange: n,
  getContainer: s,
  drawerRender: o,
  ...l
}) => {
  const e = x(n), r = x(s), i = x(o);
  return /* @__PURE__ */ m.jsx(V, {
    ...l,
    afterOpenChange: e,
    closeIcon: t.closeIcon ? /* @__PURE__ */ m.jsx(p, {
      slot: t.closeIcon
    }) : l.closeIcon,
    extra: t.extra ? /* @__PURE__ */ m.jsx(p, {
      slot: t.extra
    }) : l.extra,
    footer: t.footer ? /* @__PURE__ */ m.jsx(p, {
      slot: t.footer
    }) : l.footer,
    title: t.title ? /* @__PURE__ */ m.jsx(p, {
      slot: t.title
    }) : l.title,
    drawerRender: i,
    getContainer: typeof s == "string" ? r : s
  });
});
export {
  Se as Drawer,
  Se as default
};
