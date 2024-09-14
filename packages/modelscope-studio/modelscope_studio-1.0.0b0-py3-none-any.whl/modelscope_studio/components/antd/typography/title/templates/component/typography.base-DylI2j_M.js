import { g as Z, w as x, d as $, a as y, c as ee } from "./Index-C-QChbsP.js";
const P = window.ms_globals.React, T = window.ms_globals.React.useMemo, Y = window.ms_globals.React.useState, U = window.ms_globals.React.useEffect, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, L = window.ms_globals.ReactDOM.createPortal, w = window.ms_globals.antd.Typography;
var B = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = P, oe = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(o, n, t) {
  var s, l = {}, e = null, r = null;
  t !== void 0 && (e = "" + t), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (s in n) re.call(n, s) && !le.hasOwnProperty(s) && (l[s] = n[s]);
  if (o && o.defaultProps) for (s in n = o.defaultProps, n) l[s] === void 0 && (l[s] = n[s]);
  return {
    $$typeof: oe,
    type: o,
    key: e,
    ref: r,
    props: l,
    _owner: se.current
  };
}
S.Fragment = ne;
S.jsx = G;
S.jsxs = G;
B.exports = S;
var f = B.exports;
const {
  SvelteComponent: ie,
  assign: N,
  binding_callbacks: A,
  check_outros: ae,
  component_subscribe: D,
  compute_slots: ce,
  create_slot: ue,
  detach: I,
  element: H,
  empty: de,
  exclude_internal_props: M,
  get_all_dirty_from_scope: pe,
  get_slot_changes: fe,
  group_outros: _e,
  init: ge,
  insert: v,
  safe_not_equal: me,
  set_custom_element_data: K,
  space: be,
  transition_in: C,
  transition_out: j,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: he,
  onDestroy: xe,
  setContext: Ie
} = window.__gradio__svelte__internal;
function W(o) {
  let n, t;
  const s = (
    /*#slots*/
    o[7].default
  ), l = ue(
    s,
    o,
    /*$$scope*/
    o[6],
    null
  );
  return {
    c() {
      n = H("svelte-slot"), l && l.c(), K(n, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      v(e, n, r), l && l.m(n, null), o[9](n), t = !0;
    },
    p(e, r) {
      l && l.p && (!t || r & /*$$scope*/
      64) && ye(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        t ? fe(
          s,
          /*$$scope*/
          e[6],
          r,
          null
        ) : pe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      t || (C(l, e), t = !0);
    },
    o(e) {
      j(l, e), t = !1;
    },
    d(e) {
      e && I(n), l && l.d(e), o[9](null);
    }
  };
}
function ve(o) {
  let n, t, s, l, e = (
    /*$$slots*/
    o[4].default && W(o)
  );
  return {
    c() {
      n = H("react-portal-target"), t = be(), e && e.c(), s = de(), K(n, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      v(r, n, i), o[8](n), v(r, t, i), e && e.m(r, i), v(r, s, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, i), i & /*$$slots*/
      16 && C(e, 1)) : (e = W(r), e.c(), C(e, 1), e.m(s.parentNode, s)) : e && (_e(), j(e, 1, 1, () => {
        e = null;
      }), ae());
    },
    i(r) {
      l || (C(e), l = !0);
    },
    o(r) {
      j(e), l = !1;
    },
    d(r) {
      r && (I(n), I(t), I(s)), o[8](null), e && e.d(r);
    }
  };
}
function z(o) {
  const {
    svelteInit: n,
    ...t
  } = o;
  return t;
}
function Ce(o, n, t) {
  let s, l, {
    $$slots: e = {},
    $$scope: r
  } = n;
  const i = ce(e);
  let {
    svelteInit: d
  } = n;
  const g = x(z(n)), a = x();
  D(o, a, (u) => t(0, s = u));
  const c = x();
  D(o, c, (u) => t(1, l = u));
  const p = [], m = he("$$ms-gr-antd-react-wrapper"), {
    slotKey: b,
    slotIndex: E,
    subSlotIndex: R
  } = Z() || {}, k = d({
    parent: m,
    props: g,
    target: a,
    slot: c,
    slotKey: b,
    slotIndex: E,
    subSlotIndex: R,
    onDestroy(u) {
      p.push(u);
    }
  });
  Ie("$$ms-gr-antd-react-wrapper", k), we(() => {
    g.set(z(n));
  }), xe(() => {
    p.forEach((u) => u());
  });
  function J(u) {
    A[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  function V(u) {
    A[u ? "unshift" : "push"](() => {
      l = u, c.set(l);
    });
  }
  return o.$$set = (u) => {
    t(17, n = N(N({}, n), M(u))), "svelteInit" in u && t(5, d = u.svelteInit), "$$scope" in u && t(6, r = u.$$scope);
  }, n = M(n), [s, l, a, c, i, d, r, e, J, V];
}
class Se extends ie {
  constructor(n) {
    super(), ge(this, n, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ee(o) {
  function n(t) {
    const s = x(), l = new Se({
      ...t,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: o,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, r], F({
            createPortal: L,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== s), F({
              createPortal: L,
              node: O
            });
          }), r;
        },
        ...t.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((t) => {
    window.ms_globals.initializePromise.then(() => {
      t(n);
    });
  });
}
function Re(o) {
  const [n, t] = Y(() => y(o));
  return U(() => {
    let s = !0;
    return o.subscribe((e) => {
      s && (s = !1, e === n) || t(e);
    });
  }, [o]), n;
}
function ke(o) {
  const n = T(() => $(o, (t) => t), [o]);
  return Re(n);
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(o) {
  return o ? Object.keys(o).reduce((n, t) => {
    const s = o[t];
    return typeof s == "number" && !Oe.includes(t) ? n[t] = s + "px" : n[t] = s, n;
  }, {}) : {};
}
function q(o) {
  const n = o.cloneNode(!0);
  Object.keys(o.getEventListeners()).forEach((s) => {
    o.getEventListeners(s).forEach(({
      listener: e,
      type: r,
      useCapture: i
    }) => {
      n.addEventListener(r, e, i);
    });
  });
  const t = Array.from(o.children);
  for (let s = 0; s < t.length; s++) {
    const l = t[s], e = q(l);
    n.replaceChild(e, n.children[s]);
  }
  return n;
}
function Pe(o, n) {
  o && (typeof o == "function" ? o(n) : o.current = n);
}
const _ = Q(({
  slot: o,
  clone: n,
  className: t,
  style: s
}, l) => {
  const e = X();
  return U(() => {
    var g;
    if (!e.current || !o)
      return;
    let r = o;
    function i() {
      let a = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (a = r.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Pe(l, a), t && a.classList.add(...t.split(" ")), s) {
        const c = je(s);
        Object.keys(c).forEach((p) => {
          a.style[p] = c[p];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var c;
        r = q(o), r.style.display = "contents", i(), (c = e.current) == null || c.appendChild(r);
      };
      a(), d = new window.MutationObserver(() => {
        var c, p;
        (c = e.current) != null && c.contains(r) && ((p = e.current) == null || p.removeChild(r)), a();
      }), d.observe(o, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (g = e.current) == null || g.appendChild(r);
    return () => {
      var a, c;
      r.style.display = "", (a = e.current) != null && a.contains(r) && ((c = e.current) == null || c.removeChild(r)), d == null || d.disconnect();
    };
  }, [o, n, t, s, l]), P.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Te(o, n) {
  const t = T(() => P.Children.toArray(o).filter((e) => e.props.node && n === e.props.nodeSlotKey).sort((e, r) => {
    if (e.props.node.slotIndex && r.props.node.slotIndex) {
      const i = y(e.props.node.slotIndex) || 0, d = y(r.props.node.slotIndex) || 0;
      return i - d === 0 && e.props.node.subSlotIndex && r.props.node.subSlotIndex ? (y(e.props.node.subSlotIndex) || 0) - (y(r.props.node.subSlotIndex) || 0) : i - d;
    }
    return 0;
  }).map((e) => e.props.node.target), [o, n]);
  return ke(t);
}
function h(o) {
  return typeof o == "object" && o !== null ? o : {};
}
const Ne = Ee(({
  component: o,
  className: n,
  slots: t,
  children: s,
  copyable: l,
  editable: e,
  ellipsis: r,
  ...i
}) => {
  const d = Te(s, "copyable.tooltips"), g = t["copyable.icon"] || d.length > 0 || l, a = t["editable.icon"] || t["editable.tooltip"] || t["editable.enterIcon"] || e, c = t["ellipsis.symbol"] || t["ellipsis.tooltip"] || t["ellipsis.tooltip.title"] || r, p = h(l), m = h(e), b = h(r), E = T(() => {
    switch (o) {
      case "title":
        return w.Title;
      case "paragraph":
        return w.Paragraph;
      case "text":
        return w.Text;
      case "link":
        return w.Link;
    }
  }, [o]);
  return /* @__PURE__ */ f.jsx(E, {
    ...i,
    className: ee(n, `ms-gr-antd-typography-${o}`),
    copyable: g ? {
      ...h(l),
      tooltips: d.length > 0 ? d.map((R, k) => /* @__PURE__ */ f.jsx(_, {
        slot: R
      }, k)) : p.tooltips,
      icon: t["copyable.icon"] ? /* @__PURE__ */ f.jsx(_, {
        slot: t["copyable.icon"]
      }) : p.icon
    } : void 0,
    editable: a ? {
      ...m,
      icon: t["editable.icon"] ? /* @__PURE__ */ f.jsx(_, {
        slot: t["editable.icon"]
      }) : m.icon,
      tooltip: t["editable.tooltip"] ? /* @__PURE__ */ f.jsx(_, {
        slot: t["editable.tooltip"]
      }) : m.tooltip,
      enterIcon: t["editable.enterIcon"] ? /* @__PURE__ */ f.jsx(_, {
        slot: t["editable.enterIcon"]
      }) : m.enterIcon
    } : void 0,
    ellipsis: o === "link" ? !!c : c ? {
      ...b,
      symbol: t["ellipsis.symbol"] ? /* @__PURE__ */ f.jsx(_, {
        slot: t["ellipsis.symbol"]
      }) : b.symbol,
      tooltip: t["ellipsis.tooltip"] ? /* @__PURE__ */ f.jsx(_, {
        slot: t["ellipsis.tooltip"]
      }) : {
        ...b.tooltip,
        title: t["ellipsis.tooltip.title"] ? /* @__PURE__ */ f.jsx(_, {
          slot: t["ellipsis.tooltip.title"]
        }) : b.tooltip.title
      }
    } : void 0,
    children: s
  });
});
export {
  Ne as TypographyBase,
  Ne as default
};
