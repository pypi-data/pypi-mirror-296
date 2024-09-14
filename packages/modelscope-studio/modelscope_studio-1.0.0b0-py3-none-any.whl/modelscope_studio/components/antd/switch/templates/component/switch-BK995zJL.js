import { g as J, w as p } from "./Index-BBY2WLfi.js";
const j = window.ms_globals.React, K = window.ms_globals.React.forwardRef, M = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, C = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.Switch;
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
var Q = j, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), V = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(n, t, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (r in t) V.call(t, r) && !ee.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: X,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: $.current
  };
}
b.Fragment = Z;
b.jsx = N;
b.jsxs = N;
L.exports = b;
var _ = L.exports;
const {
  SvelteComponent: te,
  assign: k,
  binding_callbacks: x,
  check_outros: ne,
  component_subscribe: E,
  compute_slots: re,
  create_slot: oe,
  detach: h,
  element: D,
  empty: se,
  exclude_internal_props: I,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: de,
  insert: w,
  safe_not_equal: ae,
  set_custom_element_data: F,
  space: ue,
  transition_in: g,
  transition_out: v,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: me,
  onDestroy: pe,
  setContext: he
} = window.__gradio__svelte__internal;
function S(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = oe(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), l && l.c(), F(t, "class", "svelte-1rt0kpf");
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
      s || (g(l, e), s = !0);
    },
    o(e) {
      v(l, e), s = !1;
    },
    d(e) {
      e && h(t), l && l.d(e), n[9](null);
    }
  };
}
function we(n) {
  let t, s, r, l, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = D("react-portal-target"), s = ue(), e && e.c(), r = se(), F(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      w(o, t, i), n[8](t), w(o, s, i), e && e.m(o, i), w(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && g(e, 1)) : (e = S(o), e.c(), g(e, 1), e.m(r.parentNode, r)) : e && (ce(), v(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(o) {
      l || (g(e), l = !0);
    },
    o(o) {
      v(e), l = !1;
    },
    d(o) {
      o && (h(t), h(s), h(r)), n[8](null), e && e.d(o);
    }
  };
}
function R(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function ge(n, t, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = re(e);
  let {
    svelteInit: u
  } = t;
  const m = p(R(t)), c = p();
  E(n, c, (d) => s(0, r = d));
  const a = p();
  E(n, a, (d) => s(1, l = d));
  const f = [], z = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U
  } = J() || {}, q = u({
    parent: z,
    props: m,
    target: c,
    slot: a,
    slotKey: A,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(d) {
      f.push(d);
    }
  });
  he("$$ms-gr-antd-react-wrapper", q), _e(() => {
    m.set(R(t));
  }), pe(() => {
    f.forEach((d) => d());
  });
  function G(d) {
    x[d ? "unshift" : "push"](() => {
      r = d, c.set(r);
    });
  }
  function H(d) {
    x[d ? "unshift" : "push"](() => {
      l = d, a.set(l);
    });
  }
  return n.$$set = (d) => {
    s(17, t = k(k({}, t), I(d))), "svelteInit" in d && s(5, u = d.svelteInit), "$$scope" in d && s(6, o = d.$$scope);
  }, t = I(t), [r, l, c, a, i, u, o, e, G, H];
}
class be extends te {
  constructor(t) {
    super(), de(this, t, ge, we, ae, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, y = window.ms_globals.tree;
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
          return i.nodes = [...i.nodes, o], O({
            createPortal: C,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== r), O({
              createPortal: C,
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
function Ce(n) {
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
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const P = K(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, l) => {
  const e = M();
  return B(() => {
    var m;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ke(l, c), s && c.classList.add(...s.split(" ")), r) {
        const a = Ce(r);
        Object.keys(a).forEach((f) => {
          c.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var a;
        o = W(n), o.style.display = "contents", i(), (a = e.current) == null || a.appendChild(o);
      };
      c(), u = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(o) && ((f = e.current) == null || f.removeChild(o)), c();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (m = e.current) == null || m.appendChild(o);
    return () => {
      var c, a;
      o.style.display = "", (c = e.current) != null && c.contains(o) && ((a = e.current) == null || a.removeChild(o)), u == null || u.disconnect();
    };
  }, [n, t, s, r, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ee = ye(({
  slots: n,
  children: t,
  onValueChange: s,
  onChange: r,
  ...l
}) => /* @__PURE__ */ _.jsxs(_.Fragment, {
  children: [/* @__PURE__ */ _.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ _.jsx(Y, {
    ...l,
    onChange: (e, ...o) => {
      s == null || s(e), r == null || r(e, ...o);
    },
    checkedChildren: n.checkedChildren ? /* @__PURE__ */ _.jsx(P, {
      slot: n.checkedChildren
    }) : l.checkedChildren,
    unCheckedChildren: n.unCheckedChildren ? /* @__PURE__ */ _.jsx(P, {
      slot: n.unCheckedChildren
    }) : l.unCheckedChildren
  })]
}));
export {
  Ee as Switch,
  Ee as default
};
