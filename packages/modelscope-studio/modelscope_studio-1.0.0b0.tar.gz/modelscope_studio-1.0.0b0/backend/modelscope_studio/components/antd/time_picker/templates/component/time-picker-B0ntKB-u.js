import { g as ae, w as R } from "./Index-Cj39yi8B.js";
const B = window.ms_globals.React, ie = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ue = window.ms_globals.React.useEffect, w = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, de = window.ms_globals.antd.TimePicker, M = window.ms_globals.dayjs;
var J = {
  exports: {}
}, P = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var fe = B, _e = Symbol.for("react.element"), me = Symbol.for("react.fragment"), pe = Object.prototype.hasOwnProperty, ve = fe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, we = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function V(e, n, s) {
  var o, l = {}, t = null, r = null;
  s !== void 0 && (t = "" + s), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (o in n) pe.call(n, o) && !we.hasOwnProperty(o) && (l[o] = n[o]);
  if (e && e.defaultProps) for (o in n = e.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: _e,
    type: e,
    key: t,
    ref: r,
    props: l,
    _owner: ve.current
  };
}
P.Fragment = me;
P.jsx = V;
P.jsxs = V;
J.exports = P;
var f = J.exports;
const {
  SvelteComponent: be,
  assign: W,
  binding_callbacks: z,
  check_outros: ge,
  component_subscribe: U,
  compute_slots: ye,
  create_slot: xe,
  detach: j,
  element: Y,
  empty: Ie,
  exclude_internal_props: q,
  get_all_dirty_from_scope: he,
  get_slot_changes: Ee,
  group_outros: Re,
  init: je,
  insert: k,
  safe_not_equal: ke,
  set_custom_element_data: Q,
  space: Oe,
  transition_in: O,
  transition_out: T,
  update_slot_base: Pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Se,
  getContext: Fe,
  onDestroy: Ce,
  setContext: De
} = window.__gradio__svelte__internal;
function G(e) {
  let n, s;
  const o = (
    /*#slots*/
    e[7].default
  ), l = xe(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = Y("svelte-slot"), l && l.c(), Q(n, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      k(t, n, r), l && l.m(n, null), e[9](n), s = !0;
    },
    p(t, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && Pe(
        l,
        o,
        t,
        /*$$scope*/
        t[6],
        s ? Ee(
          o,
          /*$$scope*/
          t[6],
          r,
          null
        ) : he(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (O(l, t), s = !0);
    },
    o(t) {
      T(l, t), s = !1;
    },
    d(t) {
      t && j(n), l && l.d(t), e[9](null);
    }
  };
}
function Ne(e) {
  let n, s, o, l, t = (
    /*$$slots*/
    e[4].default && G(e)
  );
  return {
    c() {
      n = Y("react-portal-target"), s = Oe(), t && t.c(), o = Ie(), Q(n, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      k(r, n, i), e[8](n), k(r, s, i), t && t.m(r, i), k(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, i), i & /*$$slots*/
      16 && O(t, 1)) : (t = G(r), t.c(), O(t, 1), t.m(o.parentNode, o)) : t && (Re(), T(t, 1, 1, () => {
        t = null;
      }), ge());
    },
    i(r) {
      l || (O(t), l = !0);
    },
    o(r) {
      T(t), l = !1;
    },
    d(r) {
      r && (j(n), j(s), j(o)), e[8](null), t && t.d(r);
    }
  };
}
function H(e) {
  const {
    svelteInit: n,
    ...s
  } = e;
  return s;
}
function Le(e, n, s) {
  let o, l, {
    $$slots: t = {},
    $$scope: r
  } = n;
  const i = ye(t);
  let {
    svelteInit: d
  } = n;
  const p = R(H(n)), c = R();
  U(e, c, (u) => s(0, o = u));
  const a = R();
  U(e, a, (u) => s(1, l = u));
  const _ = [], S = Fe("$$ms-gr-antd-react-wrapper"), {
    slotKey: y,
    slotIndex: x,
    subSlotIndex: F
  } = ae() || {}, C = d({
    parent: S,
    props: p,
    target: c,
    slot: a,
    slotKey: y,
    slotIndex: x,
    subSlotIndex: F,
    onDestroy(u) {
      _.push(u);
    }
  });
  De("$$ms-gr-antd-react-wrapper", C), Se(() => {
    p.set(H(n));
  }), Ce(() => {
    _.forEach((u) => u());
  });
  function m(u) {
    z[u ? "unshift" : "push"](() => {
      o = u, c.set(o);
    });
  }
  function D(u) {
    z[u ? "unshift" : "push"](() => {
      l = u, a.set(l);
    });
  }
  return e.$$set = (u) => {
    s(17, n = W(W({}, n), q(u))), "svelteInit" in u && s(5, d = u.svelteInit), "$$scope" in u && s(6, r = u.$$scope);
  }, n = q(n), [o, l, c, a, i, d, r, t, m, D];
}
class Te extends be {
  constructor(n) {
    super(), je(this, n, Le, Ne, ke, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, N = window.ms_globals.tree;
function Ae(e) {
  function n(s) {
    const o = R(), l = new Te({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const r = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? N;
          return i.nodes = [...i.nodes, r], K({
            createPortal: A,
            node: N
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== o), K({
              createPortal: A,
              node: N
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
      s(n);
    });
  });
}
const Me = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function We(e) {
  return e ? Object.keys(e).reduce((n, s) => {
    const o = e[s];
    return typeof o == "number" && !Me.includes(s) ? n[s] = o + "px" : n[s] = o, n;
  }, {}) : {};
}
function X(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: t,
      type: r,
      useCapture: i
    }) => {
      n.addEventListener(r, t, i);
    });
  });
  const s = Array.from(e.children);
  for (let o = 0; o < s.length; o++) {
    const l = s[o], t = X(l);
    n.replaceChild(t, n.children[o]);
  }
  return n;
}
function ze(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const v = ie(({
  slot: e,
  clone: n,
  className: s,
  style: o
}, l) => {
  const t = ce();
  return ue(() => {
    var p;
    if (!t.current || !e)
      return;
    let r = e;
    function i() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ze(l, c), s && c.classList.add(...s.split(" ")), o) {
        const a = We(o);
        Object.keys(a).forEach((_) => {
          c.style[_] = a[_];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var a;
        r = X(e), r.style.display = "contents", i(), (a = t.current) == null || a.appendChild(r);
      };
      c(), d = new window.MutationObserver(() => {
        var a, _;
        (a = t.current) != null && a.contains(r) && ((_ = t.current) == null || _.removeChild(r)), c();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (p = t.current) == null || p.appendChild(r);
    return () => {
      var c, a;
      r.style.display = "", (c = t.current) != null && c.contains(r) && ((a = t.current) == null || a.removeChild(r)), d == null || d.disconnect();
    };
  }, [e, n, s, o, l]), B.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Ue(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function E(e) {
  return w(() => Ue(e), [e]);
}
function b(e) {
  return Array.isArray(e) ? e.map((n) => b(n)) : M(typeof e == "number" ? e * 1e3 : e);
}
function L(e) {
  return Array.isArray(e) ? e.map((n) => n ? n.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const Ge = Ae(({
  slots: e,
  disabledDate: n,
  disabledTime: s,
  value: o,
  defaultValue: l,
  defaultPickerValue: t,
  pickerValue: r,
  onChange: i,
  minDate: d,
  maxDate: p,
  cellRender: c,
  panelRender: a,
  getPopupContainer: _,
  onValueChange: S,
  onPanelChange: y,
  onCalendarChange: x,
  children: F,
  elRef: C,
  ...m
}) => {
  const D = E(n), u = E(s), Z = E(_), $ = E(c), ee = E(a), te = w(() => o ? b(o) : void 0, [o]), ne = w(() => l ? b(l) : void 0, [l]), re = w(() => t ? b(t) : void 0, [t]), oe = w(() => r ? b(r) : void 0, [r]), se = w(() => d ? b(d) : void 0, [d]), le = w(() => p ? b(p) : void 0, [p]);
  return /* @__PURE__ */ f.jsxs(f.Fragment, {
    children: [/* @__PURE__ */ f.jsx("div", {
      style: {
        display: "none"
      },
      children: F
    }), /* @__PURE__ */ f.jsx(de, {
      ...m,
      ref: C,
      value: te,
      defaultValue: ne,
      defaultPickerValue: re,
      pickerValue: oe,
      minDate: se,
      maxDate: le,
      disabledTime: u,
      disabledDate: D,
      getPopupContainer: Z,
      cellRender: $,
      panelRender: ee,
      onPanelChange: (I, ...h) => {
        const g = L(I);
        y == null || y(g, ...h);
      },
      onChange: (I, ...h) => {
        const g = L(I);
        i == null || i(g, ...h), S(g);
      },
      onCalendarChange: (I, ...h) => {
        const g = L(I);
        x == null || x(g, ...h);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ f.jsx(v, {
        slot: e.renderExtraFooter
      }) : null : m.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ f.jsx(v, {
        slot: e.prevIcon
      }) : m.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ f.jsx(v, {
        slot: e.nextIcon
      }) : m.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ f.jsx(v, {
        slot: e.suffixIcon
      }) : m.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ f.jsx(v, {
        slot: e.superNextIcon
      }) : m.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ f.jsx(v, {
        slot: e.superPrevIcon
      }) : m.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ f.jsx(v, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear
    })]
  });
});
export {
  Ge as TimePicker,
  Ge as default
};
