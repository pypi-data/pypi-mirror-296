import { g as J, w as m } from "./Index-DGsIGvXt.js";
const j = window.ms_globals.React, K = window.ms_globals.React.forwardRef, M = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.Tag;
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
L.exports = b;
var h = L.exports;
const {
  SvelteComponent: te,
  assign: x,
  binding_callbacks: E,
  check_outros: ne,
  component_subscribe: C,
  compute_slots: oe,
  create_slot: re,
  detach: p,
  element: T,
  empty: se,
  exclude_internal_props: R,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: ae,
  insert: g,
  safe_not_equal: ue,
  set_custom_element_data: D,
  space: de,
  transition_in: w,
  transition_out: v,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: me,
  onDestroy: pe,
  setContext: ge
} = window.__gradio__svelte__internal;
function S(n) {
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
      t = T("svelte-slot"), l && l.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      g(e, t, o), l && l.m(t, null), n[9](t), s = !0;
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
      s || (w(l, e), s = !0);
    },
    o(e) {
      v(l, e), s = !1;
    },
    d(e) {
      e && p(t), l && l.d(e), n[9](null);
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
      t = T("react-portal-target"), s = de(), e && e.c(), r = se(), D(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      g(o, t, i), n[8](t), g(o, s, i), e && e.m(o, i), g(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && w(e, 1)) : (e = S(o), e.c(), w(e, 1), e.m(r.parentNode, r)) : e && (ce(), v(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(o) {
      l || (w(e), l = !0);
    },
    o(o) {
      v(e), l = !1;
    },
    d(o) {
      o && (p(t), p(s), p(r)), n[8](null), e && e.d(o);
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
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const i = oe(e);
  let {
    svelteInit: d
  } = t;
  const _ = m(k(t)), c = m();
  C(n, c, (a) => s(0, r = a));
  const u = m();
  C(n, u, (a) => s(1, l = a));
  const f = [], z = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: F,
    subSlotIndex: U
  } = J() || {}, q = d({
    parent: z,
    props: _,
    target: c,
    slot: u,
    slotKey: A,
    slotIndex: F,
    subSlotIndex: U,
    onDestroy(a) {
      f.push(a);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", q), _e(() => {
    _.set(k(t));
  }), pe(() => {
    f.forEach((a) => a());
  });
  function G(a) {
    E[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function H(a) {
    E[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return n.$$set = (a) => {
    s(17, t = x(x({}, t), R(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, t = R(t), [r, l, c, u, i, d, o, e, G, H];
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
    const r = m(), l = new he({
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
            createPortal: I,
            node: y
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), O({
              createPortal: I,
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
function Ie(n) {
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
function xe(n, t) {
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
    var _;
    if (!e.current || !n)
      return;
    let o = n;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), xe(l, c), s && c.classList.add(...s.split(" ")), r) {
        const u = Ie(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var u;
        o = W(n), o.style.display = "contents", i(), (u = e.current) == null || u.appendChild(o);
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
      o.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(o);
    return () => {
      var c, u;
      o.style.display = "", (c = e.current) != null && c.contains(o) && ((u = e.current) == null || u.removeChild(o)), d == null || d.disconnect();
    };
  }, [n, t, s, r, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ce = ye(({
  slots: n,
  ...t
}) => /* @__PURE__ */ h.jsx(Y, {
  ...t,
  icon: n.icon ? /* @__PURE__ */ h.jsx(P, {
    slot: n.icon
  }) : t.icon,
  closeIcon: n.closeIcon ? /* @__PURE__ */ h.jsx(P, {
    slot: n.closeIcon
  }) : t.closeIcon
}));
export {
  Ce as Tag,
  Ce as default
};
