import { g as Z, w as v, d as $, a as w } from "./Index-RWr4oiX8.js";
const j = window.ms_globals.React, F = window.ms_globals.React.useMemo, Y = window.ms_globals.React.useState, U = window.ms_globals.React.useEffect, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, L = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Transfer;
var G = {
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
var te = j, ne = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(t, n, s) {
  var r, l = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) re.call(n, r) && !le.hasOwnProperty(r) && (l[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: ne,
    type: t,
    key: e,
    ref: o,
    props: l,
    _owner: se.current
  };
}
S.Fragment = oe;
S.jsx = H;
S.jsxs = H;
G.exports = S;
var m = G.exports;
const {
  SvelteComponent: ie,
  assign: P,
  binding_callbacks: A,
  check_outros: ce,
  component_subscribe: N,
  compute_slots: ae,
  create_slot: ue,
  detach: h,
  element: q,
  empty: de,
  exclude_internal_props: T,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert: x,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: be,
  transition_in: I,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: ye,
  getContext: ve,
  onDestroy: he,
  setContext: xe
} = window.__gradio__svelte__internal;
function D(t) {
  let n, s;
  const r = (
    /*#slots*/
    t[7].default
  ), l = ue(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = q("svelte-slot"), l && l.c(), B(n, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      x(e, n, o), l && l.m(n, null), t[9](n), s = !0;
    },
    p(e, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && we(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? pe(
          r,
          /*$$scope*/
          e[6],
          o,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (I(l, e), s = !0);
    },
    o(e) {
      k(l, e), s = !1;
    },
    d(e) {
      e && h(n), l && l.d(e), t[9](null);
    }
  };
}
function Ie(t) {
  let n, s, r, l, e = (
    /*$$slots*/
    t[4].default && D(t)
  );
  return {
    c() {
      n = q("react-portal-target"), s = be(), e && e.c(), r = de(), B(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      x(o, n, i), t[8](n), x(o, s, i), e && e.m(o, i), x(o, r, i), l = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, i), i & /*$$slots*/
      16 && I(e, 1)) : (e = D(o), e.c(), I(e, 1), e.m(r.parentNode, r)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(o) {
      l || (I(e), l = !0);
    },
    o(o) {
      k(e), l = !1;
    },
    d(o) {
      o && (h(n), h(s), h(r)), t[8](null), e && e.d(o);
    }
  };
}
function M(t) {
  const {
    svelteInit: n,
    ...s
  } = t;
  return s;
}
function Se(t, n, s) {
  let r, l, {
    $$slots: e = {},
    $$scope: o
  } = n;
  const i = ae(e);
  let {
    svelteInit: d
  } = n;
  const p = v(M(n)), c = v();
  N(t, c, (u) => s(0, r = u));
  const a = v();
  N(t, a, (u) => s(1, l = u));
  const _ = [], E = ve("$$ms-gr-antd-react-wrapper"), {
    slotKey: C,
    slotIndex: R,
    subSlotIndex: f
  } = Z() || {}, g = d({
    parent: E,
    props: p,
    target: c,
    slot: a,
    slotKey: C,
    slotIndex: R,
    subSlotIndex: f,
    onDestroy(u) {
      _.push(u);
    }
  });
  xe("$$ms-gr-antd-react-wrapper", g), ye(() => {
    p.set(M(n));
  }), he(() => {
    _.forEach((u) => u());
  });
  function K(u) {
    A[u ? "unshift" : "push"](() => {
      r = u, c.set(r);
    });
  }
  function V(u) {
    A[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return t.$$set = (u) => {
    s(17, n = P(P({}, n), T(u))), "svelteInit" in u && s(5, d = u.svelteInit), "$$scope" in u && s(6, o = u.$$scope);
  }, n = T(n), [r, l, c, a, i, d, o, e, K, V];
}
class Ee extends ie {
  constructor(n) {
    super(), me(this, n, Se, Ie, ge, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ce(t) {
  function n(s) {
    const r = v(), l = new Ee({
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
          }, i = e.parent ?? O;
          return i.nodes = [...i.nodes, o], W({
            createPortal: L,
            node: O
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), W({
              createPortal: L,
              node: O
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
function Re(t) {
  const [n, s] = Y(() => w(t));
  return U(() => {
    let r = !0;
    return t.subscribe((e) => {
      r && (r = !1, e === n) || s(e);
    });
  }, [t]), n;
}
function Oe(t) {
  const n = F(() => $(t, (s) => s), [t]);
  return Re(n);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(t) {
  return t ? Object.keys(t).reduce((n, s) => {
    const r = t[s];
    return typeof r == "number" && !ke.includes(s) ? n[s] = r + "px" : n[s] = r, n;
  }, {}) : {};
}
function J(t) {
  const n = t.cloneNode(!0);
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: e,
      type: o,
      useCapture: i
    }) => {
      n.addEventListener(o, e, i);
    });
  });
  const s = Array.from(t.children);
  for (let r = 0; r < s.length; r++) {
    const l = s[r], e = J(l);
    n.replaceChild(e, n.children[r]);
  }
  return n;
}
function Fe(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const b = Q(({
  slot: t,
  clone: n,
  className: s,
  style: r
}, l) => {
  const e = X();
  return U(() => {
    var p;
    if (!e.current || !t)
      return;
    let o = t;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Fe(l, c), s && c.classList.add(...s.split(" ")), r) {
        const a = je(r);
        Object.keys(a).forEach((_) => {
          c.style[_] = a[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var a;
        o = J(t), o.style.display = "contents", i(), (a = e.current) == null || a.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var a, _;
        (a = e.current) != null && a.contains(o) && ((_ = e.current) == null || _.removeChild(o)), c();
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (p = e.current) == null || p.appendChild(o);
    return () => {
      var c, a;
      o.style.display = "", (c = e.current) != null && c.contains(o) && ((a = e.current) == null || a.removeChild(o)), d == null || d.disconnect();
    };
  }, [t, n, s, r, l]), j.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Le(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function y(t) {
  return F(() => Le(t), [t]);
}
function z(t, n) {
  const s = F(() => j.Children.toArray(t).filter((e) => e.props.node && (!n && !e.props.nodeSlotKey || n && n === e.props.nodeSlotKey)).sort((e, o) => {
    if (e.props.node.slotIndex && o.props.node.slotIndex) {
      const i = w(e.props.node.slotIndex) || 0, d = w(o.props.node.slotIndex) || 0;
      return i - d === 0 && e.props.node.subSlotIndex && o.props.node.subSlotIndex ? (w(e.props.node.subSlotIndex) || 0) - (w(o.props.node.subSlotIndex) || 0) : i - d;
    }
    return 0;
  }).map((e) => e.props.node.target), [t, n]);
  return Oe(s);
}
const Ae = Ce(({
  slots: t,
  children: n,
  render: s,
  filterOption: r,
  footer: l,
  listStyle: e,
  locale: o,
  onChange: i,
  onValueChange: d,
  ...p
}) => {
  const c = z(n, "titles"), a = z(n, "selectAllLabels"), _ = y(s), E = y(e), C = y(l), R = y(r);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ m.jsx(ee, {
      ...p,
      onChange: (f, ...g) => {
        i == null || i(f, ...g), d(f);
      },
      selectionsIcon: t.selectionsIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: t.selectionsIcon
      }) : p.selectionsIcon,
      locale: t["locale.notFoundContent"] ? {
        ...o,
        notFoundContent: /* @__PURE__ */ m.jsx(b, {
          slot: t["locale.notFoundContent"]
        })
      } : o,
      render: _ || ((f) => ({
        label: f.title || f.label,
        value: f.value || f.title || f.label
      })),
      filterOption: R,
      footer: C || (t.footer ? () => t.footer ? /* @__PURE__ */ m.jsx(b, {
        slot: t.footer
      }) : null : l),
      titles: c.length > 0 ? c.map((f, g) => /* @__PURE__ */ m.jsx(b, {
        slot: f
      }, g)) : p.titles,
      listStyle: E || e,
      selectAllLabels: a.length > 0 ? a.map((f, g) => /* @__PURE__ */ m.jsx(b, {
        slot: f
      }, g)) : p.selectAllLabels
    })]
  });
});
export {
  Ae as Transfer,
  Ae as default
};
