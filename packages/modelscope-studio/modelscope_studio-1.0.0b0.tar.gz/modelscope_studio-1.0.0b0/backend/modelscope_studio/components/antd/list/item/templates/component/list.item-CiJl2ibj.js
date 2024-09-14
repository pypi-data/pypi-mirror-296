import { g as Q, w as m, d as X, a as _ } from "./Index-KWMSaLYJ.js";
const I = window.ms_globals.React, N = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, A = window.ms_globals.React.useEffect, V = window.ms_globals.React.forwardRef, Y = window.ms_globals.React.useRef, S = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.antd.List;
var D = {
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
var $ = I, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, oe = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(n, t, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (o in t) ne.call(t, o) && !re.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: ee,
    type: n,
    key: e,
    ref: r,
    props: l,
    _owner: oe.current
  };
}
h.Fragment = te;
h.jsx = M;
h.jsxs = M;
D.exports = h;
var y = D.exports;
const {
  SvelteComponent: se,
  assign: E,
  binding_callbacks: C,
  check_outros: le,
  component_subscribe: R,
  compute_slots: ie,
  create_slot: ae,
  detach: g,
  element: T,
  empty: ce,
  exclude_internal_props: k,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: pe,
  insert: w,
  safe_not_equal: _e,
  set_custom_element_data: W,
  space: me,
  transition_in: b,
  transition_out: v,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: he,
  setContext: ye
} = window.__gradio__svelte__internal;
function O(n) {
  let t, s;
  const o = (
    /*#slots*/
    n[7].default
  ), l = ae(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = T("svelte-slot"), l && l.c(), W(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      w(e, t, r), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && ge(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? de(
          o,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ue(
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
      v(l, e), s = !1;
    },
    d(e) {
      e && g(t), l && l.d(e), n[9](null);
    }
  };
}
function xe(n) {
  let t, s, o, l, e = (
    /*$$slots*/
    n[4].default && O(n)
  );
  return {
    c() {
      t = T("react-portal-target"), s = me(), e && e.c(), o = ce(), W(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      w(r, t, i), n[8](t), w(r, s, i), e && e.m(r, i), w(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = O(r), e.c(), b(e, 1), e.m(o.parentNode, o)) : e && (fe(), v(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(r) {
      l || (b(e), l = !0);
    },
    o(r) {
      v(e), l = !1;
    },
    d(r) {
      r && (g(t), g(s), g(o)), n[8](null), e && e.d(r);
    }
  };
}
function L(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function ve(n, t, s) {
  let o, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const i = ie(e);
  let {
    svelteInit: d
  } = t;
  const p = m(L(t)), a = m();
  R(n, a, (c) => s(0, o = c));
  const u = m();
  R(n, u, (c) => s(1, l = c));
  const f = [], F = be("$$ms-gr-antd-react-wrapper"), {
    slotKey: U,
    slotIndex: G,
    subSlotIndex: H
  } = Q() || {}, K = d({
    parent: F,
    props: p,
    target: a,
    slot: u,
    slotKey: U,
    slotIndex: G,
    subSlotIndex: H,
    onDestroy(c) {
      f.push(c);
    }
  });
  ye("$$ms-gr-antd-react-wrapper", K), we(() => {
    p.set(L(t));
  }), he(() => {
    f.forEach((c) => c());
  });
  function q(c) {
    C[c ? "unshift" : "push"](() => {
      o = c, a.set(o);
    });
  }
  function B(c) {
    C[c ? "unshift" : "push"](() => {
      l = c, u.set(l);
    });
  }
  return n.$$set = (c) => {
    s(17, t = E(E({}, t), k(c))), "svelteInit" in c && s(5, d = c.svelteInit), "$$scope" in c && s(6, r = c.$$scope);
  }, t = k(t), [o, l, a, u, i, d, r, e, q, B];
}
class Ie extends se {
  constructor(t) {
    super(), pe(this, t, ve, xe, _e, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, x = window.ms_globals.tree;
function Se(n) {
  function t(s) {
    const o = m(), l = new Ie({
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
          }, i = e.parent ?? x;
          return i.nodes = [...i.nodes, r], P({
            createPortal: S,
            node: x
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), P({
              createPortal: S,
              node: x
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
function Ee(n) {
  const [t, s] = J(() => _(n));
  return A(() => {
    let o = !0;
    return n.subscribe((e) => {
      o && (o = !1, e === t) || s(e);
    });
  }, [n]), t;
}
function Ce(n) {
  const t = N(() => X(n, (s) => s), [n]);
  return Ee(t);
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !Re.includes(s) ? t[s] = o + "px" : t[s] = o, t;
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
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const j = V(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, l) => {
  const e = Y();
  return A(() => {
    var p;
    if (!e.current || !n)
      return;
    let r = n;
    function i() {
      let a = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (a = r.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Oe(l, a), s && a.classList.add(...s.split(" ")), o) {
        const u = ke(o);
        Object.keys(u).forEach((f) => {
          a.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var u;
        r = z(n), r.style.display = "contents", i(), (u = e.current) == null || u.appendChild(r);
      };
      a(), d = new window.MutationObserver(() => {
        var u, f;
        (u = e.current) != null && u.contains(r) && ((f = e.current) == null || f.removeChild(r)), a();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (p = e.current) == null || p.appendChild(r);
    return () => {
      var a, u;
      r.style.display = "", (a = e.current) != null && a.contains(r) && ((u = e.current) == null || u.removeChild(r)), d == null || d.disconnect();
    };
  }, [n, t, s, o, l]), I.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Le(n, t) {
  const s = N(() => I.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, r) => {
    if (e.props.node.slotIndex && r.props.node.slotIndex) {
      const i = _(e.props.node.slotIndex) || 0, d = _(r.props.node.slotIndex) || 0;
      return i - d === 0 && e.props.node.subSlotIndex && r.props.node.subSlotIndex ? (_(e.props.node.subSlotIndex) || 0) - (_(r.props.node.subSlotIndex) || 0) : i - d;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Ce(s);
}
const je = Se(({
  slots: n,
  children: t,
  ...s
}) => {
  const o = Le(t, "actions");
  return /* @__PURE__ */ y.jsx(Z.Item, {
    ...s,
    extra: n.extra ? /* @__PURE__ */ y.jsx(j, {
      slot: n.extra
    }) : s.extra,
    actions: o.length > 0 ? o.map((l, e) => /* @__PURE__ */ y.jsx(j, {
      slot: l
    }, e)) : s.actions,
    children: t
  });
});
export {
  je as ListItem,
  je as default
};
