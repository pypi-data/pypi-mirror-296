import { g as Y, w as p } from "./Index-vkVOlmsL.js";
const P = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, J = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Alert;
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
var V = P, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), $ = Object.prototype.hasOwnProperty, ee = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, te = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(e, n, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (r in n) $.call(n, r) && !te.hasOwnProperty(r) && (l[r] = n[r]);
  if (e && e.defaultProps) for (r in n = e.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: X,
    type: e,
    key: t,
    ref: s,
    props: l,
    _owner: ee.current
  };
}
y.Fragment = Z;
y.jsx = F;
y.jsxs = F;
L.exports = y;
var _ = L.exports;
const {
  SvelteComponent: ne,
  assign: C,
  binding_callbacks: E,
  check_outros: oe,
  component_subscribe: R,
  compute_slots: re,
  create_slot: se,
  detach: b,
  element: N,
  empty: le,
  exclude_internal_props: S,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ce,
  group_outros: ae,
  init: ue,
  insert: w,
  safe_not_equal: de,
  set_custom_element_data: A,
  space: fe,
  transition_in: h,
  transition_out: x,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: me,
  getContext: ge,
  onDestroy: pe,
  setContext: be
} = window.__gradio__svelte__internal;
function k(e) {
  let n, o;
  const r = (
    /*#slots*/
    e[7].default
  ), l = se(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = N("svelte-slot"), l && l.c(), A(n, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      w(t, n, s), l && l.m(n, null), e[9](n), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && _e(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? ce(
          r,
          /*$$scope*/
          t[6],
          s,
          null
        ) : ie(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (h(l, t), o = !0);
    },
    o(t) {
      x(l, t), o = !1;
    },
    d(t) {
      t && b(n), l && l.d(t), e[9](null);
    }
  };
}
function we(e) {
  let n, o, r, l, t = (
    /*$$slots*/
    e[4].default && k(e)
  );
  return {
    c() {
      n = N("react-portal-target"), o = fe(), t && t.c(), r = le(), A(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      w(s, n, i), e[8](n), w(s, o, i), t && t.m(s, i), w(s, r, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && h(t, 1)) : (t = k(s), t.c(), h(t, 1), t.m(r.parentNode, r)) : t && (ae(), x(t, 1, 1, () => {
        t = null;
      }), oe());
    },
    i(s) {
      l || (h(t), l = !0);
    },
    o(s) {
      x(t), l = !1;
    },
    d(s) {
      s && (b(n), b(o), b(r)), e[8](null), t && t.d(s);
    }
  };
}
function O(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function he(e, n, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: s
  } = n;
  const i = re(t);
  let {
    svelteInit: d
  } = n;
  const m = p(O(n)), c = p();
  R(e, c, (a) => o(0, r = a));
  const u = p();
  R(e, u, (a) => o(1, l = a));
  const f = [], M = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: T
  } = Y() || {}, U = d({
    parent: M,
    props: m,
    target: c,
    slot: u,
    slotKey: W,
    slotIndex: z,
    subSlotIndex: T,
    onDestroy(a) {
      f.push(a);
    }
  });
  be("$$ms-gr-antd-react-wrapper", U), me(() => {
    m.set(O(n));
  }), pe(() => {
    f.forEach((a) => a());
  });
  function q(a) {
    E[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function G(a) {
    E[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return e.$$set = (a) => {
    o(17, n = C(C({}, n), S(a))), "svelteInit" in a && o(5, d = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, n = S(n), [r, l, c, u, i, d, s, t, q, G];
}
class ye extends ne {
  constructor(n) {
    super(), ue(this, n, he, we, de, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(e) {
  function n(o) {
    const r = p(), l = new ye({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? v;
          return i.nodes = [...i.nodes, s], j({
            createPortal: I,
            node: v
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), j({
              createPortal: I,
              node: v
            });
          }), s;
        },
        ...o.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const r = e[o];
    return typeof r == "number" && !xe.includes(o) ? n[o] = r + "px" : n[o] = r, n;
  }, {}) : {};
}
function D(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: t,
      type: s,
      useCapture: i
    }) => {
      n.addEventListener(s, t, i);
    });
  });
  const o = Array.from(e.children);
  for (let r = 0; r < o.length; r++) {
    const l = o[r], t = D(l);
    n.replaceChild(t, n.children[r]);
  }
  return n;
}
function Ce(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const g = H(({
  slot: e,
  clone: n,
  className: o,
  style: r
}, l) => {
  const t = K();
  return B(() => {
    var m;
    if (!t.current || !e)
      return;
    let s = e;
    function i() {
      let c = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (c = s.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ce(l, c), o && c.classList.add(...o.split(" ")), r) {
        const u = Ie(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        s = D(e), s.style.display = "contents", i(), (u = t.current) == null || u.appendChild(s);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = t.current) != null && u.contains(s) && ((f = t.current) == null || f.removeChild(s)), c();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", i(), (m = t.current) == null || m.appendChild(s);
    return () => {
      var c, u;
      s.style.display = "", (c = t.current) != null && c.contains(s) && ((u = t.current) == null || u.removeChild(s)), d == null || d.disconnect();
    };
  }, [e, n, o, r, l]), P.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Ee(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Re(e) {
  return J(() => Ee(e), [e]);
}
const ke = ve(({
  slots: e,
  afterClose: n,
  ...o
}) => {
  const r = Re(n);
  return /* @__PURE__ */ _.jsx(Q, {
    ...o,
    afterClose: r,
    action: e.action ? /* @__PURE__ */ _.jsx(g, {
      slot: e.action
    }) : o.action,
    closable: e["closable.closeIcon"] ? {
      ...typeof o.closable == "object" ? o.closable : {},
      closeIcon: /* @__PURE__ */ _.jsx(g, {
        slot: e["closable.closeIcon"]
      })
    } : o.closable,
    description: e.description ? /* @__PURE__ */ _.jsx(g, {
      slot: e.description
    }) : o.description,
    icon: e.icon ? /* @__PURE__ */ _.jsx(g, {
      slot: e.icon
    }) : o.icon,
    message: e.message ? /* @__PURE__ */ _.jsx(g, {
      slot: e.message
    }) : o.message
  });
});
export {
  ke as Alert,
  ke as default
};
