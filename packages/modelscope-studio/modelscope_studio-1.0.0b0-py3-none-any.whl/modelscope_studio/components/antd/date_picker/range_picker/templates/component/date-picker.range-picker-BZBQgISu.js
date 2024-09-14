import { g as _e, w as R } from "./Index-d4IFOtWh.js";
const J = window.ms_globals.React, ue = window.ms_globals.React.forwardRef, fe = window.ms_globals.React.useRef, de = window.ms_globals.React.useEffect, v = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, me = window.ms_globals.antd.DatePicker, W = window.ms_globals.dayjs;
var Y = {
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
var pe = J, be = Symbol.for("react.element"), ge = Symbol.for("react.fragment"), ve = Object.prototype.hasOwnProperty, we = pe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, xe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(e, n, r) {
  var o, s = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (o in n) ve.call(n, o) && !xe.hasOwnProperty(o) && (s[o] = n[o]);
  if (e && e.defaultProps) for (o in n = e.defaultProps, n) s[o] === void 0 && (s[o] = n[o]);
  return {
    $$typeof: be,
    type: e,
    key: t,
    ref: l,
    props: s,
    _owner: we.current
  };
}
P.Fragment = ge;
P.jsx = K;
P.jsxs = K;
Y.exports = P;
var p = Y.exports;
const {
  SvelteComponent: ye,
  assign: z,
  binding_callbacks: U,
  check_outros: Ie,
  component_subscribe: q,
  compute_slots: he,
  create_slot: Ee,
  detach: O,
  element: Q,
  empty: je,
  exclude_internal_props: G,
  get_all_dirty_from_scope: Re,
  get_slot_changes: Oe,
  group_outros: ke,
  init: Se,
  insert: k,
  safe_not_equal: Pe,
  set_custom_element_data: X,
  space: De,
  transition_in: S,
  transition_out: A,
  update_slot_base: Fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ce,
  getContext: Ne,
  onDestroy: Le,
  setContext: Ae
} = window.__gradio__svelte__internal;
function H(e) {
  let n, r;
  const o = (
    /*#slots*/
    e[7].default
  ), s = Ee(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = Q("svelte-slot"), s && s.c(), X(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      k(t, n, l), s && s.m(n, null), e[9](n), r = !0;
    },
    p(t, l) {
      s && s.p && (!r || l & /*$$scope*/
      64) && Fe(
        s,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? Oe(
          o,
          /*$$scope*/
          t[6],
          l,
          null
        ) : Re(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (S(s, t), r = !0);
    },
    o(t) {
      A(s, t), r = !1;
    },
    d(t) {
      t && O(n), s && s.d(t), e[9](null);
    }
  };
}
function Me(e) {
  let n, r, o, s, t = (
    /*$$slots*/
    e[4].default && H(e)
  );
  return {
    c() {
      n = Q("react-portal-target"), r = De(), t && t.c(), o = je(), X(n, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      k(l, n, c), e[8](n), k(l, r, c), t && t.m(l, c), k(l, o, c), s = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && S(t, 1)) : (t = H(l), t.c(), S(t, 1), t.m(o.parentNode, o)) : t && (ke(), A(t, 1, 1, () => {
        t = null;
      }), Ie());
    },
    i(l) {
      s || (S(t), s = !0);
    },
    o(l) {
      A(t), s = !1;
    },
    d(l) {
      l && (O(n), O(r), O(o)), e[8](null), t && t.d(l);
    }
  };
}
function B(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function We(e, n, r) {
  let o, s, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const c = he(t);
  let {
    svelteInit: f
  } = n;
  const m = R(B(n)), a = R();
  q(e, a, (i) => r(0, o = i));
  const u = R();
  q(e, u, (i) => r(1, s = i));
  const _ = [], y = Ne("$$ms-gr-antd-react-wrapper"), {
    slotKey: D,
    slotIndex: F,
    subSlotIndex: I
  } = _e() || {}, h = f({
    parent: y,
    props: m,
    target: a,
    slot: u,
    slotKey: D,
    slotIndex: F,
    subSlotIndex: I,
    onDestroy(i) {
      _.push(i);
    }
  });
  Ae("$$ms-gr-antd-react-wrapper", h), Ce(() => {
    m.set(B(n));
  }), Le(() => {
    _.forEach((i) => i());
  });
  function C(i) {
    U[i ? "unshift" : "push"](() => {
      o = i, a.set(o);
    });
  }
  function N(i) {
    U[i ? "unshift" : "push"](() => {
      s = i, u.set(s);
    });
  }
  return e.$$set = (i) => {
    r(17, n = z(z({}, n), G(i))), "svelteInit" in i && r(5, f = i.svelteInit), "$$scope" in i && r(6, l = i.$$scope);
  }, n = G(n), [o, s, a, u, c, f, l, t, C, N];
}
class ze extends ye {
  constructor(n) {
    super(), Se(this, n, We, Me, Pe, {
      svelteInit: 5
    });
  }
}
const T = window.ms_globals.rerender, L = window.ms_globals.tree;
function Ue(e) {
  function n(r) {
    const o = R(), s = new ze({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
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
          }, c = t.parent ?? L;
          return c.nodes = [...c.nodes, l], T({
            createPortal: M,
            node: L
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((f) => f.svelteInstance !== o), T({
              createPortal: M,
              node: L
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
      r(n);
    });
  });
}
const qe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ge(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const o = e[r];
    return typeof o == "number" && !qe.includes(r) ? n[r] = o + "px" : n[r] = o, n;
  }, {}) : {};
}
function Z(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: t,
      type: l,
      useCapture: c
    }) => {
      n.addEventListener(l, t, c);
    });
  });
  const r = Array.from(e.children);
  for (let o = 0; o < r.length; o++) {
    const s = r[o], t = Z(s);
    n.replaceChild(t, n.children[o]);
  }
  return n;
}
function He(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const b = ue(({
  slot: e,
  clone: n,
  className: r,
  style: o
}, s) => {
  const t = fe();
  return de(() => {
    var m;
    if (!t.current || !e)
      return;
    let l = e;
    function c() {
      let a = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (a = l.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), He(s, a), r && a.classList.add(...r.split(" ")), o) {
        const u = Ge(o);
        Object.keys(u).forEach((_) => {
          a.style[_] = u[_];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var u;
        l = Z(e), l.style.display = "contents", c(), (u = t.current) == null || u.appendChild(l);
      };
      a(), f = new window.MutationObserver(() => {
        var u, _;
        (u = t.current) != null && u.contains(l) && ((_ = t.current) == null || _.removeChild(l)), a();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", c(), (m = t.current) == null || m.appendChild(l);
    return () => {
      var a, u;
      l.style.display = "", (a = t.current) != null && a.contains(l) && ((u = t.current) == null || u.removeChild(l)), f == null || f.disconnect();
    };
  }, [e, n, r, o, s]), J.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Be(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function E(e) {
  return v(() => Be(e), [e]);
}
function V(e, n) {
  return e.filter(Boolean).map((r) => {
    if (typeof r != "object")
      return r;
    const o = {
      ...r.props
    };
    let s = o;
    Object.keys(r.slots).forEach((l) => {
      if (!r.slots[l] || !(r.slots[l] instanceof Element) && !r.slots[l].el)
        return;
      const c = l.split(".");
      c.forEach((_, y) => {
        s[_] || (s[_] = {}), y !== c.length - 1 && (s = o[_]);
      });
      const f = r.slots[l];
      let m, a, u = !1;
      f instanceof Element ? m = f : (m = f.el, a = f.callback, u = f.clone || !1), s[c[c.length - 1]] = m ? a ? (..._) => (a(c[c.length - 1], _), /* @__PURE__ */ p.jsx(b, {
        slot: m,
        clone: u || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ p.jsx(b, {
        slot: m,
        clone: u || (n == null ? void 0 : n.clone)
      }) : s[c[c.length - 1]], s = o;
    });
    const t = "children";
    return r[t] && (o[t] = V(r[t], n)), o;
  });
}
function g(e) {
  return W(typeof e == "number" ? e * 1e3 : e);
}
function j(e) {
  return (e == null ? void 0 : e.map((n) => n ? n.valueOf() / 1e3 : null)) || [null, null];
}
const Je = Ue(({
  slots: e,
  disabledDate: n,
  value: r,
  defaultValue: o,
  defaultPickerValue: s,
  pickerValue: t,
  presets: l,
  presetItems: c,
  showTime: f,
  onChange: m,
  minDate: a,
  maxDate: u,
  cellRender: _,
  panelRender: y,
  getPopupContainer: D,
  onValueChange: F,
  onPanelChange: I,
  onCalendarChange: h,
  children: C,
  elRef: N,
  ...i
}) => {
  const $ = E(n), ee = E(D), te = E(_), ne = E(y), re = v(() => {
    var d;
    return typeof f == "object" ? {
      ...f,
      defaultValue: (d = f.defaultValue) == null ? void 0 : d.map((w) => g(w))
    } : f;
  }, [f]), oe = v(() => r == null ? void 0 : r.map((d) => g(d)), [r]), le = v(() => o == null ? void 0 : o.map((d) => g(d)), [o]), se = v(() => Array.isArray(s) ? s.map((d) => g(d)) : s ? g(s) : void 0, [s]), ce = v(() => Array.isArray(t) ? t.map((d) => g(d)) : t ? g(t) : void 0, [t]), ie = v(() => a ? g(a) : void 0, [a]), ae = v(() => u ? g(u) : void 0, [u]);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: C
    }), /* @__PURE__ */ p.jsx(me.RangePicker, {
      ...i,
      ref: N,
      value: oe,
      defaultValue: le,
      defaultPickerValue: se,
      pickerValue: ce,
      minDate: ie,
      maxDate: ae,
      showTime: re,
      disabledDate: $,
      getPopupContainer: ee,
      cellRender: te,
      panelRender: ne,
      presets: v(() => (l || V(c)).map((d) => ({
        ...d,
        value: j(d.value)
      })), [l, c]),
      onPanelChange: (d, ...w) => {
        const x = j(d);
        I == null || I(x, ...w);
      },
      onChange: (d, ...w) => {
        const x = j(d);
        m == null || m(x, ...w), F(x);
      },
      onCalendarChange: (d, ...w) => {
        const x = j(d);
        h == null || h(x, ...w);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ p.jsx(b, {
        slot: e.renderExtraFooter
      }) : null : i.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.prevIcon
      }) : i.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.nextIcon
      }) : i.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.suffixIcon
      }) : i.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.superNextIcon
      }) : i.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ p.jsx(b, {
        slot: e.superPrevIcon
      }) : i.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(b, {
          slot: e["allowClear.clearIcon"]
        })
      } : i.allowClear,
      separator: e.separator ? /* @__PURE__ */ p.jsx(b, {
        slot: e.separator
      }) : i.separator
    })]
  });
});
export {
  Je as DateRangePicker,
  Je as default
};
