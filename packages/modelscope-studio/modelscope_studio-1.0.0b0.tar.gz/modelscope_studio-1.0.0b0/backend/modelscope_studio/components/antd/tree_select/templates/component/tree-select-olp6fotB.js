import { g as Z, w as C } from "./Index-CGQykDTS.js";
const z = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, V = window.ms_globals.React.useRef, X = window.ms_globals.React.useEffect, A = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.TreeSelect;
var q = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = z, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(e, t, r) {
  var l, s = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) re.call(t, l) && !le.hasOwnProperty(l) && (s[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) s[l] === void 0 && (s[l] = t[l]);
  return {
    $$typeof: te,
    type: e,
    key: n,
    ref: o,
    props: s,
    _owner: oe.current
  };
}
O.Fragment = ne;
O.jsx = G;
O.jsxs = G;
q.exports = O;
var m = q.exports;
const {
  SvelteComponent: se,
  assign: T,
  binding_callbacks: L,
  check_outros: ce,
  component_subscribe: N,
  compute_slots: ie,
  create_slot: ae,
  detach: E,
  element: H,
  empty: ue,
  exclude_internal_props: D,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: me,
  insert: R,
  safe_not_equal: ge,
  set_custom_element_data: B,
  space: we,
  transition_in: S,
  transition_out: k,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: be,
  onDestroy: ye,
  setContext: xe
} = window.__gradio__svelte__internal;
function M(e) {
  let t, r;
  const l = (
    /*#slots*/
    e[7].default
  ), s = ae(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = H("svelte-slot"), s && s.c(), B(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      R(n, t, o), s && s.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && pe(
        s,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? fe(
          l,
          /*$$scope*/
          n[6],
          o,
          null
        ) : de(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (S(s, n), r = !0);
    },
    o(n) {
      k(s, n), r = !1;
    },
    d(n) {
      n && E(t), s && s.d(n), e[9](null);
    }
  };
}
function ve(e) {
  let t, r, l, s, n = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      t = H("react-portal-target"), r = we(), n && n.c(), l = ue(), B(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      R(o, t, c), e[8](t), R(o, r, c), n && n.m(o, c), R(o, l, c), s = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, c), c & /*$$slots*/
      16 && S(n, 1)) : (n = M(o), n.c(), S(n, 1), n.m(l.parentNode, l)) : n && (_e(), k(n, 1, 1, () => {
        n = null;
      }), ce());
    },
    i(o) {
      s || (S(n), s = !0);
    },
    o(o) {
      k(n), s = !1;
    },
    d(o) {
      o && (E(t), E(r), E(l)), e[8](null), n && n.d(o);
    }
  };
}
function U(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ie(e, t, r) {
  let l, s, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const c = ie(n);
  let {
    svelteInit: u
  } = t;
  const _ = C(U(t)), i = C();
  N(e, i, (d) => r(0, l = d));
  const a = C();
  N(e, a, (d) => r(1, s = d));
  const f = [], g = be("$$ms-gr-antd-react-wrapper"), {
    slotKey: h,
    slotIndex: b,
    subSlotIndex: y
  } = Z() || {}, x = u({
    parent: g,
    props: _,
    target: i,
    slot: a,
    slotKey: h,
    slotIndex: b,
    subSlotIndex: y,
    onDestroy(d) {
      f.push(d);
    }
  });
  xe("$$ms-gr-antd-react-wrapper", x), he(() => {
    _.set(U(t));
  }), ye(() => {
    f.forEach((d) => d());
  });
  function v(d) {
    L[d ? "unshift" : "push"](() => {
      l = d, i.set(l);
    });
  }
  function I(d) {
    L[d ? "unshift" : "push"](() => {
      s = d, a.set(s);
    });
  }
  return e.$$set = (d) => {
    r(17, t = T(T({}, t), D(d))), "svelteInit" in d && r(5, u = d.svelteInit), "$$scope" in d && r(6, o = d.$$scope);
  }, t = D(t), [l, s, i, a, c, u, o, n, v, I];
}
class Ce extends se {
  constructor(t) {
    super(), me(this, t, Ie, ve, ge, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, j = window.ms_globals.tree;
function Ee(e) {
  function t(r) {
    const l = C(), s = new Ce({
      ...r,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? j;
          return c.nodes = [...c.nodes, o], W({
            createPortal: F,
            node: j
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== l), W({
              createPortal: F,
              node: j
            });
          }), o;
        },
        ...r.props
      }
    });
    return l.set(s), s;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Re = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Se(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return typeof l == "number" && !Re.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function J(e) {
  const t = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: n,
      type: o,
      useCapture: c
    }) => {
      t.addEventListener(o, n, c);
    });
  });
  const r = Array.from(e.children);
  for (let l = 0; l < r.length; l++) {
    const s = r[l], n = J(s);
    t.replaceChild(n, t.children[l]);
  }
  return t;
}
function Oe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const w = Q(({
  slot: e,
  clone: t,
  className: r,
  style: l
}, s) => {
  const n = V();
  return X(() => {
    var _;
    if (!n.current || !e)
      return;
    let o = e;
    function c() {
      let i = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (i = o.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Oe(s, i), r && i.classList.add(...r.split(" ")), l) {
        const a = Se(l);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        o = J(e), o.style.display = "contents", c(), (a = n.current) == null || a.appendChild(o);
      };
      i(), u = new window.MutationObserver(() => {
        var a, f;
        (a = n.current) != null && a.contains(o) && ((f = n.current) == null || f.removeChild(o)), i();
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", c(), (_ = n.current) == null || _.appendChild(o);
    return () => {
      var i, a;
      o.style.display = "", (i = n.current) != null && i.contains(o) && ((a = n.current) == null || a.removeChild(o)), u == null || u.disconnect();
    };
  }, [e, t, r, l, s]), z.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  });
});
function je(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function p(e) {
  return A(() => je(e), [e]);
}
function ke(e) {
  return Object.keys(e).reduce((t, r) => (e[r] !== void 0 && (t[r] = e[r]), t), {});
}
function Y(e, t) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const l = {
      ...r.props
    };
    let s = l;
    Object.keys(r.slots).forEach((o) => {
      if (!r.slots[o] || !(r.slots[o] instanceof Element) && !r.slots[o].el)
        return;
      const c = o.split(".");
      c.forEach((f, g) => {
        s[f] || (s[f] = {}), g !== c.length - 1 && (s = l[f]);
      });
      const u = r.slots[o];
      let _, i, a = !1;
      u instanceof Element ? _ = u : (_ = u.el, i = u.callback, a = u.clone || !1), s[c[c.length - 1]] = _ ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ m.jsx(w, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ m.jsx(w, {
        slot: _,
        clone: a || (t == null ? void 0 : t.clone)
      }) : s[c[c.length - 1]], s = l;
    });
    const n = "children";
    return r[n] && (l[n] = Y(r[n], t)), l;
  });
}
const Fe = Ee(({
  slots: e,
  filterTreeNode: t,
  getPopupContainer: r,
  dropdownRender: l,
  tagRender: s,
  treeTitleRender: n,
  treeData: o,
  onValueChange: c,
  onChange: u,
  children: _,
  slotItems: i,
  maxTagPlaceholder: a,
  elRef: f,
  ...g
}) => {
  const h = p(t), b = p(r), y = p(a), x = p(s), v = p(l), I = p(n), d = A(() => ({
    ...g,
    treeData: o || Y(i),
    dropdownRender: v,
    allowClear: e["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ m.jsx(w, {
        slot: e["allowClear.clearIcon"]
      })
    } : g.allowClear,
    suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(w, {
      slot: e.suffixIcon
    }) : g.suffixIcon,
    switcherIcon: e.switcherIcon ? /* @__PURE__ */ m.jsx(w, {
      slot: e.switcherIcon
    }) : g.switcherIcon,
    getPopupContainer: b,
    tagRender: x,
    treeTitleRender: I,
    filterTreeNode: h || t,
    maxTagPlaceholder: y || (e.maxTagPlaceholder ? /* @__PURE__ */ m.jsx(w, {
      slot: e.maxTagPlaceholder
    }) : a),
    notFoundContent: e.notFoundContent ? /* @__PURE__ */ m.jsx(w, {
      slot: e.notFoundContent
    }) : g.notFoundContent
  }), [v, t, h, b, a, y, g, i, e, x, o, I]);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: _
    }), /* @__PURE__ */ m.jsx($, {
      ...ke(d),
      ref: f,
      onChange: (P, ...K) => {
        u == null || u(P, ...K), c(P);
      }
    })]
  });
});
export {
  Fe as TreeSelect,
  Fe as default
};
