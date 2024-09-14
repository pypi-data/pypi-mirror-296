import { g as J, w as p } from "./Index-Bc-T_mI-.js";
const P = window.ms_globals.React, K = window.ms_globals.React.forwardRef, M = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, C = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.Statistic;
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
var Q = P, V = Symbol.for("react.element"), X = Symbol.for("react.fragment"), Z = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(r, t, o) {
  var n, l = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) Z.call(t, n) && !ee.hasOwnProperty(n) && (l[n] = t[n]);
  if (r && r.defaultProps) for (n in t = r.defaultProps, t) l[n] === void 0 && (l[n] = t[n]);
  return {
    $$typeof: V,
    type: r,
    key: e,
    ref: s,
    props: l,
    _owner: $.current
  };
}
h.Fragment = X;
h.jsx = N;
h.jsxs = N;
L.exports = h;
var _ = L.exports;
const {
  SvelteComponent: te,
  assign: E,
  binding_callbacks: I,
  check_outros: ne,
  component_subscribe: S,
  compute_slots: re,
  create_slot: oe,
  detach: g,
  element: D,
  empty: se,
  exclude_internal_props: R,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: ae,
  insert: w,
  safe_not_equal: ue,
  set_custom_element_data: F,
  space: de,
  transition_in: b,
  transition_out: v,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: me,
  onDestroy: pe,
  setContext: ge
} = window.__gradio__svelte__internal;
function k(r) {
  let t, o;
  const n = (
    /*#slots*/
    r[7].default
  ), l = oe(
    n,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), l && l.c(), F(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      w(e, t, s), l && l.m(t, null), r[9](t), o = !0;
    },
    p(e, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && fe(
        l,
        n,
        e,
        /*$$scope*/
        e[6],
        o ? ie(
          n,
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
      o || (b(l, e), o = !0);
    },
    o(e) {
      v(l, e), o = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), r[9](null);
    }
  };
}
function we(r) {
  let t, o, n, l, e = (
    /*$$slots*/
    r[4].default && k(r)
  );
  return {
    c() {
      t = D("react-portal-target"), o = de(), e && e.c(), n = se(), F(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      w(s, t, i), r[8](t), w(s, o, i), e && e.m(s, i), w(s, n, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = k(s), e.c(), b(e, 1), e.m(n.parentNode, n)) : e && (ce(), v(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(s) {
      l || (b(e), l = !0);
    },
    o(s) {
      v(e), l = !1;
    },
    d(s) {
      s && (g(t), g(o), g(n)), r[8](null), e && e.d(s);
    }
  };
}
function O(r) {
  const {
    svelteInit: t,
    ...o
  } = r;
  return o;
}
function be(r, t, o) {
  let n, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = re(e);
  let {
    svelteInit: d
  } = t;
  const m = p(O(t)), c = p();
  S(r, c, (a) => o(0, n = a));
  const u = p();
  S(r, u, (a) => o(1, l = a));
  const f = [], z = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U
  } = J() || {}, q = d({
    parent: z,
    props: m,
    target: c,
    slot: u,
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(a) {
      f.push(a);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", q), _e(() => {
    m.set(O(t));
  }), pe(() => {
    f.forEach((a) => a());
  });
  function G(a) {
    I[a ? "unshift" : "push"](() => {
      n = a, c.set(n);
    });
  }
  function H(a) {
    I[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return r.$$set = (a) => {
    o(17, t = E(E({}, t), R(a))), "svelteInit" in a && o(5, d = a.svelteInit), "$$scope" in a && o(6, s = a.$$scope);
  }, t = R(t), [n, l, c, u, i, d, s, e, G, H];
}
class he extends te {
  constructor(t) {
    super(), ae(this, t, be, we, ue, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, y = window.ms_globals.tree;
function ye(r) {
  function t(o) {
    const n = p(), l = new he({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? y;
          return i.nodes = [...i.nodes, s], j({
            createPortal: C,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== n), j({
              createPortal: C,
              node: y
            });
          }), s;
        },
        ...o.props
      }
    });
    return n.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ve(r) {
  return r ? Object.keys(r).reduce((t, o) => {
    const n = r[o];
    return typeof n == "number" && !xe.includes(o) ? t[o] = n + "px" : t[o] = n, t;
  }, {}) : {};
}
function W(r) {
  const t = r.cloneNode(!0);
  Object.keys(r.getEventListeners()).forEach((n) => {
    r.getEventListeners(n).forEach(({
      listener: e,
      type: s,
      useCapture: i
    }) => {
      t.addEventListener(s, e, i);
    });
  });
  const o = Array.from(r.children);
  for (let n = 0; n < o.length; n++) {
    const l = o[n], e = W(l);
    t.replaceChild(e, t.children[n]);
  }
  return t;
}
function Ce(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const x = K(({
  slot: r,
  clone: t,
  className: o,
  style: n
}, l) => {
  const e = M();
  return B(() => {
    var m;
    if (!e.current || !r)
      return;
    let s = r;
    function i() {
      let c = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (c = s.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ce(l, c), o && c.classList.add(...o.split(" ")), n) {
        const u = ve(n);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var u;
        s = W(r), s.style.display = "contents", i(), (u = e.current) == null || u.appendChild(s);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(s) && ((f = e.current) == null || f.removeChild(s)), c();
      }), d.observe(r, {
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
  }, [r, t, o, n, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ie = ye(({
  children: r,
  value: t,
  slots: o,
  ...n
}) => /* @__PURE__ */ _.jsxs(_.Fragment, {
  children: [/* @__PURE__ */ _.jsx("div", {
    style: {
      display: "none"
    },
    children: r
  }), /* @__PURE__ */ _.jsx(Y.Countdown, {
    ...n,
    value: typeof t == "number" ? t * 1e3 : t,
    title: o.title ? /* @__PURE__ */ _.jsx(x, {
      slot: o.title
    }) : n.title,
    prefix: o.prefix ? /* @__PURE__ */ _.jsx(x, {
      slot: o.prefix
    }) : n.prefix,
    suffix: o.suffix ? /* @__PURE__ */ _.jsx(x, {
      slot: o.suffix
    }) : n.suffix
  })]
}));
export {
  Ie as StatisticCountdown,
  Ie as default
};
