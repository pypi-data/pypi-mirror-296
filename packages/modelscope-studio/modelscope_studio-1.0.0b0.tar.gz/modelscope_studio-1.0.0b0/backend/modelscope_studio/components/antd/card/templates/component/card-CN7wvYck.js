import { g as X, w as b, d as Z, a as g } from "./Index-BzKFL4cN.js";
const C = window.ms_globals.React, A = window.ms_globals.React.useMemo, V = window.ms_globals.React.useState, B = window.ms_globals.React.useEffect, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, S = window.ms_globals.ReactDOM.createPortal, E = window.ms_globals.antd.Card;
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
var $ = C, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(n, t, o) {
  var r, l = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) ne.call(t, r) && !oe.hasOwnProperty(r) && (l[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) l[r] === void 0 && (l[r] = t[r]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: s,
    props: l,
    _owner: re.current
  };
}
y.Fragment = te;
y.jsx = M;
y.jsxs = M;
D.exports = y;
var _ = D.exports;
const {
  SvelteComponent: se,
  assign: R,
  binding_callbacks: k,
  check_outros: le,
  component_subscribe: O,
  compute_slots: ie,
  create_slot: ae,
  detach: w,
  element: T,
  empty: ce,
  exclude_internal_props: j,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: _e,
  insert: x,
  safe_not_equal: pe,
  set_custom_element_data: W,
  space: me,
  transition_in: h,
  transition_out: I,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: we,
  onDestroy: xe,
  setContext: he
} = window.__gradio__svelte__internal;
function P(n) {
  let t, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = ae(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = T("svelte-slot"), l && l.c(), W(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      x(e, t, s), l && l.m(t, null), n[9](t), o = !0;
    },
    p(e, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && ge(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        o ? de(
          r,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ue(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (h(l, e), o = !0);
    },
    o(e) {
      I(l, e), o = !1;
    },
    d(e) {
      e && w(t), l && l.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, o, r, l, e = (
    /*$$slots*/
    n[4].default && P(n)
  );
  return {
    c() {
      t = T("react-portal-target"), o = me(), e && e.c(), r = ce(), W(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      x(s, t, i), n[8](t), x(s, o, i), e && e.m(s, i), x(s, r, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && h(e, 1)) : (e = P(s), e.c(), h(e, 1), e.m(r.parentNode, r)) : e && (fe(), I(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(s) {
      l || (h(e), l = !0);
    },
    o(s) {
      I(e), l = !1;
    },
    d(s) {
      s && (w(t), w(o), w(r)), n[8](null), e && e.d(s);
    }
  };
}
function L(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function ve(n, t, o) {
  let r, l, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = ie(e);
  let {
    svelteInit: d
  } = t;
  const p = b(L(t)), a = b();
  O(n, a, (c) => o(0, r = c));
  const u = b();
  O(n, u, (c) => o(1, l = c));
  const f = [], F = we("$$ms-gr-antd-react-wrapper"), {
    slotKey: G,
    slotIndex: U,
    subSlotIndex: H
  } = X() || {}, K = d({
    parent: F,
    props: p,
    target: a,
    slot: u,
    slotKey: G,
    slotIndex: U,
    subSlotIndex: H,
    onDestroy(c) {
      f.push(c);
    }
  });
  he("$$ms-gr-antd-react-wrapper", K), be(() => {
    p.set(L(t));
  }), xe(() => {
    f.forEach((c) => c());
  });
  function q(c) {
    k[c ? "unshift" : "push"](() => {
      r = c, a.set(r);
    });
  }
  function J(c) {
    k[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  return n.$$set = (c) => {
    o(17, t = R(R({}, t), j(c))), "svelteInit" in c && o(5, d = c.svelteInit), "$$scope" in c && o(6, s = c.$$scope);
  }, t = j(t), [r, l, a, u, i, d, s, e, q, J];
}
class Ie extends se {
  constructor(t) {
    super(), _e(this, t, ve, ye, pe, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ce(n) {
  function t(o) {
    const r = b(), l = new Ie({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, i = e.parent ?? v;
          return i.nodes = [...i.nodes, s], N({
            createPortal: S,
            node: v
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), N({
              createPortal: S,
              node: v
            });
          }), s;
        },
        ...o.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function Se(n) {
  const [t, o] = V(() => g(n));
  return B(() => {
    let r = !0;
    return n.subscribe((e) => {
      r && (r = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Ee(n) {
  const t = A(() => Z(n, (o) => o), [n]);
  return Se(t);
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const r = n[o];
    return typeof r == "number" && !Re.includes(o) ? t[o] = r + "px" : t[o] = r, t;
  }, {}) : {};
}
function z(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: e,
      type: s,
      useCapture: i
    }) => {
      t.addEventListener(s, e, i);
    });
  });
  const o = Array.from(n.children);
  for (let r = 0; r < o.length; r++) {
    const l = o[r], e = z(l);
    t.replaceChild(e, t.children[r]);
  }
  return t;
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const m = Y(({
  slot: n,
  clone: t,
  className: o,
  style: r
}, l) => {
  const e = Q();
  return B(() => {
    var p;
    if (!e.current || !n)
      return;
    let s = n;
    function i() {
      let a = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (a = s.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(l, a), o && a.classList.add(...o.split(" ")), r) {
        const u = ke(r);
        Object.keys(u).forEach((f) => {
          a.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var u;
        s = z(n), s.style.display = "contents", i(), (u = e.current) == null || u.appendChild(s);
      };
      a(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(s) && ((f = e.current) == null || f.removeChild(s)), a();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", i(), (p = e.current) == null || p.appendChild(s);
    return () => {
      var a, u;
      s.style.display = "", (a = e.current) != null && a.contains(s) && ((u = e.current) == null || u.removeChild(s)), d == null || d.disconnect();
    };
  }, [n, t, o, r, l]), C.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function je(n, t) {
  const o = A(() => C.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const i = g(e.props.node.slotIndex) || 0, d = g(s.props.node.slotIndex) || 0;
      return i - d === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (g(e.props.node.subSlotIndex) || 0) - (g(s.props.node.subSlotIndex) || 0) : i - d;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Ee(o);
}
const Le = Ce(({
  children: n,
  containsGrid: t,
  slots: o,
  ...r
}) => {
  const l = je(n, "actions");
  return /* @__PURE__ */ _.jsxs(E, {
    ...r,
    title: o.title ? /* @__PURE__ */ _.jsx(m, {
      slot: o.title
    }) : r.title,
    extra: o.extra ? /* @__PURE__ */ _.jsx(m, {
      slot: o.extra
    }) : r.extra,
    cover: o.cover ? /* @__PURE__ */ _.jsx(m, {
      slot: o.cover
    }) : r.cover,
    tabBarExtraContent: o.tabBarExtraContent ? /* @__PURE__ */ _.jsx(m, {
      slot: o.tabBarExtraContent
    }) : r.tabBarExtraContent,
    actions: l.length > 0 ? l.map((e, s) => /* @__PURE__ */ _.jsx(m, {
      slot: e
    }, s)) : r.actions,
    children: [t ? /* @__PURE__ */ _.jsx(E.Grid, {
      style: {
        display: "none"
      }
    }) : null, n]
  });
});
export {
  Le as Card,
  Le as default
};
