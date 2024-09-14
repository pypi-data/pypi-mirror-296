import { g as X, w as x } from "./Index-D4FftijA.js";
const M = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, Q = window.ms_globals.React.useEffect, F = window.ms_globals.React.useMemo, R = window.ms_globals.ReactDOM.createPortal, Z = window.ms_globals.internalContext.FormItemContext, $ = window.ms_globals.antd.Form;
var T = {
  exports: {}
}, E = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ee = M, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(e, n, r) {
  var l, s = {}, t = null, o = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (l in n) oe.call(n, l) && !le.hasOwnProperty(l) && (s[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) s[l] === void 0 && (s[l] = n[l]);
  return {
    $$typeof: te,
    type: e,
    key: t,
    ref: o,
    props: s,
    _owner: re.current
  };
}
E.Fragment = ne;
E.jsx = G;
E.jsxs = G;
T.exports = E;
var _ = T.exports;
const {
  SvelteComponent: se,
  assign: S,
  binding_callbacks: P,
  check_outros: ie,
  component_subscribe: L,
  compute_slots: ce,
  create_slot: ae,
  detach: y,
  element: U,
  empty: ue,
  exclude_internal_props: N,
  get_all_dirty_from_scope: fe,
  get_slot_changes: de,
  group_outros: pe,
  init: _e,
  insert: v,
  safe_not_equal: me,
  set_custom_element_data: V,
  space: ge,
  transition_in: C,
  transition_out: k,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: he,
  getContext: we,
  onDestroy: xe,
  setContext: ye
} = window.__gradio__svelte__internal;
function z(e) {
  let n, r;
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
      n = U("svelte-slot"), s && s.c(), V(n, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      v(t, n, o), s && s.m(n, null), e[9](n), r = !0;
    },
    p(t, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && be(
        s,
        l,
        t,
        /*$$scope*/
        t[6],
        r ? de(
          l,
          /*$$scope*/
          t[6],
          o,
          null
        ) : fe(
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
      k(s, t), r = !1;
    },
    d(t) {
      t && y(n), s && s.d(t), e[9](null);
    }
  };
}
function ve(e) {
  let n, r, l, s, t = (
    /*$$slots*/
    e[4].default && z(e)
  );
  return {
    c() {
      n = U("react-portal-target"), r = ge(), t && t.c(), l = ue(), V(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      v(o, n, i), e[8](n), v(o, r, i), t && t.m(o, i), v(o, l, i), s = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, i), i & /*$$slots*/
      16 && C(t, 1)) : (t = z(o), t.c(), C(t, 1), t.m(l.parentNode, l)) : t && (pe(), k(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(o) {
      s || (C(t), s = !0);
    },
    o(o) {
      k(t), s = !1;
    },
    d(o) {
      o && (y(n), y(r), y(l)), e[8](null), t && t.d(o);
    }
  };
}
function D(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ce(e, n, r) {
  let l, s, {
    $$slots: t = {},
    $$scope: o
  } = n;
  const i = ce(t);
  let {
    svelteInit: u
  } = n;
  const d = x(D(n)), c = x();
  L(e, c, (f) => r(0, l = f));
  const a = x();
  L(e, a, (f) => r(1, s = f));
  const p = [], h = we("$$ms-gr-antd-react-wrapper"), {
    slotKey: w,
    slotIndex: g,
    subSlotIndex: I
  } = X() || {}, j = u({
    parent: h,
    props: d,
    target: c,
    slot: a,
    slotKey: w,
    slotIndex: g,
    subSlotIndex: I,
    onDestroy(f) {
      p.push(f);
    }
  });
  ye("$$ms-gr-antd-react-wrapper", j), he(() => {
    d.set(D(n));
  }), xe(() => {
    p.forEach((f) => f());
  });
  function B(f) {
    P[f ? "unshift" : "push"](() => {
      l = f, c.set(l);
    });
  }
  function J(f) {
    P[f ? "unshift" : "push"](() => {
      s = f, a.set(s);
    });
  }
  return e.$$set = (f) => {
    r(17, n = S(S({}, n), N(f))), "svelteInit" in f && r(5, u = f.svelteInit), "$$scope" in f && r(6, o = f.$$scope);
  }, n = N(n), [l, s, c, a, i, u, o, t, B, J];
}
class Ee extends se {
  constructor(n) {
    super(), _e(this, n, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, O = window.ms_globals.tree;
function Ie(e) {
  function n(r) {
    const l = x(), s = new Ee({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? O;
          return i.nodes = [...i.nodes, o], W({
            createPortal: R,
            node: O
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== l), W({
              createPortal: R,
              node: O
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
      r(n);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const l = e[r];
    return typeof l == "number" && !je.includes(r) ? n[r] = l + "px" : n[r] = l, n;
  }, {}) : {};
}
function q(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: t,
      type: o,
      useCapture: i
    }) => {
      n.addEventListener(o, t, i);
    });
  });
  const r = Array.from(e.children);
  for (let l = 0; l < r.length; l++) {
    const s = r[l], t = q(s);
    n.replaceChild(t, n.children[l]);
  }
  return n;
}
function ke(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const m = Y(({
  slot: e,
  clone: n,
  className: r,
  style: l
}, s) => {
  const t = K();
  return Q(() => {
    var d;
    if (!t.current || !e)
      return;
    let o = e;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ke(s, c), r && c.classList.add(...r.split(" ")), l) {
        const a = Oe(l);
        Object.keys(a).forEach((p) => {
          c.style[p] = a[p];
        });
      }
    }
    let u = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var a;
        o = q(e), o.style.display = "contents", i(), (a = t.current) == null || a.appendChild(o);
      };
      c(), u = new window.MutationObserver(() => {
        var a, p;
        (a = t.current) != null && a.contains(o) && ((p = t.current) == null || p.removeChild(o)), c();
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (d = t.current) == null || d.appendChild(o);
    return () => {
      var c, a;
      o.style.display = "", (c = t.current) != null && c.contains(o) && ((a = t.current) == null || a.removeChild(o)), u == null || u.disconnect();
    };
  }, [e, n, r, l, s]), M.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Fe(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function b(e) {
  return F(() => Fe(e), [e]);
}
function H(e, n) {
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
      const i = o.split(".");
      i.forEach((p, h) => {
        s[p] || (s[p] = {}), h !== i.length - 1 && (s = l[p]);
      });
      const u = r.slots[o];
      let d, c, a = !1;
      u instanceof Element ? d = u : (d = u.el, c = u.callback, a = u.clone || !1), s[i[i.length - 1]] = d ? c ? (...p) => (c(i[i.length - 1], p), /* @__PURE__ */ _.jsx(m, {
        slot: d,
        clone: a || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ _.jsx(m, {
        slot: d,
        clone: a || (n == null ? void 0 : n.clone)
      }) : s[i[i.length - 1]], s = l;
    });
    const t = "children";
    return r[t] && (l[t] = H(r[t], n)), l;
  });
}
function Re(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const A = ({
  children: e,
  ...n
}) => /* @__PURE__ */ _.jsx(Z.Provider, {
  value: F(() => n, [n]),
  children: e
}), Pe = Ie(({
  slots: e,
  getValueFromEvent: n,
  getValueProps: r,
  normalize: l,
  shouldUpdate: s,
  tooltip: t,
  ruleItems: o,
  rules: i,
  children: u,
  ...d
}) => {
  const c = e["tooltip.icon"] || e["tooltip.title"] || typeof t == "object", a = b(n), p = b(r), h = b(l), w = b(s), g = Re(t), I = b(g.afterOpenChange), j = b(g.getPopupContainer);
  return /* @__PURE__ */ _.jsx($.Item, {
    ...d,
    getValueFromEvent: a,
    getValueProps: p,
    normalize: h,
    shouldUpdate: w || s,
    rules: F(() => i || H(o), [o, i]),
    tooltip: e.tooltip ? /* @__PURE__ */ _.jsx(m, {
      slot: e.tooltip
    }) : c ? {
      ...g,
      afterOpenChange: I,
      getPopupContainer: j,
      icon: e["tooltip.icon"] ? /* @__PURE__ */ _.jsx(m, {
        slot: e["tooltip.icon"]
      }) : g.icon,
      title: e["tooltip.title"] ? /* @__PURE__ */ _.jsx(m, {
        slot: e["tooltip.title"]
      }) : g.title
    } : t,
    extra: e.extra ? /* @__PURE__ */ _.jsx(m, {
      slot: e.extra
    }) : d.extra,
    help: e.help ? /* @__PURE__ */ _.jsx(m, {
      slot: e.help
    }) : d.help,
    label: e.label ? /* @__PURE__ */ _.jsx(m, {
      slot: e.label
    }) : d.label,
    children: w || s ? () => /* @__PURE__ */ _.jsx(A, {
      children: u
    }) : /* @__PURE__ */ _.jsx(A, {
      children: u
    })
  });
});
export {
  Pe as FormItem,
  Pe as default
};
