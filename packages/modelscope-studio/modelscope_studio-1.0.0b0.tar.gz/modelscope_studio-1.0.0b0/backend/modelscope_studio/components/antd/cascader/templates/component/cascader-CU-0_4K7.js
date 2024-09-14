import { g as oe, w as y } from "./Index-C1AjhCf6.js";
const U = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, L = window.ms_globals.ReactDOM.createPortal, le = window.ms_globals.antd.Cascader;
var G = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = U, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(e, n, l) {
  var r, s = {}, t = null, o = null;
  l !== void 0 && (t = "" + l), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) ae.call(n, r) && !de.hasOwnProperty(r) && (s[r] = n[r]);
  if (e && e.defaultProps) for (r in n = e.defaultProps, n) s[r] === void 0 && (s[r] = n[r]);
  return {
    $$typeof: ce,
    type: e,
    key: t,
    ref: o,
    props: s,
    _owner: ue.current
  };
}
R.Fragment = ie;
R.jsx = H;
R.jsxs = H;
G.exports = R;
var m = G.exports;
const {
  SvelteComponent: fe,
  assign: N,
  binding_callbacks: D,
  check_outros: _e,
  component_subscribe: T,
  compute_slots: me,
  create_slot: pe,
  detach: I,
  element: B,
  empty: ge,
  exclude_internal_props: M,
  get_all_dirty_from_scope: we,
  get_slot_changes: he,
  group_outros: be,
  init: xe,
  insert: v,
  safe_not_equal: ye,
  set_custom_element_data: J,
  space: Ie,
  transition_in: C,
  transition_out: O,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ce,
  getContext: Re,
  onDestroy: Ee,
  setContext: Se
} = window.__gradio__svelte__internal;
function W(e) {
  let n, l;
  const r = (
    /*#slots*/
    e[7].default
  ), s = pe(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = B("svelte-slot"), s && s.c(), J(n, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      v(t, n, o), s && s.m(n, null), e[9](n), l = !0;
    },
    p(t, o) {
      s && s.p && (!l || o & /*$$scope*/
      64) && ve(
        s,
        r,
        t,
        /*$$scope*/
        t[6],
        l ? he(
          r,
          /*$$scope*/
          t[6],
          o,
          null
        ) : we(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (C(s, t), l = !0);
    },
    o(t) {
      O(s, t), l = !1;
    },
    d(t) {
      t && I(n), s && s.d(t), e[9](null);
    }
  };
}
function je(e) {
  let n, l, r, s, t = (
    /*$$slots*/
    e[4].default && W(e)
  );
  return {
    c() {
      n = B("react-portal-target"), l = Ie(), t && t.c(), r = ge(), J(n, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      v(o, n, c), e[8](n), v(o, l, c), t && t.m(o, c), v(o, r, c), s = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, c), c & /*$$slots*/
      16 && C(t, 1)) : (t = W(o), t.c(), C(t, 1), t.m(r.parentNode, r)) : t && (be(), O(t, 1, 1, () => {
        t = null;
      }), _e());
    },
    i(o) {
      s || (C(t), s = !0);
    },
    o(o) {
      O(t), s = !1;
    },
    d(o) {
      o && (I(n), I(l), I(r)), e[8](null), t && t.d(o);
    }
  };
}
function z(e) {
  const {
    svelteInit: n,
    ...l
  } = e;
  return l;
}
function Fe(e, n, l) {
  let r, s, {
    $$slots: t = {},
    $$scope: o
  } = n;
  const c = me(t);
  let {
    svelteInit: d
  } = n;
  const _ = y(z(n)), i = y();
  T(e, i, (u) => l(0, r = u));
  const a = y();
  T(e, a, (u) => l(1, s = u));
  const f = [], b = Re("$$ms-gr-antd-react-wrapper"), {
    slotKey: x,
    slotIndex: g,
    subSlotIndex: E
  } = oe() || {}, S = d({
    parent: b,
    props: _,
    target: i,
    slot: a,
    slotKey: x,
    slotIndex: g,
    subSlotIndex: E,
    onDestroy(u) {
      f.push(u);
    }
  });
  Se("$$ms-gr-antd-react-wrapper", S), Ce(() => {
    _.set(z(n));
  }), Ee(() => {
    f.forEach((u) => u());
  });
  function j(u) {
    D[u ? "unshift" : "push"](() => {
      r = u, i.set(r);
    });
  }
  function F(u) {
    D[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  return e.$$set = (u) => {
    l(17, n = N(N({}, n), M(u))), "svelteInit" in u && l(5, d = u.svelteInit), "$$scope" in u && l(6, o = u.$$scope);
  }, n = M(n), [r, s, i, a, c, d, o, t, j, F];
}
class ke extends fe {
  constructor(n) {
    super(), xe(this, n, Fe, je, ye, {
      svelteInit: 5
    });
  }
}
const A = window.ms_globals.rerender, k = window.ms_globals.tree;
function Oe(e) {
  function n(l) {
    const r = y(), s = new ke({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? k;
          return c.nodes = [...c.nodes, o], A({
            createPortal: L,
            node: k
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== r), A({
              createPortal: L,
              node: k
            });
          }), o;
        },
        ...l.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(n);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Le(e) {
  return e ? Object.keys(e).reduce((n, l) => {
    const r = e[l];
    return typeof r == "number" && !Pe.includes(l) ? n[l] = r + "px" : n[l] = r, n;
  }, {}) : {};
}
function Y(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: t,
      type: o,
      useCapture: c
    }) => {
      n.addEventListener(o, t, c);
    });
  });
  const l = Array.from(e.children);
  for (let r = 0; r < l.length; r++) {
    const s = l[r], t = Y(s);
    n.replaceChild(t, n.children[r]);
  }
  return n;
}
function Ne(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const w = te(({
  slot: e,
  clone: n,
  className: l,
  style: r
}, s) => {
  const t = ne();
  return re(() => {
    var _;
    if (!t.current || !e)
      return;
    let o = e;
    function c() {
      let i = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (i = o.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ne(s, i), l && i.classList.add(...l.split(" ")), r) {
        const a = Le(r);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let i = function() {
        var a;
        o = Y(e), o.style.display = "contents", c(), (a = t.current) == null || a.appendChild(o);
      };
      i(), d = new window.MutationObserver(() => {
        var a, f;
        (a = t.current) != null && a.contains(o) && ((f = t.current) == null || f.removeChild(o)), i();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", c(), (_ = t.current) == null || _.appendChild(o);
    return () => {
      var i, a;
      o.style.display = "", (i = t.current) != null && i.contains(o) && ((a = t.current) == null || a.removeChild(o)), d == null || d.disconnect();
    };
  }, [e, n, l, r, s]), U.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function De(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function p(e) {
  return q(() => De(e), [e]);
}
function K(e, n) {
  return e.filter(Boolean).map((l) => {
    if (typeof l != "object")
      return l;
    const r = {
      ...l.props
    };
    let s = r;
    Object.keys(l.slots).forEach((o) => {
      if (!l.slots[o] || !(l.slots[o] instanceof Element) && !l.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((f, b) => {
        s[f] || (s[f] = {}), b !== c.length - 1 && (s = r[f]);
      });
      const d = l.slots[o];
      let _, i, a = !1;
      d instanceof Element ? _ = d : (_ = d.el, i = d.callback, a = d.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(w, {
        slot: _,
        clone: a || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ m.jsx(w, {
        slot: _,
        clone: a || (n == null ? void 0 : n.clone)
      }) : s[c[c.length - 1]], s = r;
    });
    const t = "children";
    return l[t] && (r[t] = K(l[t], n)), r;
  });
}
function Te(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const We = Oe(({
  slots: e,
  children: n,
  onValueChange: l,
  onChange: r,
  displayRender: s,
  elRef: t,
  getPopupContainer: o,
  tagRender: c,
  maxTagPlaceholder: d,
  dropdownRender: _,
  optionRender: i,
  onLoadData: a,
  showSearch: f,
  optionItems: b,
  options: x,
  ...g
}) => {
  const E = p(o), S = p(s), j = p(c), F = p(i), u = p(_), Q = p(d), V = typeof f == "object", h = Te(f), X = p(h.filter), Z = p(h.render), $ = p(h.sort);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ m.jsx(le, {
      ...g,
      ref: t,
      options: q(() => x || K(b), [x, b]),
      showSearch: V ? {
        ...h,
        filter: X || h.filter,
        render: Z || h.render,
        sort: $ || h.sort
      } : f,
      loadData: a,
      optionRender: F,
      dropdownRender: u,
      getPopupContainer: E,
      displayRender: S,
      tagRender: j,
      onChange: (P, ...ee) => {
        r == null || r(P, ...ee), l(P);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(w, {
        slot: e.suffixIcon
      }) : g.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ m.jsx(w, {
        slot: e.expandIcon
      }) : g.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ m.jsx(w, {
        slot: e.removeIcon
      }) : g.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ m.jsx(w, {
        slot: e.notFoundContent
      }) : g.notFoundContent,
      maxTagPlaceholder: Q || (e.maxTagPlaceholder ? /* @__PURE__ */ m.jsx(w, {
        slot: e.maxTagPlaceholder
      }) : d),
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(w, {
          slot: e["allowClear.clearIcon"]
        })
      } : g.allowClear
    })]
  });
});
export {
  We as Cascader,
  We as default
};
