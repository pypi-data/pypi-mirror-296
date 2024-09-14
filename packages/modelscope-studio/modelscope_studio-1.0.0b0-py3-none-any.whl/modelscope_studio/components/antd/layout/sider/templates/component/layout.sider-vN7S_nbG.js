import { g as B, w as m } from "./Index-CK8mbWm2.js";
const L = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, M = window.ms_globals.React.useEffect, v = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Layout;
var P = {
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
var Y = L, Q = Symbol.for("react.element"), V = Symbol.for("react.fragment"), X = Object.prototype.hasOwnProperty, Z = Y.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $ = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(n, t, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (o in t) X.call(t, o) && !$.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: Q,
    type: n,
    key: e,
    ref: r,
    props: l,
    _owner: Z.current
  };
}
b.Fragment = V;
b.jsx = j;
b.jsxs = j;
P.exports = b;
var E = P.exports;
const {
  SvelteComponent: ee,
  assign: x,
  binding_callbacks: I,
  check_outros: te,
  component_subscribe: C,
  compute_slots: ne,
  create_slot: re,
  detach: p,
  element: N,
  empty: oe,
  exclude_internal_props: S,
  get_all_dirty_from_scope: se,
  get_slot_changes: le,
  group_outros: ie,
  init: ce,
  insert: g,
  safe_not_equal: ae,
  set_custom_element_data: D,
  space: ue,
  transition_in: w,
  transition_out: y,
  update_slot_base: de
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: _e,
  onDestroy: me,
  setContext: pe
} = window.__gradio__svelte__internal;
function R(n) {
  let t, s;
  const o = (
    /*#slots*/
    n[7].default
  ), l = re(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), l && l.c(), D(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      g(e, t, r), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && de(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? le(
          o,
          /*$$scope*/
          e[6],
          r,
          null
        ) : se(
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
      y(l, e), s = !1;
    },
    d(e) {
      e && p(t), l && l.d(e), n[9](null);
    }
  };
}
function ge(n) {
  let t, s, o, l, e = (
    /*$$slots*/
    n[4].default && R(n)
  );
  return {
    c() {
      t = N("react-portal-target"), s = ue(), e && e.c(), o = oe(), D(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      g(r, t, i), n[8](t), g(r, s, i), e && e.m(r, i), g(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && w(e, 1)) : (e = R(r), e.c(), w(e, 1), e.m(o.parentNode, o)) : e && (ie(), y(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(r) {
      l || (w(e), l = !0);
    },
    o(r) {
      y(e), l = !1;
    },
    d(r) {
      r && (p(t), p(s), p(o)), n[8](null), e && e.d(r);
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
function we(n, t, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = ne(e);
  let {
    svelteInit: d
  } = t;
  const _ = m(k(t)), c = m();
  C(n, c, (a) => s(0, o = a));
  const u = m();
  C(n, u, (a) => s(1, l = a));
  const f = [], z = _e("$$ms-gr-antd-react-wrapper"), {
    slotKey: A,
    slotIndex: F,
    subSlotIndex: T
  } = B() || {}, U = d({
    parent: z,
    props: _,
    target: c,
    slot: u,
    slotKey: A,
    slotIndex: F,
    subSlotIndex: T,
    onDestroy(a) {
      f.push(a);
    }
  });
  pe("$$ms-gr-antd-react-wrapper", U), fe(() => {
    _.set(k(t));
  }), me(() => {
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
    s(17, t = x(x({}, t), S(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, t = S(t), [o, l, c, u, i, d, r, e, q, G];
}
class be extends ee {
  constructor(t) {
    super(), ce(this, t, we, ge, ae, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, h = window.ms_globals.tree;
function he(n) {
  function t(s) {
    const o = m(), l = new be({
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
          }, i = e.parent ?? h;
          return i.nodes = [...i.nodes, r], O({
            createPortal: v,
            node: h
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), O({
              createPortal: v,
              node: h
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
const ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ve(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !ye.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function W(n) {
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
    const l = s[o], e = W(l);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Ee(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const xe = H(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, l) => {
  const e = K();
  return M(() => {
    var _;
    if (!e.current || !n)
      return;
    let r = n;
    function i() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ee(l, c), s && c.classList.add(...s.split(" ")), o) {
        const u = ve(o);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var u;
        r = W(n), r.style.display = "contents", i(), (u = e.current) == null || u.appendChild(r);
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
  }, [n, t, s, o, l]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ce = he(({
  slots: n,
  ...t
}) => /* @__PURE__ */ E.jsx(J.Sider, {
  ...t,
  trigger: n.trigger ? /* @__PURE__ */ E.jsx(xe, {
    slot: n.trigger
  }) : t.trigger
}));
export {
  Ce as LayoutSider,
  Ce as default
};
