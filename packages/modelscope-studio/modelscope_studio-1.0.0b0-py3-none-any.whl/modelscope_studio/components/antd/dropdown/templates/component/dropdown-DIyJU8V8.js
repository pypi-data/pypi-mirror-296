import { g as V, w as p } from "./Index-DCHWby1d.js";
const L = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useEffect, D = window.ms_globals.React.useMemo, E = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Dropdown;
var N = {
  exports: {}
}, v = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Z = L, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function M(r, t, l) {
  var o, s = {}, e = null, n = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (n = t.ref);
  for (o in t) te.call(t, o) && !re.hasOwnProperty(o) && (s[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) s[o] === void 0 && (s[o] = t[o]);
  return {
    $$typeof: $,
    type: r,
    key: e,
    ref: n,
    props: s,
    _owner: ne.current
  };
}
v.Fragment = ee;
v.jsx = M;
v.jsxs = M;
N.exports = v;
var m = N.exports;
const {
  SvelteComponent: oe,
  assign: C,
  binding_callbacks: R,
  check_outros: le,
  component_subscribe: k,
  compute_slots: se,
  create_slot: ce,
  detach: g,
  element: W,
  empty: ie,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ue,
  group_outros: de,
  init: fe,
  insert: w,
  safe_not_equal: _e,
  set_custom_element_data: z,
  space: me,
  transition_in: h,
  transition_out: I,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: we,
  onDestroy: he,
  setContext: be
} = window.__gradio__svelte__internal;
function S(r) {
  let t, l;
  const o = (
    /*#slots*/
    r[7].default
  ), s = ce(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = W("svelte-slot"), s && s.c(), z(t, "class", "svelte-1rt0kpf");
    },
    m(e, n) {
      w(e, t, n), s && s.m(t, null), r[9](t), l = !0;
    },
    p(e, n) {
      s && s.p && (!l || n & /*$$scope*/
      64) && pe(
        s,
        o,
        e,
        /*$$scope*/
        e[6],
        l ? ue(
          o,
          /*$$scope*/
          e[6],
          n,
          null
        ) : ae(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (h(s, e), l = !0);
    },
    o(e) {
      I(s, e), l = !1;
    },
    d(e) {
      e && g(t), s && s.d(e), r[9](null);
    }
  };
}
function ve(r) {
  let t, l, o, s, e = (
    /*$$slots*/
    r[4].default && S(r)
  );
  return {
    c() {
      t = W("react-portal-target"), l = me(), e && e.c(), o = ie(), z(t, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      w(n, t, c), r[8](t), w(n, l, c), e && e.m(n, c), w(n, o, c), s = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? e ? (e.p(n, c), c & /*$$slots*/
      16 && h(e, 1)) : (e = S(n), e.c(), h(e, 1), e.m(o.parentNode, o)) : e && (de(), I(e, 1, 1, () => {
        e = null;
      }), le());
    },
    i(n) {
      s || (h(e), s = !0);
    },
    o(n) {
      I(e), s = !1;
    },
    d(n) {
      n && (g(t), g(l), g(o)), r[8](null), e && e.d(n);
    }
  };
}
function j(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function ye(r, t, l) {
  let o, s, {
    $$slots: e = {},
    $$scope: n
  } = t;
  const c = se(e);
  let {
    svelteInit: u
  } = t;
  const _ = p(j(t)), i = p();
  k(r, i, (d) => l(0, o = d));
  const a = p();
  k(r, a, (d) => l(1, s = d));
  const f = [], y = we("$$ms-gr-antd-react-wrapper"), {
    slotKey: U,
    slotIndex: q,
    subSlotIndex: G
  } = V() || {}, H = u({
    parent: y,
    props: _,
    target: i,
    slot: a,
    slotKey: U,
    slotIndex: q,
    subSlotIndex: G,
    onDestroy(d) {
      f.push(d);
    }
  });
  be("$$ms-gr-antd-react-wrapper", H), ge(() => {
    _.set(j(t));
  }), he(() => {
    f.forEach((d) => d());
  });
  function B(d) {
    R[d ? "unshift" : "push"](() => {
      o = d, i.set(o);
    });
  }
  function J(d) {
    R[d ? "unshift" : "push"](() => {
      s = d, a.set(s);
    });
  }
  return r.$$set = (d) => {
    l(17, t = C(C({}, t), O(d))), "svelteInit" in d && l(5, u = d.svelteInit), "$$scope" in d && l(6, n = d.$$scope);
  }, t = O(t), [o, s, i, a, c, u, n, e, B, J];
}
class xe extends oe {
  constructor(t) {
    super(), fe(this, t, ye, ve, _e, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, x = window.ms_globals.tree;
function Ie(r) {
  function t(l) {
    const o = p(), s = new xe({
      ...l,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const n = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, n], P({
            createPortal: E,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), P({
              createPortal: E,
              node: x
            });
          }), n;
        },
        ...l.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(t);
    });
  });
}
const Ee = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ce(r) {
  return r ? Object.keys(r).reduce((t, l) => {
    const o = r[l];
    return typeof o == "number" && !Ee.includes(l) ? t[l] = o + "px" : t[l] = o, t;
  }, {}) : {};
}
function A(r) {
  const t = r.cloneNode(!0);
  Object.keys(r.getEventListeners()).forEach((o) => {
    r.getEventListeners(o).forEach(({
      listener: e,
      type: n,
      useCapture: c
    }) => {
      t.addEventListener(n, e, c);
    });
  });
  const l = Array.from(r.children);
  for (let o = 0; o < l.length; o++) {
    const s = l[o], e = A(s);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Re(r, t) {
  r && (typeof r == "function" ? r(t) : r.current = t);
}
const b = Y(({
  slot: r,
  clone: t,
  className: l,
  style: o
}, s) => {
  const e = K();
  return Q(() => {
    var _;
    if (!e.current || !r)
      return;
    let n = r;
    function c() {
      let i = n;
      if (n.tagName.toLowerCase() === "svelte-slot" && n.children.length === 1 && n.children[0] && (i = n.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Re(s, i), l && i.classList.add(...l.split(" ")), o) {
        const a = Ce(o);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        n = A(r), n.style.display = "contents", c(), (a = e.current) == null || a.appendChild(n);
      };
      i(), u = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(n) && ((f = e.current) == null || f.removeChild(n)), i();
      }), u.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      n.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(n);
    return () => {
      var i, a;
      n.style.display = "", (i = e.current) != null && i.contains(n) && ((a = e.current) == null || a.removeChild(n)), u == null || u.disconnect();
    };
  }, [r, t, l, o, s]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function ke(r) {
  try {
    return typeof r == "string" ? new Function(`return (...args) => (${r})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function F(r) {
  return D(() => ke(r), [r]);
}
function T(r, t) {
  return r.filter(Boolean).map((l) => {
    if (typeof l != "object")
      return l;
    const o = {
      ...l.props
    };
    let s = o;
    Object.keys(l.slots).forEach((n) => {
      if (!l.slots[n] || !(l.slots[n] instanceof Element) && !l.slots[n].el)
        return;
      const c = n.split(".");
      c.forEach((f, y) => {
        s[f] || (s[f] = {}), y !== c.length - 1 && (s = o[f]);
      });
      const u = l.slots[n];
      let _, i, a = !1;
      u instanceof Element ? _ = u : (_ = u.el, i = u.callback, a = u.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(b, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(b, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = o;
    });
    const e = "children";
    return l[e] && (o[e] = T(l[e], t)), o;
  });
}
const Se = Ie(({
  getPopupContainer: r,
  innerStyle: t,
  children: l,
  slots: o,
  menuItems: s,
  dropdownRender: e,
  ...n
}) => {
  var _, i, a;
  const c = F(r), u = F(e);
  return /* @__PURE__ */ m.jsx(m.Fragment, {
    children: /* @__PURE__ */ m.jsx(X, {
      ...n,
      menu: {
        ...n.menu,
        items: D(() => {
          var f;
          return ((f = n.menu) == null ? void 0 : f.items) || T(s);
        }, [s, (_ = n.menu) == null ? void 0 : _.items]),
        expandIcon: o["menu.expandIcon"] ? /* @__PURE__ */ m.jsx(b, {
          slot: o["menu.expandIcon"],
          clone: !0
        }) : (i = n.menu) == null ? void 0 : i.expandIcon,
        overflowedIndicator: o["menu.overflowedIndicator"] ? /* @__PURE__ */ m.jsx(b, {
          slot: o["menu.overflowedIndicator"]
        }) : (a = n.menu) == null ? void 0 : a.overflowedIndicator
      },
      getPopupContainer: c,
      dropdownRender: u,
      children: /* @__PURE__ */ m.jsx("div", {
        className: "ms-gr-antd-dropdown-content",
        style: {
          display: "inline-block",
          ...t
        },
        children: l
      })
    })
  });
});
export {
  Se as Dropdown,
  Se as default
};
