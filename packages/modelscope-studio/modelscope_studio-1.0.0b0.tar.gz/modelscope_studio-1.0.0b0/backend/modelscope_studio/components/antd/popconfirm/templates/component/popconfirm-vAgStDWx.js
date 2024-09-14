import { g as Q, w as g } from "./Index-CDHeJYxS.js";
const T = window.ms_globals.React, H = window.ms_globals.React.forwardRef, K = window.ms_globals.React.useRef, J = window.ms_globals.React.useEffect, Y = window.ms_globals.React.useMemo, P = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Popconfirm;
var B = {
  exports: {}
}, y = {};
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
function L(e, n, l) {
  var r, s = {}, t = null, o = null;
  l !== void 0 && (t = "" + l), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (o = n.ref);
  for (r in n) ee.call(n, r) && !ne.hasOwnProperty(r) && (s[r] = n[r]);
  if (e && e.defaultProps) for (r in n = e.defaultProps, n) s[r] === void 0 && (s[r] = n[r]);
  return {
    $$typeof: Z,
    type: e,
    key: t,
    ref: o,
    props: s,
    _owner: te.current
  };
}
y.Fragment = $;
y.jsx = L;
y.jsxs = L;
B.exports = y;
var _ = B.exports;
const {
  SvelteComponent: oe,
  assign: k,
  binding_callbacks: C,
  check_outros: re,
  component_subscribe: E,
  compute_slots: se,
  create_slot: le,
  detach: w,
  element: F,
  empty: ie,
  exclude_internal_props: I,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ae,
  group_outros: ue,
  init: de,
  insert: b,
  safe_not_equal: fe,
  set_custom_element_data: N,
  space: _e,
  transition_in: h,
  transition_out: v,
  update_slot_base: pe
} = window.__gradio__svelte__internal, {
  beforeUpdate: me,
  getContext: ge,
  onDestroy: we,
  setContext: be
} = window.__gradio__svelte__internal;
function R(e) {
  let n, l;
  const r = (
    /*#slots*/
    e[7].default
  ), s = le(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = F("svelte-slot"), s && s.c(), N(n, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      b(t, n, o), s && s.m(n, null), e[9](n), l = !0;
    },
    p(t, o) {
      s && s.p && (!l || o & /*$$scope*/
      64) && pe(
        s,
        r,
        t,
        /*$$scope*/
        t[6],
        l ? ae(
          r,
          /*$$scope*/
          t[6],
          o,
          null
        ) : ce(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      l || (h(s, t), l = !0);
    },
    o(t) {
      v(s, t), l = !1;
    },
    d(t) {
      t && w(n), s && s.d(t), e[9](null);
    }
  };
}
function he(e) {
  let n, l, r, s, t = (
    /*$$slots*/
    e[4].default && R(e)
  );
  return {
    c() {
      n = F("react-portal-target"), l = _e(), t && t.c(), r = ie(), N(n, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      b(o, n, i), e[8](n), b(o, l, i), t && t.m(o, i), b(o, r, i), s = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, i), i & /*$$slots*/
      16 && h(t, 1)) : (t = R(o), t.c(), h(t, 1), t.m(r.parentNode, r)) : t && (ue(), v(t, 1, 1, () => {
        t = null;
      }), re());
    },
    i(o) {
      s || (h(t), s = !0);
    },
    o(o) {
      v(t), s = !1;
    },
    d(o) {
      o && (w(n), w(l), w(r)), e[8](null), t && t.d(o);
    }
  };
}
function O(e) {
  const {
    svelteInit: n,
    ...l
  } = e;
  return l;
}
function ye(e, n, l) {
  let r, s, {
    $$slots: t = {},
    $$scope: o
  } = n;
  const i = se(t);
  let {
    svelteInit: d
  } = n;
  const m = g(O(n)), c = g();
  E(e, c, (a) => l(0, r = a));
  const u = g();
  E(e, u, (a) => l(1, s = a));
  const f = [], M = ge("$$ms-gr-antd-react-wrapper"), {
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A
  } = Q() || {}, U = d({
    parent: M,
    props: m,
    target: c,
    slot: u,
    slotKey: W,
    slotIndex: z,
    subSlotIndex: A,
    onDestroy(a) {
      f.push(a);
    }
  });
  be("$$ms-gr-antd-react-wrapper", U), me(() => {
    m.set(O(n));
  }), we(() => {
    f.forEach((a) => a());
  });
  function q(a) {
    C[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  function G(a) {
    C[a ? "unshift" : "push"](() => {
      s = a, u.set(s);
    });
  }
  return e.$$set = (a) => {
    l(17, n = k(k({}, n), I(a))), "svelteInit" in a && l(5, d = a.svelteInit), "$$scope" in a && l(6, o = a.$$scope);
  }, n = I(n), [r, s, c, u, i, d, o, t, q, G];
}
class xe extends oe {
  constructor(n) {
    super(), de(this, n, ye, he, fe, {
      svelteInit: 5
    });
  }
}
const S = window.ms_globals.rerender, x = window.ms_globals.tree;
function ve(e) {
  function n(l) {
    const r = g(), s = new xe({
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
          }, i = t.parent ?? x;
          return i.nodes = [...i.nodes, o], S({
            createPortal: P,
            node: x
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((d) => d.svelteInstance !== r), S({
              createPortal: P,
              node: x
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
function ke(e) {
  return e ? Object.keys(e).reduce((n, l) => {
    const r = e[l];
    return typeof r == "number" && !Pe.includes(l) ? n[l] = r + "px" : n[l] = r, n;
  }, {}) : {};
}
function D(e) {
  const n = e.cloneNode(!0);
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: t,
      type: o,
      useCapture: i
    }) => {
      n.addEventListener(o, t, i);
    });
  });
  const l = Array.from(e.children);
  for (let r = 0; r < l.length; r++) {
    const s = l[r], t = D(s);
    n.replaceChild(t, n.children[r]);
  }
  return n;
}
function Ce(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const p = H(({
  slot: e,
  clone: n,
  className: l,
  style: r
}, s) => {
  const t = K();
  return J(() => {
    var m;
    if (!t.current || !e)
      return;
    let o = e;
    function i() {
      let c = o;
      if (o.tagName.toLowerCase() === "svelte-slot" && o.children.length === 1 && o.children[0] && (c = o.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Ce(s, c), l && c.classList.add(...l.split(" ")), r) {
        const u = ke(r);
        Object.keys(u).forEach((f) => {
          c.style[f] = u[f];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let c = function() {
        var u;
        o = D(e), o.style.display = "contents", i(), (u = t.current) == null || u.appendChild(o);
      };
      c(), d = new window.MutationObserver(() => {
        var u, f;
        (u = t.current) != null && u.contains(o) && ((f = t.current) == null || f.removeChild(o)), c();
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      o.style.display = "contents", i(), (m = t.current) == null || m.appendChild(o);
    return () => {
      var c, u;
      o.style.display = "", (c = t.current) != null && c.contains(o) && ((u = t.current) == null || u.removeChild(o)), d == null || d.disconnect();
    };
  }, [e, n, l, r, s]), T.createElement("react-child", {
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
function j(e) {
  return Y(() => Ee(e), [e]);
}
const Re = ve(({
  slots: e,
  afterOpenChange: n,
  getPopupContainer: l,
  children: r,
  ...s
}) => {
  var i, d;
  const t = j(n), o = j(l);
  return /* @__PURE__ */ _.jsx(V, {
    ...s,
    afterOpenChange: t,
    getPopupContainer: o,
    okText: e.okText ? /* @__PURE__ */ _.jsx(p, {
      slot: e.okText
    }) : s.okText,
    okButtonProps: {
      ...s.okButtonProps || {},
      icon: e["okButtonProps.icon"] ? /* @__PURE__ */ _.jsx(p, {
        slot: e["okButtonProps.icon"]
      }) : (i = s.okButtonProps) == null ? void 0 : i.icon
    },
    cancelText: e.cancelText ? /* @__PURE__ */ _.jsx(p, {
      slot: e.cancelText
    }) : s.cancelText,
    cancelButtonProps: {
      ...s.cancelButtonProps || {},
      icon: e["cancelButtonProps.icon"] ? /* @__PURE__ */ _.jsx(p, {
        slot: e["cancelButtonProps.icon"]
      }) : (d = s.cancelButtonProps) == null ? void 0 : d.icon
    },
    title: e.title ? /* @__PURE__ */ _.jsx(p, {
      slot: e.title
    }) : s.title,
    description: e.description ? /* @__PURE__ */ _.jsx(p, {
      slot: e.description
    }) : s.description,
    children: r
  });
});
export {
  Re as Popconfirm,
  Re as default
};
