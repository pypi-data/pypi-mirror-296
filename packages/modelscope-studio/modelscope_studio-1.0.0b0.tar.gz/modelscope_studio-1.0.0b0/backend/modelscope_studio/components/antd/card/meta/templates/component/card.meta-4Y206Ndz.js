import { g as J, w as p } from "./Index-DRwCu6xC.js";
const j = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, C = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.Card;
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
h.Fragment = X;
h.jsx = N;
h.jsxs = N;
L.exports = h;
var m = L.exports;
const {
  SvelteComponent: te,
  assign: E,
  binding_callbacks: I,
  check_outros: ne,
  component_subscribe: R,
  compute_slots: re,
  create_slot: oe,
  detach: g,
  element: D,
  empty: se,
  exclude_internal_props: S,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ae,
  init: ce,
  insert: w,
  safe_not_equal: de,
  set_custom_element_data: M,
  space: ue,
  transition_in: b,
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
      t = D("svelte-slot"), l && l.c(), M(t, "class", "svelte-1rt0kpf");
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
function we(n) {
  let t, s, o, l, e = (
    /*$$slots*/
    n[4].default && k(n)
  );
  return {
    c() {
      t = D("react-portal-target"), s = ue(), e && e.c(), o = se(), M(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      w(r, t, i), n[8](t), w(r, s, i), e && e.m(r, i), w(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = k(r), e.c(), b(e, 1), e.m(o.parentNode, o)) : e && (ae(), x(e, 1, 1, () => {
        e = null;
      }), ne());
    },
    i(r) {
      l || (b(e), l = !0);
    },
    o(r) {
      x(e), l = !1;
    },
    d(r) {
      r && (g(t), g(s), g(o)), n[8](null), e && e.d(r);
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
function be(n, t, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = re(e);
  let {
    svelteInit: u
  } = t;
  const _ = p(O(t)), a = p();
  R(n, a, (c) => s(0, o = c));
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
    I[c ? "unshift" : "push"](() => {
      o = c, a.set(o);
    });
  }
  function G(c) {
    I[c ? "unshift" : "push"](() => {
      l = c, d.set(l);
    });
  }
  return n.$$set = (c) => {
    s(17, t = E(E({}, t), S(c))), "svelteInit" in c && s(5, u = c.svelteInit), "$$scope" in c && s(6, r = c.$$scope);
  }, t = S(t), [o, l, a, d, i, u, r, e, q, G];
}
class he extends te {
  constructor(t) {
    super(), ce(this, t, be, we, de, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(n) {
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
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, r], P({
            createPortal: C,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== o), P({
              createPortal: C,
              node: v
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
function xe(n) {
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
function Ce(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const y = H(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, l) => {
  const e = K();
  return B(() => {
    var _;
    if (!e.current || !n)
      return;
    let r = n;
    function i() {
      let a = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (a = r.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ce(l, a), s && a.classList.add(...s.split(" ")), o) {
        const d = xe(o);
        Object.keys(d).forEach((f) => {
          a.style[f] = d[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var d;
        r = W(n), r.style.display = "contents", i(), (d = e.current) == null || d.appendChild(r);
      };
      a(), u = new window.MutationObserver(() => {
        var d, f;
        (d = e.current) != null && d.contains(r) && ((f = e.current) == null || f.removeChild(r)), a();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (_ = e.current) == null || _.appendChild(r);
    return () => {
      var a, d;
      r.style.display = "", (a = e.current) != null && a.contains(r) && ((d = e.current) == null || d.removeChild(r)), u == null || u.disconnect();
    };
  }, [n, t, s, o, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ie = ve(({
  slots: n,
  ...t
}) => /* @__PURE__ */ m.jsx(Y.Meta, {
  ...t,
  title: n.title ? /* @__PURE__ */ m.jsx(y, {
    slot: n.title
  }) : t.title,
  description: n.description ? /* @__PURE__ */ m.jsx(y, {
    slot: n.description
  }) : t.description,
  avatar: n.avatar ? /* @__PURE__ */ m.jsx(y, {
    slot: n.avatar
  }) : t.avatar
}));
export {
  Ie as CardMeta,
  Ie as default
};
