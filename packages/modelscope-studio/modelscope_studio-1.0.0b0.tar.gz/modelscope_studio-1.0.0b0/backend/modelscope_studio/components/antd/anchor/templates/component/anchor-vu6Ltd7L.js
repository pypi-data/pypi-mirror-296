import { g as V, w as m } from "./Index-CuTfnSw8.js";
const L = window.ms_globals.React, A = window.ms_globals.React.useMemo, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useEffect, C = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Anchor;
var N = {
  exports: {}
}, w = {};
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
function D(n, t, s) {
  var o, l = {}, e = null, r = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (o in t) te.call(t, o) && !re.hasOwnProperty(o) && (l[o] = t[o]);
  if (n && n.defaultProps) for (o in t = n.defaultProps, t) l[o] === void 0 && (l[o] = t[o]);
  return {
    $$typeof: $,
    type: n,
    key: e,
    ref: r,
    props: l,
    _owner: ne.current
  };
}
w.Fragment = ee;
w.jsx = D;
w.jsxs = D;
N.exports = w;
var g = N.exports;
const {
  SvelteComponent: oe,
  assign: x,
  binding_callbacks: I,
  check_outros: se,
  component_subscribe: k,
  compute_slots: le,
  create_slot: ce,
  detach: p,
  element: M,
  empty: ie,
  exclude_internal_props: O,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ue,
  group_outros: de,
  init: fe,
  insert: h,
  safe_not_equal: _e,
  set_custom_element_data: W,
  space: ge,
  transition_in: b,
  transition_out: E,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: pe,
  getContext: he,
  onDestroy: be,
  setContext: we
} = window.__gradio__svelte__internal;
function R(n) {
  let t, s;
  const o = (
    /*#slots*/
    n[7].default
  ), l = ce(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = M("svelte-slot"), l && l.c(), W(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      h(e, t, r), l && l.m(t, null), n[9](t), s = !0;
    },
    p(e, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && me(
        l,
        o,
        e,
        /*$$scope*/
        e[6],
        s ? ue(
          o,
          /*$$scope*/
          e[6],
          r,
          null
        ) : ae(
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
      E(l, e), s = !1;
    },
    d(e) {
      e && p(t), l && l.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, s, o, l, e = (
    /*$$slots*/
    n[4].default && R(n)
  );
  return {
    c() {
      t = M("react-portal-target"), s = ge(), e && e.c(), o = ie(), W(t, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      h(r, t, c), n[8](t), h(r, s, c), e && e.m(r, c), h(r, o, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, c), c & /*$$slots*/
      16 && b(e, 1)) : (e = R(r), e.c(), b(e, 1), e.m(o.parentNode, o)) : e && (de(), E(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(r) {
      l || (b(e), l = !0);
    },
    o(r) {
      E(e), l = !1;
    },
    d(r) {
      r && (p(t), p(s), p(o)), n[8](null), e && e.d(r);
    }
  };
}
function S(n) {
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
  const c = le(e);
  let {
    svelteInit: d
  } = t;
  const _ = m(S(t)), i = m();
  k(n, i, (u) => s(0, o = u));
  const a = m();
  k(n, a, (u) => s(1, l = u));
  const f = [], y = he("$$ms-gr-antd-react-wrapper"), {
    slotKey: U,
    slotIndex: q,
    subSlotIndex: G
  } = V() || {}, H = d({
    parent: y,
    props: _,
    target: i,
    slot: a,
    slotKey: U,
    slotIndex: q,
    subSlotIndex: G,
    onDestroy(u) {
      f.push(u);
    }
  });
  we("$$ms-gr-antd-react-wrapper", H), pe(() => {
    _.set(S(t));
  }), be(() => {
    f.forEach((u) => u());
  });
  function B(u) {
    I[u ? "unshift" : "push"](() => {
      o = u, i.set(o);
    });
  }
  function J(u) {
    I[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return n.$$set = (u) => {
    s(17, t = x(x({}, t), O(u))), "svelteInit" in u && s(5, d = u.svelteInit), "$$scope" in u && s(6, r = u.$$scope);
  }, t = O(t), [o, l, i, a, c, d, r, e, B, J];
}
class Ee extends oe {
  constructor(t) {
    super(), fe(this, t, ve, ye, _e, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function Ce(n) {
  function t(s) {
    const o = m(), l = new Ee({
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
          }, c = e.parent ?? v;
          return c.nodes = [...c.nodes, r], j({
            createPortal: C,
            node: v
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== o), j({
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
function xe(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function P(n) {
  return A(() => xe(n), [n]);
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !Ie.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function z(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: e,
      type: r,
      useCapture: c
    }) => {
      t.addEventListener(r, e, c);
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
const F = Y(({
  slot: n,
  clone: t,
  className: s,
  style: o
}, l) => {
  const e = K();
  return Q(() => {
    var _;
    if (!e.current || !n)
      return;
    let r = n;
    function c() {
      let i = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (i = r.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(l, i), s && i.classList.add(...s.split(" ")), o) {
        const a = ke(o);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        r = z(n), r.style.display = "contents", c(), (a = e.current) == null || a.appendChild(r);
      };
      i(), d = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(r) && ((f = e.current) == null || f.removeChild(r)), i();
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(r);
    return () => {
      var i, a;
      r.style.display = "", (i = e.current) != null && i.contains(r) && ((a = e.current) == null || a.removeChild(r)), d == null || d.disconnect();
    };
  }, [n, t, s, o, l]), L.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function T(n, t) {
  return n.filter(Boolean).map((s) => {
    if (typeof s != "object")
      return s;
    const o = {
      ...s.props
    };
    let l = o;
    Object.keys(s.slots).forEach((r) => {
      if (!s.slots[r] || !(s.slots[r] instanceof Element) && !s.slots[r].el)
        return;
      const c = r.split(".");
      c.forEach((f, y) => {
        l[f] || (l[f] = {}), y !== c.length - 1 && (l = o[f]);
      });
      const d = s.slots[r];
      let _, i, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), l[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ g.jsx(F, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ g.jsx(F, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = o;
    });
    const e = "children";
    return s[e] && (o[e] = T(s[e], t)), o;
  });
}
const Se = Ce(({
  getContainer: n,
  getCurrentAnchor: t,
  children: s,
  items: o,
  slotItems: l,
  ...e
}) => {
  const r = P(n), c = P(t);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [s, /* @__PURE__ */ g.jsx(X, {
      ...e,
      items: A(() => o || T(l), [o, l]),
      getContainer: r,
      getCurrentAnchor: c
    })]
  });
});
export {
  Se as Anchor,
  Se as default
};
