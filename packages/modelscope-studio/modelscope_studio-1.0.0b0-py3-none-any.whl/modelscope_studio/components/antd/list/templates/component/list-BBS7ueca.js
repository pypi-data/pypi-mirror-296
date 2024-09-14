import { g as J, w as p } from "./Index-Cr9XIy0s.js";
const P = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, E = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.List;
var j = {
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
var Q = P, V = Symbol.for("react.element"), X = Symbol.for("react.fragment"), Z = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) Z.call(t, r) && !ee.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: V,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: $.current
  };
}
b.Fragment = X;
b.jsx = N;
b.jsxs = N;
j.exports = b;
var m = j.exports;
const {
  SvelteComponent: te,
  assign: I,
  binding_callbacks: C,
  check_outros: ne,
  component_subscribe: R,
  compute_slots: oe,
  create_slot: re,
  detach: g,
  element: M,
  empty: se,
  exclude_internal_props: S,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ae,
  init: ce,
  insert: w,
  safe_not_equal: de,
  set_custom_element_data: D,
  space: ue,
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
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = re(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = M("svelte-slot"), l && l.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      w(e, t, o), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && fe(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? ie(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : le(
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
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function we(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && k(n)
  );
  return {
    c() {
      t = M("react-portal-target"), s = ue(), e && e.c(), r = se(), D(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, t, i), n[8](t), w(o, s, i), e && e.m(o, i), w(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = k(o), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (ae(), x(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(o) {
      l || (h(e), l = !0);
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
    svelteInit: u
  } = t;
  const _ = p(O(t)), a = p();
  R(n, a, (c) => s(0, r = c));
  const d = p();
  R(n, d, (c) => s(1, l = c));
  const f = [], z = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: F,
    subSlotIndex: T
  } = J() || {}, U = u({
    parent: z,
    props: _,
    target: a,
    slot: d,
    slotKey: A,
    slotIndex: F,
    subSlotIndex: T,
    onDestroy(c) {
      f.push(c);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", U), _e(() => {
    _.set(O(t));
  }), pe(() => {
    f.forEach((c) => c());
  });
  function q(c) {
    C[c ? "unshift" : "push"](() => {
      r = c, a.set(r);
    });
  }
  function G(c) {
    C[c ? "unshift" : "push"](() => {
      l = c, d.set(l);
    });
  }
  return n.$$set = (c) => {
    s(17, t = I(I({}, t), S(c))), "svelteInit" in c && s(5, u = c.svelteInit), "$$scope" in c && s(6, o = c.$$scope);
  }, t = S(t), [r, l, a, d, i, u, o, e, q, G];
}
class be extends te {
  constructor(t) {
    super(), ce(this, t, he, we, de, {
      svelteInit: 5
    });
  }
}
const L = window.ms_globals.rerender, y = window.ms_globals.tree;
function ye(n) {
  function t(s) {
    const r = p(), l = new be({
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
          return i.nodes = [...i.nodes, o], L({
            createPortal: E,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== r), L({
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
const ve = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !ve.includes(s) ? t[s] = r + "px" : t[s] = r, t;
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
function Ee(n, t) {
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
    var _;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let a = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (a = o.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ee(l, a), s && a.classList.add(...s.split(" ")), r) {
        const d = xe(r);
        Object.keys(d).forEach((f) => {
          a.style[f] = d[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var d;
        o = W(n), o.style.display = "contents", i(), (d = e.current) == null || d.appendChild(o);
      };
      a(), u = new window.MutationObserver(() => {
        var d, f;
        (d = e.current) != null && d.contains(o) && ((f = e.current) == null || f.removeChild(o)), a();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(o);
    return () => {
      var a, d;
      o.style.display = "", (a = e.current) != null && a.contains(o) && ((d = e.current) == null || d.removeChild(o)), u == null || u.disconnect();
    };
  }, [n, t, s, r, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ce = ye(({
  slots: n,
  ...t
}) => /* @__PURE__ */ m.jsx(Y, {
  ...t,
  footer: n.footer ? /* @__PURE__ */ m.jsx(v, {
    slot: n.footer
  }) : t.footer,
  header: n.header ? /* @__PURE__ */ m.jsx(v, {
    slot: n.header
  }) : t.header,
  loadMore: n.loadMore ? /* @__PURE__ */ m.jsx(v, {
    slot: n.loadMore
  }) : t.loadMore
}));
export {
  Ce as List,
  Ce as default
};
