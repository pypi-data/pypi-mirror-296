import { g as de, w as E } from "./Index-UR0T-FFs.js";
const J = window.ms_globals.React, ue = window.ms_globals.React.forwardRef, ae = window.ms_globals.React.useRef, fe = window.ms_globals.React.useEffect, v = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, _e = window.ms_globals.antd.DatePicker, M = window.ms_globals.dayjs;
var T = {
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
var pe = J, me = Symbol.for("react.element"), ve = Symbol.for("react.fragment"), be = Object.prototype.hasOwnProperty, ge = pe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, we = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(e, n, o) {
  var l, s = {}, t = null, r = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (l in n) be.call(n, l) && !we.hasOwnProperty(l) && (s[l] = n[l]);
  if (e && e.defaultProps) for (l in n = e.defaultProps, n) s[l] === void 0 && (s[l] = n[l]);
  return {
    $$typeof: me,
    type: e,
    key: t,
    ref: r,
    props: s,
    _owner: ge.current
  };
}
O.Fragment = ve;
O.jsx = Y;
O.jsxs = Y;
T.exports = O;
var p = T.exports;
const {
  SvelteComponent: xe,
  assign: W,
  binding_callbacks: z,
  check_outros: ye,
  component_subscribe: U,
  compute_slots: Ie,
  create_slot: he,
  detach: j,
  element: K,
  empty: Ee,
  exclude_internal_props: V,
  get_all_dirty_from_scope: je,
  get_slot_changes: Re,
  group_outros: ke,
  init: Oe,
  insert: R,
  safe_not_equal: Ce,
  set_custom_element_data: Q,
  space: Se,
  transition_in: k,
  transition_out: L,
  update_slot_base: Pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: De,
  getContext: Fe,
  onDestroy: Ne,
  setContext: Le
} = window.__gradio__svelte__internal;
function q(e) {
  let n, o;
  const l = (
    /*#slots*/
    e[7].default
  ), s = he(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = K("svelte-slot"), s && s.c(), Q(n, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      R(t, n, r), s && s.m(n, null), e[9](n), o = !0;
    },
    p(t, r) {
      s && s.p && (!o || r & /*$$scope*/
      64) && Pe(
        s,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? Re(
          l,
          /*$$scope*/
          t[6],
          r,
          null
        ) : je(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (k(s, t), o = !0);
    },
    o(t) {
      L(s, t), o = !1;
    },
    d(t) {
      t && j(n), s && s.d(t), e[9](null);
    }
  };
}
function Ae(e) {
  let n, o, l, s, t = (
    /*$$slots*/
    e[4].default && q(e)
  );
  return {
    c() {
      n = K("react-portal-target"), o = Se(), t && t.c(), l = Ee(), Q(n, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      R(r, n, c), e[8](n), R(r, o, c), t && t.m(r, c), R(r, l, c), s = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, c), c & /*$$slots*/
      16 && k(t, 1)) : (t = q(r), t.c(), k(t, 1), t.m(l.parentNode, l)) : t && (ke(), L(t, 1, 1, () => {
        t = null;
      }), ye());
    },
    i(r) {
      s || (k(t), s = !0);
    },
    o(r) {
      L(t), s = !1;
    },
    d(r) {
      r && (j(n), j(o), j(l)), e[8](null), t && t.d(r);
    }
  };
}
function G(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function Me(e, n, o) {
  let l, s, {
    $$slots: t = {},
    $$scope: r
  } = n;
  const c = Ie(t);
  let {
    svelteInit: f
  } = n;
  const _ = E(G(n)), i = E();
  U(e, i, (a) => o(0, l = a));
  const u = E();
  U(e, u, (a) => o(1, s = a));
  const d = [], x = Fe("$$ms-gr-antd-react-wrapper"), {
    slotKey: C,
    slotIndex: S,
    subSlotIndex: y
  } = de() || {}, P = f({
    parent: x,
    props: _,
    target: i,
    slot: u,
    slotKey: C,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(a) {
      d.push(a);
    }
  });
  Le("$$ms-gr-antd-react-wrapper", P), De(() => {
    _.set(G(n));
  }), Ne(() => {
    d.forEach((a) => a());
  });
  function D(a) {
    z[a ? "unshift" : "push"](() => {
      l = a, i.set(l);
    });
  }
  function m(a) {
    z[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  return e.$$set = (a) => {
    o(17, n = W(W({}, n), V(a))), "svelteInit" in a && o(5, f = a.svelteInit), "$$scope" in a && o(6, r = a.$$scope);
  }, n = V(n), [l, s, i, u, c, f, r, t, D, m];
}
class We extends xe {
  constructor(n) {
    super(), Oe(this, n, Me, Ae, Ce, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, N = window.ms_globals.tree;
function ze(e) {
  function n(o) {
    const l = E(), s = new We({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const r = {
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
          }, c = t.parent ?? N;
          return c.nodes = [...c.nodes, r], H({
            createPortal: A,
            node: N
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((f) => f.svelteInstance !== l), H({
              createPortal: A,
              node: N
            });
          }), r;
        },
        ...o.props
      }
    });
    return l.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Ue = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ve(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const l = e[o];
    return typeof l == "number" && !Ue.includes(o) ? n[o] = l + "px" : n[o] = l, n;
  }, {}) : {};
}
function X(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: t,
      type: r,
      useCapture: c
    }) => {
      n.addEventListener(r, t, c);
    });
  });
  const o = Array.from(e.children);
  for (let l = 0; l < o.length; l++) {
    const s = o[l], t = X(s);
    n.replaceChild(t, n.children[l]);
  }
  return n;
}
function qe(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const g = ue(({
  slot: e,
  clone: n,
  className: o,
  style: l
}, s) => {
  const t = ae();
  return fe(() => {
    var _;
    if (!t.current || !e)
      return;
    let r = e;
    function c() {
      let i = r;
      if (r.tagName.toLowerCase() === "svelte-slot" && r.children.length === 1 && r.children[0] && (i = r.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), qe(s, i), o && i.classList.add(...o.split(" ")), l) {
        const u = Ve(l);
        Object.keys(u).forEach((d) => {
          i.style[d] = u[d];
        });
      }
    }
    let f = null;
    if (n && window.MutationObserver) {
      let i = function() {
        var u;
        r = X(e), r.style.display = "contents", c(), (u = t.current) == null || u.appendChild(r);
      };
      i(), f = new window.MutationObserver(() => {
        var u, d;
        (u = t.current) != null && u.contains(r) && ((d = t.current) == null || d.removeChild(r)), i();
      }), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      r.style.display = "contents", c(), (_ = t.current) == null || _.appendChild(r);
    return () => {
      var i, u;
      r.style.display = "", (i = t.current) != null && i.contains(r) && ((u = t.current) == null || u.removeChild(r)), f == null || f.disconnect();
    };
  }, [e, n, o, l, s]), J.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Ge(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function h(e) {
  return v(() => Ge(e), [e]);
}
function Z(e, n) {
  return e.filter(Boolean).map((o) => {
    if (typeof o != "object")
      return o;
    const l = {
      ...o.props
    };
    let s = l;
    Object.keys(o.slots).forEach((r) => {
      if (!o.slots[r] || !(o.slots[r] instanceof Element) && !o.slots[r].el)
        return;
      const c = r.split(".");
      c.forEach((d, x) => {
        s[d] || (s[d] = {}), x !== c.length - 1 && (s = l[d]);
      });
      const f = o.slots[r];
      let _, i, u = !1;
      f instanceof Element ? _ = f : (_ = f.el, i = f.callback, u = f.clone || !1), s[c[c.length - 1]] = _ ? i ? (...d) => (i(c[c.length - 1], d), /* @__PURE__ */ p.jsx(g, {
        slot: _,
        clone: u || (n == null ? void 0 : n.clone)
      })) : /* @__PURE__ */ p.jsx(g, {
        slot: _,
        clone: u || (n == null ? void 0 : n.clone)
      }) : s[c[c.length - 1]], s = l;
    });
    const t = "children";
    return o[t] && (l[t] = Z(o[t], n)), l;
  });
}
function b(e) {
  return Array.isArray(e) ? e.map((n) => b(n)) : M(typeof e == "number" ? e * 1e3 : e);
}
function B(e) {
  return Array.isArray(e) ? e.map((n) => n ? n.valueOf() / 1e3 : null) : typeof e == "object" && e !== null ? e.valueOf() / 1e3 : e;
}
const Be = ze(({
  slots: e,
  disabledDate: n,
  value: o,
  defaultValue: l,
  defaultPickerValue: s,
  pickerValue: t,
  showTime: r,
  presets: c,
  presetItems: f,
  onChange: _,
  minDate: i,
  maxDate: u,
  cellRender: d,
  panelRender: x,
  getPopupContainer: C,
  onValueChange: S,
  onPanelChange: y,
  children: P,
  elRef: D,
  ...m
}) => {
  const a = h(n), $ = h(C), ee = h(d), te = h(x), ne = v(() => typeof r == "object" ? {
    ...r,
    defaultValue: r.defaultValue ? b(r.defaultValue) : void 0
  } : r, [r]), re = v(() => o ? b(o) : void 0, [o]), oe = v(() => l ? b(l) : void 0, [l]), le = v(() => s ? b(s) : void 0, [s]), se = v(() => t ? b(t) : void 0, [t]), ce = v(() => i ? b(i) : void 0, [i]), ie = v(() => u ? b(u) : void 0, [u]);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: P
    }), /* @__PURE__ */ p.jsx(_e, {
      ...m,
      ref: D,
      value: re,
      defaultValue: oe,
      defaultPickerValue: le,
      pickerValue: se,
      minDate: ce,
      maxDate: ie,
      showTime: ne,
      disabledDate: a,
      getPopupContainer: $,
      cellRender: ee,
      panelRender: te,
      presets: v(() => (c || Z(f)).map((w) => ({
        ...w,
        value: b(w.value)
      })), [c, f]),
      onPanelChange: (w, ...F) => {
        const I = B(w);
        y == null || y(I, ...F);
      },
      onChange: (w, ...F) => {
        const I = B(w);
        _ == null || _(I, ...F), S(I);
      },
      renderExtraFooter: e.renderExtraFooter ? () => e.renderExtraFooter ? /* @__PURE__ */ p.jsx(g, {
        slot: e.renderExtraFooter
      }) : null : m.renderExtraFooter,
      prevIcon: e.prevIcon ? /* @__PURE__ */ p.jsx(g, {
        slot: e.prevIcon
      }) : m.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ p.jsx(g, {
        slot: e.nextIcon
      }) : m.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ p.jsx(g, {
        slot: e.suffixIcon
      }) : m.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ p.jsx(g, {
        slot: e.superNextIcon
      }) : m.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ p.jsx(g, {
        slot: e.superPrevIcon
      }) : m.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(g, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear
    })]
  });
});
export {
  Be as DatePicker,
  Be as default
};
