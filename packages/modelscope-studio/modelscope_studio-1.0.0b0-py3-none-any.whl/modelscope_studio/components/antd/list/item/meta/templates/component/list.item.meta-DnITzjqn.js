import { g as J, w as p } from "./Index-BvQVhzw1.js";
const L = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, B = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, Y = window.ms_globals.antd.List;
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
var Q = L, V = Symbol.for("react.element"), X = Symbol.for("react.fragment"), Z = Object.prototype.hasOwnProperty, $ = Q.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ee = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function N(n, t, o) {
  var s, l = {}, e = null, r = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (s in t) Z.call(t, s) && !ee.hasOwnProperty(s) && (l[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
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
P.exports = h;
var _ = P.exports;
const {
  SvelteComponent: te,
  assign: E,
  binding_callbacks: C,
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
  set_custom_element_data: F,
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
  let t, o;
  const s = (
    /*#slots*/
    n[7].default
  ), l = oe(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = D("svelte-slot"), l && l.c(), F(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      w(e, t, r), l && l.m(t, null), n[9](t), o = !0;
    },
    p(e, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && fe(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? ie(
          s,
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
      o || (b(l, e), o = !0);
    },
    o(e) {
      x(l, e), o = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function we(n) {
  let t, o, s, l, e = (
    /*$$slots*/
    n[4].default && k(n)
  );
  return {
    c() {
      t = D("react-portal-target"), o = ue(), e && e.c(), s = se(), F(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      w(r, t, i), n[8](t), w(r, o, i), e && e.m(r, i), w(r, s, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = k(r), e.c(), b(e, 1), e.m(s.parentNode, s)) : e && (ae(), x(e, 1, 1, () => {
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
      r && (g(t), g(o), g(s)), n[8](null), e && e.d(r);
    }
  };
}
function O(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function be(n, t, o) {
  let s, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = re(e);
  let {
    svelteInit: u
  } = t;
  const m = p(O(t)), a = p();
  R(n, a, (c) => o(0, s = c));
  const d = p();
  R(n, d, (c) => o(1, l = c));
  const f = [], W = me("$$ms-gr-antd-react-wrapper"), {
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T
  } = J() || {}, U = u({
    parent: W,
    props: m,
    target: a,
    slot: d,
    slotKey: z,
    slotIndex: A,
    subSlotIndex: T,
    onDestroy(c) {
      f.push(c);
    }
  });
  ge("$$ms-gr-antd-react-wrapper", U), _e(() => {
    m.set(O(t));
  }), pe(() => {
    f.forEach((c) => c());
  });
  function q(c) {
    C[c ? "unshift" : "push"](() => {
      s = c, a.set(s);
    });
  }
  function G(c) {
    C[c ? "unshift" : "push"](() => {
      l = c, d.set(l);
    });
  }
  return n.$$set = (c) => {
    o(17, t = E(E({}, t), S(c))), "svelteInit" in c && o(5, u = c.svelteInit), "$$scope" in c && o(6, r = c.$$scope);
  }, t = S(t), [s, l, a, d, i, u, r, e, q, G];
}
class he extends te {
  constructor(t) {
    super(), ce(this, t, be, we, de, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(n) {
  function t(o) {
    const s = p(), l = new he({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, r], j({
            createPortal: I,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== s), j({
              createPortal: I,
              node: v
            });
          }), r;
        },
        ...o.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
const ye = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !ye.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function M(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: e,
      type: r,
      useCapture: i
    }) => {
      t.addEventListener(r, e, i);
    });
  });
  const o = Array.from(n.children);
  for (let s = 0; s < o.length; s++) {
    const l = o[s], e = M(l);
    t.replaceChild(e, t.children[s]);
  }
  return t;
}
function Ie(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const y = H(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, l) => {
  const e = K();
  return B(() => {
    var m;
    if (!e.current || !n)
      return;
    let r = n;
    function i() {
      let a = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (a = r.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ie(l, a), o && a.classList.add(...o.split(" ")), s) {
        const d = xe(s);
        Object.keys(d).forEach((f) => {
          a.style[f] = d[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var d;
        r = M(n), r.style.display = "contents", i(), (d = e.current) == null || d.appendChild(r);
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
      r.style.display = "contents", i(), (m = e.current) == null || m.appendChild(r);
    return () => {
      var a, d;
      r.style.display = "", (a = e.current) != null && a.contains(r) && ((d = e.current) == null || d.removeChild(r)), u == null || u.disconnect();
    };
  }, [n, t, o, s, l]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
}), Ce = ve(({
  slots: n,
  children: t,
  ...o
}) => /* @__PURE__ */ _.jsxs(_.Fragment, {
  children: [/* @__PURE__ */ _.jsx(_.Fragment, {
    children: t
  }), /* @__PURE__ */ _.jsx(Y.Item.Meta, {
    ...o,
    avatar: n.avatar ? /* @__PURE__ */ _.jsx(y, {
      slot: n.avatar
    }) : o.avatar,
    description: n.description ? /* @__PURE__ */ _.jsx(y, {
      slot: n.description
    }) : o.description,
    title: n.title ? /* @__PURE__ */ _.jsx(y, {
      slot: n.title
    }) : o.title
  })]
}));
export {
  Ce as ListItemMeta,
  Ce as default
};
