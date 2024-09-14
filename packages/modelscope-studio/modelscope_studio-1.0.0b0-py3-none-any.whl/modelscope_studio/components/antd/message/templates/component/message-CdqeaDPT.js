import { g as J, w as p } from "./Index-2LKISQrB.js";
const j = window.ms_globals.React, K = window.ms_globals.React.forwardRef, B = window.ms_globals.React.useRef, L = window.ms_globals.React.useEffect, x = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.message;
var N = {
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
var Q = j, X = Symbol.for("react.element"), Z = Symbol.for("react.fragment"), V = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function D(n, t, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (o in t) V.call(t, o) && !ee.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: X,
    type: n,
    key: e,
    ref: r,
    props: l,
    _owner: $.current
  };
}
y.Fragment = Z;
y.jsx = D;
y.jsxs = D;
N.exports = y;
var m = N.exports;
const {
  SvelteComponent: te,
  assign: E,
  binding_callbacks: I,
  check_outros: ne,
  component_subscribe: k,
  compute_slots: re,
  create_slot: oe,
  detach: g,
  element: A,
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
  transition_in: h,
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
      t = A("svelte-slot"), l && l.c(), F(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      w(e, t, r), l && l.m(t, null), n[9](t), s = !0;
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
      s || (h(l, e), s = !0);
    },
    o(e) {
      v(l, e), s = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function we(n) {
  let t, s, o, l, e = (
    /*$$slots*/
    n[4].default && S(n)
  );
  return {
    c() {
      t = A("react-portal-target"), s = de(), e && e.c(), o = se(), F(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      w(r, t, i), n[8](t), w(r, s, i), e && e.m(r, i), w(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = S(r), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (ce(), v(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(r) {
      l || (h(e), l = !0);
    },
    o(r) {
      v(e), l = !1;
    },
    d(r) {
      r && (g(t), g(s), g(o)), n[8](null), e && e.d(r);
    }
  };
}
function C(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function he(n, t, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = re(e);
  let {
    svelteInit: d
  } = t;
  const _ = p(C(t)), c = p();
  k(n, c, (a) => s(0, o = a));
  const u = p();
  k(n, u, (a) => s(1, l = a));
  const f = [], W = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: H,
    subSlotIndex: T
  } = J() || {}, U = d({
    parent: W,
    props: _,
    target: c,
    slot: u,
    slotKey: z,
    slotIndex: H,
    subSlotIndex: T,
    onDestroy(a) {
      f.push(a);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", U), _e(() => {
    _.set(C(t));
  }), pe(() => {
    f.forEach((a) => a());
  });
  function q(a) {
    I[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  function G(a) {
    I[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return n.$$set = (a) => {
    s(17, t = E(E({}, t), R(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, t = R(t), [o, l, c, u, i, d, r, e, q, G];
}
class ye extends te {
  constructor(t) {
    super(), ae(this, t, he, we, ue, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, b = window.ms_globals.tree;
function be(n) {
  function t(s) {
    const o = p(), l = new ye({
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
          }, i = e.parent ?? b;
          return i.nodes = [...i.nodes, r], O({
            createPortal: x,
            node: b
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), O({
              createPortal: x,
              node: b
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
function M(n) {
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
    const l = s[o], e = M(l);
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
  const e = B();
  return L(() => {
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
        r = M(n), r.style.display = "contents", i(), (u = e.current) == null || u.appendChild(r);
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
}), ke = be(({
  slots: n,
  children: t,
  visible: s,
  onVisible: o,
  onClose: l,
  ...e
}) => {
  const [r, i] = Y.useMessage();
  return L(() => (s ? r.open({
    ...e,
    icon: n.icon ? /* @__PURE__ */ m.jsx(P, {
      slot: n.icon
    }) : e.icon,
    content: n.content ? /* @__PURE__ */ m.jsx(P, {
      slot: n.content
    }) : e.content,
    onClose(...d) {
      o == null || o(!1), l == null || l(...d);
    }
  }) : r.destroy(e.key), () => {
    r.destroy(e.key);
  }), [s]), /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), i]
  });
});
export {
  ke as Message,
  ke as default
};
