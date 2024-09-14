import { g as Y, w as p } from "./Index-XQ735co0.js";
const P = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, J = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Statistic;
var L = {
  exports: {}
}, h = {};
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
function F(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) $.call(t, r) && !te.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: X,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: ee.current
  };
}
h.Fragment = Z;
h.jsx = F;
h.jsxs = F;
L.exports = h;
var _ = L.exports;
const {
  SvelteComponent: ne,
  assign: I,
  binding_callbacks: S,
  check_outros: re,
  component_subscribe: C,
  compute_slots: oe,
  create_slot: se,
  detach: g,
  element: N,
  empty: le,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ce,
  group_outros: ae,
  init: ue,
  insert: w,
  safe_not_equal: de,
  set_custom_element_data: D,
  space: fe,
  transition_in: b,
  transition_out: x,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: me,
  getContext: pe,
  onDestroy: ge,
  setContext: we
} = window.__gradio__svelte__internal;
function k(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = se(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), l && l.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      w(e, t, o), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && _e(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? ce(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : ie(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (b(l, e), s = !0);
    },
    o(e) {
      x(l, e), s = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function be(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && k(n)
  );
  return {
    c() {
      t = N("react-portal-target"), s = fe(), e && e.c(), r = le(), D(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, t, i), n[8](t), w(o, s, i), e && e.m(o, i), w(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = k(o), e.c(), b(e, 1), e.m(r.parentNode, r)) : e && (ae(), x(e, 1, 1, () => {
        e = null;
      }), re());
    },
    i(o) {
      l || (b(e), l = !0);
    },
    o(o) {
      x(e), l = !1;
    },
    d(o) {
      o && (g(t), g(s), g(r)), n[8](null), e && e.d(o);
    }
  };
}
function O(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function he(n, t, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = oe(e);
  let {
    svelteInit: d
  } = t;
  const m = p(O(t)), c = p();
  C(n, c, (a) => s(0, r = a));
  const u = p();
  C(n, u, (a) => s(1, l = a));
  const f = [], W = pe("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T
  } = Y() || {}, U = d({
    parent: W,
    props: m,
    target: c,
    slot: u,
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T,
    onDestroy(a) {
      f.push(a);
    }
  });
  we("$$ms-gr-antd-react-wrapper", U), me(() => {
    m.set(O(t));
  }), ge(() => {
    f.forEach((a) => a());
  });
  function q(a) {
    S[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function G(a) {
    S[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return n.$$set = (a) => {
    s(17, t = I(I({}, t), R(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, t = R(t), [r, l, c, u, i, d, o, e, q, G];
}
class ye extends ne {
  constructor(t) {
    super(), ue(this, t, he, be, de, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, y = window.ms_globals.tree;
function ve(n) {
  function t(s) {
    const r = p(), l = new ye({
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
          }, i = e.parent ?? y;
          return i.nodes = [...i.nodes, o], j({
            createPortal: E,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), j({
              createPortal: E,
              node: y
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
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ee(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !xe.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function M(n) {
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
    const l = s[r], e = M(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Ie(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const v = H(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, l) => {
  const e = K();
  return B(() => {
    var m;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ie(l, c), s && c.classList.add(...s.split(" ")), r) {
        const u = Ee(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var u;
        o = M(n), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(o) && ((f = e.current) == null || f.removeChild(o)), c();
      }), d.observe(n, {
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
  }, [n, t, s, r, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Se(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function Ce(n) {
  return J(() => Se(n), [n]);
}
const ke = ve(({
  children: n,
  slots: t,
  formatter: s,
  ...r
}) => {
  const l = Ce(s);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ _.jsx(Q, {
      ...r,
      formatter: l,
      title: t.title ? /* @__PURE__ */ _.jsx(v, {
        slot: t.title
      }) : r.title,
      prefix: t.prefix ? /* @__PURE__ */ _.jsx(v, {
        slot: t.prefix
      }) : r.prefix,
      suffix: t.suffix ? /* @__PURE__ */ _.jsx(v, {
        slot: t.suffix
      }) : r.suffix
    })]
  });
});
export {
  ke as Statistic,
  ke as default
};
