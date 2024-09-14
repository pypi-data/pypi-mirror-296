import { g as Z, w as b, d as $, a as g } from "./Index-DKB0yA1x.js";
const E = window.ms_globals.React, x = window.ms_globals.React.useMemo, K = window.ms_globals.React.useState, A = window.ms_globals.React.useEffect, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, C = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Dropdown;
var T = {
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
var te = E, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function B(n, t, r) {
  var s, l = {}, e = null, o = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) oe.call(t, s) && !le.hasOwnProperty(s) && (l[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: o,
    props: l,
    _owner: se.current
  };
}
y.Fragment = re;
y.jsx = B;
y.jsxs = B;
T.exports = y;
var _ = T.exports;
const {
  SvelteComponent: ce,
  assign: k,
  binding_callbacks: O,
  check_outros: ue,
  component_subscribe: j,
  compute_slots: ie,
  create_slot: ae,
  detach: h,
  element: M,
  empty: de,
  exclude_internal_props: P,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert: v,
  safe_not_equal: ge,
  set_custom_element_data: W,
  space: we,
  transition_in: I,
  transition_out: S,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ve,
  onDestroy: Ie,
  setContext: xe
} = window.__gradio__svelte__internal;
function L(n) {
  let t, r;
  const s = (
    /*#slots*/
    n[7].default
  ), l = ae(
    s,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = M("svelte-slot"), l && l.c(), W(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      v(e, t, o), l && l.m(t, null), n[9](t), r = !0;
    },
    p(e, o) {
      l && l.p && (!r || o & /*$$scope*/
      64) && be(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        r ? pe(
          s,
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
      r || (I(l, e), r = !0);
    },
    o(e) {
      S(l, e), r = !1;
    },
    d(e) {
      e && h(t), l && l.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, r, s, l, e = (
    /*$$slots*/
    n[4].default && L(n)
  );
  return {
    c() {
      t = M("react-portal-target"), r = we(), e && e.c(), s = de(), W(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      v(o, t, c), n[8](t), v(o, r, c), e && e.m(o, c), v(o, s, c), l = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && I(e, 1)) : (e = L(o), e.c(), I(e, 1), e.m(s.parentNode, s)) : e && (_e(), S(e, 1, 1, () => {
        e = null;
      }), ue());
    },
    i(o) {
      l || (I(e), l = !0);
    },
    o(o) {
      S(e), l = !1;
    },
    d(o) {
      o && (h(t), h(r), h(s)), n[8](null), e && e.d(o);
    }
  };
}
function D(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Re(n, t, r) {
  let s, l, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = ie(e);
  let {
    svelteInit: i
  } = t;
  const p = b(D(t)), u = b();
  j(n, u, (f) => r(0, s = f));
  const a = b();
  j(n, a, (f) => r(1, l = f));
  const d = [], m = ve("$$ms-gr-antd-react-wrapper"), {
    slotKey: G,
    slotIndex: H,
    subSlotIndex: q
  } = Z() || {}, J = i({
    parent: m,
    props: p,
    target: u,
    slot: a,
    slotKey: G,
    slotIndex: H,
    subSlotIndex: q,
    onDestroy(f) {
      d.push(f);
    }
  });
  xe("$$ms-gr-antd-react-wrapper", J), he(() => {
    p.set(D(t));
  }), Ie(() => {
    d.forEach((f) => f());
  });
  function V(f) {
    O[f ? "unshift" : "push"](() => {
      s = f, u.set(s);
    });
  }
  function Y(f) {
    O[f ? "unshift" : "push"](() => {
      l = f, a.set(l);
    });
  }
  return n.$$set = (f) => {
    r(17, t = k(k({}, t), P(f))), "svelteInit" in f && r(5, i = f.svelteInit), "$$scope" in f && r(6, o = f.$$scope);
  }, t = P(t), [s, l, u, a, c, i, o, e, V, Y];
}
class Se extends ce {
  constructor(t) {
    super(), me(this, t, Re, ye, ge, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, R = window.ms_globals.tree;
function Ee(n) {
  function t(r) {
    const s = b(), l = new Se({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, c = e.parent ?? R;
          return c.nodes = [...c.nodes, o], F({
            createPortal: C,
            node: R
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== s), F({
              createPortal: C,
              node: R
            });
          }), o;
        },
        ...r.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function Ce(n) {
  const [t, r] = K(() => g(n));
  return A(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function ke(n) {
  const t = x(() => $(n, (r) => r), [n]);
  return Ce(t);
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const s = n[r];
    return typeof s == "number" && !Oe.includes(r) ? t[r] = s + "px" : t[r] = s, t;
  }, {}) : {};
}
function z(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: e,
      type: o,
      useCapture: c
    }) => {
      t.addEventListener(o, e, c);
    });
  });
  const r = Array.from(n.children);
  for (let s = 0; s < r.length; s++) {
    const l = r[s], e = z(l);
    t.replaceChild(e, t.children[s]);
  }
  return t;
}
function Pe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const w = Q(({
  slot: n,
  clone: t,
  className: r,
  style: s
}, l) => {
  const e = X();
  return A(() => {
    var p;
    if (!e.current || !n)
      return;
    let o = n;
    function c() {
      let u = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (u = o.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Pe(l, u), r && u.classList.add(...r.split(" ")), s) {
        const a = je(s);
        Object.keys(a).forEach((d) => {
          u.style[d] = a[d];
        });
      }
    }
    let i = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var a;
        o = z(n), o.style.display = "contents", c(), (a = e.current) == null || a.appendChild(o);
      };
      u(), i = new window.MutationObserver(() => {
        var a, d;
        (a = e.current) != null && a.contains(o) && ((d = e.current) == null || d.removeChild(o)), u();
      }), i.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", c(), (p = e.current) == null || p.appendChild(o);
    return () => {
      var u, a;
      o.style.display = "", (u = e.current) != null && u.contains(o) && ((a = e.current) == null || a.removeChild(o)), i == null || i.disconnect();
    };
  }, [n, t, r, s, l]), E.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Le(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function N(n) {
  return x(() => Le(n), [n]);
}
function De(n, t) {
  const r = x(() => E.Children.toArray(n).filter((e) => e.props.node && t === e.props.nodeSlotKey).sort((e, o) => {
    if (e.props.node.slotIndex && o.props.node.slotIndex) {
      const c = g(e.props.node.slotIndex) || 0, i = g(o.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && o.props.node.subSlotIndex ? (g(e.props.node.subSlotIndex) || 0) - (g(o.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return ke(r);
}
function U(n, t) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const s = {
      ...r.props
    };
    let l = s;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((d, m) => {
        l[d] || (l[d] = {}), m !== c.length - 1 && (l = s[d]);
      });
      const i = r.slots[o];
      let p, u, a = !1;
      i instanceof Element ? p = i : (p = i.el, u = i.callback, a = i.clone || !1), l[c[c.length - 1]] = p ? u ? (...d) => (u(c[c.length - 1], d), /* @__PURE__ */ _.jsx(w, {
        slot: p,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ _.jsx(w, {
        slot: p,
        clone: a || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = s;
    });
    const e = "children";
    return r[e] && (s[e] = U(r[e], t)), s;
  });
}
const Ne = Ee(({
  getPopupContainer: n,
  slots: t,
  menuItems: r,
  children: s,
  dropdownRender: l,
  ...e
}) => {
  var p, u, a;
  const o = N(n), c = N(l), i = De(s, "buttonsRender");
  return /* @__PURE__ */ _.jsx(ee.Button, {
    ...e,
    buttonsRender: i.length ? () => i.map((d, m) => /* @__PURE__ */ _.jsx(w, {
      slot: d
    }, m)) : e.buttonsRender,
    menu: {
      ...e.menu,
      items: x(() => {
        var d;
        return ((d = e.menu) == null ? void 0 : d.items) || U(r);
      }, [r, (p = e.menu) == null ? void 0 : p.items]),
      expandIcon: t["menu.expandIcon"] ? /* @__PURE__ */ _.jsx(w, {
        slot: t["menu.expandIcon"],
        clone: !0
      }) : (u = e.menu) == null ? void 0 : u.expandIcon,
      overflowedIndicator: t["menu.overflowedIndicator"] ? /* @__PURE__ */ _.jsx(w, {
        slot: t["menu.overflowedIndicator"]
      }) : (a = e.menu) == null ? void 0 : a.overflowedIndicator
    },
    getPopupContainer: o,
    dropdownRender: c
  });
});
export {
  Ne as DropdownButton,
  Ne as default
};
