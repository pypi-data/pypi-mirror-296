import { g as ue, w as R } from "./Index-DBF85Hhv.js";
const B = window.ms_globals.React, ie = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ae = window.ms_globals.React.useEffect, v = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, de = window.ms_globals.antd.TimePicker, M = window.ms_globals.dayjs;
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
var fe = B, me = Symbol.for("react.element"), _e = Symbol.for("react.fragment"), pe = Object.prototype.hasOwnProperty, we = fe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, be = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(e, n, s) {
  var o, l = {}, t = null, r = null;
  s !== void 0 && (t = "" + s), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (o in n) pe.call(n, o) && !be.hasOwnProperty(o) && (l[o] = n[o]);
  if (e && e.defaultProps) for (o in n = e.defaultProps, n) l[o] === void 0 && (l[o] = n[o]);
  return {
    $$typeof: me,
    type: e,
    key: t,
    ref: r,
    props: l,
    _owner: we.current
  };
}
P.Fragment = _e;
P.jsx = Y;
P.jsxs = Y;
J.exports = P;
var m = J.exports;
const {
  SvelteComponent: ge,
  assign: W,
  binding_callbacks: z,
  check_outros: ve,
  component_subscribe: U,
  compute_slots: xe,
  create_slot: ye,
  detach: j,
  element: Q,
  empty: Ie,
  exclude_internal_props: q,
  get_all_dirty_from_scope: he,
  get_slot_changes: Ee,
  group_outros: Re,
  init: je,
  insert: S,
  safe_not_equal: Se,
  set_custom_element_data: X,
  space: Oe,
  transition_in: O,
  transition_out: T,
  update_slot_base: Pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: ke,
  getContext: Fe,
  onDestroy: Ce,
  setContext: De
} = window.__gradio__svelte__internal;
function G(e) {
  let n, s;
  const o = (
    /*#slots*/
    e[7].default
  ), l = ye(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = Q("svelte-slot"), l && l.c(), X(n, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      S(t, n, r), l && l.m(n, null), e[9](n), s = !0;
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
      n = Q("react-portal-target"), s = Oe(), t && t.c(), o = Ie(), X(n, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      S(r, n, i), e[8](n), S(r, s, i), t && t.m(r, i), S(r, o, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, i), i & /*$$slots*/
      16 && O(t, 1)) : (t = G(r), t.c(), O(t, 1), t.m(o.parentNode, o)) : t && (Re(), T(t, 1, 1, () => {
        t = null;
      }), ve());
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
  const i = xe(t);
  let {
    svelteInit: d
  } = n;
  const w = R(H(n)), c = R();
  U(e, c, (a) => s(0, o = a));
  const u = R();
  U(e, u, (a) => s(1, l = a));
  const p = [], k = Fe("$$ms-gr-antd-react-wrapper"), {
    slotKey: y,
    slotIndex: I,
    subSlotIndex: F
  } = ue() || {}, C = d({
    parent: k,
    props: w,
    target: c,
    slot: u,
    slotKey: y,
    slotIndex: I,
    subSlotIndex: F,
    onDestroy(a) {
      p.push(a);
    }
  });
  De("$$ms-gr-antd-react-wrapper", C), ke(() => {
    w.set(H(n));
  }), Ce(() => {
    p.forEach((a) => a());
  });
  function _(a) {
    z[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  function D(a) {
    z[a ? "unshift" : "push"](() => {
      l = a, u.set(l);
    });
  }
  return e.$$set = (a) => {
    s(17, n = W(W({}, n), q(a))), "svelteInit" in a && s(5, d = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, n = q(n), [o, l, c, u, i, d, r, t, _, D];
}
class Te extends ge {
  constructor(n) {
    super(), je(this, n, Le, Ne, Se, {
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
function Z(e) {
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
    const l = s[o], t = Z(l);
    n.replaceChild(t, n.children[o]);
  }
  return n;
}
function ze(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = ie(({
  slot: e,
  clone: n,
  className: s,
  style: o
}, l) => {
  const t = ce();
  return ae(() => {
    var w;
    if (!t.current || !e)
      return;
    let r = e;
    function i() {
      let c = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (c = r.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ze(l, c), s && c.classList.add(...s.split(" ")), o) {
        const u = We(o);
        Object.keys(u).forEach((p) => {
          c.style[p] = u[p];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        r = Z(e), r.style.display = "contents", i(), (u = t.current) == null || u.appendChild(r);
      };
      c(), d = new window.MutationObserver(() => {
        var u, p;
        (u = t.current) != null && u.contains(r) && ((p = t.current) == null || p.removeChild(r)), c();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", i(), (w = t.current) == null || w.appendChild(r);
    return () => {
      var c, u;
      r.style.display = "", (c = t.current) != null && c.contains(r) && ((u = t.current) == null || u.removeChild(r)), d == null || d.disconnect();
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
  return v(() => Ue(e), [e]);
}
function g(e) {
  return M(typeof e == "number" ? e * 1e3 : e);
}
function L(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
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
  maxDate: w,
  cellRender: c,
  panelRender: u,
  getPopupContainer: p,
  onValueChange: k,
  onPanelChange: y,
  onCalendarChange: I,
  children: F,
  elRef: C,
  ..._
}) => {
  const D = E(n), a = E(p), V = E(c), $ = E(u), ee = E(s), te = v(() => o == null ? void 0 : o.map((f) => g(f)), [o]), ne = v(() => l == null ? void 0 : l.map((f) => g(f)), [l]), re = v(() => Array.isArray(t) ? t.map((f) => g(f)) : t ? g(t) : void 0, [t]), oe = v(() => Array.isArray(r) ? r.map((f) => g(f)) : r ? g(r) : void 0, [r]), se = v(() => d ? g(d) : void 0, [d]), le = v(() => w ? g(w) : void 0, [w]);
  return /* @__PURE__ */ m.jsxs(m.Fragment, {
    children: [/* @__PURE__ */ m.jsx("div", {
      style: {
        display: "none"
      },
      children: F
    }), /* @__PURE__ */ m.jsx(de.RangePicker, {
      ..._,
      ref: C,
      value: te,
      disabledTime: ee,
      defaultValue: ne,
      defaultPickerValue: re,
      pickerValue: oe,
      minDate: se,
      maxDate: le,
      disabledDate: D,
      getPopupContainer: a,
      cellRender: V,
      panelRender: $,
      onPanelChange: (f, ...h) => {
        const x = L(f);
        y == null || y(x, ...h);
      },
      onChange: (f, ...h) => {
        const x = L(f);
        i == null || i(x, ...h), k(x);
      },
      onCalendarChange: (f, ...h) => {
        const x = L(f);
        I == null || I(x, ...h);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ m.jsx(b, {
        slot: e.renderExtraFooter
      }) : null : _.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.prevIcon
      }) : _.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.nextIcon
      }) : _.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.suffixIcon
      }) : _.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.superNextIcon
      }) : _.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ m.jsx(b, {
        slot: e.superPrevIcon
      }) : _.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ m.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : _.allowClear,
      separator: e.separator ? /* @__PURE__ */ m.jsx(b, {
        slot: e.separator
      }) : _.separator
    })]
  });
});
export {
  Ge as TimeRangePicker,
  Ge as default
};
