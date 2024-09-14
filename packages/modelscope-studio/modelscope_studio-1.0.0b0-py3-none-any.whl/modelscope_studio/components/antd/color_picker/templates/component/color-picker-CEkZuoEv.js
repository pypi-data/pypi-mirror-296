import { g as Z, w, d as $, a as m } from "./Index-BdoT87yG.js";
const k = window.ms_globals.React, v = window.ms_globals.React.useMemo, K = window.ms_globals.React.useState, H = window.ms_globals.React.useEffect, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, C = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.ColorPicker;
var M = {
  exports: {}
}, I = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var te = k, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function W(n, t, o) {
  var s, l = {}, e = null, r = null;
  o !== void 0 && (e = "" + o), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (s in t) oe.call(t, s) && !le.hasOwnProperty(s) && (l[s] = t[s]);
  if (n && n.defaultProps) for (s in t = n.defaultProps, t) l[s] === void 0 && (l[s] = t[s]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: r,
    props: l,
    _owner: se.current
  };
}
I.Fragment = re;
I.jsx = W;
I.jsxs = W;
M.exports = I;
var g = M.exports;
const {
  SvelteComponent: ce,
  assign: O,
  binding_callbacks: P,
  check_outros: ie,
  component_subscribe: j,
  compute_slots: ue,
  create_slot: ae,
  detach: h,
  element: z,
  empty: de,
  exclude_internal_props: F,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: ge,
  insert: y,
  safe_not_equal: me,
  set_custom_element_data: U,
  space: be,
  transition_in: x,
  transition_out: R,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: ye,
  onDestroy: xe,
  setContext: ve
} = window.__gradio__svelte__internal;
function L(n) {
  let t, o;
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
      t = z("svelte-slot"), l && l.c(), U(t, "class", "svelte-1rt0kpf");
    },
    m(e, r) {
      y(e, t, r), l && l.m(t, null), n[9](t), o = !0;
    },
    p(e, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && we(
        l,
        s,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          s,
          /*$$scope*/
          e[6],
          r,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (x(l, e), o = !0);
    },
    o(e) {
      R(l, e), o = !1;
    },
    d(e) {
      e && h(t), l && l.d(e), n[9](null);
    }
  };
}
function Ie(n) {
  let t, o, s, l, e = (
    /*$$slots*/
    n[4].default && L(n)
  );
  return {
    c() {
      t = z("react-portal-target"), o = be(), e && e.c(), s = de(), U(t, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      y(r, t, c), n[8](t), y(r, o, c), e && e.m(r, c), y(r, s, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? e ? (e.p(r, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = L(r), e.c(), x(e, 1), e.m(s.parentNode, s)) : e && (_e(), R(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(r) {
      l || (x(e), l = !0);
    },
    o(r) {
      R(e), l = !1;
    },
    d(r) {
      r && (h(t), h(o), h(s)), n[8](null), e && e.d(r);
    }
  };
}
function N(n) {
  const {
    svelteInit: t,
    ...o
  } = n;
  return o;
}
function Se(n, t, o) {
  let s, l, {
    $$slots: e = {},
    $$scope: r
  } = t;
  const c = ue(e);
  let {
    svelteInit: u
  } = t;
  const p = w(N(t)), i = w();
  j(n, i, (d) => o(0, s = d));
  const a = w();
  j(n, a, (d) => o(1, l = d));
  const f = [], _ = ye("$$ms-gr-antd-react-wrapper"), {
    slotKey: S,
    slotIndex: b,
    subSlotIndex: q
  } = Z() || {}, J = u({
    parent: _,
    props: p,
    target: i,
    slot: a,
    slotKey: S,
    slotIndex: b,
    subSlotIndex: q,
    onDestroy(d) {
      f.push(d);
    }
  });
  ve("$$ms-gr-antd-react-wrapper", J), he(() => {
    p.set(N(t));
  }), xe(() => {
    f.forEach((d) => d());
  });
  function V(d) {
    P[d ? "unshift" : "push"](() => {
      s = d, i.set(s);
    });
  }
  function Y(d) {
    P[d ? "unshift" : "push"](() => {
      l = d, a.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, t = O(O({}, t), F(d))), "svelteInit" in d && o(5, u = d.svelteInit), "$$scope" in d && o(6, r = d.$$scope);
  }, t = F(t), [s, l, i, a, c, u, r, e, V, Y];
}
class Ee extends ce {
  constructor(t) {
    super(), ge(this, t, Se, Ie, me, {
      svelteInit: 5
    });
  }
}
const T = window.ms_globals.rerender, E = window.ms_globals.tree;
function Re(n) {
  function t(o) {
    const s = w(), l = new Ee({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const r = {
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
          }, c = e.parent ?? E;
          return c.nodes = [...c.nodes, r], T({
            createPortal: C,
            node: E
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== s), T({
              createPortal: C,
              node: E
            });
          }), r;
        },
        ...o.props
      }
    });
    return s.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(t);
    });
  });
}
function ke(n) {
  const [t, o] = K(() => m(n));
  return H(() => {
    let s = !0;
    return n.subscribe((e) => {
      s && (s = !1, e === t) || o(e);
    });
  }, [n]), t;
}
function Ce(n) {
  const t = v(() => $(n, (o) => o), [n]);
  return ke(t);
}
function Oe(n) {
  try {
    return typeof n == "string" ? new Function(`return (...args) => (${n})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function A(n) {
  return v(() => Oe(n), [n]);
}
function Pe(n, t) {
  const o = v(() => k.Children.toArray(n).filter((e) => e.props.node && (!e.props.nodeSlotKey || t)).sort((e, r) => {
    if (e.props.node.slotIndex && r.props.node.slotIndex) {
      const c = m(e.props.node.slotIndex) || 0, u = m(r.props.node.slotIndex) || 0;
      return c - u === 0 && e.props.node.subSlotIndex && r.props.node.subSlotIndex ? (m(e.props.node.subSlotIndex) || 0) - (m(r.props.node.subSlotIndex) || 0) : c - u;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Ce(o);
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(n) {
  return n ? Object.keys(n).reduce((t, o) => {
    const s = n[o];
    return typeof s == "number" && !je.includes(o) ? t[o] = s + "px" : t[o] = s, t;
  }, {}) : {};
}
function B(n) {
  const t = n.cloneNode(!0);
  Object.keys(n.getEventListeners()).forEach((s) => {
    n.getEventListeners(s).forEach(({
      listener: e,
      type: r,
      useCapture: c
    }) => {
      t.addEventListener(r, e, c);
    });
  });
  const o = Array.from(n.children);
  for (let s = 0; s < o.length; s++) {
    const l = o[s], e = B(l);
    t.replaceChild(e, t.children[s]);
  }
  return t;
}
function Le(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const D = Q(({
  slot: n,
  clone: t,
  className: o,
  style: s
}, l) => {
  const e = X();
  return H(() => {
    var p;
    if (!e.current || !n)
      return;
    let r = n;
    function c() {
      let i = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (i = r.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Le(l, i), o && i.classList.add(...o.split(" ")), s) {
        const a = Fe(s);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let i = function() {
        var a;
        r = B(n), r.style.display = "contents", c(), (a = e.current) == null || a.appendChild(r);
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
      r.style.display = "contents", c(), (p = e.current) == null || p.appendChild(r);
    return () => {
      var i, a;
      r.style.display = "", (i = e.current) != null && i.contains(r) && ((a = e.current) == null || a.removeChild(r)), u == null || u.disconnect();
    };
  }, [n, t, o, s, l]), k.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  });
});
function G(n, t) {
  return n.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const s = {
      ...o.props
    };
    let l = s;
    Object.keys(o.slots).forEach((r) => {
      if (!o.slots[r] || !(o.slots[r] instanceof Element) && !o.slots[r].el)
        return;
      const c = r.split(".");
      c.forEach((f, _) => {
        l[f] || (l[f] = {}), _ !== c.length - 1 && (l = s[f]);
      });
      const u = o.slots[r];
      let p, i, a = !1;
      u instanceof Element ? p = u : (p = u.el, i = u.callback, a = u.clone || !1), l[c[c.length - 1]] = p ? i ? (...f) => (i(c[c.length - 1], f), /* @__PURE__ */ g.jsx(D, {
        slot: p,
        clone: a || (t == null ? void 0 : t.clone)
      })) : /* @__PURE__ */ g.jsx(D, {
        slot: p,
        clone: a || (t == null ? void 0 : t.clone)
      }) : l[c[c.length - 1]], l = s;
    });
    const e = "children";
    return o[e] && (s[e] = G(o[e], t)), s;
  });
}
const Te = Re(({
  onValueChange: n,
  onChange: t,
  panelRender: o,
  showText: s,
  value: l,
  presets: e,
  presetItems: r,
  children: c,
  value_format: u,
  ...p
}) => {
  const i = A(o), a = A(s), f = Pe(c);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [f.length === 0 && /* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: c
    }), /* @__PURE__ */ g.jsx(ee, {
      ...p,
      value: l,
      presets: v(() => e || G(r), [e, r]),
      showText: a,
      panelRender: i,
      onChange: (_, ...S) => {
        const b = {
          rgb: _.toRgbString(),
          hex: _.toHexString(),
          hsb: _.toHsbString()
        };
        t == null || t(b[u], ...S), n(b[u]);
      },
      children: f.length === 0 ? null : c
    })]
  });
});
export {
  Te as ColorPicker,
  Te as default
};
