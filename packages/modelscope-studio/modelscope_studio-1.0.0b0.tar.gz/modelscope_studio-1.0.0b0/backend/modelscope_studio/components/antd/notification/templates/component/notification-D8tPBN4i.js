import { g as J, w as g } from "./Index-53fkWtfs.js";
const L = window.ms_globals.React, M = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, N = window.ms_globals.React.useEffect, E = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.notification;
var D = {
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
var Q = L, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), V = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function A(t, n, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) V.call(n, r) && !ee.hasOwnProperty(r) && (l[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: X,
    type: t,
    key: e,
    ref: o,
    props: l,
    _owner: $.current
  };
}
y.Fragment = Z;
y.jsx = A;
y.jsxs = A;
D.exports = y;
var m = D.exports;
const {
  SvelteComponent: te,
  assign: k,
  binding_callbacks: R,
  check_outros: ne,
  component_subscribe: S,
  compute_slots: oe,
  create_slot: re,
  detach: w,
  element: F,
  empty: se,
  exclude_internal_props: C,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: ae,
  insert: b,
  safe_not_equal: de,
  set_custom_element_data: W,
  space: ue,
  transition_in: h,
  transition_out: I,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: me,
  onDestroy: pe,
  setContext: ge
} = window.__gradio__svelte__internal;
function O(t) {
  let n, s;
  const r = (
    /*#slots*/
    t[7].default
  ), l = re(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = F("svelte-slot"), l && l.c(), W(n, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      b(e, n, o), l && l.m(n, null), t[9](n), s = !0;
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
      I(l, e), s = !1;
    },
    d(e) {
      e && w(n), l && l.d(e), t[9](null);
    }
  };
}
function we(t) {
  let n, s, r, l, e = (
    /*$$slots*/
    t[4].default && O(t)
  );
  return {
    c() {
      n = F("react-portal-target"), s = ue(), e && e.c(), r = se(), W(n, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      b(o, n, c), t[8](n), b(o, s, c), e && e.m(o, c), b(o, r, c), l = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && h(e, 1)) : (e = O(o), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (ce(), I(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(o) {
      l || (h(e), l = !0);
    },
    o(o) {
      I(e), l = !1;
    },
    d(o) {
      o && (w(n), w(s), w(r)), t[8](null), e && e.d(o);
    }
  };
}
function j(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function be(t, n, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = n;
  const c = oe(e);
  let {
    svelteInit: u
  } = n;
  const _ = g(j(n)), i = g();
  S(t, i, (d) => s(0, r = d));
  const a = g();
  S(t, a, (d) => s(1, l = d));
  const f = [], v = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: H,
    slotIndex: T,
    subSlotIndex: U
  } = J() || {}, q = u({
    parent: v,
    props: _,
    target: i,
    slot: a,
    slotKey: H,
    slotIndex: T,
    subSlotIndex: U,
    onDestroy(d) {
      f.push(d);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", q), _e(() => {
    _.set(j(n));
  }), pe(() => {
    f.forEach((d) => d());
  });
  function G(d) {
    R[d ? "unshift" : "push"](() => {
      r = d, i.set(r);
    });
  }
  function K(d) {
    R[d ? "unshift" : "push"](() => {
      l = d, a.set(l);
    });
  }
  return t.$$set = (d) => {
    s(17, n = k(k({}, n), C(d))), "svelteInit" in d && s(5, u = d.svelteInit), "$$scope" in d && s(6, o = d.$$scope);
  }, n = C(n), [r, l, i, a, c, u, o, e, G, K];
}
class he extends te {
  constructor(n) {
    super(), ae(this, n, be, we, de, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, x = window.ms_globals.tree;
function ye(t) {
  function n(s) {
    const r = g(), l = new he({
      ...s,
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
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, o], P({
            createPortal: E,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== r), P({
              createPortal: E,
              node: x
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
      s(n);
    });
  });
}
const ve = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const r = t[s];
    return typeof r == "number" && !ve.includes(s) ? n[s] = r + "px" : n[s] = r, n;
  }, {}) : {};
}
function z(t) {
  const n = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: e,
      type: o,
      useCapture: c
    }) => {
      n.addEventListener(o, e, c);
    });
  });
  const s = Array.from(t.children);
  for (let r = 0; r < s.length; r++) {
    const l = s[r], e = z(l);
    n.replaceChild(e, n.children[r]);
  }
  return n;
}
function Ie(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const p = M(({
  slot: t,
  clone: n,
  className: s,
  style: r
}, l) => {
  const e = B();
  return N(() => {
    var _;
    if (!e.current || !t)
      return;
    let o = t;
    function c() {
      let i = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (i = o.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ie(l, i), s && i.classList.add(...s.split(" ")), r) {
        const a = xe(r);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let i = function() {
        var a;
        o = z(t), o.style.display = "contents", c(), (a = e.current) == null || a.appendChild(o);
      };
      i(), u = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(o) && ((f = e.current) == null || f.removeChild(o)), i();
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(o);
    return () => {
      var i, a;
      o.style.display = "", (i = e.current) != null && i.contains(o) && ((a = e.current) == null || a.removeChild(o)), u == null || u.disconnect();
    };
  }, [t, n, s, r, l]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), ke = ye(({
  slots: t,
  bottom: n,
  rtl: s,
  stack: r,
  top: l,
  maxCount: e,
  children: o,
  visible: c,
  onClose: u,
  onVisible: _,
  ...i
}) => {
  const [a, f] = Y.useNotification({
    bottom: n,
    rtl: s,
    stack: r,
    top: l,
    maxCount: e
  });
  return N(() => (c ? a.open({
    ...i,
    btn: t.btn ? /* @__PURE__ */ m.jsx(p, {
      slot: t.btn
    }) : i.btn,
    closeIcon: t.closeIcon ? /* @__PURE__ */ m.jsx(p, {
      slot: t.closeIcon
    }) : i.closeIcon,
    description: t.description ? /* @__PURE__ */ m.jsx(p, {
      slot: t.description
    }) : i.description,
    message: t.message ? /* @__PURE__ */ m.jsx(p, {
      slot: t.message
    }) : i.message,
    icon: t.icon ? /* @__PURE__ */ m.jsx(p, {
      slot: t.icon
    }) : i.icon,
    onClose(...v) {
      _ == null || _(!1), u == null || u(...v);
    }
  }) : a.destroy(i.key), () => {
    a.destroy(i.key);
  }), [c]), /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [o, f]
  });
});
export {
  ke as Notification,
  ke as default
};
