import { g as V, w as h } from "./Index-CbxZil7e.js";
const D = window.ms_globals.React, W = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useEffect, k = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.internalContext.AutoCompleteContext, Z = window.ms_globals.antd.AutoComplete;
var M = {
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
var $ = D, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), ne = Object.prototype.hasOwnProperty, re = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, e, r) {
  var o, s = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (o in e) ne.call(e, o) && !le.hasOwnProperty(o) && (s[o] = e[o]);
  if (n && n.defaultProps) for (o in e = n.defaultProps, e) s[o] === void 0 && (s[o] = e[o]);
  return {
    $$typeof: ee,
    type: n,
    key: t,
    ref: l,
    props: s,
    _owner: re.current
  };
}
v.Fragment = te;
v.jsx = z;
v.jsxs = z;
M.exports = v;
var m = M.exports;
const {
  SvelteComponent: oe,
  assign: j,
  binding_callbacks: S,
  check_outros: se,
  component_subscribe: P,
  compute_slots: ce,
  create_slot: ie,
  detach: b,
  element: T,
  empty: ae,
  exclude_internal_props: F,
  get_all_dirty_from_scope: ue,
  get_slot_changes: de,
  group_outros: fe,
  init: _e,
  insert: y,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: pe,
  transition_in: C,
  transition_out: R,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: he,
  onDestroy: be,
  setContext: ye
} = window.__gradio__svelte__internal;
function A(n) {
  let e, r;
  const o = (
    /*#slots*/
    n[7].default
  ), s = ie(
    o,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = T("svelte-slot"), s && s.c(), U(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      y(t, e, l), s && s.m(e, null), n[9](e), r = !0;
    },
    p(t, l) {
      s && s.p && (!r || l & /*$$scope*/
      64) && ge(
        s,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? de(
          o,
          /*$$scope*/
          t[6],
          l,
          null
        ) : ue(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (C(s, t), r = !0);
    },
    o(t) {
      R(s, t), r = !1;
    },
    d(t) {
      t && b(e), s && s.d(t), n[9](null);
    }
  };
}
function Ce(n) {
  let e, r, o, s, t = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      e = T("react-portal-target"), r = pe(), t && t.c(), o = ae(), U(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      y(l, e, c), n[8](e), y(l, r, c), t && t.m(l, c), y(l, o, c), s = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && C(t, 1)) : (t = A(l), t.c(), C(t, 1), t.m(o.parentNode, o)) : t && (fe(), R(t, 1, 1, () => {
        t = null;
      }), se());
    },
    i(l) {
      s || (C(t), s = !0);
    },
    o(l) {
      R(t), s = !1;
    },
    d(l) {
      l && (b(e), b(r), b(o)), n[8](null), t && t.d(l);
    }
  };
}
function L(n) {
  const {
    svelteInit: e,
    ...r
  } = n;
  return r;
}
function ve(n, e, r) {
  let o, s, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = ce(t);
  let {
    svelteInit: u
  } = e;
  const _ = h(L(e)), i = h();
  P(n, i, (d) => r(0, o = d));
  const a = h();
  P(n, a, (d) => r(1, s = d));
  const f = [], p = he("$$ms-gr-antd-react-wrapper"), {
    slotKey: w,
    slotIndex: x,
    subSlotIndex: H
  } = V() || {}, B = u({
    parent: p,
    props: _,
    target: i,
    slot: a,
    slotKey: w,
    slotIndex: x,
    subSlotIndex: H,
    onDestroy(d) {
      f.push(d);
    }
  });
  ye("$$ms-gr-antd-react-wrapper", B), we(() => {
    _.set(L(e));
  }), be(() => {
    f.forEach((d) => d());
  });
  function J(d) {
    S[d ? "unshift" : "push"](() => {
      o = d, i.set(o);
    });
  }
  function Y(d) {
    S[d ? "unshift" : "push"](() => {
      s = d, a.set(s);
    });
  }
  return n.$$set = (d) => {
    r(17, e = j(j({}, e), F(d))), "svelteInit" in d && r(5, u = d.svelteInit), "$$scope" in d && r(6, l = d.$$scope);
  }, e = F(e), [o, s, i, a, c, u, l, t, J, Y];
}
class xe extends oe {
  constructor(e) {
    super(), _e(this, e, ve, Ce, me, {
      svelteInit: 5
    });
  }
}
const N = window.ms_globals.rerender, E = window.ms_globals.tree;
function Ee(n) {
  function e(r) {
    const o = h(), s = new xe({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? E;
          return c.nodes = [...c.nodes, l], N({
            createPortal: O,
            node: E
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), N({
              createPortal: O,
              node: E
            });
          }), l;
        },
        ...r.props
      }
    });
    return o.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(e);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Re(n) {
  return n ? Object.keys(n).reduce((e, r) => {
    const o = n[r];
    return typeof o == "number" && !Ie.includes(r) ? e[r] = o + "px" : e[r] = o, e;
  }, {}) : {};
}
function q(n) {
  const e = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: t,
      type: l,
      useCapture: c
    }) => {
      e.addEventListener(l, t, c);
    });
  });
  const r = Array.from(n.children);
  for (let o = 0; o < r.length; o++) {
    const s = r[o], t = q(s);
    e.replaceChild(t, e.children[o]);
  }
  return e;
}
function ke(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const g = W(({
  slot: n,
  clone: e,
  className: r,
  style: o
}, s) => {
  const t = K();
  return Q(() => {
    var _;
    if (!t.current || !n)
      return;
    let l = n;
    function c() {
      let i = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (i = l.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), ke(s, i), r && i.classList.add(...r.split(" ")), o) {
        const a = Re(o);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var a;
        l = q(n), l.style.display = "contents", c(), (a = t.current) == null || a.appendChild(l);
      };
      i(), u = new window.MutationObserver(() => {
        var a, f;
        (a = t.current) != null && a.contains(l) && ((f = t.current) == null || f.removeChild(l)), i();
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", c(), (_ = t.current) == null || _.appendChild(l);
    return () => {
      var i, a;
      l.style.display = "", (i = t.current) != null && i.contains(l) && ((a = t.current) == null || a.removeChild(l)), u == null || u.disconnect();
    };
  }, [n, e, r, o, s]), D.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Oe(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function I(n) {
  return k(() => Oe(n), [n]);
}
function G(n, e) {
  return n.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const o = {
      ...r.props
    };
    let s = o;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const c = l.split(".");
      c.forEach((f, p) => {
        s[f] || (s[f] = {}), p !== c.length - 1 && (s = o[f]);
      });
      const u = r.slots[l];
      let _, i, a = !1;
      u instanceof Element ? _ = u : (_ = u.el, i = u.callback, a = u.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(g, {
        slot: _,
        clone: a || (e == null ? void 0 : e.clone)
      })) : /* @__PURE__ */ m.jsx(g, {
        slot: _,
        clone: a || (e == null ? void 0 : e.clone)
      }) : s[c[c.length - 1]], s = o;
    });
    const t = (e == null ? void 0 : e.children) || "children";
    return r[t] && (o[t] = G(r[t], e)), o;
  });
}
const je = W(({
  children: n,
  ...e
}, r) => /* @__PURE__ */ m.jsx(X.Provider, {
  value: k(() => ({
    ...e,
    elRef: r
  }), [e, r]),
  children: n
})), Pe = Ee(({
  slots: n,
  children: e,
  onValueChange: r,
  filterOption: o,
  onChange: s,
  options: t,
  optionItems: l,
  getPopupContainer: c,
  dropdownRender: u,
  elRef: _,
  ...i
}) => {
  const a = I(c), f = I(o), p = I(u);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [n.children ? null : /* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ m.jsx(Z, {
      ...i,
      ref: _,
      allowClear: n["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(g, {
          slot: n["allowClear.clearIcon"]
        })
      } : i.allowClear,
      options: k(() => t || G(l, {
        children: "options"
      }), [l, t]),
      onChange: (w, ...x) => {
        s == null || s(w, ...x), r(w);
      },
      notFoundContent: n.notFoundContent ? /* @__PURE__ */ m.jsx(g, {
        slot: n.notFoundContent
      }) : i.notFoundContent,
      filterOption: f || o,
      getPopupContainer: a,
      dropdownRender: p,
      children: n.children ? /* @__PURE__ */ m.jsxs(je, {
        children: [/* @__PURE__ */ m.jsx("div", {
          style: {
            display: "none"
          },
          children: e
        }), /* @__PURE__ */ m.jsx(g, {
          slot: n.children
        })]
      }) : null
    })]
  });
});
export {
  Pe as AutoComplete,
  Pe as default
};
