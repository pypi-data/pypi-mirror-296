import { g as Y, w } from "./Index-CuM_V1yR.js";
const j = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, J = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, Q = window.ms_globals.antd.Input;
var P = {
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
var V = j, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), $ = Object.prototype.hasOwnProperty, ee = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, te = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function L(r, t, n) {
  var o, l = {}, e = null, s = null;
  n !== void 0 && (e = "" + n), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) $.call(t, o) && !te.hasOwnProperty(o) && (l[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: X,
    type: r,
    key: e,
    ref: s,
    props: l,
    _owner: ee.current
  };
}
h.Fragment = Z;
h.jsx = L;
h.jsxs = L;
P.exports = h;
var m = P.exports;
const {
  SvelteComponent: re,
  assign: E,
  binding_callbacks: C,
  check_outros: ne,
  component_subscribe: S,
  compute_slots: oe,
  create_slot: se,
  detach: g,
  element: N,
  empty: le,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ae,
  group_outros: ce,
  init: de,
  insert: b,
  safe_not_equal: ue,
  set_custom_element_data: D,
  space: fe,
  transition_in: y,
  transition_out: x,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: me,
  getContext: pe,
  onDestroy: we,
  setContext: ge
} = window.__gradio__svelte__internal;
function k(r) {
  let t, n;
  const o = (
    /*#slots*/
    r[7].default
  ), l = se(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), l && l.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      b(e, t, s), l && l.m(t, null), r[9](t), n = !0;
    },
    p(e, s) {
      l && l.p && (!n || s & /*$$scope*/
      64) && _e(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        n ? ae(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ie(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (y(l, e), n = !0);
    },
    o(e) {
      x(l, e), n = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), r[9](null);
    }
  };
}
function be(r) {
  let t, n, o, l, e = (
    /*$$slots*/
    r[4].default && k(r)
  );
  return {
    c() {
      t = N("react-portal-target"), n = fe(), e && e.c(), o = le(), D(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      b(s, t, i), r[8](t), b(s, n, i), e && e.m(s, i), b(s, o, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && y(e, 1)) : (e = k(s), e.c(), y(e, 1), e.m(o.parentNode, o)) : e && (ce(), x(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(s) {
      l || (y(e), l = !0);
    },
    o(s) {
      x(e), l = !1;
    },
    d(s) {
      s && (g(t), g(n), g(o)), r[8](null), e && e.d(s);
    }
  };
}
function O(r) {
  const {
    svelteInit: t,
    ...n
  } = r;
  return n;
}
function ye(r, t, n) {
  let o, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = oe(e);
  let {
    svelteInit: u
  } = t;
  const _ = w(O(t)), a = w();
  S(r, a, (d) => n(0, o = d));
  const c = w();
  S(r, c, (d) => n(1, l = d));
  const f = [], A = pe("$$ms-gr-antd-react-wrapper"), {
    slotKey: M,
    slotIndex: W,
    subSlotIndex: z
  } = Y() || {}, U = u({
    parent: A,
    props: _,
    target: a,
    slot: c,
    slotKey: M,
    slotIndex: W,
    subSlotIndex: z,
    onDestroy(d) {
      f.push(d);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", U), me(() => {
    _.set(O(t));
  }), we(() => {
    f.forEach((d) => d());
  });
  function q(d) {
    C[d ? "unshift" : "push"](() => {
      o = d, a.set(o);
    });
  }
  function G(d) {
    C[d ? "unshift" : "push"](() => {
      l = d, c.set(l);
    });
  }
  return r.$$set = (d) => {
    n(17, t = E(E({}, t), R(d))), "svelteInit" in d && n(5, u = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, t = R(t), [o, l, a, c, i, u, s, e, q, G];
}
class he extends re {
  constructor(t) {
    super(), de(this, t, ye, be, ue, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(r) {
  function t(n) {
    const o = w(), l = new he({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, s], F({
            createPortal: I,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== o), F({
              createPortal: I,
              node: v
            });
          }), s;
        },
        ...n.props
      }
    });
    return o.set(l), l;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(r) {
  return r ? Object.keys(r).reduce((t, n) => {
    const o = r[n];
    return typeof o == "number" && !xe.includes(n) ? t[n] = o + "px" : t[n] = o, t;
  }, {}) : {};
}
function T(r) {
  const t = r.cloneNode(!0);
  Object.keys(r.getEventListeners()).forEach((o) => {
    r.getEventListeners(o).forEach(({
      listener: e,
      type: s,
      useCapture: i
    }) => {
      t.addEventListener(s, e, i);
    });
  });
  const n = Array.from(r.children);
  for (let o = 0; o < n.length; o++) {
    const l = n[o], e = T(l);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Ee(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const Ce = H(({
  slot: r,
  clone: t,
  className: n,
  style: o
}, l) => {
  const e = K();
  return B(() => {
    var _;
    if (!e.current || !r)
      return;
    let s = r;
    function i() {
      let a = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (a = s.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ee(l, a), n && a.classList.add(...n.split(" ")), o) {
        const c = Ie(o);
        Object.keys(c).forEach((f) => {
          a.style[f] = c[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var c;
        s = T(r), s.style.display = "contents", i(), (c = e.current) == null || c.appendChild(s);
      };
      a(), u = new window.MutationObserver(() => {
        var c, f;
        (c = e.current) != null && c.contains(s) && ((f = e.current) == null || f.removeChild(s)), a();
      }), u.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(s);
    return () => {
      var a, c;
      s.style.display = "", (a = e.current) != null && a.contains(s) && ((c = e.current) == null || c.removeChild(s)), u == null || u.disconnect();
    };
  }, [r, t, n, o, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Se(r) {
  try {
    return typeof r == "string" ? new Function(`return (...args) => (${r})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function p(r) {
  return J(() => Se(r), [r]);
}
const ke = ve(({
  slots: r,
  children: t,
  count: n,
  showCount: o,
  onValueChange: l,
  onChange: e,
  elRef: s,
  ...i
}) => {
  const u = p(n == null ? void 0 : n.strategy), _ = p(n == null ? void 0 : n.exceedFormatter), a = p(n == null ? void 0 : n.show), c = p(typeof o == "object" ? o.formatter : void 0);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ m.jsx(Q.TextArea, {
      ...i,
      ref: s,
      onChange: (f) => {
        e == null || e(f), l(f.target.value);
      },
      showCount: typeof o == "object" && c ? {
        formatter: c
      } : o,
      count: {
        ...n,
        exceedFormatter: _,
        strategy: u,
        show: a || (n == null ? void 0 : n.show)
      },
      allowClear: r["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(Ce, {
          slot: r["allowClear.clearIcon"]
        })
      } : i.allowClear
    })]
  });
});
export {
  ke as InputTextarea,
  ke as default
};
