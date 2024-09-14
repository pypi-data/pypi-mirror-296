import { g as V, w as b } from "./Index-BY3P03Re.js";
const N = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useEffect, D = window.ms_globals.React.useMemo, S = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Mentions;
var W = {
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
var Z = N, $ = Symbol.for("react.element"), ee = Symbol.for("react.fragment"), te = Object.prototype.hasOwnProperty, ne = Z.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, re = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, s) {
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
v.Fragment = ee;
v.jsx = z;
v.jsxs = z;
W.exports = v;
var p = W.exports;
const {
  SvelteComponent: oe,
  assign: k,
  binding_callbacks: R,
  check_outros: se,
  component_subscribe: j,
  compute_slots: le,
  create_slot: ce,
  detach: h,
  element: A,
  empty: ie,
  exclude_internal_props: F,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ue,
  group_outros: de,
  init: fe,
  insert: w,
  safe_not_equal: _e,
  set_custom_element_data: T,
  space: pe,
  transition_in: y,
  transition_out: I,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: be,
  onDestroy: he,
  setContext: we
} = window.__gradio__svelte__internal;
function P(n) {
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
      t = A("svelte-slot"), l && l.c(), T(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      w(e, t, r), l && l.m(t, null), n[9](t), s = !0;
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
      s || (y(l, e), s = !0);
    },
    o(e) {
      I(l, e), s = !1;
    },
    d(e) {
      e && h(t), l && l.d(e), n[9](null);
    }
  };
}
function ye(n) {
  let t, s, o, l, e = (
    /*$$slots*/
    n[4].default && P(n)
  );
  return {
    c() {
      t = A("react-portal-target"), s = pe(), e && e.c(), o = ie(), T(t, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      w(r, t, c), n[8](t), w(r, s, c), e && e.m(r, c), w(r, o, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, c), c & /*$$slots*/
      16 && y(e, 1)) : (e = P(r), e.c(), y(e, 1), e.m(o.parentNode, o)) : e && (de(), I(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(r) {
      l || (y(e), l = !0);
    },
    o(r) {
      I(e), l = !1;
    },
    d(r) {
      r && (h(t), h(s), h(o)), n[8](null), e && e.d(r);
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
  const c = le(e);
  let {
    svelteInit: u
  } = t;
  const _ = b(L(t)), i = b();
  j(n, i, (d) => s(0, o = d));
  const a = b();
  j(n, a, (d) => s(1, l = d));
  const f = [], m = be("$$ms-gr-antd-react-wrapper"), {
    slotKey: g,
    slotIndex: E,
    subSlotIndex: G
  } = V() || {}, H = u({
    parent: m,
    props: _,
    target: i,
    slot: a,
    slotKey: g,
    slotIndex: E,
    subSlotIndex: G,
    onDestroy(d) {
      f.push(d);
    }
  });
  we("$$ms-gr-antd-react-wrapper", H), ge(() => {
    _.set(L(t));
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
      l = d, a.set(l);
    });
  }
  return n.$$set = (d) => {
    s(17, t = k(k({}, t), F(d))), "svelteInit" in d && s(5, u = d.svelteInit), "$$scope" in d && s(6, r = d.$$scope);
  }, t = F(t), [o, l, i, a, c, u, r, e, B, J];
}
class Ee extends oe {
  constructor(t) {
    super(), fe(this, t, ve, ye, _e, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, x = window.ms_globals.tree;
function xe(n) {
  function t(s) {
    const o = b(), l = new Ee({
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
          }, c = e.parent ?? x;
          return c.nodes = [...c.nodes, r], M({
            createPortal: S,
            node: x
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), M({
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
const Ce = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const o = n[s];
    return typeof o == "number" && !Ce.includes(s) ? t[s] = o + "px" : t[s] = o, t;
  }, {}) : {};
}
function U(n) {
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
    const l = s[o], e = U(l);
    t.replaceChild(e, t.children[o]);
  }
  return t;
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const O = Y(({
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
        const a = Ie(o);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        r = U(n), r.style.display = "contents", c(), (a = e.current) == null || a.appendChild(r);
      };
      i(), u = new window.MutationObserver(() => {
        var a, f;
        (a = e.current) != null && a.contains(r) && ((f = e.current) == null || f.removeChild(r)), i();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", c(), (_ = e.current) == null || _.appendChild(r);
    return () => {
      var i, a;
      r.style.display = "", (i = e.current) != null && i.contains(r) && ((a = e.current) == null || a.removeChild(r)), u == null || u.disconnect();
    };
  }, [n, t, s, o, l]), N.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function Se(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function C(n) {
  return D(() => Se(n), [n]);
}
function q(n, t) {
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
      c.forEach((f, m) => {
        l[f] || (l[f] = {}), m !== c.length - 1 && (l = o[f]);
      });
      const u = s.slots[r];
      let _, i, a = !1;
      u instanceof Element ? _ = u : (_ = u.el, i = u.callback, a = u.clone || !1), l[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ p.jsx(O, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ p.jsx(O, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = o;
    });
    const e = "children";
    return s[e] && (o[e] = q(s[e], t)), o;
  });
}
const Re = xe(({
  slots: n,
  children: t,
  onValueChange: s,
  filterOption: o,
  onChange: l,
  options: e,
  validateSearch: r,
  optionItems: c,
  getPopupContainer: u,
  elRef: _,
  ...i
}) => {
  const a = C(u), f = C(o), m = C(r);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx(X, {
      ...i,
      ref: _,
      options: D(() => e || q(c), [c, e]),
      onChange: (g, ...E) => {
        l == null || l(g, ...E), s(g);
      },
      validateSearch: m,
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ p.jsx(O, {
        slot: n.notFoundContent
      }) : i.notFoundContent,
      filterOption: f || o,
      getPopupContainer: a
    })]
  });
});
export {
  Re as Mentions,
  Re as default
};
