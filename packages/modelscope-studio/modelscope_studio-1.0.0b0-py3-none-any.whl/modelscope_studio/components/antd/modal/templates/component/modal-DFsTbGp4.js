import { g as Q, w as b } from "./Index-BMVD0mcz.js";
const T = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, J = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Modal;
var B = {
  exports: {}
}, x = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var X = T, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(e, o, l) {
  var r, s = {}, t = null, n = null;
  l !== void 0 && (t = "" + l), o.key !== void 0 && (t = "" + o.key), o.ref !== void 0 && (n = o.ref);
  for (r in o) ee.call(o, r) && !ne.hasOwnProperty(r) && (s[r] = o[r]);
  if (e && e.defaultProps) for (r in o = e.defaultProps, o) s[r] === void 0 && (s[r] = o[r]);
  return {
    $$typeof: Z,
    type: e,
    key: t,
    ref: n,
    props: s,
    _owner: te.current
  };
}
x.Fragment = $;
x.jsx = F;
x.jsxs = F;
B.exports = x;
var _ = B.exports;
const {
  SvelteComponent: oe,
  assign: C,
  binding_callbacks: E,
  check_outros: re,
  component_subscribe: P,
  compute_slots: le,
  create_slot: se,
  detach: w,
  element: L,
  empty: ce,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ie,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: h,
  safe_not_equal: fe,
  set_custom_element_data: M,
  space: _e,
  transition_in: y,
  transition_out: I,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: ge,
  getContext: pe,
  onDestroy: be,
  setContext: we
} = window.__gradio__svelte__internal;
function O(e) {
  let o, l;
  const r = (
    /*#slots*/
    e[7].default
  ), s = se(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      o = L("svelte-slot"), s && s.c(), M(o, "class", "svelte-1rt0kpf");
    },
    m(t, n) {
      h(t, o, n), s && s.m(o, null), e[9](o), l = !0;
    },
    p(t, n) {
      s && s.p && (!l || n & /*$$scope*/
      64) && me(
        s,
        r,
        t,
        /*$$scope*/
        t[6],
        l ? ae(
          r,
          /*$$scope*/
          t[6],
          n,
          null
        ) : ie(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (y(s, t), l = !0);
    },
    o(t) {
      I(s, t), l = !1;
    },
    d(t) {
      t && w(o), s && s.d(t), e[9](null);
    }
  };
}
function he(e) {
  let o, l, r, s, t = (
    /*$$slots*/
    e[4].default && O(e)
  );
  return {
    c() {
      o = L("react-portal-target"), l = _e(), t && t.c(), r = ce(), M(o, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      h(n, o, c), e[8](o), h(n, l, c), t && t.m(n, c), h(n, r, c), s = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? t ? (t.p(n, c), c & /*$$slots*/
      16 && y(t, 1)) : (t = O(n), t.c(), y(t, 1), t.m(r.parentNode, r)) : t && (ue(), I(t, 1, 1, () => {
        t = null;
      }), re());
    },
    i(n) {
      s || (y(t), s = !0);
    },
    o(n) {
      I(t), s = !1;
    },
    d(n) {
      n && (w(o), w(l), w(r)), e[8](null), t && t.d(n);
    }
  };
}
function S(e) {
  const {
    svelteInit: o,
    ...l
  } = e;
  return l;
}
function ye(e, o, l) {
  let r, s, {
    $$slots: t = {},
    $$scope: n
  } = o;
  const c = le(t);
  let {
    svelteInit: d
  } = o;
  const g = b(S(o)), i = b();
  P(e, i, (u) => l(0, r = u));
  const a = b();
  P(e, a, (u) => l(1, s = u));
  const f = [], D = pe("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A
  } = Q() || {}, U = d({
    parent: D,
    props: g,
    target: i,
    slot: a,
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A,
    onDestroy(u) {
      f.push(u);
    }
  });
  we("$$ms-gr-antd-react-wrapper", U), ge(() => {
    g.set(S(o));
  }), be(() => {
    f.forEach((u) => u());
  });
  function q(u) {
    E[u ? "unshift" : "push"](() => {
      r = u, i.set(r);
    });
  }
  function G(u) {
    E[u ? "unshift" : "push"](() => {
      s = u, a.set(s);
    });
  }
  return e.$$set = (u) => {
    l(17, o = C(C({}, o), R(u))), "svelteInit" in u && l(5, d = u.svelteInit), "$$scope" in u && l(6, n = u.$$scope);
  }, o = R(o), [r, s, i, a, c, d, n, t, q, G];
}
class xe extends oe {
  constructor(o) {
    super(), de(this, o, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const j = window.ms_globals.rerender, v = window.ms_globals.tree;
function ve(e) {
  function o(l) {
    const r = b(), s = new xe({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const n = {
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
          }, c = t.parent ?? v;
          return c.nodes = [...c.nodes, n], j({
            createPortal: k,
            node: v
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((d) => d.svelteInstance !== r), j({
              createPortal: k,
              node: v
            });
          }), n;
        },
        ...l.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(o);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(e) {
  return e ? Object.keys(e).reduce((o, l) => {
    const r = e[l];
    return typeof r == "number" && !Ie.includes(l) ? o[l] = r + "px" : o[l] = r, o;
  }, {}) : {};
}
function N(e) {
  const o = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: t,
      type: n,
      useCapture: c
    }) => {
      o.addEventListener(n, t, c);
    });
  });
  const l = Array.from(e.children);
  for (let r = 0; r < l.length; r++) {
    const s = l[r], t = N(s);
    o.replaceChild(t, o.children[r]);
  }
  return o;
}
function Ce(e, o) {
  e && (typeof e == "function" ? e(o) : e.current = o);
}
const m = H(({
  slot: e,
  clone: o,
  className: l,
  style: r
}, s) => {
  const t = K();
  return J(() => {
    var g;
    if (!t.current || !e)
      return;
    let n = e;
    function c() {
      let i = n;
      if (n.tagName.toLowerCase() === "svelte-slot" && n.children.length === 1 && n.children[0] && (i = n.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), Ce(s, i), l && i.classList.add(...l.split(" ")), r) {
        const a = ke(r);
        Object.keys(a).forEach((f) => {
          i.style[f] = a[f];
        });
      }
    }
    let d = null;
    if (o && window.MutationObserver) {
      let i = function() {
        var a;
        n = N(e), n.style.display = "contents", c(), (a = t.current) == null || a.appendChild(n);
      };
      i(), d = new window.MutationObserver(() => {
        var a, f;
        (a = t.current) != null && a.contains(n) && ((f = t.current) == null || f.removeChild(n)), i();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      n.style.display = "contents", c(), (g = t.current) == null || g.appendChild(n);
    return () => {
      var i, a;
      n.style.display = "", (i = t.current) != null && i.contains(n) && ((a = t.current) == null || a.removeChild(n)), d == null || d.disconnect();
    };
  }, [e, o, l, r, s]), T.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  });
});
function Ee(e) {
  try {
    return typeof e == "string" ? new Function(`return (...args) => (${e})(...args)`)() : void 0;
  } catch {
    return;
  }
}
function p(e) {
  return Y(() => Ee(e), [e]);
}
const Re = ve(({
  slots: e,
  afterClose: o,
  afterOpenChange: l,
  getContainer: r,
  children: s,
  modalRender: t,
  ...n
}) => {
  var a, f;
  const c = p(l), d = p(o), g = p(r), i = p(t);
  return /* @__PURE__ */ _.jsx(V, {
    ...n,
    afterOpenChange: c,
    afterClose: d,
    okText: e.okText ? /* @__PURE__ */ _.jsx(m, {
      slot: e.okText
    }) : n.okText,
    okButtonProps: {
      ...n.okButtonProps || {},
      icon: e["okButtonProps.icon"] ? /* @__PURE__ */ _.jsx(m, {
        slot: e["okButtonProps.icon"]
      }) : (a = n.okButtonProps) == null ? void 0 : a.icon
    },
    cancelText: e.cancelText ? /* @__PURE__ */ _.jsx(m, {
      slot: e.cancelText
    }) : n.cancelText,
    cancelButtonProps: {
      ...n.cancelButtonProps || {},
      icon: e["cancelButtonProps.icon"] ? /* @__PURE__ */ _.jsx(m, {
        slot: e["cancelButtonProps.icon"]
      }) : (f = n.cancelButtonProps) == null ? void 0 : f.icon
    },
    closable: e["closable.closeIcon"] ? {
      ...typeof n.closable == "object" ? n.closable : {},
      closeIcon: /* @__PURE__ */ _.jsx(m, {
        slot: e["closable.closeIcon"]
      })
    } : n.closable,
    closeIcon: e.closeIcon ? /* @__PURE__ */ _.jsx(m, {
      slot: e.closeIcon
    }) : n.closeIcon,
    footer: e.footer ? /* @__PURE__ */ _.jsx(m, {
      slot: e.footer
    }) : n.footer,
    title: e.title ? /* @__PURE__ */ _.jsx(m, {
      slot: e.title
    }) : n.title,
    modalRender: i,
    getContainer: typeof r == "string" ? g : r,
    children: s
  });
});
export {
  Re as Modal,
  Re as default
};
