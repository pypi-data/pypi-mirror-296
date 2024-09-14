import { g as J, w as p } from "./Index-rJ_1X_Ua.js";
const j = window.ms_globals.React, K = window.ms_globals.React.forwardRef, M = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, x = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.Spin;
var L = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Q = j, V = Symbol.for("react.element"), X = Symbol.for("react.fragment"), Z = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(n, t, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (o in t) Z.call(t, o) && !ee.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: V,
    type: n,
    key: e,
    ref: r,
    props: l,
    _owner: $.current
  };
}
b.Fragment = X;
b.jsx = N;
b.jsxs = N;
L.exports = b;
var h = L.exports;
const {
  SvelteComponent: te,
  assign: E,
  binding_callbacks: I,
  check_outros: ne,
  component_subscribe: S,
  compute_slots: re,
  create_slot: oe,
  detach: m,
  element: D,
  empty: se,
  exclude_internal_props: C,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: ae,
  insert: g,
  safe_not_equal: ue,
  set_custom_element_data: W,
  space: de,
  transition_in: w,
  transition_out: v,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: pe,
  onDestroy: me,
  setContext: ge
} = window.__gradio__svelte__internal;
function R(n) {
  let t, s;
  const o = (
    /*#slots*/
    n[7].default
  ), l = oe(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), l && l.c(), W(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      g(e, t, r), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && fe(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? ie(
          o,
          /*$$scope*/
          e[6],
          r,
          null
        ) : le(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (w(l, e), s = !0);
    },
    o(e) {
      v(l, e), s = !1;
    },
    d(e) {
      e && m(t), l && l.d(e), n[9](null);
    }
  };
}
function we(n) {
  let t, s, o, l, e = (
    /*$$slots*/
    n[4].default && R(n)
  );
  return {
    c() {
      t = D("react-portal-target"), s = de(), e && e.c(), o = se(), W(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      g(r, t, i), n[8](t), g(r, s, i), e && e.m(r, i), g(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && w(e, 1)) : (e = R(r), e.c(), w(e, 1), e.m(o.parentNode, o)) : e && (ce(), v(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(r) {
      l || (w(e), l = !0);
    },
    o(r) {
      v(e), l = !1;
    },
    d(r) {
      r && (m(t), m(s), m(o)), n[8](null), e && e.d(r);
    }
  };
}
function k(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function be(n, t, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = re(e);
  let {
    svelteInit: d
  } = t;
  const _ = p(k(t)), c = p();
  S(n, c, (a) => s(0, o = a));
  const u = p();
  S(n, u, (a) => s(1, l = a));
  const f = [], A = pe("$$ms-gr-antd-react-wrapper"), {
    slotKey: F,
    slotIndex: T,
    subSlotIndex: U
  } = J() || {}, q = d({
    parent: A,
    props: _,
    target: c,
    slot: u,
    slotKey: F,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(a) {
      f.push(a);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", q), _e(() => {
    _.set(k(t));
  }), me(() => {
    f.forEach((a) => a());
  });
  function G(a) {
    I[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  function H(a) {
    I[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return n.$$set = (a) => {
    s(17, t = E(E({}, t), C(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, t = C(t), [o, l, c, u, i, d, r, e, G, H];
}
class he extends te {
  constructor(t) {
    super(), ae(this, t, be, we, ue, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, y = window.ms_globals.tree;
function ye(n) {
  function t(s) {
    const o = p(), l = new he({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
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
          }, i = e.parent ?? y;
          return i.nodes = [...i.nodes, r], O({
            createPortal: x,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), O({
              createPortal: x,
              node: y
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
      s(t);
    });
  });
}
const ve = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !ve.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function z(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: e,
      type: r,
      useCapture: i
    }) => {
      t.addEventListener(r, e, i);
    });
  });
  const s = Array.from(n.children);
  for (let o = 0; o < s.length; o++) {
    const l = s[o], e = z(l);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Ee(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const P = K(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, l) => {
  const e = M();
  return B(() => {
    var _;
    if (!e.current || !n)
      return;
    let r = n;
    function i() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ee(l, c), s && c.classList.add(...s.split(" ")), o) {
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
        r = z(n), r.style.display = "contents", i(), (u = e.current) == null || u.appendChild(r);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(r) && ((f = e.current) == null || f.removeChild(r)), c();
      }), d.observe(n, {
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
  }, [n, t, s, o, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Se = ye(({
  slots: n,
  ...t
}) => /* @__PURE__ */ h.jsx(Y, {
  ...t,
  tip: n.tip ? /* @__PURE__ */ h.jsx(P, {
    slot: n.tip
  }) : t.tip,
  indicator: n.indicator ? /* @__PURE__ */ h.jsx(P, {
    slot: n.indicator
  }) : t.indicator
}));
export {
  Se as Spin,
  Se as default
};
